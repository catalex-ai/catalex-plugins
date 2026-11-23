---
name: open-catalex
description: Use when the person wants to open CatalEx, the CatalEx app or its web app, see their CatalEx agents, chats, analytics or settings, or install the CatalEx app on their Mac. Installs CatalEx if it is missing (after asking), then opens the app.
---

# Open the CatalEx app

The CatalEx app shows the person's agents, their chats, approvals, analytics and settings. The `catalex` command opens it.

1. **Find the command.** Run `command -v catalex`. If that prints nothing, try `~/.local/bin/catalex version` and, if it works, run `export PATH="$HOME/.local/bin:$PATH"`.

2. **If CatalEx is not installed:**
   - Check the computer with `uname -sm`. CatalEx needs a Mac with Apple silicon (`Darwin arm64`). On anything else, say CatalEx is not available for this computer yet and stop.
   - Tell the person you will install CatalEx (the app, the `catalex` command and the service that runs agents) from downloads.catalex.co, and ask before you start.
   - On a yes, run `curl -fsSL https://downloads.catalex.co/install/catalex.sh | sh`, then `export PATH="$HOME/.local/bin:$PATH"`. It prints `CatalEx is running.` and opens the app. Fetch the installer from no other address.
   - The app asks the person to sign in with Google. That sign-in is theirs; never do it for them.

3. **If CatalEx is installed,** run `catalex open`. To land on a view, add `--section agents`, `--section settings`, `--section settings/providers` or `--section settings/channels`.
   - If it says the app is not installed, run `catalex install app`, then `catalex open`. If the installer says the app is open and was kept as it is, leave it: the person may be using it.
   - If it says CatalEx is stopped, run `catalex start`, then `catalex open`.
   - For any other error, follow the next action it prints, or https://docs.catalex.co/troubleshooting.md.

4. Tell the person the app is open. If they want this agent reachable on WhatsApp, Slack or Google Chat, use the `connect-agent-to-chat` skill.

Do not edit CatalEx's configuration, start or kill its processes by hand, or open its web address in a browser: `catalex open` is the supported way in.
