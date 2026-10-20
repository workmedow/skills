# Record requested work

Use this lifecycle for work the human requests in their selected, connected project. A later request to continue that goal does not need to mention WorkMedow again. A connection check, unrelated chat or strictly read-only request does not authorize this lifecycle's writes.

## Connection and identifiers

Read capabilities and authorized projects, then project context. Confirm that `effective_scopes` includes `write`, and that the intended project appears in `effective_projects` with `write` in its `scopes`. Use the authenticated identity shown by the connection/context; never choose another Agent's name to gain access. If the project is not selected or write access is missing, explain the missing choice or permission instead of writing elsewhere. Connection success or an open session alone does not prove write access.

Agent credentials normally have `personal_access: false`: they cannot use private captures or personal reviews. That flag does not disable writes to an authorized shared project, even when its display name is “Personal space.” Check that project's own scopes.

Use the existing active session only if it belongs to this external conversation, identity and project. Otherwise open one session and save its returned ID. Do not open a session on every tool call or borrow another conversation's session. Read the non-consuming queue and input history when useful; no ACK is required merely to inspect the queue.

| MCP tool | CLI / HTTP command operation |
|---|---|
| `capabilities_get` | `capabilities.get` |
| `projects_list` | `projects.list` |
| `project_context_get` | `projects.snapshot` |
| `agent_session_open` | `sessions.open` |
| `agent_work_queue` | `agent.work_queue` |
| `task_get` / `tasks_list` | `tasks.get` / `tasks.list` |
| `task_create` | `tasks.create` |
| `task_update` | `tasks.update` |
| `task_progress_post` | `tasks.progress` |
| `task_complete` | `tasks.complete` |

Read `capabilities_get` and `projects_list` with `{}`. Project context uses `{"project_id":"PROJECT_ID"}`. Use JSON arguments directly for MCP; for CLI pass a JSON file or quoted stdin to `workmedow --profile NAME api call OPERATION --input FILE`. Direct HTTP sends the same payload to the command endpoint but uses `session_id` in place of `business_session_id`. Read calls need no idempotency key.

Successful results are inside `data`: use MCP `structuredContent.data` or the text JSON's `data`, and CLI/HTTP `data`. The session/task fields below refer to that object. A CLI `operation_id` identifies the local write journal, not a task or session.

All uppercase string values below are placeholders: replace them with actual server-returned IDs or a newly saved unique key for that write. Use a different key for each distinct write and preserve its original payload. Versions `1` and `2` illustrate an unchanged new task, not values to assume for an existing task; use the actual latest integer `task.version`.

## One goal, then start

Open a session if needed:

```json
{"project_id":"PROJECT_ID","name":"Current work conversation","idempotency_key":"OPEN_KEY"}
```

Save the session response's `data.id`. Subsequent queue reads use:

```json
{"project_id":"PROJECT_ID","business_session_id":"SESSION_ID"}
```

If the human provides a task ID, or the selected assignment clearly identifies this goal, read it with `task_get` / `tasks.get`:

```json
{"project_id":"PROJECT_ID","task_id":"TASK_ID"}
```

Reuse that task when its goal and responsibility match. Do not merge unrelated work just because titles resemble each other. Do not create a duplicate for a follow-up or a reconnect. If the task is owned by someone else or claimed by a different session, explain the required handoff; do not silently reassign or impersonate them.

When no existing task represents the requested goal, create one with `task_create` / `tasks.create`:

```json
{"project_id":"PROJECT_ID","business_session_id":"SESSION_ID","idempotency_key":"CREATE_KEY","title":"The human's requested outcome","description":"The agreed scope and how the result will be checked."}
```

Use the actual requested goal, not the example text. Save the returned task `id` and `version`. The new task is `todo`, assigned to the authenticated Agent by default. Omit `assignee_id` for this self-recorded work; no extra claim is needed. Keep internal plans, tool calls and subagents outside the shared task list. Preserve project/human review requirements.

Before substantial work, mark a legal `todo` task as started with `task_update` / `tasks.update`:

```json
{"project_id":"PROJECT_ID","business_session_id":"SESSION_ID","idempotency_key":"START_KEY","task_id":"TASK_ID","expected_version":1,"status":"in_progress"}
```

Use the version just returned by creation, or reread an existing task. Save the returned new task version. If already `in_progress`, reuse that state. Do not reopen `done`, `cancelled` or `in_review` automatically. Blocked work needs its blockers resolved and an explicit legal resume; resolving input alone does not resume it.

## Meaningful progress

At a significant result, obstacle or change of approach, call `task_progress_post` / `tasks.progress` for this same task:

```json
{"project_id":"PROJECT_ID","business_session_id":"SESSION_ID","idempotency_key":"PROGRESS_KEY","task_id":"TASK_ID","body":"What was actually achieved or what is blocking the requested outcome."}
```

This returns an activity, not a task. Keep the saved task ID; do not replace it with the activity ID. Progress does not change `Task.version` or task status and needs no `expected_version`. Avoid per-tool chatter. For a short goal, a start and verified final result may suffice.

Ask a structured input request only for a real decision or missing input. Use current request/task versions. Blocking request changes can change the task version; reread the task afterwards. Keep human and request blockers separate, and explicitly resume only when legal. An answer, progress post or ACK is not task completion or external execution authority.

## Verified completion and readback

After doing and verifying the actual work, reread the task with `task_get` / `tasks.get`. Complete it with the returned current version and a factual result/verification summary using `task_complete` / `tasks.complete`:

```json
{"project_id":"PROJECT_ID","business_session_id":"SESSION_ID","idempotency_key":"COMPLETE_KEY","task_id":"TASK_ID","expected_version":2,"summary":"The actual outcome, checks performed and remaining limitations."}
```

Optional `artifact_ids` must be real artifacts already published in this project/task. Never invent a result, link or passing check. `done` means completed; `in_review` means submitted for human acceptance. Do not bypass review or call a pending submission done. Read the task back again, then report its real project, task ID, saved status and result. Acceptance, receipt ACK and task completion remain separate facts.

## Recording failures

Do not say a goal, progress or completion was recorded until the service confirms it. If creation/start fails, report which record is missing and resolve the recording gap before substantial untracked work when the human expects a shared record. If work finished but completion recording failed, report both facts separately.

On an ordinary version conflict, reread and reassess before a new write. On an unknown result, preserve the original payload, idempotency key and expected versions; first confirm or explicitly recover that original operation. Do not create another goal, use a new key, submit edited input or replay automatically on reconnect. CLI recovery and direct HTTP durability are described in their transport references.
