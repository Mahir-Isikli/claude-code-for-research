# News Digest Routine

> **Status: draft.** Source list is a first proposal; Sulin will refine it with her preferred journals and outlets.

A scheduled routine that compiles a weekly digest of news and academic papers around a research topic (example here: migration).

## What it does

Every Monday morning, the agent searches the sources below for items from the past week, filters for relevance to the topic, and produces a short digest: 5-10 items, grouped into **News & policy**, **New research**, and **New data**, each with a one-sentence summary and link.

## Proposed sources (to be refined)

**New research**
- NEP-MIG: "New Economics Papers, Economics of Human Migration" weekly RePEc digest
- IZA Discussion Papers
- NBER working papers
- CEPR discussion papers
- CReAM (UCL Centre for Research & Analysis of Migration) working papers
- New issues: Journal of Population Economics, Journal of Development Economics, International Migration Review, Migration Studies, Demography

**News & policy**
- Migration Policy Institute (migrationpolicy.org)
- Mediendienst Integration (German coverage)
- Politico Europe (EU migration policy)
- UNHCR and IOM newsrooms

**New data**
- Eurostat migration datasets (migr_*)
- Destatis and BAMF releases (German asylum/migration statistics)
- UN DESA International Migrant Stock revisions
- UNHCR Refugee Data Finder updates

## How to set it up (Claude Desktop app)

1. Open the Claude Desktop app (Cowork)
2. Ask: "Create a scheduled task that runs every Monday at 8:00 and builds my migration news digest following routines/news-digest/README.md in this folder"
3. The agent will create the routine; review the first digest and steer the format

## Output format

```
# Migration Digest, Week of <date>

## News & policy
- <headline>: one-sentence why it matters (link)

## New research
- <authors, title>: one-sentence finding (link)

## New data
- <dataset/release>: what changed (link)
```
