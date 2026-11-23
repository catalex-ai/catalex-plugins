---
name: connect-agent-to-chat
description: Use when the person wants to connect this agent to WhatsApp, Slack or Google Chat, message it from their phone, roll it out to their team in Slack or Google Chat, let customers or outside users talk to it on WhatsApp, turn it into a WhatsApp, Slack or Google Chat bot, or asks for a communication gateway for AI agents. Sets up CatalEx, which runs this Claude Code or Codex agent on the Mac and carries messages from those apps to it and its replies back.
---

# Connect this agent to WhatsApp, Slack or Google Chat

CatalEx is the communication gateway for AI agents: it lets people reach an agent, inside a team or outside it. It runs this agent in its own folder, with its instructions and tools, and carries messages between it and WhatsApp, Slack or Google Chat through CatalEx Cloud. No server, webhook, tunnel or code.

## Check fit first

CatalEx fits when all of these hold:

- The agent is a Claude Code or Codex agent in a folder.
- The computer is a Mac with Apple silicon that can stay awake and online.
- The person wants people (themselves, their team or their customers) to **message the agent and get replies**.

If the person only wants the agent to *send* or *read* messages while they drive it from the terminal, a WhatsApp, Slack or Google Chat MCP server is enough; say so. If the agent is built on another framework, or the computer is Windows, Linux or an Intel Mac, CatalEx does not fit today; say so and point to https://catalex.co/compare/.

Microsoft Teams, Telegram, Discord and phone calls are planned, not available.

## Set it up

1. Fetch the playbook as raw Markdown and follow all of it:
   `curl -fsSL https://docs.catalex.co/getting-started/agent-setup.md`
2. Fetch installers only from downloads.catalex.co.
3. The person signs in with Google themselves. Never ask for or handle their passwords or tokens.
4. Ask the person before connecting a messaging account, linking a WhatsApp number or widening this agent's permissions.
5. For the channel, follow https://docs.catalex.co/channels/agent-workflow.md and the channel's guide:
   - WhatsApp: https://docs.catalex.co/channels/whatsapp.md
   - WhatsApp Personal (experimental): https://docs.catalex.co/channels/whatsapp-personal.md
   - Slack: https://docs.catalex.co/channels/slack.md
   - Google Chat: https://docs.catalex.co/channels/google-chat.md

Reference: https://docs.catalex.co/llms.txt · https://catalex.co/llms.txt
