# Getting started (no terminal needed)

A step-by-step setup for the workshop. The easiest path is the **Claude Desktop app**: a normal window with tabs, no terminal. If you have never used a tool like this, this is the one to use.

Total setup time: about 10 minutes.

## 1. Install the Claude Desktop app

1. Go to [claude.com/download](https://claude.com/download).
2. Download the app for your system (macOS, or Windows including ARM64).
3. Open it and sign in (or create a free account).

## 2. Turn on the agent features (the part that does the work)

The free chat is enough to ask questions, but the workshop uses Claude's **agent** features (Claude Code / Cowork), which can read files, run code, and build things on your computer. Those need a **Pro subscription** (about 20 EUR/month, cancellable anytime).

- If you want to follow along live and build things yourself, set up Pro **before the session**.
- If you just want to watch today and try later, the free account is fine for now.

## 3. Point it at a folder

The agent works inside a folder on your computer. Give it this workshop's folder:

**Option A, download (simplest):**
1. Open [github.com/Mahir-Isikli/claude-code-for-research](https://github.com/Mahir-Isikli/claude-code-for-research).
2. Click the green **Code** button, then **Download ZIP**.
3. Unzip it somewhere you can find (e.g. your Desktop).
4. In the Claude Desktop app, open that folder.

**Option B, clone (if you know git):**
```
git clone https://github.com/Mahir-Isikli/claude-code-for-research.git
```
Then open the folder in the app.

## 4. Try it

Type, or just **talk to it** (the app has speech-to-text, click the microphone). For example:

> "Look at the data-visualization skill in this folder, then pull net migration for Germany from the World Bank and make me a clean line chart."

That is the whole loop: open a folder, describe what you want in plain language, review what it produces.

## Tips for a good first experience

- **Be specific.** "Make a chart" gets a guess. "A line chart, 1960 to 2025, serif font, label the axes, save as PDF" gets what you want. You steer the quality.
- **Give it the real data or source.** It should not invent numbers. Point it at a file, an API, or paste the data.
- **Verify the output.** You are the expert. Check the figure and the numbers; that is your job, not writing the code.
- **Speak to it.** Dictation is often faster than typing, especially for longer instructions.

## What is in this repo

- `.claude/skills/data-visualization/` build publication-ready charts from raw data or public APIs. Includes a runnable demo, cached example data, and pre-rendered charts. (Lives under `.claude/skills/` so Claude Code loads it automatically.)
- `routines/news-digest/` a weekly digest of news and academic papers on a research topic.

Everything here is meant to be taken home and adapted to your own research.
