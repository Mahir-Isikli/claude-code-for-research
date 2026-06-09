---
name: migration-digest
description: Build a same-day or this-week migration digest from live sources (NEP-MIG, IZA, MPI, UNHCR, Eurostat). Use when asked for a migration briefing, news digest, or weekly update. Always anchors searches to today's date — no stale results.
---

# Migration Digest

Produces a scannable digest of new migration papers, policy news, and data releases, anchored to **today's date**. Every search query includes the current date so results stay within the past 7 days. If a section has no new items this week, that is noted explicitly rather than backfilling with older content.

This skill has two parts:
- **This file** is the workflow Claude follows every time the skill is invoked.
- `routines/news-digest/data-digest-design.md` is the engineering spec (source tiers, dedup, scoring, state file). Refer to it when adding sources or changing cadence.

---

## Workflow

### Step 0 — Set the date window

Before searching, establish:
- **Today**: use the date from system context (e.g. `2026-06-09`)
- **Window start**: today minus 7 days (weekly digest) or today (same-day digest)
- **Append the current year and month** to every search query — this is the single most important step for preventing stale results

### Step 1 — New research (run all in parallel)

Search each source below. Include the current year and month in every query.

| Source | Query pattern |
|---|---|
| NEP-MIG | `site:nep.repec.org/nep-mig/ [current year]` — NEP-MIG is a curated weekly list of new econ papers on migration; the latest issue is the anchor |
| IZA Discussion Papers | `site:docs.iza.org migration [month year]` |
| NBER Working Papers | `site:nber.org "working paper" migration [month year]` |
| CEPR / VoxEU | `site:voxeu.org migration [month year]` |
| CReAM | `site:cream-migration.org [year]` |

For each paper: title, authors, series + number, date posted, 1-sentence finding. Skip papers posted before the window start.

### Step 2 — Policy & news (run all in parallel)

| Source | Query pattern |
|---|---|
| Migration Policy Institute | `site:migrationpolicy.org [month year]` |
| Politico Europe | `site:politico.eu migration asylum [month year]` |
| UNHCR newsroom | `site:unhcr.org news [month year]` |
| IOM newsroom | `site:iom.int news [month year]` |
| Reuters / Guardian / BBC | `migration asylum policy [current week] site:reuters.com OR site:theguardian.com OR site:bbc.com` |

For each item: headline, outlet, publication date, 1-sentence why it matters. Hard cutoff: discard anything published before the window start.

### Step 3 — New data releases (run all in parallel)

| Source | Query pattern |
|---|---|
| Eurostat | `site:ec.europa.eu/eurostat migration asylum [month year]` |
| BAMF (German asylum stats) | `site:bamf.de [month year]` |
| Destatis | `site:destatis.de migration [month year]` |
| UNHCR Refugee Data Finder | `site:data.unhcr.org [month year]` |
| World Bank | `site:worldbank.org migration data [month year]` |

For each release: dataset name, source, date published, what the release covers or what changed.

### Step 4 — Filter, dedup, cap

1. **Hard cutoff**: discard anything published before the window start. Do not fill gaps with older items.
2. **Dedup**: if the same paper or event surfaces from two sources, keep the most authoritative version and note "also via X."
3. **Cap**: 4–6 items per section. Fewer focused items beats a long list.
4. **Flag empty sections**: if a monitored section has nothing new this week, write one line: *No new [research / data releases] from monitored sources this week.*

### Step 5 — Write the digest

```
# Migration Digest — [Date]

## New Research
- **[Title]** — [Authors] ([Series + number], [Date])
  [One-sentence finding]. [link]

## Policy & News
- **[Headline]** — [Outlet], [Date]
  [One-sentence why it matters]. [link]

## New Data
- **[Dataset / Release]** — [Source], [Date]
  [What changed or what the release covers]. [link]

---
*Sources checked: [list]. Lookback window: [window start] – [today]. Items before [window start] excluded.*
```

---

## Source quick reference

Full source hierarchy and fetch notes are in `routines/news-digest/data-digest-design.md`.

| Source | Best for | URL |
|---|---|---|
| NEP-MIG | New econ migration papers (weekly) | https://nep.repec.org/nep-mig/ |
| IZA | Discussion papers | https://www.iza.org/publications/dp |
| NBER | Working papers (Labor Studies, PE) | https://www.nber.org/papers?q=migration |
| CReAM | UCL migration working papers | https://www.cream-migration.org/publications.php |
| MPI | Policy analysis | https://www.migrationpolicy.org |
| Politico EU | EU migration news | https://www.politico.eu |
| UNHCR | Displacement & refugee news/data | https://www.unhcr.org |
| IOM | Global migration news | https://www.iom.int |
| Eurostat | EU asylum/migration statistics | https://ec.europa.eu/eurostat |
| BAMF | German asylum monthly statistics | https://www.bamf.de |
| Destatis | German national statistics | https://www.destatis.de |
