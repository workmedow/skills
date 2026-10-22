# CLI workflow

The operator installs the binary for this machine and signs in with a named profile for one stable Agent identity and its human-approved projects. Browser PKCE is the default; `login --device` supports a headless machine when the server advertises device authorization. A private Agent credential can alternatively be imported with `--token-file`; never put a token in command arguments or chat. Multi-project profiles require the CLI build that supports profile v2; an older installed binary does not gain this behavior when the Skill is updated.

`doctor` does not refresh an expired access token. Normal API calls can renew the existing OAuth profile within its approved identity, projects and scopes before reading or writing. Renewal does not approve an authorization fingerprint change. If renewal cannot be confirmed, report that limitation and reauthorize explicitly; do not switch identities or broaden access to continue. The current server rejects the whole refresh if any originally granted project is no longer authorized; it does not silently shrink the grant to the remaining projects.

```sh
workmedow --profile team login
workmedow --profile team doctor
```

Use the operator-provided profile name. The human can select several intended projects in the authorization page. A first login approving only one project keeps the automatic single-project binding. A multi-project profile does not choose the first project: select an authorized target for each operation. `login --project PROJECT_A` creates an explicit single-project binding and rejects other projects. To upgrade an existing binding, the operator explicitly runs `login --multi-project` and approves the intended projects again; it reuses the registered OAuth client and Agent. The two login flags are mutually exclusive.

The default service is the official global origin. An explicit `--url`/`--region` can select another authorized environment; use another profile for a different origin, region, account, workspace or Agent identity. Discovering another project never grants access to it; adding projects requires explicit human reauthorization. `doctor` and the following reads do not create business objects:

```sh
workmedow --profile team api call capabilities.get --input - <<'JSON'
{}
JSON
workmedow --profile team api call projects.list --input - <<'JSON'
{}
JSON
```

JSON arguments come from stdin or `--input /path/to/arguments.json`. Output is JSON with `data` and, for a journaled mutation, `operation_id`. Do not construct shell commands by interpolating task text. Supply JSON through a file or a quoted heredoc; keep personal content out of terminal logs when possible.

For requested work, use the operation names and JSON payloads in [workflow.md](workflow.md). A multi-project profile needs `--project PROJECT_A` on the call or an explicit JSON `project_id`; omitting the target is an error. A single-project binding supplies its project when omitted and rejects a different explicit target. The CLI accepts `business_session_id` and maps it to HTTP `session_id`. Each business session belongs to one project: if this conversation works in A and B, open and save separate sessions and never pass A's session to B. Save the task ID for each actual goal.

For example, save the selected operation's JSON arguments in a file, then run:

```sh
workmedow --profile team api call tasks.create --project PROJECT_A --input /path/to/create-goal.json
```

The same form invokes `tasks.get`, `tasks.update`, `tasks.progress` and `tasks.complete` with their corresponding payloads. The target must be both human-approved and currently effective; `--project` cannot override an existing single-project binding. There is no CLI schema subcommand: use the field contract in the workflow reference, not guessed flags. A progress response is an activity, not a new task version. CLI mutations missing a key receive one durable key before transmission; callers may supply their own stable key. Never reuse a key for changed arguments.

For local MCP, `workmedow --profile team mcp stdio` requires a multi-project connection's tools to name `project_id` explicitly. `mcp stdio --project PROJECT_A` binds only that process to one approved, currently effective project without changing the profile. Do not maintain a shared mutable current project across host conversations.

If the terminal reports an unknown operation result or the process was killed:

```sh
workmedow --profile team api operations
workmedow --profile team api operations --project PROJECT_A
workmedow --profile team api recover OPERATION_ID --confirm
```

Operation journals are partitioned by stable identity and actual target project. A multi-project `api operations` reads local history across that identity's projects and includes `project_id`, even for a later-revoked project; `--project` filters history without a network request or credential refresh. Changing projects must not hide an unknown result. That project's unknown or prepared operation blocks its next new write.

Recovery is an explicit resend of the original immutable wire request with the original project and key. It does not resend edited input or move an A operation to B. `--project` on recovery only filters the original record; it cannot retarget it. Authorization or identity changes isolate the old operation. A server conflict requires checking the original result and current version; do not bypass isolation by using a new key.

Consuming `inbox.read/wait` calls are different: their receipt leases are non-idempotent and cannot be recovered by replay. Prefer `agent.work_queue`. If an inbox response was lost, an operator must verify the server receipt state, then use `api resolve-receipt ID --confirmed --evidence 'verified server observation'`; this only records the observation and never completes a task or bypasses an unknown task write.

`logout` revokes an OAuth family when available and removes that profile's local credentials. Imported static credentials must be revoked in WorkMedow by an authorized human. Drafts and operation journals remain isolated for recovery. Windows, macOS and Linux use the operating system's private configuration directory; no fixed path is required in the skill.
