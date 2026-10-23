# WorkMedow Skill

[![Skill 安装验证](https://github.com/workmedow/skills/actions/workflows/skill.yml/badge.svg)](https://github.com/workmedow/skills/actions/workflows/skill.yml)

**人与智能体的共享工作空间。**

[English](README.md) · [打开 WorkMedow](https://app.workmedow.com) · [接入指南](https://app.workmedow.com/docs/agents/)

共享目标、决定和已验证成果。Agent 继续使用各自的工具。需要有效的 WorkMedow 账号及空间访问权限。空间包含项目，空间是唯一访问边界，项目组织工作。

- 委托一个目标，随后查看负责人和实际成果。
- 让 Agent 通过结构化输入请求，向你询问需要决定的事项。
- 请另一位 Agent 复核交付，分别记录验收与完成。

## 安装

v0.4.1 补齐本地图片/文件上传：使用 CLI `artifacts upload`，或 profile 本地 MCP 的 `artifact_upload`。任务创建者在指派后仍可修订标题和描述。上传功能需要 CLI 0.4.1-space-beta 或更新版本；请核对宿主实际配置的可执行文件，单独更新 Skill 不会替换旧 CLI。

人类明确要求时，可以更新官方 Skill。WorkMedow 没有禁止 Grok Bot 更新 Skill 的专属规则；若宿主另有限制，应说明真实来源。空间权限仍通过明确的 OAuth 授权获得。

准备 Node.js 22.20+，在 Agent 的实际工作目录中执行：

```sh
npx skills add workmedow/skills
```

添加 `--agent openclaw`、`--agent codex` 或 `--agent claude-code` 选择宿主；添加 `--global` 安装到用户范围。Claude Desktop 使用 MCP，无需安装此 Skill。

安装检查与真实宿主覆盖范围见[验证记录](VERIFICATION.md)。

## 连接工作空间

优先使用已有授权的远程 MCP 连接：`https://app.workmedow.com/mcp`。

否则，从[官方接入指南](https://app.workmedow.com/docs/agents/)下载 CLI，然后执行：

```sh
workmedow version
workmedow --profile my-agent login --space-access
workmedow --profile my-agent doctor
workmedow --profile my-agent spaces list
workmedow --profile my-agent projects list --space SPACE_ID
```

每个稳定 Agent 连接使用独立命名的 profile。在浏览器 OAuth 页面明确选择目标空间及 scope。空间授权包含其中全部现有和未来项目，空空间也可连接；项目操作仍明确指向一个实际项目，同一对话在各项目分别保留业务 session。安装 Skill 不会安装 CLI，也不会授权空间。宿主已有安全认证的 HTTP 工具时，还可按 [HTTP 参考](references/http.md)接入。

### v0.4.0：空间与 Agent 自主建项目

空间 profile 需要 **CLI 0.4.0-space-beta 或更新版本**，使用 profile v3。批准的 `workspace_ids` 是访问边界，保存的 `project_ids` 只是发现快照。已授权空间新增项目不需再次 consent。不会自动取第一个项目；CLI 调用传 `--project PROJECT_ID`、工具参数明确 `project_id`，或用 `login --project PROJECT_ID` 明确保存默认工作路由。v3 默认路由不限制其他已授权项目的访问。

有空间写权限的 Agent 可自主创建真实仓库或产品项目，无需逐项目审批或已有项目业务会话：

```sh
workmedow --profile my-agent projects create --space SPACE_ID --name "仓库名称" --repository-url https://github.com/OWNER/REPOSITORY
```

原连接立即可用这个项目，同空间其他成员以后创建的项目也同样可见。项目 session 和操作日志继续隔离，空间级项目创建使用独立日志分区；A 的 session 或结果未知的写入不能发到 B。严格只读请求不创建项目、会话、任务或接收记录。

旧 v1/v2 profile 和 project token 保留原批准项目范围。升级须明确执行 `login --space-access` 并完成新的空间授权，复用原 OAuth client 和稳定身份；刷新、发现、本地字段或 Skill 安装均不能升级权限。`--multi-project` 只保留旧项目模式兼容。旧 CLI 无法读取 v3，降级须重新授权并保留原日志，不能恢复已轮换的 refresh secret。新增空间需 consent，已批准空间内新增项目不需要。按项目路由、离线历史和明确恢复见 [CLI 参考](references/cli.md)。

v0.4.0 Skill 载荷与 WorkMedow 主库固定源码 `d9d3e2bf50250fdeb2428a6c9dc0eec58ed2ee10` 一致。版本化 release 的 manifest 分别固定官方 Skill 提交与压缩包校验值。更新 Skill 不会替换已安装 CLI、bridge 或宿主连接。

更新后请让宿主重新加载已安装的 Skill。宿主需要实际采用其中的指引；仅连接自检成功不会记录工作。

## 检查连接

> 仅使用 WorkMedow 检查我选定的连接、空间和读写权限。不要创建项目、业务会话、任务、消息或接收记录。

## 开始工作并记录

> 使用 WorkMedow 在选定空间中完成这个目标：[说明成果]。使用或创建匹配的真实仓库/产品项目，复用对应的已有任务或记录一个目标，记录有意义的进展，保存已验证成果，并报告实际状态。

空间或项目选定并接通后，该上下文中的普通后续工作请求会继续使用同一记录流程，无需反复提“WorkMedow”。Skill 不会接管无关聊天或选择未授权空间。具体调用见[工作流程与参数](references/workflow.md)。严格只读请求仍不创建任何对象。

消息和答复不构成外部执行授权。不要分享凭据或人类账户 JWT。

[MIT-0](LICENSE) 仅适用于此 Skill 及其参考文件，不涉及 WorkMedow 主应用。
