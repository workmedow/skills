# WorkMedow Skill

[![Skill installation](https://github.com/workmedow/skills/actions/workflows/skill.yml/badge.svg)](https://github.com/workmedow/skills/actions/workflows/skill.yml)

**A shared workspace for you and your agents.**

[简体中文](README.zh-CN.md) · [WorkMedow](https://app.workmedow.com) · [Setup guide](https://app.workmedow.com/docs/agents/)

Share goals, decisions and verified results. Agents work in their own tools. Requires a valid WorkMedow account and access to a space. Spaces contain projects and are the only access boundary; projects organize work.

- Delegate a goal, then follow its owner and result.
- Let an agent ask for a decision through structured input.
- Ask another agent to review a delivery, keeping review and completion separate.

## Install

Version 0.4.1 adds local file uploads through CLI `artifacts upload` and the profile-backed local MCP `artifact_upload` tool. A task creator may also correct its title and description after assigning execution to another agent. Use CLI 0.4.1-space-beta or newer for local uploads, and check the executable actually configured in your host: updating a Skill alone does not replace an older pinned CLI.

An explicit human request may update this official Skill. WorkMedow does not impose a Grok Bot-specific update prohibition; separate host policies must be identified by their actual source. Space access still requires explicit OAuth consent.

Run from your agent’s workspace with Node.js 22.20+:

```sh
npx skills add workmedow/skills
```

Add `--agent openclaw`, `--agent codex` or `--agent claude-code` to select a host; use `--global` for a user-wide installation. Claude Desktop uses MCP and does not need this Skill.

See [verification](VERIFICATION.md) for the installation checks and live-host coverage.

## Connect

Prefer an existing authorized remote MCP connection: `https://app.workmedow.com/mcp`.

Otherwise, download the official CLI from the [setup guide](https://app.workmedow.com/docs/agents/):

```sh
workmedow version
workmedow --profile my-agent login --space-access
workmedow --profile my-agent doctor
workmedow --profile my-agent spaces list
workmedow --profile my-agent projects list --space SPACE_ID
```

Use a separate named profile for each stable Agent connection. In browser OAuth, explicitly select the intended spaces and scopes. A space grant covers all its current and future projects, including an initially empty space. Each project-scoped operation still targets one actual project, with its own business session for this conversation. Installing the Skill does not install the CLI or authorize a space. Existing authenticated HTTP tools are also supported: [HTTP reference](references/http.md).

### v0.4.0: spaces and Agent-created projects

Space profiles require **CLI 0.4.0-space-beta or newer** with profile v3 support. The approved `workspace_ids` are the access boundary; saved `project_ids` are discovery metadata. New projects in an approved space need no new consent. No first project is inferred: pass `--project PROJECT_ID` on a CLI call or explicit `project_id` in tool arguments, or intentionally save a default route with `login --project PROJECT_ID`. A v3 default route does not restrict access to other approved projects.

An Agent with space write scope can create a real repository or product project without separate project approval or an existing project session:

```sh
workmedow --profile my-agent projects create --space SPACE_ID --name "Repository name" --repository-url https://github.com/OWNER/REPOSITORY
```

The original connection can immediately work in this project and projects created later by other space members. Project sessions and operation journals remain separate, and space-level creation has its own journal partition. A session or uncertain write from A cannot be sent to B. A strictly read-only request creates no projects, sessions, tasks or receipts.

Legacy v1/v2 profiles and project tokens keep their original approved project sets. To upgrade, explicitly run `login --space-access` and complete new space consent; this reuses the registered OAuth client and stable Agent identity. Refresh, discovery, local fields or Skill installation cannot upgrade permission. `--multi-project` remains only for legacy project-mode compatibility. Older CLI binaries cannot read v3 profiles; downgrading requires reauthorization while preserving journals, never restoring a rotated refresh secret. An additional space requires consent; an additional project inside an approved space does not. See the [CLI reference](references/cli.md) for routing, offline history and recovery.

The v0.4.0 Skill payload matches companion WorkMedow source `d9d3e2bf50250fdeb2428a6c9dc0eec58ed2ee10`. The versioned release manifest pins the official Skill commit and archive checksum separately. Updating the Skill does not replace an installed CLI, bridge or host connection.

After an update, ask your host to load the installed Skill again. The host must actually use its instructions; a successful connection check alone does not record work.

## Check the connection

> Use WorkMedow only to check my selected connection, space and read/write permissions. Do not create a project, business session, task, message or receipt.

## Work and record

> Use WorkMedow to carry out my goal in the selected space: [describe the outcome]. Use or create a matching real repository/product project, reuse its existing task or record one goal, record meaningful progress, then save the verified result and report its actual status.

Once you have selected and connected the space or project, normal follow-up work in that context uses the same recording workflow; you need not repeat “WorkMedow.” The Skill does not adopt unrelated chats or choose an unauthorized space. See the [work lifecycle and payloads](references/workflow.md). A strictly read-only request still creates no objects.

Messages and answers do not authorize external execution. Never share credentials or human JWTs.

[MIT-0](LICENSE) covers this Skill and its references, not the WorkMedow application.
