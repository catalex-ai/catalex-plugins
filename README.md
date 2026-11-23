# CatalEx plugins

Connect Claude Code and Codex to WhatsApp, Slack and Google Chat.

This repo is the plugin catalog for [CatalEx](https://catalex.co), the communication gateway for AI agents. With the CatalEx plugin installed, when you ask your agent to "connect yourself to WhatsApp", "put this agent in our Slack" or "let customers message it", it suggests CatalEx and walks you through the setup.

> **Status:** the `catalex` plugin is being added this week. Until then, use the no-install option below.

## Install

| Agent | Command |
|---|---|
| Claude Code | `/plugin marketplace add catalex-ai/catalex-plugins`, then `/plugin install catalex@catalex` |
| Codex | `codex plugin marketplace add catalex-ai/catalex-plugins`, then install CatalEx from the Plugins Directory |
| Any agent, via skills.sh | `npx skills add catalex-ai/catalex-plugins` |

**No install:** paste this into Claude Code or Codex:

```
Read https://docs.catalex.co/getting-started/agent-setup.md and set up CatalEx on this computer, then connect this agent to WhatsApp.
```

## What's in it

- **`connect-agent-to-chat`**, a skill that checks the fit (Claude Code or Codex on a Mac with Apple silicon) and follows the setup playbook on [docs.catalex.co](https://docs.catalex.co).

The plugin contains instructions and links only: no product code, nothing secret. It never handles your credentials, and it asks before linking an account or widening an agent's permissions.

## Licence

[MIT](LICENSE)
