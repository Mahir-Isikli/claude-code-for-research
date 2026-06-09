# Agent Instructions

This repo holds Claude Code materials for an academic research workshop at HU Berlin (June 9, 2026): skills, routines, and install instructions for Master/PhD students.

## Structure

- `.claude/skills/<skill-name>/SKILL.md`: one folder per skill, frontmatter with `name` and `description`, optional helper scripts in the same folder. Skills live under `.claude/skills/` so Claude Code discovers them automatically.
- `routines/<routine-name>/README.md`: scheduled automations (e.g. news digest), each with sources, schedule, output format, and setup instructions
- `README.md`: student-facing entry point with the session outline and getting-started guide

## Conventions

- Audience is researchers with little to no terminal experience. Write instructions for the Claude Desktop app first, terminal second.
- Keep skills self-contained and installable by copy-paste or clone.
- Visualizations should target publication use: clean exports (PDF/PNG) that work with LaTeX/Overleaf.
- No personal data, credentials, or meeting notes in this repo. It is public.
