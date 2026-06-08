---
name: data-visualization
description: Fetch data from public APIs (e.g. World Bank) and build publication-ready charts and figures. Use when asked to visualize data, create figures for a paper or thesis, or explore a dataset graphically.
---

# Data Visualization

> **Status: testing.** The publication profile below is a first draft; Sulin will refine it based on how her figures should look.

Build charts directly from raw data or public APIs, no notebooks or manual downloads needed, and export them ready for papers and slides.

This skill has two layers:
- **This file** is the working checklist: dataset to clean, publication-ready figure, plus a World Bank API quick reference and a runnable example.
- **`reference.md`** is the teaching reference: design principles, a chart-selection guide, and Python/R/Stata style presets, adapted from Sulin Sardoschau's notes and Kieran Healy's *Data Visualization: A Practical Introduction*. Read it when you need to justify a chart choice or set up a new language.

## Workflow

1. **Find the data.** For country-level statistics, the World Bank API needs no key or login (reference below). Otherwise ask the user for a CSV/XLSX or the source.
2. **Inspect before plotting.** Check variable types (continuous, categorical, ordinal, temporal), ranges, missingness, and N. Check coverage: which years, which countries, where are the gaps? Tell the user about gaps before plotting.
3. **Choose the chart type, and say why.** Map the question to a chart using the selection guide in `reference.md`: state the choice, why it fits, and why a tempting alternative is worse.
4. **Plot with the publication profile** (below).
5. **Export both formats:** PDF (vector, for LaTeX/Overleaf) and PNG (300 dpi for print, 150 for screen).
6. **Always cite the source** in a note under the figure (dataset name + indicator code).

## Publication profile (the export target for papers / Overleaf)

The house style for figures that go into a paper or thesis. It is intentionally stricter than the teaching defaults in `reference.md` (a colourblind seaborn theme for on-screen teaching). Both share the same principles; this profile is the final polish step.

- Serif fonts, 10-11 pt, to match LaTeX body text
- No top/right spines, subtle grid (alpha ~0.25)
- Title top-left, bold; axis labels only where not obvious
- Direct line labels instead of legends where possible
- Colourblind-safe palette for any categorical colour
- Honest scales: never truncate axes to exaggerate; bar-chart y-axes start at zero
- Source note bottom-left in small grey text
- Export PDF (vector) for Overleaf and PNG at 300 dpi for print

## World Bank API quick reference

```
https://api.worldbank.org/v2/country/{ISO3;ISO3}/indicator/{INDICATOR}?format=json&per_page=1000&date=1960:2025
```

Useful migration indicators (coverage verified June 2026):

| Indicator | Name | Coverage |
|---|---|---|
| `SM.POP.NETM` | Net migration | Annual, 1960-2025 |
| `SM.POP.TOTL` | International migrant stock, total | 1990-2024, 5-year steps |
| `SM.POP.TOTL.ZS` | Migrant stock (% of population) | 1990-2024, 5-year steps |
| `SG.POP.MIGR.FE.ZS` | Female migrants (% of migrant stock) | 1990-2020, 5-year steps |
| `SM.POP.RHCR.EA` | UNHCR refugees, by country of asylum | Annual, 1960-2024 |
| `SM.POP.RHCR.EO` | UNHCR refugees, by country of origin | Annual, 1960-2024 |

## Example

`scripts/wb_migration_demo.py` fetches two of the indicators above and produces two charts (net migration Germany 1960-2025, female migrant share by country 1990-2020) as PNG + PDF:

```
uv run scripts/wb_migration_demo.py
```
