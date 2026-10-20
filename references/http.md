# Direct HTTP tools

Use this path when MCP and an installed CLI are unavailable but the host already has an authenticated HTTP tool for the human-selected regional origin. Credentials must be injected from the host's secure connection store, never placed in skill text, request examples, chat, URLs, or diagnostic output. Use the project's scoped Agent credential, not another principal's identity. Include the connection's `X-WWM-Region` header. Keep HTTPS certificate verification enabled and do not forward credentials to a redirected origin.

The following paths are relative to that approved origin. Successful responses use `{"data": ...}`; errors use `{"error": {"code": ..., "message": ...}}`. Examples contain identifiers to replace with values verified from this connection, never guessed values.

## Read without creating objects

1. `GET /api/v1/me` with the tool's securely injected Bearer authorization. Check the actual `id`, `agent_id`, `kind`, `workspace_id`, and `region`; editable client names do not establish identity.
2. `POST /api/v1/commands/capabilities.get` with `{}`. Check `contract_version`, effective project/scope/transport capabilities, and the non-secret authorization fingerprint. Do not claim unavailable personal APIs or host execution.
3. `POST /api/v1/commands/projects.list` with `{}`. Confirm the actual authorized project matches the human's request. This POST is a classified read and needs no write key.

These reads do not require the CLI or a business session. Project context can then be read with `POST /api/v1/commands/projects.snapshot` and `{"project_id":"APPROVED_PROJECT_ID"}`. Input history uses `action_requests.list` with the same project field. A strictly read-only request must not open a session merely to obtain its session-bound queue.

## Session-bound work

Only when creating a business session is within the human's request and the host can meet the write requirements below:

```http
POST /api/v1/commands/sessions.open
Content-Type: application/json

{"project_id":"APPROVED_PROJECT_ID","name":"Current external conversation","idempotency_key":"DURABLY_SAVED_UNIQUE_KEY"}
```

Persist the returned `data.id` for this conversation. A different conversation needs its own session; reconnects of this conversation reuse its existing session. Do not infer it from an HTTP/MCP transport session or borrow another conversation's session.

```http
POST /api/v1/commands/agent.work_queue
Content-Type: application/json

{"project_id":"APPROVED_PROJECT_ID","session_id":"CURRENT_CONVERSATION_SESSION_ID"}
```

The queue is non-consuming: it does not claim tasks or ACK messages. The HTTP command contract uses **`session_id`**; MCP publishes **`business_session_id`** and performs an explicit adapter conversion. Direct HTTP calls must use the HTTP field. Use current task/request versions for subsequent mutations rather than copying versions from old conversation text.

## Host-owned write durability

Direct HTTP does not inherit the CLI's local journal. Before sending any write, the host must atomically persist its operation ID, exact original request bytes, unique idempotency key, expected versions, and binding to origin/region/principal/project/authorization. Serialize conflicting attempts. Save the confirmed response durably before marking the operation complete.

After a timeout, disconnect, crash, malformed successful response, server failure, or `operation_result_unknown`, preserve the operation and block changed or newly keyed writes until its original result is confirmed. A failed recovery attempt does not prove the first request failed. Reconnection must not resend anything automatically; an explicitly authorized recovery resends the original immutable request/key/versions only after verifying the same identity and current authorization. Permission changes isolate the old operation.

If the host cannot provide these durable guarantees, restrict this connection to reads; do not open a new session, answer, ACK, assign, submit, or complete work through it. An existing verified session of this conversation may still be used for the non-consuming queue read. Consuming `inbox.read/wait` uses non-idempotent receipt claims and must never be blindly replayed; prefer `agent.work_queue`.

Authentication, session creation, messages, answers and ACKs do not grant deployment, purchase, sending to external services, model invocation or other execution authority. WorkMedow records collaboration; the external host remains responsible for the human's actual requested work and its permission rules.
