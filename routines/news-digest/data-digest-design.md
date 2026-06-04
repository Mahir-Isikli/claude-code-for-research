# Data Digest — Skill Design

A generalizable skill that produces a periodic digest of new academic work, data releases, and policy news on a configurable topic. The default config targets welfare-state / migration / labor economics, but retargeting to any subject is a config edit, not a code change.

## Core principle

Separate **what to watch** (config) from **how to fetch** (logic). The skill reads a config file, iterates over sources by priority tier, fetches, dedups, ranks, and renders. Adding a topic or swapping a field means editing `config.yaml` only.

---

## 1. Config structure

```yaml
# config.yaml
digest:
  name: "Migration & Labor Economics Digest"
  cadence: weekly          # weekly | daily | monthly
  lookback_days: 7         # window of "new" items relative to run date
  max_items_per_section: 8 # cap so the digest stays skimmable
  output_format: markdown  # markdown | latex | html
  output_dir: "output/digests/"  # where rendered digests are saved

topics:
  # Keywords drive keyword-based sources (Scholar, Google News, OpenAlex).
  # Curated feeds (NEP, IZA series) ignore these and use feed_id instead.
  keywords:
    - "refugee integration"
    - "labor market assimilation"
    - "activation policy"
    - "welfare state"
    - "immigration policy"
  authors:                 # optional author-watch list
    - "Dustmann"
    - "Bertrand"
  # Optional: map keywords to course modules for student-facing annotations.
  # If set, the summary step tags items with the most relevant module.
  course_modules:
    - id: week3_iv
      label: "Week 3 — Instrumental Variables"
      keywords: ["instrument", "2SLS", "LATE"]
    - id: week5_did
      label: "Week 5 — Difference-in-Differences"
      keywords: ["diff-in-diff", "parallel trends", "event study"]

sources:
  # Tier 1 — curated, low-noise, structured. Hit first, trust most.
  - id: nep_mig
    type: nep
    feed_id: NEP-MIG       # fetch method: scrape https://nep.repec.org/nep-mig/ archive page
    tier: 1
  - id: nep_lab
    type: nep
    feed_id: NEP-LAB
    tier: 1
  - id: iza_dp
    type: rss
    url: "https://www.iza.org/publications/dp"
    tier: 1
  - id: nber_new
    type: rss
    url: "https://www.nber.org/rss/new.xml"
    program_filter: ["LS", "PE"]   # Labor Studies, Public Economics
    tier: 1

  # Tier 2 — broad academic, needs ranking/dedup against Tier 1.
  - id: openalex
    type: api
    endpoint: "https://api.openalex.org/works"
    rate_limit: 10/sec     # polite: OpenAlex asks for max 10 req/s
    tier: 2
  - id: cepr_vox
    type: rss
    url: "https://cepr.org/voxeu"
    tier: 2

  # Tier 3 — data-release calendars (announce datasets, not papers).
  - id: eurostat
    type: api
    endpoint: "https://ec.europa.eu/eurostat/api"
    datasets: ["migr_asyappctzm", "lfsa_ergan"]
    tier: 3
  - id: worldbank
    type: api
    endpoint: "https://api.worldbank.org/v2"
    indicators: ["SM.POP.NETM", "SL.UEM.TOTL.ZS"]
    tier: 3

  # Tier 4 — fragile / noisy. Deferred to v2. Wrap in fallbacks,
  # dedup hard, rank last. A failure here must never break the run.
  # - id: scholar_alerts
  #   type: gmail_filter     # requires OAuth + Gmail API — scope for v2
  #   label: "Scholar Alerts"
  #   tier: 4
  # - id: ssrn
  #   type: rss              # SSRN feeds are unstable; needs concrete URL + scraping fallback
  #   url: TBD
  #   tier: 4
  # - id: google_news
  #   type: rss_query
  #   query: "migration policy OR asylum reform"
  #   tier: 4
```

## 2. Run trigger

The digest can be triggered in three ways:

1. **Scheduled (cron):** Use Claude Code's `/schedule` or a system cron job matching the `cadence` field.
2. **On-demand skill:** A `/digest` command that runs the full pipeline immediately.
3. **Student mode:** Students can run `/digest` manually at any time — the state file ensures they only see items new since their last run, regardless of `lookback_days`.

Precedence rule: the state file (Section 7) is the authority on "seen" items. `lookback_days` sets the maximum window for fetching; the state file filters within that window. If an item is within the lookback window but already in the state file, it is skipped.

## 3. Fetch & priority ordering

Sources are processed in tier order so that the cleanest items establish the canonical record before noisier ones are merged in.

1. **Tier 1 (curated academic):** NEP reports, IZA, NBER. Trust anchors — well-structured, low duplication, already field-filtered. Items here are kept verbatim and seed the dedup index.
2. **Tier 2 (broad academic):** OpenAlex and VoxEU fill gaps Tier 1 missed. Each item is checked against the Tier 1 dedup index before being added.
3. **Tier 3 (data releases):** Eurostat / World Bank. Populate a separate "New data" section.
4. **Tier 4 (fragile / noisy):** Scholar alerts, SSRN, Google News. **Deferred to v2.** When implemented: run last, behind try/except with 2 retries + exponential backoff, aggressive dedup. A Tier 4 failure degrades gracefully.

### Source-specific fetch notes

| Source | Method | Gotchas |
|---|---|---|
| NEP | Scrape archive page at `https://nep.repec.org/nep-{id}/` | HTML structure may change; pin CSS selectors, add fallback regex |
| IZA / NBER / VoxEU | Standard RSS | Stable; parse with `feedparser` |
| OpenAlex | JSON API (`/works?filter=...`) | Rate limit 10 req/s; use `mailto` param for polite pool |
| Eurostat / World Bank | REST API | Rate limits vary; cache responses for 24h |
| Scholar alerts (v2) | Gmail API + OAuth | Requires service account or user OAuth consent flow |
| SSRN (v2) | TBD — RSS unreliable | Need to identify stable feed URL or fall back to scraping |

### Error handling

All sources: timeout after 30s, retry up to 2× with exponential backoff (1s, 4s). Log failures but continue — a partial digest is better than no digest. Report skipped sources in a footer note.

## 4. Deduplication

A single item often surfaces in several feeds. Dedup keys, in order of reliability:

1. **DOI** — exact match, most reliable.
2. **Normalized title + author overlap** — lowercase, strip punctuation/stopwords, fuzzy match (token-set ratio ≥ 90) **AND** at least one overlapping author surname. Title-only fuzzy matching is too aggressive for short/generic titles.
3. **Author + year + venue** — fallback when no DOI and titles diverge.

First occurrence (lowest tier number) wins and keeps its metadata; later duplicates are dropped but contribute a source tag ("also via Scholar") if useful.

**Preprint → published version handling:** When a preprint and its published version are both found, keep the published version's metadata (journal, DOI, final title) but note the earliest-seen date (the preprint date). The published version is more authoritative; the preprint date gives priority credit.

## 5. Relevance scoring & ranking

After dedup, each item receives a relevance score:

1. **Keyword score:** Number of config keywords matched in title + abstract, normalized by total keywords. Weight title matches 2× over abstract matches.
2. **Author score:** +0.3 if any author is on the `authors` watchlist.
3. **Recency score:** Linear decay over the lookback window (today = 1.0, oldest day = 0.0).

Final score = `0.4 × keyword + 0.3 × recency + 0.2 × (1/tier) + 0.1 × author`. Truncate each section to `max_items_per_section`.

## 6. Summarization

Each item gets a one-line summary generated by an LLM call (Claude):

- **Input:** Title + abstract (or first 500 chars if no abstract).
- **Prompt:** "Summarize this paper in one sentence for an economics audience. Focus on the method and main finding, not motivation."
- **Course module tagging (optional):** If `course_modules` is configured, the summary step also tags items with the most relevant module (by keyword overlap between abstract and module keywords). Displayed as a badge in output, e.g., `[Week 3 — IV]`.
- **Fallback:** If no abstract is available, use the title as-is with no LLM call.

## 7. State file

Persist seen-item IDs across runs in `state.json`:

```json
{
  "last_run": "2026-06-01",
  "seen": {
    "doi:10.1234/example": {"first_seen": "2026-05-25", "tier": 1},
    "title_hash:a1b2c3d4": {"first_seen": "2026-05-28", "tier": 2}
  }
}
```

- On each run, fetch items within the `lookback_days` window, then filter out any already in `seen`.
- Add new items to `seen` after rendering.
- Prune entries older than 2× `lookback_days` to keep the file small.

## 8. Output

Render to the configured format. Default markdown layout:

```
# {digest.name} — {run_date}

## New working papers
- **{title}** — {authors} ({venue}, {date}) [Week 3 — IV]
  {one-line LLM summary}. [link]

## New data releases
- **{dataset}** — {source}, updated {date}. {what changed}. [link]

## Policy & news
- {headline} — {outlet}, {date}. [link]

---
*Sources: {list of sources that responded}. Skipped: {list of sources that failed, if any}.*
```

For LaTeX/Beamer output, the same item objects render via a swapped template (Beamer `\item` blocks or article `\bibitem`-style entries).

**Output location:** saved to `{output_dir}/{run_date}_digest.{ext}`.

## 9. Scope & phasing

| Phase | What's in | What's out |
|---|---|---|
| **v1** | Tiers 1–3, dedup, relevance scoring, LLM summaries, markdown output, state file | Tier 4 sources, Gmail OAuth, LaTeX output |
| **v2** | Tier 4 (Scholar alerts, SSRN, Google News), LaTeX/Beamer template, course module tagging | — |

## 10. Notes for implementation

- **Config-driven retargeting:** changing the whole digest's subject = editing `topics` + swapping `feed_id`s. No logic touched.
- **NEP is the highest-leverage single source** — the curation is already done, so it's the cheapest path to a good Tier 1.
- **OpenAlex over raw Scholar** for automation: documented JSON API, no scraping, stable. Use Scholar alerts only as a recall booster (v2).
- **Wrap all fetchers in the error-handling contract** (Section 3). A run should never fail because one source changed its HTML.
- **State file is the single source of truth** for "new vs. seen." `lookback_days` bounds the fetch window; the state file filters within it.
