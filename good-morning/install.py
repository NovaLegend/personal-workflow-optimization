#!/usr/bin/env python3
"""Install workspace-local skills without overwriting existing files.

Python 3.9+, standard library only. No network or global configuration changes.
"""

import argparse
from pathlib import Path
import sys


SOURCE = Path(__file__).resolve().parent
SKILLS = ("good-morning", "good-evening")
AGENT_DIRS = {"claude": ".claude", "codex": ".agents"}
PROFILE = """# Good Morning! profile

- Setup confirmed: no
- Preferred name: optional; ask the user
- Timezone: ask the user
- Tone: concise, direct, and nonjudgmental
- Main goals: ask the user
- Current focus: ask the user
- Calendar: none configured; use commitments the user provides
- Approved context paths: none
- Sensitive details: retain only necessary operational implications

The assistant should ask before saving personal preferences here.
Private records stay in this workspace; they must not be published.
"""


class InstallError(Exception):
    """A predictable safety or configuration error."""


def reject_symlinks(path):
    """Check lexical ancestors before creating or reading workspace files."""
    for part in (path, *path.parents):
        if part.is_symlink():
            raise InstallError(f"Refusing symlinked path: {part}")


def install(workspace, agent, dry_run=False):
    if agent not in (*AGENT_DIRS, "both"):
        raise InstallError("Agent must be claude, codex, or both.")

    workspace = Path(workspace).expanduser()
    if not workspace.is_absolute():
        raise InstallError("Use an absolute path for --workspace.")
    reject_symlinks(workspace)
    workspace = workspace.resolve()
    if workspace == SOURCE or SOURCE in workspace.parents:
        raise InstallError("Choose a private workspace outside the source repository.")
    if workspace.exists() and not workspace.is_dir():
        raise InstallError("The workspace path is not a directory.")

    selected = tuple(AGENT_DIRS) if agent == "both" else (agent,)
    files = {}
    # Explicit allowlist: never copy arbitrary source files or user data.
    for skill in SKILLS:
        source = SOURCE / "skills" / skill / "SKILL.md"
        reject_symlinks(source)
        content = source.read_text(encoding="utf-8")
        if not content.startswith(f"---\nname: {skill}\n"):
            raise InstallError(f"Invalid skill manifest: {source}")
        for client in selected:
            destination = workspace / AGENT_DIRS[client] / "skills" / skill
            reject_symlinks(destination)
            if destination.exists():
                raise InstallError(
                    f"Already exists; no files changed: {destination}. "
                    "Review existing skills before replacing them manually."
                )
            for parent in destination.parents:
                if parent.exists() and not parent.is_dir():
                    raise InstallError(f"Expected a directory: {parent}")
            files[destination / "SKILL.md"] = content

    state = workspace / ".good-morning"
    reject_symlinks(state)
    if state.exists():
        # Adding another client must not modify an existing profile or journal.
        if not state.is_dir():
            raise InstallError(f"Expected a directory: {state}")
        for name in ("profile.md", ".gitignore"):
            path = state / name
            reject_symlinks(path)
            if not path.is_file():
                raise InstallError(f"Existing state is incomplete; review it first: {path}")
        if state.joinpath(".gitignore").read_text(encoding="utf-8").strip() != "*":
            raise InstallError("Existing journal ignore rules differ; review them first.")
        reject_symlinks(state / "days")
        if not (state / "days").is_dir():
            raise InstallError("Existing state has no days directory; review it first.")
    else:
        files[state / "profile.md"] = PROFILE
        files[state / ".gitignore"] = "*\n"

    # Preflight all target files before making any changes.
    for path in files:
        reject_symlinks(path)
        if path.exists():
            raise InstallError(f"Refusing to overwrite: {path}")

    if dry_run:
        return tuple(files)

    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also protects against an unexpected concurrent file.
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    (state / "days").mkdir(exist_ok=True)
    return tuple(files)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=("claude", "codex", "both"), required=True)
    parser.add_argument("--workspace", required=True, help="Absolute private workspace path.")
    parser.add_argument("--dry-run", action="store_true", help="Show intended files; write nothing.")
    args = parser.parse_args(argv)
    try:
        paths = install(args.workspace, args.agent, args.dry_run)
    except (InstallError, OSError, UnicodeError) as exc:
        print(f"Installation stopped: {exc}", file=sys.stderr)
        print(
            "Existing files are not overwritten. If an I/O error occurred during writing, "
            "inspect the destination for a partial installation before retrying.",
            file=sys.stderr,
        )
        return 1
    print("Would create:" if args.dry_run else "Created:")
    for path in paths:
        print(f"  {path}")
    if not args.dry_run:
        print("\nOpen the planning workspace in your assistant and invoke good-morning.")
        print("Journal records stay local; context read by the assistant may reach its provider.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
