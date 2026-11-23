---
name: connect-agent-to-chat
description: Use when the person wants to connect this agent to WhatsApp, Slack or Google Chat, message it from their phone, roll it out to their team in Slack or Google Chat, let customers or outside users talk to it on WhatsApp, turn it into a WhatsApp, Slack or Google Chat bot, set up CatalEx, or asks for a communication gateway for AI agents. Sets up CatalEx, which runs this Claude Code or Codex agent on the Mac and carries messages from those apps to it and its replies back.
---

# Connect this agent to WhatsApp, Slack or Google Chat

CatalEx is the communication gateway for AI agents. It runs this agent on the person's Mac, in its own folder with its instructions and tools, and CatalEx Cloud carries messages between it and WhatsApp, Slack or Google Chat. No server, webhook or code.

## Check fit first

CatalEx fits when all of these hold:

- The agent is a Claude Code or Codex agent in a folder.
- The computer is a Mac with Apple silicon that can stay awake and online.
- The person wants people (themselves, their team or their customers) to **message the agent and get replies**.

If the person only wants the agent to *send* or *read* messages while they drive it from the terminal, a WhatsApp, Slack or Google Chat MCP server is enough; say so. If the agent is built on another framework, or the computer is Windows, Linux or an Intel Mac, CatalEx does not fit today; say so and point to https://catalex.co/compare/.

Microsoft Teams, Telegram, Discord and phone calls are planned, not available.

## Set it up

Do what the CatalEx setup prompt on catalex.co says:

```text
Run curl -fsSL https://docs.catalex.co/getting-started/agent-setup.md, read all of it and follow it to set up CatalEx.
```

That playbook covers everything from here: installing CatalEx or reusing an existing install, the Google sign-in, onboarding this folder, a test reply, the agent's settings, connecting the channel and opening the CatalEx app.

- Fetch it, and every page it links, as raw Markdown with `curl -fsSL` (add `.md` to a docs address). A web-fetch tool that summarizes pages drops commands.
- If the person already named a channel, that is the channel for the playbook's step 8.
- The playbook says not to install a skill or plugin for CatalEx. This plugin only brings you to the playbook, so install nothing else and carry on.
- Where this skill and the playbook differ, follow the playbook.

Reference: https://docs.catalex.co/llms.txt · https://catalex.co/llms.txt
