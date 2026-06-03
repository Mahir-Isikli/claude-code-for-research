# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "pandas", "matplotlib"]
# ///
"""Demo for HU session: World Bank migration data -> publication-ready charts.

Chart 1: Net migration, Germany, 1960-2025 (annual)        [SM.POP.NETM]
Chart 2: Female share of migrant stock, 1990-2020, 6 countries [SG.POP.MIGR.FE.ZS]
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

WB = "https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"


def fetch(countries: str, indicator: str, date: str) -> pd.DataFrame:
    r = requests.get(
        WB.format(countries=countries, indicator=indicator),
        params={"format": "json", "per_page": 1000, "date": date},
        timeout=30,
    )
    r.raise_for_status()
    rows = r.json()[1]
    df = pd.DataFrame(
        {
            "country": x["country"]["value"],
            "year": int(x["date"]),
            "value": x["value"],
        }
        for x in rows
        if x["value"] is not None
    )
    return df.sort_values(["country", "year"])


# Publication style: serif, no chartjunk
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "figure.dpi": 150,
    }
)

# --- Chart 1: Net migration, Germany, 1960-2025 ---
de = fetch("DEU", "SM.POP.NETM", "1960:2025")
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.axhline(0, color="black", lw=0.8)
ax.fill_between(de["year"], de["value"] / 1000, 0, alpha=0.25, color="#1f5fa8")
ax.plot(de["year"], de["value"] / 1000, color="#1f5fa8", lw=1.6)
for yr, label in [(1973, "Recruitment\nban"), (1990, "Reunification"), (2015, "Refugee\ninflux"), (2022, "Ukraine\nwar")]:
    v = de.loc[de["year"] == yr, "value"]
    if not v.empty:
        ax.annotate(label, (yr, v.iloc[0] / 1000), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=8, color="#444")
ax.set_title("Net migration, Germany, 1960–2025", loc="left", fontweight="bold")
ax.set_ylabel("Thousands of people")
ax.set_xlabel("")
fig.text(0.01, 0.01, "Source: World Bank WDI (SM.POP.NETM), UN Population Division.", fontsize=7.5, color="#666")
fig.tight_layout(rect=(0, 0.03, 1, 1))
for ext in ("png", "pdf"):
    fig.savefig(OUT / f"net_migration_germany.{ext}")

# --- Chart 2: Female share of international migrant stock ---
COUNTRIES = "DEU;USA;FRA;TUR;SAU;ARE"
fe = fetch(COUNTRIES, "SG.POP.MIGR.FE.ZS", "1990:2020")
fig, ax = plt.subplots(figsize=(8, 4.5))
palette = {
    "Germany": "#1f5fa8", "United States": "#2a9d8f", "France": "#7b2cbf",
    "Turkiye": "#e76f51", "Saudi Arabia": "#b08900", "United Arab Emirates": "#9b2226",
}
for country, grp in fe.groupby("country"):
    ax.plot(grp["year"], grp["value"], marker="o", ms=3.5, lw=1.6,
            color=palette.get(country, "gray"), label=country)
    ax.annotate(country, (grp["year"].iloc[-1], grp["value"].iloc[-1]),
                textcoords="offset points", xytext=(6, 0), va="center",
                fontsize=8.5, color=palette.get(country, "gray"))
ax.axhline(50, color="black", lw=0.8, ls="--", alpha=0.5)
ax.annotate("gender parity", (1990.2, 50.6), fontsize=8, color="#444")
ax.set_title("Female share of international migrant stock, 1990–2020", loc="left", fontweight="bold")
ax.set_ylabel("% of migrant stock")
ax.set_xlim(1989, 2027)
ax.set_ylim(20, 60)
fig.text(0.01, 0.01, "Source: World Bank Gender Statistics (SG.POP.MIGR.FE.ZS), UN DESA.", fontsize=7.5, color="#666")
fig.tight_layout(rect=(0, 0.03, 1, 1))
for ext in ("png", "pdf"):
    fig.savefig(OUT / f"female_migrant_share.{ext}")

print("Wrote charts to", OUT)
for f in sorted(OUT.iterdir()):
    print(" -", f.name, f.stat().st_size // 1024, "KB")
