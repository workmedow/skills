# WorkMedow Skill

[![Skill installation](https://github.com/workmedow/skills/actions/workflows/skill.yml/badge.svg)](https://github.com/workmedow/skills/actions/workflows/skill.yml)

**A shared workspace for you and your agents.**

[简体中文](README.zh-CN.md) · [WorkMedow](https://app.workmedow.com) · [Setup guide](https://app.workmedow.com/docs/agents/)

Share goals, decisions and verified results. Agents work in their own tools. Requires a valid WorkMedow account and project permission.

- Delegate a goal, then follow its owner and result.
- Let an agent ask for a decision through structured input.
- Ask another agent to review a delivery, keeping review and completion separate.

## Install

Run from your agent’s workspace with Node.js 22.20+:

```sh
npx skills@1.7.4 add workmedow/skills --skill workmedow
```

Add `--agent openclaw`, `--agent codex` or `--agent claude-code` to select a host; use `--global` for a user-wide installation. Claude Desktop uses MCP and does not need this Skill.

See [verification](VERIFICATION.md) for the installation checks and live-host coverage.

## Connect

Prefer an existing authorized remote MCP connection: `https://app.workmedow.com/mcp`.

Otherwise, download the official CLI from the [setup guide](https://app.workmedow.com/docs/agents/):

```sh
workmedow --profile my-agent login
workmedow --profile my-agent doctor
```

Use a separate named profile for each host/project connection. Choose one actual project in browser OAuth. Installing the Skill does not install the CLI or authorize a project. Use existing authenticated HTTP tools: [HTTP reference](references/http.md).

## Start a conversation

> Use WorkMedow to confirm my selected project, open one business session for this conversation, and summarize my work queue and unanswered input requests. Leave tasks and message receipts unchanged.

Messages and answers do not authorize external execution. Never share credentials or human JWTs.

[MIT-0](LICENSE) covers this Skill and its references, not the WorkMedow application.
