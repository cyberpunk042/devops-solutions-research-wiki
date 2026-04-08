Ingest sources into the research wiki.

Usage: /ingest URL1 URL2 ... or /ingest (then provide URLs or paste content)

1. If arguments provided, fetch them: `python3 -m tools.pipeline fetch $ARGUMENTS`
2. If no arguments, ask the user for URLs, topics, or pasted content
3. After fetching, process each raw file into wiki source-synthesis pages
4. Run `python3 -m tools.pipeline post` after all pages created
5. Run `python3 -m tools.pipeline crossref` to find new connections
6. Report: pages created, relationships added, new cross-references found
