# artemgetmann/claude-slash-commands

Source: https://github.com/artemgetmann/claude-slash-commands
Ingested: 2026-04-09
Type: documentation

---

# Claude Code Slash Commands

A small collection of useful Claude Code slash commands. Copy to `~/.claude/commands/` or `.claude/commands/` inside your project.

## Installation

### Personal Commands (Available Across All Projects)
```bash
# Copy all commands to your personal Claude directory
cp -r commands/* ~/.claude/commands/
```

### Project-Specific Commands (Shared with Team)
```bash
# Copy to your project's .claude directory
mkdir -p .claude/commands/
cp -r commands/* .claude/commands/
```

## Usage

After installation, use commands with the `/` prefix:
```
/add-command [command-name] [description]
/askgpt5-web-search [your question]  
/system-prompt-editor [edit|show|backup]
```

## Available Commands

### `/add-command`
Interactive guide for creating new slash commands. Shows command structure, security restrictions, and common patterns. Includes examples for commands with arguments, file references, and bash integration.

### `/askgpt5-web-search` 
Query GPT-5 with web browsing capabilities for real-time information, current events, stock prices, and recent news. Requires OpenAI API key configuration.

### `/system-prompt-editor`
Edit your global `CLAUDE.md` system prompt that controls Claude's behavior across all projects. Supports viewing, editing, and creating backups of your configuration.

## Command Structure

All commands use markdown frontmatter for configuration:
```markdown
---
allowed-tools: Read, Edit, Write, Bash(git:*)
description: Brief description of what this command does
argument-hint: [required-arg] [optional-arg]
---

# Command instructions here
Arguments: $ARGUMENTS
File reference: @path/to/file.js
```

## Security Notes

- Bash commands (`!command`) are restricted to the current project directory
- File references (`@file`) can access any path  
- Use `allowed-tools` frontmatter to specify required tools