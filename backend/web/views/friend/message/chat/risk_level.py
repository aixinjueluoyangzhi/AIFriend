import re

# 高危关键字（直接阻断）
DANGEROUS_PATTERNS = [
    r"rm\s+-rf",
    r"del\s+/f\s+/s\s+/q",
    r"rmdir\s+/s\s+/q",
    r"Remove-Item\s+-Recurse\s+-Force",
    r"shutdown",
    r":\(\)\{\s*:\|:&\s*\};:",  # fork bomb
    r"mkfs",
    r"dd\s+if=",
]

RISK_PATTERNS = {
    r"sudo": 30,
    r"chmod\s+777": 40,
    r"chown": 25,
    r"pip\s+install": 10,
    r"rm\s+": 50,
    r"del\s+": 40,
    r"git\s+push\s+--force": 60,
    r"curl\s+.*\|\s*sh": 70,
}

SAFE_COMMANDS = [
    "ls",
    "pwd",
    "echo",
    "cat",
    "python",
    "pip",
    "git status",
    "git log",
    "node",
]
def calculate_risk(command: str) -> tuple[int, str]:
    """
    返回 (risk_score, reason)
    """

    cmd = command.strip()

    # 1. 黑名单：直接阻断
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return 100, f"命中高危规则: {pattern}"

    score = 0
    reasons = []

    # 2. 风险规则评分
    for pattern, weight in RISK_PATTERNS.items():
        if re.search(pattern, cmd, re.IGNORECASE):
            score += weight
            reasons.append(f"{pattern} (+{weight})")

    # 3. 是否在安全命令列表
    if any(cmd.startswith(safe) for safe in SAFE_COMMANDS):
        score -= 10

    score = max(0, min(100, score))

    reason = "; ".join(reasons) if reasons else "low risk command"

    return score, reason