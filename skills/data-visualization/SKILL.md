---
name: data-visualization
description: Fetch data from public APIs (e.g. World Bank) and build publication-ready charts and figures. Use when asked to visualize data, create figures for a paper or thesis, or explore a dataset graphically.
---

# Data Visualization

> **Status: testing.** Publication standards below are a first draft; Sulin will refine them based on how her figures should look.

Build charts directly from raw data or public APIs, no notebooks or manual downloads needed, and export them ready for papers.

## Workflow

1. **Find the data.** For country-level statistics, the World Bank API needs no key or login (see reference below). Otherwise ask the user for a CSV/XLSX or the source.
2. **Fetch and inspect.** Check coverage first: which years, which countries, where are the gaps? Tell the user about gaps before plotting.
3. **Plot with publication style** (see standards below).
4. **Export both formats**: PDF (vector, for LaTeX/Overleaf) and PNG (for slides and docs).
5. **Always cite the source** in a note under the figure (dataset name + indicator code).

## Publication standards (draft)

- Serif fonts, 10-11 pt
- No top/right spines, subtle grid (alpha ~0.25)
- Title top-left, bold; axis labels only where not obvious
- Direct line labels instead of legends where possible
- Source note bottom-left in small gray text
- PNG at 150 dpi for screen, 300 dpi if it goes to print

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
