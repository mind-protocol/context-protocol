from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

AGENT_CHOICES = ("gemini", "claude", "codex")
DEFAULT_AGENT = "claude"


@dataclass(frozen=True)
class AgentCommand:
    cmd: List[str]
    stdin: Optional[str] = None


def normalize_agent(agent: Optional[str]) -> str:
    if not agent:
        return DEFAULT_AGENT
    agent = agent.lower()
    if agent not in AGENT_CHOICES:
        raise ValueError(f"Unknown agent provider: {agent}")
    return agent


def build_agent_command(
    agent: str,
    prompt: str,
    system_prompt: str = "",
    stream_json: bool = True,
    continue_session: bool = False,
    add_dir: Optional[Path] = None,
    allowed_tools: Optional[str] = None,
    use_dangerous: bool = True,
    model_name: Optional[str] = None, # New: Optional model name for Gemini
) -> AgentCommand:
    agent = normalize_agent(agent)
    if agent == "gemini":
        # Use internal Gemini adapter
        import sys
        cmd = [sys.executable, "-m", "ngram.llms.gemini_agent", "--prompt", prompt]

        if system_prompt:
            cmd.extend(["--system-prompt", system_prompt])
        
        cmd.extend(["--output-format", "stream-json" if stream_json else "text"])
        
        if allowed_tools:
            cmd.extend(["--allowed-tools", allowed_tools])
        
        if model_name: # Pass model name if specified
            cmd.extend(["--model-name", model_name])
        
        return AgentCommand(cmd=cmd)
    if agent == "claude":
        cmd = ["claude"]
        if continue_session:
            cmd.append("--continue")
        cmd.extend(["-p", prompt])
        cmd.extend(["--output-format", "stream-json" if stream_json else "text"])
        if use_dangerous:
            cmd.append("--dangerously-skip-permissions")
        if allowed_tools:
            cmd.extend(["--allowedTools", allowed_tools])
        if add_dir:
            cmd.extend(["--add-dir", str(add_dir)])
        if system_prompt:
            cmd.extend(["--append-system-prompt", system_prompt])
        cmd.append("--verbose")
        return AgentCommand(cmd=cmd)

    combined_prompt = prompt if not system_prompt else f"{system_prompt}\n\n{prompt}"
    cmd = ["codex", "exec"]
    if stream_json:
        cmd.append("--json")
    if use_dangerous:
        cmd.append("--dangerously-bypass-approvals-and-sandbox")
    if continue_session:
        cmd.extend(["resume", "--last", "-"])
    else:
        cmd.append("-")
    return AgentCommand(cmd=cmd, stdin=combined_prompt)
