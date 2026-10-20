# Verification

This repository distributes the WorkMedow Skill. Installing it does not configure a model, install the WorkMedow CLI, authorize a project, or start an agent.

## Installation checks

The release smoke test uses the official `skills@1.7.4` installer with explicit Codex and OpenClaw targets, project scope, and copy mode. It verifies the installed Skill, every relative Markdown reference, and Codex UI metadata byte for byte against the source. Tests run in a separate Git workspace with telemetry disabled and do not install into the operator's personal Skill directories.

On 2026-10-20, the Skill format check and isolated local installation passed on macOS 26.6.2 with Node.js 25.2.1 and `skills@1.7.4`. Both host directories contained identical copies of `SKILL.md`, `agents/openai.yaml`, `references/cli.md` and `references/http.md`; personal Skill directory metadata was unchanged. This verifies file installation targets, not live agent execution.

The same installation check also passed from the public `workmedow/skills` source into a second fresh workspace. The installed Skill SHA-256 was `d7aae7662d17d286af4a9750c64cc4db194046dfa9112205f3b7a37e2c513a2b` in both targets.

The initial [GitHub Actions run](https://github.com/workmedow/skills/actions/runs/39356830852) passed on Ubuntu with Node.js 22.20.0. The [workflow](.github/workflows/skill.yml) repeats the file installation check on pushes and pull requests. These are install checks for the official Skill installer; they are not live-host model or OAuth tests.

## Runtime and authorization

- Standard Skill hosts need a working WorkMedow MCP connection, the WorkMedow CLI and a command tool, or an already authenticated HTTP tool.
- Claude Desktop connects through MCP; it does not use the coding-agent Skill folder route.
- Browser project authorization, business-session creation and live collaboration are separate from the file installation checks.
- The smoke test does not exercise OpenClaw's native Git installer, a live OpenClaw model, project OAuth, task changes, input answers, or message ACKs.

Use the [official setup guide](https://app.workmedow.com/docs/agents/) for runtime downloads and project authorization. Earlier product integration results do not automatically establish a live-host result for this public Skill release.
