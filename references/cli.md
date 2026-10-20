# CLI workflow

The operator installs the binary for this machine and signs in once with a named profile bound to one real project. Browser PKCE is the default; `login --device` supports a headless machine when the server advertises device authorization. A private project credential can alternatively be imported with `--token-file`; never put a token in command arguments or chat.

```sh
workmedow --profile team login
workmedow --profile team doctor
```

Use the operator-provided profile name. The human selects one real project in the authorization page; no project ID needs to be copied. The default service is the official global origin. An explicit `--url`/`--region` can select another authorized environment; use another profile when an existing binding conflicts. `doctor` and the following reads do not create business objects:

```sh
workmedow --profile team api call capabilities.get --input - <<'JSON'
{}
JSON
workmedow --profile team api call projects.list --input - <<'JSON'
{}
JSON
```

JSON arguments come from stdin or `--input /path/to/arguments.json`. Output is JSON with `data` and, for a journaled mutation, `operation_id`. Do not construct shell commands by interpolating task text. Supply JSON through a file or a quoted heredoc; keep personal content out of terminal logs when possible.

Open a session deliberately, then use its returned `data.id` for this conversation:

```sh
workmedow --profile team api call sessions.open --input - <<'JSON'
{"name":"Current work conversation","idempotency_key":"A_UNIQUE_OPERATION_KEY"}
JSON
workmedow --profile team api call agent.work_queue --input - <<'JSON'
{"business_session_id":"SESSION_ID"}
JSON
```

The profile binds the project; a different explicit `project_id` is rejected. Obtain latest task versions with `tasks.get`. Use supported operations from the server contract: `tasks.create/update/complete`, `projects.post_update`, `action_requests.list/create/answer`, and `sessions.close`. Inspect the tool/API schema for required versions rather than inventing them. CLI mutations missing a key receive one durable key before transmission; callers may also supply their own stable key. Never reuse a key for changed arguments.

If the terminal reports an unknown operation result or the process was killed:

```sh
workmedow --profile team api operations
workmedow --profile team api recover OPERATION_ID --confirm
```

Recovery is an explicit resend of the original immutable wire request with the original key. It does not resend edited input. Authorization or identity changes isolate the old operation. A server conflict requires checking the original result and current version; do not bypass isolation by using a new key.

Consuming `inbox.read/wait` calls are different: their receipt leases are non-idempotent and cannot be recovered by replay. Prefer `agent.work_queue`. If an inbox response was lost, an operator must verify the server receipt state, then use `api resolve-receipt ID --confirmed --evidence 'verified server observation'`; this only records the observation and never completes a task or bypasses an unknown task write.

`logout` revokes an OAuth family when available and removes that profile's local credentials. Imported static credentials must be revoked in WorkMedow by an authorized human. Drafts and operation journals remain isolated for recovery. Windows, macOS and Linux use the operating system's private configuration directory; no fixed path is required in the skill.
