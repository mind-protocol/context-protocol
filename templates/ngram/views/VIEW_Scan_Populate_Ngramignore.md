# VIEW: Scan — Populate .ngramignore

**You're scanning a repository to identify files and patterns that should be excluded from ngram's health checks.**

---

## WHY THIS VIEW EXISTS

Not all files in a repository should be tracked by ngram:
- Dependencies and vendor code (not your code)
- Build outputs (generated, not source)
- Large data files (not documentation)
- IDE configs (local, not project)

This view helps you systematically identify what to ignore.

---

## CONTEXT TO LOAD

### Current Ignore File

```
.ngramignore
```

Check what's already ignored. Don't duplicate patterns.

### Repository Structure

Run `ls -la` at root and explore directories to understand what exists.

---

## THE WORK

### Step 1: Identify Dependency Directories

Look for:
```
node_modules/     # JavaScript
vendor/           # PHP, Go
.venv/ venv/      # Python virtual environments
__pycache__/      # Python bytecode
.gradle/          # Java/Kotlin
Pods/             # iOS CocoaPods
```

### Step 2: Identify Build Outputs

Look for:
```
dist/ build/ out/        # Generic builds
.next/ .nuxt/ .output/   # Framework builds
target/                   # Rust, Java
bin/ obj/                 # .NET, C++
*.min.js *.bundle.js      # Bundled assets
```

### Step 3: Identify Generated Files

Look for:
```
coverage/ .coverage       # Test coverage
*.map                      # Source maps
*.generated.*             # Code generation
__generated__/            # Generated directories
```

### Step 4: Identify Data/Assets

Look for:
```
data/                 # Data files
assets/ static/       # Static assets
uploads/              # User uploads
*.sqlite *.db         # Databases
```

### Step 5: Identify IDE/Tool Files

Look for:
```
.idea/ .vscode/       # IDE configs
*.swp *.swo           # Vim swap files
.DS_Store             # macOS
Thumbs.db             # Windows
```

### Step 6: Identify Lock Files

Look for:
```
package-lock.json     # npm
yarn.lock             # Yarn
pnpm-lock.yaml        # pnpm
Pipfile.lock          # Pipenv
poetry.lock           # Poetry
Cargo.lock            # Rust
```

---

## OUTPUT FORMAT

Add discovered patterns to `.ngramignore`:

```
# Dependencies
node_modules/
.venv/

# Build outputs
dist/
build/

# Project-specific
some-project-specific-dir/
```

Group by category with comments.

---

## VERIFICATION

After updating `.ngramignore`, run:

```bash
ngram doctor
```

Verify that:
- Health score improved (fewer false positives)
- No project code was accidentally excluded
- Ignored paths make sense

---

## WHAT TO IGNORE vs KEEP

**IGNORE:**
- Third-party code you don't maintain
- Generated/compiled output
- Binary files and databases
- IDE/editor configs
- OS-specific files

**KEEP (don't ignore):**
- Your source code
- Your documentation
- Configuration files you maintain
- Test files you wrote
- Scripts you maintain

---

## HANDOFF

Update `.ngramignore` directly. No SYNC update needed unless you found patterns that should be added to the default template.
