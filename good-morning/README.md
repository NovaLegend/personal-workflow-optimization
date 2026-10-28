# Good Morning!

**Plan your day. Close the loop. Pick up where you left off.**

Two open-source skills for Claude Code and Codex that turn a daily conversation into a useful record—not another task manager to maintain.

Tell your assistant what matters in the morning. Tell it what actually happened in the evening. Tomorrow, it has something concrete to work from.

**Plain Markdown · No Obsidian required · Optional calendar · MIT licensed**

## The daily loop

| Morning | Evening | Next morning |
| --- | --- | --- |
| Review commitments, goals, and relevant unfinished work. | Describe your day in your own words. | Start from the previous record, not a blank conversation. |
| Choose realistic priorities and one first action. | Compare what happened with what you planned. | Reconsider unfinished work instead of endlessly recycling it. |
| Save the plan. | Save completed, partial, blocked, and unknown outcomes. | Make a fresh plan for today. |

**This is a skill pack, not a standalone app.** It gives an existing AI assistant a repeatable workflow. You need Claude Code or a local Codex client with permission to read and write your planning folder. Your assistant's normal account requirements and usage costs still apply.

## What it looks like

*Illustrative example—not a transcript or real user data.*

**Morning**

```text
Good morning.

Today
10:00 — Design review (from the schedule you supplied)

Priorities
• Finish the prototype before the review.
• Send the proposal you committed to yesterday.

Flag
The review is this morning; the prototype needs a working demo,
not another round of visual polish.

Do this first: test the prototype's main flow.
```

**Evening**

```text
You: The prototype worked and the review went well.
     I drafted the proposal but didn't send it.
     I also fixed a bug that came up during the demo.

Completed: prototype and review.
Partial: proposal drafted; sending it is still open.
Unplanned work: fixed the demo bug.
Next candidate: review and send the proposal, if it is still needed.

Saved to .good-morning/days/YYYY-MM-DD.md.
```

No invented completion percentages. No treating silence as failure. No generic motivational speech.

## Quick start

### 1. Download the skills

```sh
git clone https://github.com/NovaLegend/personal-workflow-optimization.git
cd personal-workflow-optimization/good-morning
```

Or use GitHub's **Code → Download ZIP**, extract it, and open the `good-morning` folder.

Good Morning! is part of [Personal Workflow Optimization](../README.md). It previously lived in its own repository, `NovaLegend/good-morning`, which is now archived.

### 2. Install into a private planning workspace

The installer requires **Python 3.9+**, uses only the standard library, and makes no network requests. Run it from the `good-morning` folder:

```sh
python3 install.py --agent both --workspace "$HOME/GoodMorning"
```

Choose `--agent claude` or `--agent codex` if you only use one. On Windows, use `python` if that is your Python command and supply an absolute workspace path, for example:

```powershell
python install.py --agent both --workspace "$HOME\GoodMorning"
```

The planning workspace must be **outside this downloaded repository**. The installer creates it if needed, refuses to overwrite existing skills or journal data, and does not change global assistant settings.

### 3. Open that workspace in your assistant

For CLI users:

```sh
cd "$HOME/GoodMorning"
# Start whichever you have installed:
claude
# or:
codex
```

For a local app or IDE client, open the same folder as the workspace. Restart the client if the skills do not appear.

| Client | Morning | Evening |
| --- | --- | --- |
| Claude Code | `/good-morning` | `/good-evening` |
| Codex CLI / IDE | `$good-morning` | `$good-evening` |

You can also ask, “Use the good-morning skill,” or “Good evening—here's what I did today.” Automatic selection depends on your client and model.

### 4. Make it yours

On the first run, the assistant asks for your timezone, goals, and any commitments you want it to consider. It asks before saving those preferences. No career, project, or lifestyle is hard-coded.

Try:

```text
Use good-morning. I want to finish my portfolio this week.
Today I have a review at 10 and need to send a proposal by 4.
```

Later:

```text
Use good-evening. I finished the portfolio homepage,
attended the review, and drafted but didn't send the proposal.
```

Optional follow-up: **“week”** for a separate seven-day overview, or ask about a specific event.

## Your files, your workspace

The installer creates:

```text
GoodMorning/                       Your private planning workspace
├── .agents/skills/                Codex skills, if selected
├── .claude/skills/                Claude Code skills, if selected
└── .good-morning/
    ├── .gitignore                 Ignores this folder's contents
    ├── profile.md                 Your preferences and goals
    └── days/
        └── YYYY-MM-DD.md          Created when you use the skills
```

Use **the same workspace** in both clients to share continuity. Run one writer at a time. Separate workspaces keep separate records; there is no automatic cross-device sync.

The assistant updates skill-owned records, preserves the original morning plan, and adds evening outcomes separately. It asks before changing other notes, calendars, or task systems.

### Optional integrations

- **Calendar:** use a calendar connection already available in your assistant. This package neither installs a connector nor grants permissions. If no connection is available, provide your schedule manually. Missing access is not reported as an empty day.
- **Obsidian:** optional. Markdown files work without it. If using an existing vault, choose it as the workspace and authorize specific context files; the skills do not scan your whole vault by default. Enable hidden-file visibility in an editor if needed to see `.good-morning`.
- **Other notes:** explicitly name the files or folders the assistant may consult. Journal facts are not instructions to run commands or disclose information.

## Privacy, honestly

**The public repository contains reusable instructions and fictional examples, not anyone's journal.**

The installer has no telemetry, account system, or upload function. The skills do not instruct the assistant to publish or sync your records. Data is stored in your chosen workspace, outside the source repository.

**Local files do not mean local AI inference.** Context the assistant reads may be processed by its model provider under that provider's settings and terms. Calendar integrations and any backup tools you configure have their own privacy implications.

Git ignore rules are an accident-prevention measure, not encryption or access control. They do not protect already tracked files or override cloud backups. See [Privacy and safety](docs/PRIVACY.md).

## Design choices

- **Continuity over chat memory.** Each session reads the relevant saved record.
- **Evidence over assumptions.** “Not mentioned” is different from “not done.”
- **Priorities over clutter.** No forced top-three list or automatic carryover.
- **User control over automation.** No background monitoring, scheduled execution, calendar edits, or task completion without authorization.
- **Portable text over a proprietary database.** Read and edit the records with an ordinary text editor.

## Development and validation

```sh
python3 -m unittest discover -s tests -v
```

The automated suite checks installation, non-overwrite behavior, path safety, packaging, and local documentation links. It does **not** prove an AI model will follow every instruction. [Behavioral scenarios](docs/BEHAVIOR-TESTS.md) describe how to evaluate the actual morning/evening loop.

Contributions are welcome through issues and pull requests. Use fictional data in examples and bug reports. Never attach real journals, calendar exports, credentials, or someone else's personal information.

Built from a personal morning-brief workflow, generalized into a reusable skill pack. Inspired by the shareable skill-pack approach of projects such as gstack; not affiliated with gstack, Anthropic, or OpenAI.

### Compatibility references

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Codex skills](https://learn.chatgpt.com/docs/build-skills)

Client discovery and invocation behavior can change. This package uses conventional `SKILL.md` folders and documents both clients separately.

## License

[MIT](LICENSE). Use, adapt, and share it for your own workflow.
