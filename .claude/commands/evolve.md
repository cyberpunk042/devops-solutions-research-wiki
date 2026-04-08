Run the knowledge evolution pipeline.

1. Run `python3 -m tools.pipeline evolve --score --top 10` to show candidates
2. Present the ranked candidates and ask what to do:
   - "scaffold" → `python3 -m tools.pipeline evolve --scaffold --top N`
   - "generate" → fill scaffolded pages with real content (this session)
   - "review" → `python3 -m tools.pipeline evolve --review` for maturity promotions
   - "stale" → `python3 -m tools.pipeline evolve --stale` for freshness check
3. After any generation, run `python3 -m tools.pipeline post`
