"""Deterministic package/installer checks; not model-behavior evaluations."""

import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("good_morning_install", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.workspace = self.base / "private planner"

    def test_both_clients_receive_exact_skill_contents(self):
        installer.install(self.workspace, "both")
        for agent_dir in (".agents", ".claude"):
            for skill in installer.SKILLS:
                source = ROOT / "skills" / skill / "SKILL.md"
                dest = self.workspace / agent_dir / "skills" / skill / "SKILL.md"
                self.assertEqual(dest.read_bytes(), source.read_bytes())
        self.assertEqual(
            (self.workspace / ".good-morning/.gitignore").read_text(), "*\n"
        )
        self.assertTrue((self.workspace / ".good-morning/days").is_dir())
        self.assertIn("Setup confirmed: no", (self.workspace / ".good-morning/profile.md").read_text())

    def test_only_requested_client_is_installed(self):
        installer.install(self.workspace, "codex")
        self.assertTrue((self.workspace / ".agents/skills/good-morning/SKILL.md").is_file())
        self.assertFalse((self.workspace / ".claude").exists())

    def test_reinstall_does_not_overwrite(self):
        installer.install(self.workspace, "both")
        profile = self.workspace / ".good-morning/profile.md"
        profile.write_text("Fictional custom profile\n")
        with self.assertRaises(installer.InstallError):
            installer.install(self.workspace, "both")
        self.assertEqual(profile.read_text(), "Fictional custom profile\n")

    def test_second_client_preserves_existing_records(self):
        installer.install(self.workspace, "claude")
        profile = self.workspace / ".good-morning/profile.md"
        profile.write_text("Fictional custom profile\n")
        journal = self.workspace / ".good-morning/days/2000-01-01.md"
        journal.write_text("Fictional daily entry\n")
        installer.install(self.workspace, "codex")
        self.assertEqual(profile.read_text(), "Fictional custom profile\n")
        self.assertEqual(journal.read_text(), "Fictional daily entry\n")

    def test_preflight_conflict_does_not_partially_install(self):
        occupied = self.workspace / ".agents/skills/good-evening"
        occupied.mkdir(parents=True)
        with self.assertRaises(installer.InstallError):
            installer.install(self.workspace, "both")
        self.assertFalse((self.workspace / ".claude").exists())
        self.assertFalse((self.workspace / ".good-morning").exists())
        self.assertFalse((self.workspace / ".agents/skills/good-morning").exists())

    def test_source_repository_is_not_a_planning_workspace(self):
        for path in (ROOT, ROOT / "private-records"):
            with self.subTest(path=path):
                with self.assertRaises(installer.InstallError):
                    installer.install(path, "codex")

    def test_relative_workspace_rejected(self):
        with self.assertRaises(installer.InstallError):
            installer.install("relative-workspace", "both")

    def test_dry_run_writes_nothing(self):
        paths = installer.install(self.workspace, "both", dry_run=True)
        self.assertEqual(len(paths), 6)
        self.assertFalse(self.workspace.exists())

    def test_symlinked_workspace_rejected(self):
        actual = self.base / "actual"
        actual.mkdir()
        try:
            self.workspace.symlink_to(actual, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation not available for this user/platform.")
        with self.assertRaises(installer.InstallError):
            installer.install(self.workspace, "both")
        self.assertEqual(list(actual.iterdir()), [])

    def test_symlinked_state_rejected(self):
        self.workspace.mkdir()
        actual = self.base / "outside"
        actual.mkdir()
        try:
            (self.workspace / ".good-morning").symlink_to(actual, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation not available for this user/platform.")
        with self.assertRaises(installer.InstallError):
            installer.install(self.workspace, "both")
        self.assertFalse((self.workspace / ".claude").exists())

    def test_file_in_place_of_parent_rejected(self):
        self.workspace.mkdir()
        (self.workspace / ".agents").write_text("not a directory")
        with self.assertRaises(installer.InstallError):
            installer.install(self.workspace, "both")
        self.assertFalse((self.workspace / ".claude").exists())

    def test_incomplete_existing_state_rejected(self):
        (self.workspace / ".good-morning").mkdir(parents=True)
        with self.assertRaises(installer.InstallError):
            installer.install(self.workspace, "both")
        self.assertFalse((self.workspace / ".agents").exists())

    def test_cli_reports_success(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "install.py"), "--agent", "both",
             "--workspace", str(self.workspace)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Created:", result.stdout)


class PackageTests(unittest.TestCase):
    def test_skill_frontmatter(self):
        for name in installer.SKILLS:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            header = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n", text)
            self.assertIsNotNone(header)
            self.assertEqual(header.group(1), name)
            self.assertLessEqual(len(header.group(2)), 1024)
            self.assertNotIn("[TODO:", text)

    def test_local_documentation_links_exist(self):
        for path in ROOT.rglob("*.md"):
            if "__pycache__" in path.parts:
                continue
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                self.assertTrue((path.parent / target.split("#")[0]).exists(), (path, target))

    def test_source_tree_has_no_runtime_state(self):
        self.assertFalse((ROOT / ".good-morning").exists())
        self.assertFalse((ROOT / ".env").exists())


if __name__ == "__main__":
    unittest.main()
