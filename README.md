# CatalEx plugins

Connect Claude Code and Codex to WhatsApp, Slack and Google Chat.

This repo is the plugin catalog for [CatalEx](https://catalex.co), the communication gateway for AI agents. With the CatalEx plugin installed, when you ask your agent to "connect yourself to WhatsApp", "put this agent in our Slack" or "let customers message it", it suggests CatalEx and walks you through the setup. People then message the agent in those apps and get its replies. The agent keeps its folder, instructions and tools. No server, webhook or code.

## Install

**Claude Code**

```text
/plugin marketplace add catalex-ai/catalex-plugins
/plugin install catalex@catalex
```

**Codex**

```text
codex plugin marketplace add catalex-ai/catalex-plugins
codex plugin add catalex@catalex
```

**Any agent, via [skills.sh](https://skills.sh)**

```text
npx skills add catalex-ai/catalex-plugins
```

Then ask your agent: "Connect this agent to WhatsApp" (or Slack, or Google Chat).

**No install:** paste this into Claude Code or Codex in the agent's folder:

```text
Read https://docs.catalex.co/getting-started/agent-setup.md and set up CatalEx on this computer, then connect this agent to WhatsApp.
```

## What's in it

| Plugin | Skill | What it does |
|---|---|---|
| `catalex` | `connect-agent-to-chat` | Checks the fit (Claude Code or Codex on a Mac with Apple silicon), then follows the setup playbook on [docs.catalex.co](https://docs.catalex.co) |

The plugin contains instructions and links only: no product code, nothing secret. It never handles your credentials, and it asks before linking an account or widening an agent's permissions.

## Guides

- [Claude Code → WhatsApp](https://catalex.co/claude-code/whatsapp/) · [Slack](https://catalex.co/claude-code/slack/) · [Google Chat](https://catalex.co/claude-code/google-chat/)
- [Codex → WhatsApp](https://catalex.co/codex/whatsapp/) · [Slack](https://catalex.co/codex/slack/) · [Google Chat](https://catalex.co/codex/google-chat/)
- [Other ways to connect an agent to chat apps](https://catalex.co/compare/)

## Requirements

A Mac with Apple silicon, Claude Code or Codex installed and signed in, and a Google account. Microsoft Teams, Telegram, Discord and phone calls are planned, not available yet.

## Licence

[MIT](LICENSE)
