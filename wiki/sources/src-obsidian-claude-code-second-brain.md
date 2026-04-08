---
title: "Synthesis: Obsidian + Claude Code Second Brain Setup"
type: source-synthesis
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-obsidian-claude-code-second-brain
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=Y2rpFa43jTo"
    file: raw/transcripts/obsidian-claude-code-the-second-brain-setup-that-actually-works.txt
    title: "Obsidian + Claude Code: The Second Brain Setup That Actually Works"
    ingested: 2026-04-08
tags: [obsidian, claude-code, second-brain, git-sync, obsidian-cli, skills, project-management, gmail-integration]
---

# Synthesis: Obsidian + Claude Code Second Brain Setup

## Summary

This video demonstrates a practical implementation of using Claude Code as an AI assistant for managing an Obsidian-based second brain. The presenter (Eric Tech) walks through three main components: (1) setting up Obsidian with Git/GitHub for free version control and cloud sync using the Obsidian Git community plugin, (2) enabling the Obsidian CLI to allow Claude Code to interact with Obsidian programmatically, and (3) building custom Claude Code skills -- specifically an "onboard projects" skill -- that automates the process of ingesting data from multiple sources (Gmail, local files, screenshots) into a structured Obsidian project folder. The workflow creates per-project folders with standardized files (overview, conversation log, links, documents) and a projects dashboard using Obsidian's database plugin. The presenter demonstrates querying the knowledge base through Claude Code to get project status, action items, and even draft email responses.

## Key Insights

- **Git + Obsidian for free sync and version control**: Instead of paying for Obsidian Sync, the presenter creates a private GitHub repository, clones it locally, opens it as an Obsidian vault, and uses the Obsidian Git community plugin to auto-commit changes at configurable intervals (e.g., every 1 minute after edits stop). This provides free cloud backup, version history, and multi-device sync via Git pull-on-startup.

- **Obsidian CLI as the integration bridge**: Enabling the Obsidian CLI (Settings > General > Command Line Interface) allows Claude Code to interact with Obsidian programmatically -- creating notes, managing folders, and using markdown and JSON Canvas capabilities through the command line rather than the GUI.

- **Custom skills for domain-specific workflows**: The "onboard projects" skill is a multi-step automation that collects data from Gmail (via Google API OAuth credentials), local files (PDFs, docs, contracts), and pasted text/screenshots, then organizes everything into a standardized project folder structure within Obsidian.

- **Standardized project structure**: Each project gets: an overview.md (project profile, scope, tech stack), a conversation-log.md (chronological summary of all communications), a links.md (external references), a documents folder (static files like NDAs and contracts that should not be summarized), and an entry in a projects.base dashboard for status tracking.

- **Intelligent content routing**: The skill distinguishes between content that should be summarized and condensed (email conversations, meeting notes) versus static files that must be preserved as-is (contracts, agreements, NDAs). This prevents information loss from over-summarization.

- **Gmail integration via Google API scripts**: The skill includes scripts for fetching email labels, messages, threads, and attachments from Gmail using OAuth2 credentials, enabling automatic ingestion of email-based project communications.

- **AI-powered project querying**: Once data is onboarded, the user can ask Claude Code questions about project status, action items, and next steps. The presenter demonstrates getting a full project status summary with recommended actions and drafted email responses, all grounded in the ingested project data.

- **Auto-extraction of project metadata**: The skill automatically extracts wiki links, industry classification, and project profiles from ingested data to populate the overview.md file, reducing manual metadata entry.

- **Composability with other tools**: The presenter mentions combining the Obsidian + Claude Code setup with NotebookLM for research workflows and Google Workspace CLI for sending emails, suggesting an emerging pattern of Claude Code as a hub connecting multiple tool-specific integrations.

## Deep Analysis

This video demonstrates a practical, production-oriented implementation of the second-brain concept that differs from Karpathy's LLM Wiki pattern in important ways. Where Karpathy's approach is research-oriented (ingesting articles, building knowledge graphs, synthesizing across sources), this approach is operations-oriented (managing active projects, tracking communications, maintaining actionable status dashboards).

The Obsidian Git integration pattern is significant because it solves a real cost and sync problem. Obsidian's paid sync service is unnecessary when Git provides the same capabilities for free. The auto-commit plugin with configurable intervals means changes are preserved without any manual Git workflow -- the user edits in Obsidian and changes appear on GitHub automatically. The pull-on-startup feature ensures multi-device consistency.

The "onboard projects" skill represents a more sophisticated use of Claude Code skills than the NotebookLM skill demonstrated in previous sources. It involves multiple data source types (email API, local filesystem, user-pasted content), conditional processing logic (summarize vs. preserve as-is), structured output generation (multiple files per project following a consistent schema), and dashboard maintenance (updating a central project database). This suggests that Claude Code skills can scale from simple tool wrappers to complex multi-step workflow automations.

The Gmail integration is particularly noteworthy because it bridges the gap between communication tools and knowledge management. Email threads contain significant project knowledge that typically remains trapped in the inbox. By automatically ingesting and summarizing email conversations into the project folder, the skill prevents this knowledge loss.

The querying capability -- asking Claude Code about project status and getting actionable recommendations -- demonstrates the "second brain" value proposition in concrete terms. The knowledge base is not just an archive; it is an active assistant that can synthesize across all ingested project data to provide situational awareness and recommended actions.

## Open Questions

- How does the Gmail integration handle rate limits and large mailboxes with thousands of messages per label?
- What happens when project data conflicts between Gmail threads and local documents?
- How does the system handle project archival or completion -- is there a lifecycle for project folders?
- Can the onboarding skill handle incremental updates (new emails arriving after initial onboarding)?
- How does the Obsidian Git auto-commit interact with Claude Code making changes simultaneously -- are there merge conflict risks?

## Relationships

- DERIVED FROM: src-obsidian-claude-code-second-brain
- EXTENDS: Obsidian Knowledge Vault
- EXTENDS: Claude Code Skills
- RELATES TO: LLM Wiki Pattern
- RELATES TO: Wiki Ingestion Pipeline
- RELATES TO: AI-Driven Content Pipeline

## Backlinks

[[src-obsidian-claude-code-second-brain]]
[[Obsidian Knowledge Vault]]
[[Claude Code Skills]]
[[LLM Wiki Pattern]]
[[Wiki Ingestion Pipeline]]
[[AI-Driven Content Pipeline]]
