# Obsidian CLI — Official Documentation

Source: https://help.obsidian.md/cli (redirects to https://obsidian.md/help/cli)
Fetched: 2026-04-08

## Overview

Obsidian CLI is a command-line interface that lets you control Obsidian from your terminal for scripting, automation, and integration with external tools. Anything you can do in Obsidian can be done from the command line. Ships with Obsidian v1.12.7+.

## Requirements

- Obsidian 1.12.7+ installer
- Obsidian app must be running (auto-launches if not active)
- Platform-specific PATH setup

## Setup

1. Upgrade to latest Obsidian installer
2. Settings > General > Enable "Command line interface"
3. Follow registration prompts
4. Restart terminal for PATH changes

### Platform Notes

- **Windows:** Requires terminal redirector (Obsidian.com); adds CLI to PATH
- **macOS:** Creates symlink at /usr/local/bin/obsidian; needs admin privileges
- **Linux:** Copies binary to ~/.local/bin/obsidian; requires PATH configuration

## Interface Modes

**Single Command Mode:** `obsidian <command>`
**TUI (Terminal User Interface):** Run `obsidian` alone for interactive mode with autocomplete, history, reverse search (Ctrl+R)

## Vault Targeting

Default: current working directory vault or active vault
Override: `vault=<name>` or `vault=<id>` as first parameter

## File Targeting

- `file=<name>` — resolves via wikilink logic
- `path=<path>` — exact path from vault root

## Complete Command Reference

### General
- help [command], version, reload, restart

### Bases (Database)
- bases, base:views, base:create, base:query [format=json|csv|tsv|md|paths]

### Bookmarks
- bookmarks [format=json|tsv|csv], bookmark [file] [subpath] [folder]

### Commands & Hotkeys
- commands [filter=prefix], command id=<id>, hotkeys, hotkey id=<id>

### Daily Notes
- daily, daily:path, daily:read, daily:append content=<text>, daily:prepend content=<text>

### File History
- diff [from=n] [to=n], history, history:list, history:read [version=n], history:restore version=n, history:open

### Files & Folders
- file, files [folder] [ext], folder path=<path>, folders, open, create [template], read, append content=<text>, prepend content=<text>, move to=<path>, rename name=<name>, delete [permanent]

### Links & References
- backlinks [format=json|tsv|csv], links, unresolved, orphans, deadends

### Outline
- outline [format=tree|md|json]

### Plugins
- plugins [filter=core|community], plugins:enabled, plugins:restrict [on|off], plugin id=<id>, plugin:enable id=<id>, plugin:disable id=<id>, plugin:install id=<id>, plugin:uninstall id=<id>, plugin:reload id=<id>

### Properties
- aliases, properties [format=yaml|json|tsv], property:set name=<n> value=<v>, property:remove name=<n>, property:read name=<n>

### Publish
- publish:site, publish:list, publish:status, publish:add, publish:remove, publish:open

### Random Notes
- random, random:read

### Search
- search query=<text> [limit=n] [format=text|json], search:context query=<text>, search:open

### Sync
- sync [on|off], sync:status, sync:history, sync:read version=n, sync:restore version=n, sync:open, sync:deleted

### Tags
- tags [sort=count] [format=json|tsv|csv], tag name=<tag>

### Tasks
- tasks [status=char] [done] [todo] [daily] [format=json|tsv|csv], task ref=<path:line> [toggle]

### Templates
- templates, template:read name=<name> [resolve], template:insert name=<name>

### Themes & Snippets
- themes, theme, theme:set name=<name>, theme:install name=<name>, theme:uninstall name=<name>, snippets, snippets:enabled, snippet:enable name=<name>, snippet:disable name=<name>

### Unique Note
- unique [name] [content]

### Vault
- vault [info=name|path|files|folders|size], vaults

### Web
- web url=<url>

### Word Count
- wordcount [words] [characters]

### Workspace
- workspace [ids], workspaces, workspace:save name=<name>, workspace:load name=<name>, workspace:delete name=<name>, tabs [ids], tab:open, recents

### Developer
- devtools, dev:debug [on|off], dev:cdp method=<CDP.method>, dev:errors [clear], dev:screenshot [path=filename], dev:console [limit=50] [level=log|warn|error], dev:css selector=<css>, dev:dom selector=<css>, dev:mobile [on|off], eval code=<javascript>

## Limitations

- Requires running Obsidian app (use Obsidian Headless for app-free sync)
- file= fails if multiple files share same name; use path= instead
- move and rename auto-update links only if setting enabled
