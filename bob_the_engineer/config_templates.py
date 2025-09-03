"""Configuration templates for coding agents."""

import json
from dataclasses import dataclass
from typing import Any

from bob_the_engineer.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class ConfigTemplate:
    """Configuration template definition."""

    name: str
    description: str
    best_for: str
    config_claude_code: dict[str, Any]
    config_cursor: dict[str, Any]

    def get_config(self, agent_type: str) -> dict[str, Any]:
        """Get configuration for specific agent type."""
        if agent_type == "claude-code":
            return self.config_claude_code
        elif agent_type == "cursor":
            return self.config_cursor
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")


# Configuration Templates
DEVELOPMENT_TEAM = ConfigTemplate(
    name="development-team",
    description="Optimized for 2-5 developers with established CI/CD and code review process",
    best_for="Team collaboration, code quality focus, established development practices",
    config_claude_code={
        "defaultMode": "plan",
        "autoApprove": False,
        "confirmBeforeToolUse": True,
        "tools": {
            "thinking": True,
            "allowedTools": [
                "Read",
                "Write",
                "Edit",
                "MultiEdit",
                "Bash",
                "Task",
                "CreateDiagram",
            ],
            "bashTimeout": 90,
            "maxFileSize": "1MB",
        },
        "permissions": {
            "allowedCommands": [
                "git status",
                "git diff",
                "git add .",
                "git commit -m",
                "pytest",
                "npm test",
                "npm run lint",
                "npm run build",
                "ruff check",
                "ruff format",
                "mypy",
                "black",
                "ls",
                "find",
                "grep",
                "cat",
                "head",
                "tail",
            ],
            "restrictedPaths": [".env*", "secrets.yml", "*.key", "*.pem"],
            "requireApprovalFor": ["git push", "npm publish", "pip install"],
        },
        "collaboration": {
            "autoCommit": False,
            "requireCommitMessage": True,
            "commitMessageTemplate": "[{type}] {description}\n\nCo-authored-by: Coding Agent <agent@bot.com>",
            "notifyOnLargeChanges": 50,
            "branchProtection": True,
        },
        "quality": {
            "runTestsAfterChanges": True,
            "formatCodeOnSave": True,
            "requireLintingPass": True,
            "autoFixLintIssues": True,
        },
    },
    config_cursor={
        "chat.defaultModel": "claude-3-5-sonnet",
        "chat.mode": "plan-first",
        "agent.alwaysConfirm": True,
        "agent.maxIterations": 10,
        "files.autoSave": "afterDelay",
        "editor.formatOnSave": True,
        "rules": {
            "development-workflow": "enabled",
            "code-standards": "enabled",
            "project-structure": "enabled",
            "logging-patterns": "enabled",
            "team-collaboration": "enabled",
        },
    },
)

SOLO_DEVELOPER = ConfigTemplate(
    name="solo-developer",
    description="Streamlined for individual developers doing rapid prototyping and personal projects",
    best_for="Speed and efficiency, personal projects, rapid iteration, minimal overhead",
    config_claude_code={
        "defaultMode": "code",
        "autoApprove": False,
        "confirmBeforeToolUse": False,
        "tools": {
            "thinking": False,
            "allowedTools": ["Read", "Write", "Edit", "MultiEdit", "Bash"],
            "bashTimeout": 45,
            "parallelOperations": True,
        },
        "permissions": {
            "allowedCommands": [
                "git status",
                "git add .",
                "git commit -m",
                "git push",
                "pytest -x",
                "npm test",
                "npm start",
                "npm run dev",
                "python -m",
                "pip install",
                "npm install",
                "ruff check --fix",
                "black .",
                "isort .",
                "ls",
                "find",
                "grep",
                "cat",
                "mkdir",
                "mv",
                "cp",
            ],
            "autoApprovePatterns": ["git add", "git commit", "format*", "lint*"],
            "restrictedCommands": ["rm -rf", "sudo", "curl", "wget"],
        },
        "workflow": {
            "fastCommits": True,
            "autoCommitOnSuccess": False,
            "smartFormatting": True,
            "quickTests": "pytest --maxfail=1 -x",
            "autoInstallDependencies": True,
        },
        "optimization": {
            "cacheResults": True,
            "skipUnnecessaryChecks": True,
            "batchOperations": True,
        },
    },
    config_cursor={
        "chat.defaultModel": "claude-3-5-sonnet",
        "chat.mode": "code-first",
        "agent.alwaysConfirm": False,
        "agent.maxIterations": 15,
        "files.autoSave": "onFocusChange",
        "editor.formatOnSave": True,
        "rules": {
            "development-workflow": "streamlined",
            "code-standards": "relaxed",
            "quick-iteration": "enabled",
        },
    },
)

ENTERPRISE_SECURITY = ConfigTemplate(
    name="enterprise-security",
    description="High-security configuration for large teams in regulated environments",
    best_for="Regulated environments, large teams, production systems, compliance requirements",
    config_claude_code={
        "defaultMode": "plan",
        "autoApprove": False,
        "confirmBeforeToolUse": True,
        "requireExplicitApproval": True,
        "tools": {
            "thinking": True,
            "allowedTools": ["Read", "Edit", "Task", "CreateDiagram"],
            "restrictedBash": True,
            "bashTimeout": 30,
            "logAllOperations": True,
        },
        "permissions": {
            "allowedCommands": [
                "git status",
                "git diff --name-only",
                "pytest --collect-only",
                "npm audit",
                "ls",
                "find . -name",
                "grep -n",
                "head",
                "tail",
            ],
            "deniedCommands": [
                "git push",
                "npm publish",
                "pip install",
                "npm install",
                "curl",
                "wget",
                "chmod",
                "chown",
                "sudo",
                "rm",
            ],
            "requireApprovalFor": "*",
            "auditLog": "~/.agent-audit.log",
        },
        "security": {
            "sandboxMode": True,
            "fileAccessControl": "whitelist",
            "allowedDirectories": ["./src/", "./tests/", "./docs/"],
            "encryptSensitiveData": True,
            "sessionTimeout": 1800,
        },
        "validation": {
            "requireTestsForChanges": True,
            "codeReviewRequired": True,
            "securityScanOnWrite": True,
            "complianceChecks": ["pii-scan", "secret-scan", "license-check"],
        },
        "monitoring": {
            "trackAllFileChanges": True,
            "notifyOnSensitiveAccess": True,
            "generateComplianceReports": True,
        },
    },
    config_cursor={
        "chat.defaultModel": "claude-3-5-sonnet",
        "chat.mode": "plan-first",
        "agent.alwaysConfirm": True,
        "agent.requireApproval": True,
        "agent.maxIterations": 5,
        "files.autoSave": "never",
        "editor.formatOnSave": False,
        "rules": {
            "security-first": "enabled",
            "compliance": "enabled",
            "audit-logging": "enabled",
            "restricted-access": "enabled",
        },
    },
)


# Template registry
TEMPLATES = {
    template.name: template
    for template in [
        DEVELOPMENT_TEAM,
        SOLO_DEVELOPER,
        ENTERPRISE_SECURITY,
    ]
}


def get_template(template_name: str) -> ConfigTemplate:
    """Get a configuration template by name."""
    if template_name not in TEMPLATES:
        available = ", ".join(TEMPLATES.keys())
        raise ValueError(
            f"Template '{template_name}' not found. Available: {available}"
        )

    return TEMPLATES[template_name]


def list_templates() -> list[ConfigTemplate]:
    """List all available configuration templates."""
    return list(TEMPLATES.values())


def generate_config_content(template: ConfigTemplate, agent_type: str) -> str:
    """Generate configuration file content for a template and agent type."""
    config = template.get_config(agent_type)

    if agent_type == "claude-code":
        return json.dumps(config, indent=2)
    elif agent_type == "cursor":
        # For Cursor, we generate .cursorrules content
        rules_content = f"""# Cursor Configuration - {template.name.title().replace("-", " ")}
# Generated by bob-the-engineer

# {template.description}
# Best for: {template.best_for}

## Core Settings
{json.dumps(config, indent=2)}

## Usage Guidelines
This configuration is optimized for {template.best_for.lower()}.

## Key Features:
- Default Model: {config.get("chat.defaultModel", "claude-3-5-sonnet")}
- Mode: {config.get("chat.mode", "plan-first")}
- Auto Confirm: {config.get("agent.alwaysConfirm", True)}
- Max Iterations: {config.get("agent.maxIterations", 10)}

## Rules
{chr(10).join([f"- {rule}: {status}" for rule, status in config.get("rules", {}).items()])}
"""
        return rules_content
    else:
        raise ValueError(f"Unsupported agent type: {agent_type}")
