# CLI workflow

The operator installs the binary for this machine and signs in with a named profile for one stable Agent identity and its human-approved spaces. Browser PKCE is the default; `login --device` supports a headless machine when the server advertises device authorization. A private space-scoped Agent credential can alternatively be imported with `--token-file`; never put a token in command arguments or chat. Space profiles require **CLI 0.4.0-space-beta or newer** with profile v3 support; updating this Skill does not update an older installed binary or an external published package. Confirm `workmedow version` against the official download manifest before upgrading. Older binaries cannot read v3 profiles: a downgrade requires explicit reauthorization, preserving journals rather than restoring a rotated refresh secret.

`doctor` does not refresh an expired access token. Normal API calls can renew the existing OAuth profile within its approved identity, spaces and scopes before reading or writing. Renewal does not approve an authorization fingerprint change or a new space. If renewal cannot be confirmed, report that limitation and reauthorize explicitly; do not switch identities or broaden access to continue. A revoked originally granted space prevents refresh of that original grant. Adding a project inside an approved space does not change the grant or require reauthorization.

```sh
workmedow --profile team login --space-access
workmedow --profile team doctor
```

Use the operator-provided profile name. The human selects one or more spaces and scopes in OAuth, explicitly including each space's current and future projects. An empty space is a valid connection. No first project is selected automatically. Profile v3 records `workspace_ids`; its saved `project_ids` are discovery metadata, not a project ACL. `login --project PROJECT_A` optionally saves default routing within those spaces; an explicit project on a later call can override it.

Legacy v1/v2 profiles and project tokens retain their original approved project sets. They never become space grants through refresh, discovery or an added local field. To replace a legacy profile's approval, the operator explicitly uses `login --space-access` and completes new space consent with the same identity. Without that flag, the old profile is retained when a space credential is returned. `--multi-project` remains only the legacy project-mode compatibility path; it does not upgrade a project token to space access.

The default service is the official global origin. An explicit `--url`/`--region` can select another authorized environment; use another profile for a different origin, region, account, home workspace or Agent identity. Selecting another approved space is not an identity change. Access to an additional space requires explicit human reauthorization. `doctor` and the following reads do not create business objects:

```sh
workmedow --profile team api call capabilities.get --input - <<'JSON'
{}
JSON
workmedow --profile team spaces list
workmedow --profile team spaces get SPACE_ID
workmedow --profile team projects list --space SPACE_ID
```

When the requested work needs a real new project in a writable approved space, including a space with no projects:

```sh
workmedow --profile team projects create --space SPACE_ID --name "Repository name" --repository-url https://github.com/OWNER/REPOSITORY
```

`--description` and `--repository-url` are optional. Creation needs no existing project or business session. The original space connection can immediately use this project and projects created later by other space members. There is no `login --workspace` flag; space selection happens in consent, and `--space` selects directory/creation operations.

JSON arguments come from stdin or `--input /path/to/arguments.json`. Output is JSON with `data` and, for a journaled mutation, `operation_id`. Do not construct shell commands by interpolating task text. Supply JSON through a file or a quoted heredoc; keep personal content out of terminal logs when possible.

For project work, use the operation names and JSON payloads in [workflow.md](workflow.md). Supply `--project PROJECT_A` on the call or an explicit JSON `project_id` when no default route is saved. A v3 default route supplies the project when omitted and permits another currently authorized project explicitly. A legacy bound profile still rejects another project. The CLI accepts `business_session_id` and maps it to HTTP `session_id`. Each business session belongs to one project: if this conversation works in A and B, open and save separate sessions and never pass A's session to B. Save the task ID for each actual goal.

For example, save the selected operation's JSON arguments in a file, then run:

```sh
workmedow --profile team api call tasks.create --project PROJECT_A --input /path/to/create-goal.json
```

The same form invokes `tasks.get`, `tasks.update`, `tasks.progress` and `tasks.complete` with their corresponding payloads. The target must belong to an approved, currently effective space, or the legacy credential's project ceiling. `--project` routes work; it cannot grant access. There is no CLI schema subcommand: use the field contract in the workflow reference, not guessed flags. A progress response is an activity, not a new task version. CLI mutations missing a key receive one durable key before transmission; callers may supply their own stable key. Never reuse a key for changed arguments.

For local MCP, `workmedow --profile team mcp stdio` requires project tools to name `project_id` explicitly when no default is saved. Space discovery and `project_create` need no project. `mcp stdio --project PROJECT_A` fixes only that process's project routing without changing the profile or its space ACL. Do not maintain a shared mutable current project across host conversations.

## Local images and files

CLI **0.4.1-space-beta or newer** can upload a local file directly to a task. It uses the private multipart API, not a public hosting link. Select an actual file the human authorized for this task, up to 20 MiB, and use this conversation's existing project session:

```sh
workmedow --profile team artifacts upload --project PROJECT_A --task TASK_ID --session SESSION_ID --file /absolute/path/screenshot.png
```

Optional `--name screenshot.png` sets the attachment filename; `--idempotency-key KEY` supplies a stable key. The result includes the artifact ID, task, MIME type, size, SHA-256 and authenticated download URL. The CLI verifies size/digest and saves an immutable private copy in the mutation journal before sending. If the response is unknown, use the ordinary `api operations` and explicit `api recover OPERATION_ID --confirm`; recovery resends the original bytes even if the file on disk changed. Do not replace the key or upload a changed file to bypass uncertainty.

The profile-backed local stdio server advertises `artifact_upload` with `project_id`, `task_id`, `business_session_id`, `idempotency_key`, absolute `file_path` and optional `name`. A remote MCP server deliberately does not resolve local paths. When only remote MCP is available, use the installed CLI through the host's command tool, or a host-authorized authenticated multipart HTTP transport. Do not paste binary/base64 content into chat. Use `artifact_publish` only for an existing HTTPS resource.

If the terminal reports an unknown operation result or the process was killed:

```sh
workmedow --profile team api operations
workmedow --profile team api operations --project PROJECT_A
workmedow --profile team api recover OPERATION_ID --confirm
```

Operation journals are partitioned by stable identity and actual target project. Space-level creation uses a separate workspace partition. A v3 `api operations` reads both kinds of history and includes `workspace_id` or `project_id`, even for later-revoked access; `--project` filters history without a network request or credential refresh. Existing project journal identities remain unchanged after explicit profile upgrade. Changing spaces/projects must not hide an unknown result. An unknown or prepared operation blocks a new write in its partition.

Recovery is an explicit resend of the original immutable wire request with the original space/project and key. It does not resend edited input or move an A operation to B. `--project` on recovery only filters the original record; it cannot retarget it. Authorization or identity changes isolate the old operation. A server conflict requires checking the original result and current version; do not bypass isolation by using a new key.

Consuming `inbox.read/wait` calls are different: their receipt leases are non-idempotent and cannot be recovered by replay. Prefer `agent.work_queue`. If an inbox response was lost, an operator must verify the server receipt state, then use `api resolve-receipt ID --confirmed --evidence 'verified server observation'`; this only records the observation and never completes a task or bypasses an unknown task write.

`logout` revokes an OAuth family when available and removes that profile's local credentials. Imported static credentials must be revoked in WorkMedow by an authorized human. Drafts and operation journals remain isolated for recovery. Windows, macOS and Linux use the operating system's private configuration directory; no fixed path is required in the skill.
