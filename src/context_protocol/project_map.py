"""
Project Map - Visual representation of module structure and health.

Prototype for visualizing:
- Modules organized by area/feature (from modules.yaml)
- Dependencies between modules (arrows)
- Documentation coverage per module ([P][B][A][V][T][S])
- Health warnings (monoliths)
- Line counts per module
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class ModuleInfo:
    """Information about a single module."""
    name: str
    code_pattern: str
    docs_path: str
    maturity: str = "UNKNOWN"
    depends_on: List[str] = field(default_factory=list)

    # Computed
    code_files: List[Path] = field(default_factory=list)
    total_lines: int = 0
    doc_coverage: Dict[str, bool] = field(default_factory=dict)
    is_monolith: bool = False


def load_modules_yaml(project_dir: Path) -> Dict[str, Any]:
    """Load modules.yaml configuration."""
    if not HAS_YAML:
        return {}

    config_path = project_dir / ".context-protocol" / "modules.yaml"
    if not config_path.exists():
        return {}

    try:
        with open(config_path) as f:
            data = yaml.safe_load(f)
            return data.get("modules", {}) if data else {}
    except Exception:
        return {}


def count_file_lines(file_path: Path) -> int:
    """Count non-empty lines in a file."""
    try:
        return sum(1 for line in file_path.read_text().splitlines() if line.strip())
    except Exception:
        return 0


def glob_to_regex(pattern: str) -> str:
    """Convert a glob pattern to regex."""
    # Escape special chars except * and **
    result = re.escape(pattern)
    # ** matches any path
    result = result.replace(r'\*\*', '.*')
    # * matches within path segment
    result = result.replace(r'\*', '[^/]*')
    return f"^{result}$"


def find_code_files(project_dir: Path, pattern: str) -> List[Path]:
    """Find all code files matching a pattern."""
    files = []

    # Handle glob-style patterns
    if '**' in pattern:
        base = pattern.split('**')[0].rstrip('/')
        base_path = project_dir / base if base else project_dir
        if base_path.exists():
            for f in base_path.rglob('*'):
                if f.is_file() and f.suffix in ['.py', '.ts', '.tsx', '.js', '.jsx', '.go', '.rs']:
                    files.append(f)
    elif '*' in pattern:
        base = pattern.split('*')[0].rstrip('/')
        base_path = project_dir / base if base else project_dir
        if base_path.exists():
            for f in base_path.glob('*'):
                if f.is_file() and f.suffix in ['.py', '.ts', '.tsx', '.js', '.jsx', '.go', '.rs']:
                    files.append(f)
    else:
        # Exact path
        path = project_dir / pattern
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            for f in path.rglob('*'):
                if f.is_file() and f.suffix in ['.py', '.ts', '.tsx', '.js', '.jsx', '.go', '.rs']:
                    files.append(f)

    return files


def check_doc_coverage(project_dir: Path, docs_path: str) -> Dict[str, bool]:
    """Check which doc types exist for a module."""
    doc_types = {
        'P': 'PATTERNS',
        'B': 'BEHAVIORS',
        'A': 'ALGORITHM',
        'V': 'VALIDATION',
        'T': 'TEST',
        'S': 'SYNC'
    }

    coverage = {k: False for k in doc_types.keys()}

    docs_dir = project_dir / docs_path
    if not docs_dir.exists():
        return coverage

    # Check for doc files in the docs path and its subdirectories
    for md_file in docs_dir.rglob('*.md'):
        for short, prefix in doc_types.items():
            if md_file.name.startswith(prefix + '_'):
                coverage[short] = True

    return coverage


def analyze_modules(project_dir: Path, monolith_threshold: int = 500) -> List[ModuleInfo]:
    """Analyze all modules defined in modules.yaml."""
    modules_config = load_modules_yaml(project_dir)

    if not modules_config:
        return []

    modules = []

    for name, config in modules_config.items():
        if not isinstance(config, dict):
            continue

        module = ModuleInfo(
            name=name,
            code_pattern=config.get('code', ''),
            docs_path=config.get('docs', ''),
            maturity=config.get('maturity', 'UNKNOWN'),
            depends_on=config.get('depends_on', []) or []
        )

        # Find code files
        if module.code_pattern:
            module.code_files = find_code_files(project_dir, module.code_pattern)
            module.total_lines = sum(count_file_lines(f) for f in module.code_files)
            module.is_monolith = module.total_lines > monolith_threshold * 2  # Aggregate threshold

        # Check doc coverage
        if module.docs_path:
            module.doc_coverage = check_doc_coverage(project_dir, module.docs_path)

        modules.append(module)

    return modules


def format_doc_coverage(coverage: Dict[str, bool]) -> str:
    """Format doc coverage as [P][B][A][V][T][S] with filled/empty indicators."""
    result = []
    for key in ['P', 'B', 'A', 'V', 'T', 'S']:
        if coverage.get(key, False):
            result.append(f"[{key}]")
        else:
            result.append(f"[·]")
    return ''.join(result)


def format_doc_coverage_short(coverage: Dict[str, bool]) -> str:
    """Format doc coverage as compact string like 'PBS' for present docs."""
    return ''.join(k for k, v in coverage.items() if v) or '?'


def draw_box(name: str, lines: int, coverage: Dict[str, bool], is_monolith: bool, width: int = 15) -> List[str]:
    """Draw a single module box."""
    warning = " ⚠" if is_monolith else ""
    line_str = f"{lines}L{warning}"
    cov_str = format_doc_coverage(coverage)

    # Calculate content width
    content_width = max(len(name), len(line_str), len(cov_str))
    box_width = max(width, content_width + 4)
    inner = box_width - 2

    lines_out = []
    lines_out.append("┌" + "─" * inner + "┐")
    lines_out.append("│" + name.center(inner) + "│")
    lines_out.append("│" + line_str.center(inner) + "│")
    lines_out.append("│" + cov_str.center(inner) + "│")
    lines_out.append("└" + "─" * inner + "┘")

    return lines_out


def topological_layers(modules: List[ModuleInfo]) -> List[List[ModuleInfo]]:
    """Group modules into layers based on dependencies."""
    module_map = {m.name: m for m in modules}
    layers = []
    assigned = set()

    while len(assigned) < len(modules):
        # Find modules whose dependencies are all assigned
        layer = []
        for m in modules:
            if m.name in assigned:
                continue
            # All deps must be already assigned (or not in our module set)
            deps_satisfied = all(
                d in assigned or d not in module_map
                for d in m.depends_on
            )
            if deps_satisfied:
                layer.append(m)

        if not layer:
            # Circular dependency - add remaining
            layer = [m for m in modules if m.name not in assigned]

        for m in layer:
            assigned.add(m.name)
        layers.append(layer)

    return layers


def generate_project_map(project_dir: Path) -> str:
    """Generate ASCII project map visualization."""
    modules = analyze_modules(project_dir)

    if not modules:
        return "No modules found in modules.yaml"

    output = []
    output.append("┌" + "─" * 70 + "┐")
    output.append("│" + "PROJECT MAP".center(70) + "│")
    output.append("│" + f"{project_dir.name}".center(70) + "│")
    output.append("└" + "─" * 70 + "┘")
    output.append("")

    # Group into topological layers
    layers = topological_layers(modules)

    BOX_WIDTH = 18
    BOX_SPACING = 2

    def draw_layer(layer: List[ModuleInfo]) -> List[str]:
        """Draw a layer of module boxes."""
        if not layer:
            return []

        boxes = [draw_box(m.name, m.total_lines, m.doc_coverage, m.is_monolith, BOX_WIDTH) for m in layer]
        max_lines = max(len(b) for b in boxes)

        row_lines = []
        for line_idx in range(max_lines):
            row = ""
            for j, box in enumerate(boxes):
                if line_idx < len(box):
                    row += box[line_idx]
                else:
                    row += " " * BOX_WIDTH
                if j < len(boxes) - 1:
                    row += " " * BOX_SPACING
            row_lines.append(row)

        return row_lines

    # Draw each layer with arrows between
    for i, layer in enumerate(layers):
        if i == 0:
            output.append("─── FOUNDATION (no dependencies) " + "─" * 37)
        else:
            output.append(f"─── LAYER {i} " + "─" * 58)
        output.append("")

        output.extend(draw_layer(layer))
        output.append("")

        # Draw dependency arrows to next layer
        if i < len(layers) - 1:
            next_layer = layers[i + 1]
            arrow_lines = []
            for nm in next_layer:
                deps_in_current = [d for d in nm.depends_on if any(m.name == d for m in layer)]
                if deps_in_current:
                    arrow_lines.append(f"        ↑ {nm.name} uses [{', '.join(deps_in_current)}]")

            if arrow_lines:
                output.append("        │")
                for al in arrow_lines:
                    output.append(al)
                output.append("")

    # Legend
    output.append("─── LEGEND " + "─" * 59)
    output.append("")
    output.append("[P]ATTERNS [B]EHAVIORS [A]LGORITHM [V]ALIDATION [T]EST [S]YNC")
    output.append("[·] = missing    ⚠ = monolith (>1000L)")
    output.append("")

    # Summary stats
    total_lines = sum(m.total_lines for m in modules)
    total_files = sum(len(m.code_files) for m in modules)
    monoliths = sum(1 for m in modules if m.is_monolith)

    coverage_totals = {k: sum(1 for m in modules if m.doc_coverage.get(k, False)) for k in ['P', 'B', 'A', 'V', 'T', 'S']}

    output.append("─── SUMMARY " + "─" * 58)
    output.append("")
    output.append(f"Modules: {len(modules)}    Files: {total_files}    Lines: {total_lines}")
    if monoliths:
        output.append(f"⚠ Monoliths: {monoliths}")

    cov_summary = " ".join(f"{k}:{v}/{len(modules)}" for k, v in coverage_totals.items())
    output.append(f"Doc coverage: {cov_summary}")
    output.append("")

    return "\n".join(output)


def generate_html_map(project_dir: Path) -> str:
    """Generate an interactive HTML project map visualization."""
    modules = analyze_modules(project_dir)
    layers = topological_layers(modules)

    module_map = {m.name: m for m in modules}

    # Calculate positions
    positions = {}
    y_offset = 100
    layer_height = 180

    for layer_idx, layer in enumerate(layers):
        x_spacing = 200
        start_x = 50
        for mod_idx, mod in enumerate(layer):
            positions[mod.name] = {
                'x': start_x + mod_idx * x_spacing,
                'y': y_offset + layer_idx * layer_height
            }

    # Build edges
    edges = []
    for m in modules:
        for dep in m.depends_on:
            if dep in positions:
                edges.append((m.name, dep))

    # Get project name
    project_name = project_dir.resolve().name

    # Generate HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Map - {project_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 20px;
            color: #fff;
        }}
        .map-container {{
            position: relative;
            width: 100%;
            min-height: 800px;
        }}
        svg {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: visible;
        }}
        .module-box {{
            position: absolute;
            z-index: 10;
            width: 160px;
            background: #16213e;
            border: 2px solid #0f3460;
            border-radius: 8px;
            padding: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .module-box:hover {{
            border-color: #e94560;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(233, 69, 96, 0.3);
        }}
        .module-box.monolith {{
            border-color: #ff6b6b;
        }}
        .module-box.full-docs {{
            border-color: #4ecdc4;
        }}
        .module-name {{
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 6px;
            color: #fff;
        }}
        .module-lines {{
            font-size: 12px;
            color: #888;
            margin-bottom: 8px;
        }}
        .module-lines.warning {{
            color: #ff6b6b;
        }}
        .doc-coverage {{
            display: flex;
            gap: 2px;
            flex-wrap: wrap;
        }}
        .doc-badge {{
            font-size: 10px;
            padding: 2px 4px;
            border-radius: 3px;
            background: #0f3460;
            color: #666;
        }}
        .doc-badge.present {{
            background: #4ecdc4;
            color: #000;
        }}
        .doc-badge.missing {{
            background: #333;
            color: #555;
        }}
        .legend {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #16213e;
            padding: 16px;
            border-radius: 8px;
            font-size: 12px;
        }}
        .legend h3 {{
            margin-bottom: 8px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 4px 0;
        }}
        .legend-color {{
            width: 20px;
            height: 12px;
            border-radius: 2px;
        }}
        .summary {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #16213e;
            padding: 16px;
            border-radius: 8px;
            font-size: 13px;
        }}
        .layer-label {{
            position: absolute;
            left: 10px;
            font-size: 11px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
    </style>
</head>
<body>
    <h1>Project Map: {project_name}</h1>

    <div class="map-container">
        <svg id="arrows" style="height: {y_offset + len(layers) * layer_height + 100}px;"></svg>
'''

    # Add layer labels
    for layer_idx, layer in enumerate(layers):
        if layer:
            y = y_offset + layer_idx * layer_height - 30
            label = "Foundation" if layer_idx == 0 else f"Layer {layer_idx}"
            html += f'        <div class="layer-label" style="top: {y}px">{label}</div>\n'

    # Add module boxes
    for m in modules:
        pos = positions[m.name]
        classes = ["module-box"]
        if m.is_monolith:
            classes.append("monolith")
        if all(m.doc_coverage.get(k, False) for k in ['P', 'B', 'A', 'V', 'T', 'S']):
            classes.append("full-docs")

        line_class = "warning" if m.is_monolith else ""

        doc_badges = ""
        for k in ['P', 'B', 'A', 'V', 'T', 'S']:
            present = m.doc_coverage.get(k, False)
            badge_class = "present" if present else "missing"
            doc_badges += f'<span class="doc-badge {badge_class}">{k}</span>'

        html += f'''
        <div class="{' '.join(classes)}" style="left: {pos['x']}px; top: {pos['y']}px" data-module="{m.name}">
            <div class="module-name">{m.name}</div>
            <div class="module-lines {line_class}">{m.total_lines} lines{' ⚠' if m.is_monolith else ''}</div>
            <div class="doc-coverage">{doc_badges}</div>
        </div>
'''

    # Summary stats
    total_lines = sum(m.total_lines for m in modules)
    total_files = sum(len(m.code_files) for m in modules)
    monoliths = sum(1 for m in modules if m.is_monolith)

    html += f'''
    </div>

    <div class="summary">
        <strong>Summary</strong><br>
        Modules: {len(modules)}<br>
        Files: {total_files}<br>
        Lines: {total_lines}<br>
        {'⚠ Monoliths: ' + str(monoliths) + '<br>' if monoliths else ''}
    </div>

    <div class="legend">
        <h3>Legend</h3>
        <div class="legend-item">
            <div class="legend-color" style="background: #4ecdc4"></div>
            <span>Full documentation</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #ff6b6b"></div>
            <span>Monolith (>1000L)</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #0f3460"></div>
            <span>Normal module</span>
        </div>
    </div>

    <script>
        // Draw arrows
        const edges = {json.dumps([[e[0], e[1]] for e in edges])};
        const positions = {json.dumps(positions)};

        const svg = document.getElementById('arrows');
        const ns = 'http://www.w3.org/2000/svg';

        // Add arrow marker
        const defs = document.createElementNS(ns, 'defs');
        defs.innerHTML = `
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#4a5568" />
            </marker>
        `;
        svg.appendChild(defs);

        edges.forEach(([from, to]) => {{
            const fromPos = positions[from];
            const toPos = positions[to];
            if (!fromPos || !toPos) return;

            // Draw curved path from bottom of 'from' box to top of 'to' box
            const x1 = fromPos.x + 80;
            const y1 = fromPos.y + 90;  // bottom of from box
            const x2 = toPos.x + 80;
            const y2 = toPos.y;  // top of to box

            const path = document.createElementNS(ns, 'path');
            const midY = (y1 + y2) / 2;
            const d = `M ${{x1}} ${{y1}} C ${{x1}} ${{midY}}, ${{x2}} ${{midY}}, ${{x2}} ${{y2}}`;
            path.setAttribute('d', d);
            path.setAttribute('stroke', '#4a5568');
            path.setAttribute('stroke-width', '2');
            path.setAttribute('fill', 'none');
            path.setAttribute('marker-end', 'url(#arrowhead)');
            svg.appendChild(path);
        }});
    </script>
</body>
</html>
'''
    return html


def print_project_map(project_dir: Path, output_html: Optional[Path] = None):
    """Generate and optionally save the project map."""
    if output_html:
        html = generate_html_map(project_dir)
        output_html.write_text(html)
        print(f"Project map saved to: {output_html}")
    else:
        # Default: generate HTML and open in browser
        import tempfile
        import webbrowser

        html = generate_html_map(project_dir)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html)
            temp_path = f.name

        print(f"Opening project map in browser...")
        print(f"File: {temp_path}")
        webbrowser.open(f'file://{temp_path}')


if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    print_project_map(target)
