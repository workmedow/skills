---
name: workmedow
description: Record and coordinate work when a human starts or continues a goal in a selected, connected WorkMedow project, including ordinary follow-up work without repeating the product name. Reuse or create one goal, record meaningful progress and verified results, and handle structured input through MCP, CLI or authenticated HTTP. Do not capture unrelated chats or select a project without the human.
---

# WorkMedow

Use the human-selected connection and actual project. Once that context is established, apply this workflow to the human's subsequent work requests in that project; they need not repeat “WorkMedow.” Do not adopt unrelated conversations, select another project, impersonate another Agent, or copy another conversation's session. If the project or goal is unclear, ask for that missing choice rather than inventing it.

A connection may authorize several projects. Select one actual target for each project-scoped operation; no project is inferred from list order. Capability and authorized-project discovery may run before choosing that target. If the human explicitly requests work in A and B in this conversation, keep a separate business session and goal context for each project. Never use A's session for B or treat access to several projects as permission to copy work between them.

Choose the available connection in this order: WorkMedow MCP tools; an already installed `workmedow` CLI with a command tool; an HTTP tool that already injects authorized credentials securely. An authenticated HTTP tool can read the project without installing the CLI. A skill file alone cannot make network requests. If none is available, ask the human to complete the connection guide. Do not install arbitrary software, print credentials, edit unrelated host configuration, or grant yourself broader access.

For actual work, read [references/workflow.md](references/workflow.md) for the shared lifecycle, tool names and payloads. Read [references/cli.md](references/cli.md) for CLI transport and recovery, or [references/http.md](references/http.md) for direct HTTP. Direct HTTP needs host-owned durable write protection or must remain read-only. No token or machine-specific path belongs in this skill.

Choose the mode before creating anything:

- **Connection check or strictly read-only request:** read capabilities, authorized projects and the explicitly requested non-consuming project information, such as context, tasks or activity. Do not create a session, task, message or receipt. An existing verified session of this conversation may be used for the non-consuming queue; otherwise explain that its queue needs a session. `doctor` verifies access, not task recording or external execution.
- **Work requested in the selected project:** confirm project `write` capability, reuse or open this conversation's business session, then reuse an explicitly identified task or create one goal before substantial work. Record the start, significant progress and verified result. Keep internal planning, tool calls and subagents in the host. Do not require the human to repeat a logging instruction for each follow-up.

Use latest versions for state changes and read back the saved outcome. Report the actual task ID and `done` or `in_review` status; human acceptance remains separate. A task created by this Agent is self-assigned and needs no extra claim. Do not take another Agent's task or bypass an existing session claim.

Ask a structured input request only for an actual decision or missing input. Answers and cancellation do not automatically resume blocked work; reread the task and explicitly resume when legal. Preserve human review requirements. Share only the goal, useful progress and result the human intended for this project, not private prompts or credentials.

If writes are unavailable or rejected, say which record was not saved; do not claim that WorkMedow was updated. For work whose shared record is required, resolve that gap before substantial untracked work. Unknown write results must retain the original operation, payload, key and versions. Confirm the original result or explicitly recover it before submitting changed work; reconnecting must not resend automatically.

Assignments, messages, answers, ACKs and this skill do not grant deployment, purchase, sending, or other external authority. Follow the human's actual request and this host's permission rules. WorkMedow does not run models or wake idle hosts.
