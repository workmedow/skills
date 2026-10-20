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
npx skills@1.7.4 add workmedow/skills --skill workmedow
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

## 开始一次对话

> 使用 WorkMedow 确认我选定的实际项目，为这次对话创建一个业务会话，然后总结工作队列和待回答的输入请求。保持任务和消息接收状态不变。

消息和答复不构成外部执行授权。不要分享凭据或人类账户 JWT。

[MIT-0](LICENSE) 仅适用于此 Skill 及其参考文件，不涉及 WorkMedow 主应用。
