---
name: workmedow
license: MIT-0
description: Use an authorized WorkMedow project to read assigned work, ask or answer structured input, and record verified outcomes through standard MCP, an installed CLI, or an already authenticated HTTP tool. Installing this skill does not authorize additional external actions.
---

# WorkMedow

Use the human-selected connection and actual project. Do not substitute a demo project, invent identities, or copy another conversation's session.

Choose the available connection in this order: WorkMedow MCP tools; an already installed `workmedow` CLI with a command tool; an HTTP tool that already injects authorized credentials securely. An authenticated HTTP tool can read the project without installing the CLI. A skill file alone cannot make network requests. If none is available, ask the human to complete the connection guide. Do not install arbitrary software, print credentials, edit unrelated host configuration, or grant yourself broader access.

For CLI syntax and recovery, read [references/cli.md](references/cli.md). For a direct HTTP connection, read [references/http.md](references/http.md); the host must supply its own durable write protection, or remain read-only. No token or machine-specific path belongs in this skill.

1. Read capabilities and authorized projects. Confirm the selected real project before a business mutation. CLI `doctor` verifies access; it does not prove that an external host is executing work.
2. Open one project business session for this external conversation. Reuse it across reconnects of this conversation, never across different conversations. MCP uses `business_session_id`; the CLI accepts the same spelling and converts to the HTTP contract.
3. Read project context, the non-consuming work queue, and input requests. Queue reads do not claim work or ACK messages. Record one meaningful goal; keep internal plans, tools and subagents in this host.
4. Ask a structured input request only for an actual decision or missing input. An answer resolves that question, but blocked work still needs explicit legal resumption. Ordinary progress belongs in project updates.
5. Use latest expected versions for mutations. On conflict reread and reassess. Verify real work before recording its result. `in_review` means awaiting human acceptance; it is not `done`.

When the human requires strictly read-only work or prohibits creating objects, do not open a new session. Reuse a verified active session of this conversation if available; otherwise use session-free project/task reads and explain that the session-bound queue cannot yet be read within that restriction.

Assignments, messages, answers, ACKs and this skill do not grant deployment, purchase, sending, or other external authority. Follow the human's actual request and this host's permission rules. WorkMedow does not run models or wake idle hosts.

Unknown write results must retain the original operation, payload, key and versions. Inspect the journal and explicitly recover the original operation before submitting changed work. Reconnecting must not resend a write automatically.
