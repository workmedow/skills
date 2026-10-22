# Verification

This repository distributes the WorkMedow Skill. Installing it does not configure a model, install the WorkMedow CLI, authorize a project, or start an agent.

## Installation checks

### Initial v0.1.0 publication

The release smoke test uses the official `skills@1.7.4` installer with explicit Codex and OpenClaw targets, project scope, and copy mode. It verifies the installed Skill, every relative Markdown reference, and Codex UI metadata byte for byte against the source. Tests run in a separate Git workspace with telemetry disabled and do not install into the operator's personal Skill directories.

On 2026-10-20, the Skill format check and isolated local installation passed on macOS 26.6.2 with Node.js 25.2.1 and `skills@1.7.4`. Both host directories contained identical copies of `SKILL.md`, `agents/openai.yaml`, `references/cli.md` and `references/http.md`; personal Skill directory metadata was unchanged. This verifies file installation targets, not live agent execution.

The same installation check also passed from the public `workmedow/skills` source into a second fresh workspace. The installed Skill SHA-256 was `d7aae7662d17d286af4a9750c64cc4db194046dfa9112205f3b7a37e2c513a2b` in both targets.

The initial [GitHub Actions run](https://github.com/workmedow/skills/actions/runs/39356830852) passed on Ubuntu with Node.js 22.20.0. The [workflow](.github/workflows/skill.yml) repeats the file installation check on pushes and pull requests. These are install checks for the official Skill installer; they are not live-host model or OAuth tests.

## Work-recording checks for v0.1.1

On 2026-10-20, the revised Skill and all three workflow/transport references passed format checks and isolated copy-mode installation into Codex and OpenClaw project directories. All five Skill payload files matched their source bytes. This remains an installer check, not proof that either host automatically selected the Skill.

- An independent agent explicitly loaded the Skill, used an already configured CLI and a local MySQL-backed project, reproduced and fixed a small code defect, and passed the two existing tests. It reused one goal through `todo → in_progress → done` and read back the saved result. This verifies a loaded Skill's work-recording behavior through the CLI.
- A separate independent agent received a strictly read-only connection-check request while its credential had write permission. It created no business session, task, progress, completion or receipt; the local operation journal remained empty.
- The companion service's official MCP SDK test completed the same lifecycle against real local Agent authentication and MySQL. Replaying a progress write with the original key returned the identical Activity, preserved the task version and did not duplicate progress. The independent protocol session was closed after completion.

These checks used isolated fixtures. They do not establish Muse cloud execution, Muse's automatic Skill discovery, a live OpenClaw model, production OAuth, or a different project's authorization. Installing/updating a Skill does not replace instructions already cached by a running host; ask that host to load the installed Skill again before evaluating it.

## Collaboration contracts for v0.2.0

On 2026-10-21, the optional collaboration workflow passed the format check and
the pinned `skills@1.7.4` installer in a fresh project for Codex and OpenClaw.
All five installed payload files matched the source. No personal host settings
or credentials were changed by this installation check.

Companion-product tests used a dedicated local MySQL database. A real Codex
stdio MCP host and Grok Bot through its existing Mac command tool/CLI each read
actual evidence, an answered decision and effective guidance, created a report,
submitted it and independently read back `in_review`. Neither accepted its own
submission. Grok used an updated private Skill, so that result is protocol and
host evidence, not proof of automatic discovery of this exact public release.

The host checks exposed a distinction now explicit in the workflow:
`verification_bundles.create` needs `expected_task_version`; `tasks.complete`
needs `expected_version`. Each check's evidence uses its own `artifact_ids`
array. An incomplete report remains a record and must not be mistaken for
evidence-complete delivery. Capability support and creation enablement are
checked separately; older services retain their lightweight workflow.

## Multi-project connections for v0.3.0

On 2026-10-22, the five Skill payload files matched companion WorkMedow commit
`8366bae3be7a4e979c1109e60e48174d4fb5bde4` byte for byte. The Skill format check
and the pinned `skills@1.7.4` installer passed in a fresh isolated Git project
for Codex and OpenClaw. The check compared `SKILL.md`, UI metadata and all three
references against the source; it did not alter a personal Skill installation.

An independent read-through evaluated a read-only request in project A followed
by explicitly requested work in project B. The guidance keeps A's reads free of
new sessions or receipts, selects B explicitly for its work, and preserves B's
own business session and original operation during unknown-result recovery.
This is a behavioral review of the instructions, not an executed model-host or
production OAuth test.

The companion product's isolated OAuth/API, stdio subprocess and real-MySQL
tests cover multi-project approval, explicit project selection, project-bound
business sessions, journal isolation, v1 profile upgrade and reauthorization
boundaries. Those product checks are separate from installation of this public
Skill release. Multi-project CLI profiles require CLI
`0.3.0-multi-project-beta` or newer; updating these files does not update a binary.

## Runtime and authorization

- Standard Skill hosts need a working WorkMedow MCP connection, the WorkMedow CLI and a command tool, or an already authenticated HTTP tool.
- Claude Desktop connects through MCP; it does not use the coding-agent Skill folder route.
- Browser project authorization, business-session creation and live collaboration are separate from the file installation checks.
- The smoke test does not exercise OpenClaw's native Git installer, a live OpenClaw model, project OAuth, task changes, input answers, or message ACKs.

Use the [official setup guide](https://app.workmedow.com/docs/agents/) for runtime downloads and project authorization. Earlier product integration results do not automatically establish a live-host result for this public Skill release.
