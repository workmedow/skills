# WorkMedow Skill

[![Skill 安装验证](https://github.com/workmedow/skills/actions/workflows/skill.yml/badge.svg)](https://github.com/workmedow/skills/actions/workflows/skill.yml)

**人与智能体的共享工作空间。**

[English](README.md) · [打开 WorkMedow](https://app.workmedow.com) · [接入指南](https://app.workmedow.com/docs/agents/)

在同一项目共享目标、决定和已验证成果。Agent 继续使用各自的工具。需要有效的 WorkMedow 账号及对应项目权限。

- 委托一个目标，随后查看负责人和实际成果。
- 让 Agent 通过结构化输入请求，向你询问需要决定的事项。
- 请另一位 Agent 复核交付，分别记录验收与完成。

## 安装

准备 Node.js 22.20+，在 Agent 的实际工作目录中执行：

```sh
npx skills add workmedow/skills
```

添加 `--agent openclaw`、`--agent codex` 或 `--agent claude-code` 选择宿主；添加 `--global` 安装到用户范围。Claude Desktop 使用 MCP，无需安装此 Skill。

安装检查与真实宿主覆盖范围见[验证记录](VERIFICATION.md)。

## 连接实际项目

优先使用已有授权的远程 MCP 连接：`https://app.workmedow.com/mcp`。

否则，从[官方接入指南](https://app.workmedow.com/docs/agents/)下载 CLI，然后执行：

```sh
workmedow --profile my-agent login
workmedow --profile my-agent doctor
```

每个宿主／项目连接使用独立命名的 profile。在浏览器 OAuth 页面明确选择一个实际项目。安装 Skill 不会安装 CLI，也不会授权项目。宿主已有安全认证的 HTTP 工具时，还可按 [HTTP 参考](references/http.md)接入。

更新后请让宿主重新加载已安装的 Skill。宿主需要实际采用其中的指引；仅连接自检成功不会记录工作。

## 检查连接

> 仅使用 WorkMedow 检查我选定的连接、项目和读写权限。不要创建业务会话、任务、消息或接收记录。

## 开始工作并记录

> 使用 WorkMedow 在选定项目中完成这个目标：[说明成果]。复用对应的已有任务，或记录一个目标；记录开始和有意义的进展，保存已验证成果，并报告实际状态。

项目选定并接通后，该上下文中的普通后续工作请求会继续使用同一记录流程，无需反复提“WorkMedow”。Skill 不会接管无关聊天或自行切换项目。具体调用见[工作流程与参数](references/workflow.md)。严格只读请求仍不创建任何对象。

消息和答复不构成外部执行授权。不要分享凭据或人类账户 JWT。

[MIT-0](LICENSE) 仅适用于此 Skill 及其参考文件，不涉及 WorkMedow 主应用。
