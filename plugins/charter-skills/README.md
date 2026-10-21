<img src="assets/charter-skills.png" width="72" height="72" alt="">

# Charter Skills

Specialist skills for product, design, engineering, research and creative work
in Codex and Claude Code. Charter is an opinionated, Mac-first library: call
on the expertise a task needs while keeping your agent's native model,
permissions and settings.

**Version 1.0.0-rc.9**

> **Release candidate.**

## Choose a starting point

Bring an idea, problem, document or task. Start with **Work Discovery** when
you are unsure how to approach it, or choose a specialist from the
[catalogue](CATALOGUE.md) when you know what you need.

- “Improve this frontend; the first visit feels confusing.”
- “Explore a logo direction and produce something we can use.”
- “This setting does not take effect. Find the cause and fix it.”
- “We want an AI feature. Help us decide what it should actually do.”

A clear request should lead to work, not an intake interview. Work Discovery's
seven use-case guides suggest useful combinations; they are not mandatory
stages or a requirement to load every skill. You can invoke specialists
directly, and the native agent can select them when relevant.

## Install

Install **Charter Skills** from the shared
[Tiziano AI marketplace](https://github.com/Tiziano-AI/plugins). The commands
below register that marketplace and install this library, not the other
plugins it lists.

These setup commands run in Terminal; afterward, you can work in your Mac
desktop app or CLI. You need Git and the CLI for the host you use. Installing
the desktop app does not necessarily install its Terminal command.

Open Terminal from Applications → Utilities. Check `git --version` and either
`codex --version` or `claude --version`, depending on the app you use. If the
matching command is missing, follow the official
[Codex CLI setup](https://developers.openai.com/codex/cli) or
[Claude Code setup](https://code.claude.com/docs/en/setup) first. You do not
need both CLIs, a Charter account or Charter's deployment engine. Public
repository access needs no private token. Follow your organization's
installation and plugin policies.

**Compatibility:** installation, update and removal have been exercised with
Codex CLI 0.163.0 and Claude Code 2.1.304. The desktop instructions follow the
host documentation; desktop use and first-time setup on a colleague's Mac
remain untested for this release candidate.

### Codex: macOS app and CLI

In Terminal:

```bash
codex plugin marketplace add Tiziano-AI/plugins
codex plugin add charter-skills@tiziano-ai
codex plugin list --marketplace tiziano-ai
```

Use your normal Codex configuration. A CLI launched with another `CODEX_HOME`
installs there instead. In the macOS app's Plugins screen, choose
**tiziano-ai** and confirm **Charter Skills** is installed and enabled.
Start a fresh conversation. If the app has not refreshed the marketplace,
save your work before restarting it.

In a project, type `$charter-skills:charter-work-discovery`, select the
installed skill from the picker, and add your request. For example:

> I have an idea for improving our onboarding, but I am not sure what to build.
> Help me work it out and carry it through to a useful result.

See the [native Codex plugin commands](https://learn.chatgpt.com/docs/developer-commands#codex-plugin)
for current host support.

### Claude: desktop local Code mode and Claude Code CLI

In Terminal:

```bash
claude plugin marketplace add Tiziano-AI/plugins
claude plugin install charter-skills@tiziano-ai --scope user
claude plugin list
```

Desktop **local Code** sessions and the CLI share plugin configuration. In
desktop Code, choose **Local** and select your project. Next to the prompt,
open **+ → Add plugins**, or **+ → Plugins → Manage plugins**, depending on
your app version. This guide covers local Code, not Chat, Cowork or remote
sessions.

Start a fresh session, or run `/reload-plugins`. Invoke:

```text
/charter-skills:charter-work-discovery Help me work out what to do with this idea.
```

Keep the full namespace; other specialists follow the same pattern. See
[Claude's desktop plugin guide](https://code.claude.com/docs/en/desktop#install-plugins)
and [plugin commands](https://code.claude.com/docs/en/plugins/cli-reference).

## What gets installed

The library contains on-demand guidance, linked examples and a macOS Cleanup
helper. Adaptive Communication is **selectable**, not always-on. It does not
install Charter's standing or personal instructions, runtime adapters, custom
roles, Forge or deployment engine. There is no MCP server, install hook,
account setup, scheduled job or automatic cleanup.

Skills do not supply the tools or accounts your work needs: research access
for current facts, image tools, Xcode for native Apple development, or a 3D
editor and renderer. If a prerequisite is missing, the agent should say what
is missing rather than claim the work is complete.

The macOS Cleanup helper uses Python 3.11+ and its standard library. It checks
the interpreter, guarded-removal support and any relevant native owner/version
before admitting an operation. Inspection is not permission to delete. Keep
its plans, operation reports and recovery state until the work is settled;
uninstalling the plugin does not settle an interrupted operation.

### Privacy

This plugin runs no collection service and uploads nothing on installation.
When you use a skill, your agent and any tools it calls retain their own data
handling and permission boundaries. Do not treat local bundled examples as
a promise that the host runs offline.

## Update, disable or remove

Release versions are immutable. Refresh the shared marketplace and update
only this plugin, then start a fresh conversation:

```bash
# Codex
codex plugin marketplace upgrade tiziano-ai
codex plugin add charter-skills@tiziano-ai
codex plugin list --marketplace tiziano-ai

# Claude Code
claude plugin marketplace update tiziano-ai
claude plugin update charter-skills@tiziano-ai --scope user
```

For Codex, use the app's plugin enable/disable control. The CLI's global
`--disable` flag controls features, not a named plugin. For Claude Code, use
`claude plugin disable charter-skills@tiziano-ai --scope user` or the
matching `enable` action; reload plugins or open a fresh session afterward.

To remove only this library:

```bash
codex plugin remove charter-skills@tiziano-ai
# Or, in Claude Code:
claude plugin uninstall charter-skills@tiziano-ai --scope user --keep-data
```

Keep separately stored cleanup reports and recovery state regardless of the
host's plugin-data option. Removal does not undo completed work, remove tools
you installed separately or delete your artifacts. After disabling or removing
the plugin, start a fresh conversation: an open conversation may retain
instructions it already loaded. Do not remove the whole
**tiziano-ai** marketplace just to remove Charter Skills: it distributes
other plugins too.

## If a skill does not appear or help

Check the native plugin list, selected origin and installed version in the
app/configuration you actually use. Refresh the marketplace and reopen the
session after updating. Source changes do not update an installed cached
package. Resolve duplicates through the native plugin manager, not by deleting
skill directories or editing caches.

If public Git access fails, check the exact repository URL and your network
or organization's Git policy. Do not place credentials in a repository URL.
For a concrete missed result, [open an issue](https://github.com/Tiziano-AI/charter-skills/issues)
with what you asked, what happened, the host and installed release. Leave out
secrets and private transcripts.
Skills do not promise identical results across models.

Original teaching, helpers and other authored material use the [MIT License](LICENSE).
Bundled examples keep their separate [third-party credits and terms](THIRD_PARTY_NOTICES.md).
