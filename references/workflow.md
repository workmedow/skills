# Record requested work

Use this lifecycle for work the human requests in their selected, connected project. A later request to continue that goal does not need to mention WorkMedow again. A connection check, unrelated chat or strictly read-only request does not authorize this lifecycle's writes.

## Connection and identifiers

Read capabilities and authorized spaces/projects, then project context. Confirm `authorization_mode` and the target's effective `write` scopes. Space credentials advertise `effective_workspaces` and cover each authorized space's current and future projects. A writable space permits creating a real product/repository project with `project_create` before any project session exists, including in an empty space. Legacy project credentials remain restricted to `effective_projects` and require explicit space reauthorization to upgrade. Use the authenticated identity shown by the connection/context; never choose another Agent's name to gain access. If the work target is unclear or write access is missing, explain the missing choice or permission instead of writing elsewhere. Connection success or an open session alone does not prove write access.

Agent credentials normally have `personal_access: false`: they cannot use private captures or personal reviews. That flag does not disable shared writes inside an authorized space. Display names do not determine scope or turn private data into shared project content.

Use the existing active session only if it belongs to this external conversation, identity and project. Otherwise open one session and save its returned ID. If this conversation explicitly works in multiple projects, keep separate session IDs and task context for each project; never pass A's session to B. Do not open a session on every tool call or borrow another conversation's session. Read the non-consuming queue and input history when useful; no ACK is required merely to inspect the queue.

| MCP tool | CLI / HTTP command operation |
|---|---|
| `capabilities_get` | `capabilities.get` |
| `workspaces_list` / `workspace_get` | `workspaces.list` / `workspaces.get` |
| `projects_list` | `projects.list` |
| `project_create` | `projects.create` |
| `project_context_get` | `projects.snapshot` |
| `agent_session_open` | `sessions.open` |
| `agent_work_queue` | `agent.work_queue` |
| `task_get` / `tasks_list` | `tasks.get` / `tasks.list` |
| `task_create` | `tasks.create` |
| `task_update` | `tasks.update` |
| `task_progress_post` | `tasks.progress` |
| `task_complete` | `tasks.complete` |
| `task_context_get` | `tasks.context` |
| `task_contract_get` / `task_contract_propose` | `task_contracts.get` / `task_contracts.propose` |
| `verification_bundle_create` / `verification_bundle_get` / `verification_bundles_list` | `verification_bundles.create/get/list` |
| `task_input_request_clarification` | `action_requests.request_clarification` |
| `project_guidance_list/get/propose/update/report_implementation` | corresponding `project_guidance.*` operations |
| `artifact_get` / `artifact_preview` | `artifacts.get` / `artifacts.preview` |
| local stdio `artifact_upload` | CLI `artifacts upload`; multipart HTTP `/api/v1/projects/{project_id}/artifacts/upload` |

Read `capabilities_get` and `workspaces_list` with `{}`. `workspace_get` takes `{"workspace_id":"SPACE_ID"}`; `projects_list` optionally accepts that field to filter the directory. To create a requested real project in a writable space, use `project_create` with `{"workspace_id":"SPACE_ID","name":"Repository name","idempotency_key":"NEW_PROJECT_KEY"}`, optionally adding `description` and `repository_url`. Do not send `project_id` or a business session for creation; use the returned project ID for subsequent work. Space access is unchanged by adding a project, so the original connection can use the new project immediately.

Project context uses `{"project_id":"PROJECT_ID"}`. Use JSON arguments directly for MCP; for CLI pass a JSON file or quoted stdin to `workmedow --profile NAME api call OPERATION --input FILE`. Direct HTTP sends the same payload to the command endpoint but uses `session_id` in place of `business_session_id`. Read calls need no idempotency key.

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

The creator keeps authority to revise a handed-off task's `title` and `description` using `task_update`, its own business session and the latest `expected_version`. Send only those definition fields in this correction. The task keeps its assignee, execution status and claim; other agents cannot make this edit, and the creator cannot complete or control execution after handoff. A corrected goal advances its version and invalidates stale review evidence. Replace the actual description instead of using a comment as a competing source of requirements.

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

## Optional collaboration capabilities

Read the advertised `features` and their independent `version/enabled` values.
`version:1` establishes contract support; `enabled:true` is also required to start
a new workflow. With `enabled:false`, supported existing records remain readable
and existing tasks may finish evidence, answers and resolution.
When available, call `task_context_get` with the real task at goal start, explicit
handoff and before completion. Read every remaining applicable-guidance page if
the bounded context is truncated. Effective rules are shared context, never
permission to run tools, deploy, change access or weaken human review.

For human-enabled completion standards, record actual checks with
`verification_bundle_create`: pass `task_id`, current `expected_task_version`,
`contract_id`, and `checks` entries containing `criterion_id`, `result`
(`passed`, `failed`, `unverified`), `method`, RFC3339 `checked_at`,
`artifact_version`, and actual `artifact_ids`. Failed or incomplete reports are
valid records; they do not satisfy completion. Agent self-report is not independent
CI verification. Only humans activate/weaken standards or grant a scoped waiver.
Pass a current unused `verification_bundle_id` to `task_complete`; after rejection
or changed goal/assignment/standards, create a new report. Review remains separate.

The bundle's task concurrency field is **`expected_task_version`**. Completion
uses **`expected_version`**. Check evidence is the **`artifact_ids` array inside
each check**; a singular `artifact_id` or `evidence_artifact_ids` is not that field.
Read back the returned checks before completing. An incomplete report may be
saved, but cannot satisfy an enabled criterion without its evidence or a human
waiver. Keep unused reports as history; never overwrite them to fix a submission.

Choose artifacts explicitly for each submission. Optional `presentation` is
`{primary_artifact_id,items:[{artifact_id,role,title,description,cover_artifact_id,
preview_artifact_id}]}`. Roles are `result`, `evidence`, `support`; optional strings
may be omitted. Cover/preview IDs must be selected authorized files from the same
task/project. Preview editions stay distinct from originals. Do not invent
screenshots or silently include historical attachments.

Use `request_kind:"decision"` only for a real decision. Supply `decision_brief`
with `background`, `why_recipient`, at least two `choices:[{id,label,tradeoff}]`,
`recommended_id`, `recommendation`, optional evidence `artifact_ids`, and optional
RFC3339 `answer_by`. Information requests stay lightweight. Decision answers must
include the observed `expected_revision`; never apply an old answer to a revised
question. A clarification request preserves the blocker and does not resume work.

Propose reusable guidance from the actual shared source and its version using
`project_guidance_propose` with `title`, `body`,
`guidance_source:{type,id,version}`, optional `applies_to_tags`, `expires_at`,
`supersedes_id`. Source types are `task`, answered `action_request`, rejected
`submission`, or task-discussion `message`. Agents edit only their own unpublished
proposals. All writable humans may publish; Agents cannot publish or retire.
After separately authorized implementation, report real code/test/lint/document
work and evidence with `project_guidance_report_implementation`. Published rules
and implementation reports are distinct facts.

Preview reads return bounded text/structured content or metadata, not large binary
base64. They do not ACK or accept results. New optional fields must not be added to
an already journaled unknown write; settle its original payload/key first.

## Recording failures

Do not say a goal, progress or completion was recorded until the service confirms it. If creation/start fails, report which record is missing and resolve the recording gap before substantial untracked work when the human expects a shared record. If work finished but completion recording failed, report both facts separately.

On an ordinary version conflict, reread and reassess before a new write. On an unknown result, preserve the original payload, idempotency key and expected versions; first confirm or explicitly recover that original operation before another conflicting write in its space/project partition. Do not create another goal to replace it, use a new key, submit edited input or replay automatically on reconnect. Explicitly requested work in a different authorized project may continue in its separate partition with its own session and goal; keep the original unresolved record visible and never retarget it. An unknown space-level project creation still blocks conflicting creation in that space. CLI recovery and direct HTTP durability are described in their transport references.
