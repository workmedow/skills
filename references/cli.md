# CLI workflow

The operator installs the binary for this machine and signs in once with a named profile bound to one real project. Browser PKCE is the default; `login --device` supports a headless machine when the server advertises device authorization. A private project credential can alternatively be imported with `--token-file`; never put a token in command arguments or chat.

`doctor` does not refresh an expired access token. Normal API calls can renew the existing OAuth profile within its approved identity/project/scopes before reading or writing. If renewal cannot be confirmed, report that limitation and reauthorize explicitly; do not switch profiles or broaden access to continue.

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

For requested work, use the operation names and JSON payloads in [workflow.md](workflow.md). The CLI accepts `business_session_id` and maps it to HTTP `session_id`; the profile supplies its project when omitted and rejects a different explicit `project_id`. Save the returned session ID for this conversation and task ID for this goal.

For example, save the selected operation's JSON arguments in a file, then run:

```sh
workmedow --profile team api call tasks.create --input /path/to/create-goal.json
```

The same form invokes `tasks.get`, `tasks.update`, `tasks.progress` and `tasks.complete` with their corresponding payloads. There is no CLI schema subcommand: use the field contract in the workflow reference, not guessed flags. A progress response is an activity, not a new task version. CLI mutations missing a key receive one durable key before transmission; callers may supply their own stable key. Never reuse a key for changed arguments.

If the terminal reports an unknown operation result or the process was killed:

```sh
workmedow --profile team api operations
workmedow --profile team api recover OPERATION_ID --confirm
```

Recovery is an explicit resend of the original immutable wire request with the original key. It does not resend edited input. Authorization or identity changes isolate the old operation. A server conflict requires checking the original result and current version; do not bypass isolation by using a new key.

Consuming `inbox.read/wait` calls are different: their receipt leases are non-idempotent and cannot be recovered by replay. Prefer `agent.work_queue`. If an inbox response was lost, an operator must verify the server receipt state, then use `api resolve-receipt ID --confirmed --evidence 'verified server observation'`; this only records the observation and never completes a task or bypasses an unknown task write.

`logout` revokes an OAuth family when available and removes that profile's local credentials. Imported static credentials must be revoked in WorkMedow by an authorized human. Drafts and operation journals remain isolated for recovery. Windows, macOS and Linux use the operating system's private configuration directory; no fixed path is required in the skill.
