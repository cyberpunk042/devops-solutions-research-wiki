Add a log entry to wiki/log/.

1. Ask the user what type of entry: directive, session summary, or completion note
2. Create the file in wiki/log/ with proper frontmatter (type: note, domain: log, note_type)
3. Include the user's content verbatim in the entry
4. Run `python3 -m tools.pipeline post` to rebuild the log index
5. Commit the new log entry
