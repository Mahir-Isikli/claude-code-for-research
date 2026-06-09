# Claude Code for Research

Materials for the Claude Code session at Humboldt University Berlin (June 9, 2026), part of the "How to Develop a Research Proposal" course by Prof. Sulin Sardoschau.

Everything in this repo is meant to be taken home: install the skills, set up the routines, and adapt them to your own research.

## What's in here

```
.claude/skills/
  data-visualization/   Build publication-ready charts from raw data (status: testing)
  migration-digest/     Same-day or this-week digest of migration papers, policy news, and data releases (status: final)
routines/
  news-digest/          Weekly digest of news + academic papers on your research topic (status: draft)
```

Skills live in `.claude/skills/` so Claude Code discovers and loads them automatically when you open this repo.

Things marked **testing** or **draft** are work in progress; they become **final** before the session.

## Session outline

1. **Intro** (~5 min): why agentic coding tools matter for research
2. **Live demo**: download migration data from a public API (e.g. World Bank) and build visualizations end to end, no notebooks, no browser tabs
3. **Build a skill together**: turn the demo into a reusable data visualization skill
4. **Routines**: set up a scheduled news digest (news + academic papers on a topic)
5. **Q&A** with Mahir and Sulin

## Getting started

The easiest way to start is the **Claude Desktop app**, no terminal needed:

1. Download it from [claude.com/download](https://claude.com/download) (macOS and Windows, including ARM64)
2. Sign in. Chat is free; the agent features used in this workshop (Claude Code / Cowork) require a Pro subscription (~$20/month, cancellable anytime) or higher. If you want to follow along live, set this up before the session
3. Open a folder (e.g. a clone of this repo) and start asking

See **[INSTALL.md](INSTALL.md)** for the full step-by-step walkthrough (no terminal needed, including speech-to-text).

## Contributing

This repo is built by Mahir Isikli and Sulin Sardoschau. Students are welcome to open issues or PRs with their own skills and routines after the session.
