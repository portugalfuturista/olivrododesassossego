#!/usr/bin/env python3
"""
Aurélio Wiki Sync Bridge — olivrododesassossego

Functional CLI for managing Git-backed memory sync between the Aurélio
VS Code extension and this wiki repository.

Commands:
  --push           Stage .aurelio/memory/ + sessions/, commit, push
  --pull           Pull latest from origin (rebase)
  --status         Show pending changes in sync-managed dirs
  --export-session Export a JSON session file into sessions/<id>/

Usage:
  python3 sync.py --push
  python3 sync.py --pull
  python3 sync.py --status
  python3 sync.py --export-session /path/to/session.json
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Resolve repo root (parent of .aurelio/)
REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories managed by sync
MEMORY_DIR = REPO_ROOT / ".aurelio" / "memory"
SESSIONS_DIR = REPO_ROOT / "sessions"

# Commit prefixes
MEMORY_PREFIX = "🧠 memoria:"
SESSION_PREFIX = "📓 sessão:"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command in the repo root."""
    result = subprocess.run(
        ["git", *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    if check and result.returncode != 0:
        print(f"git {' '.join(args)} failed: {result.stderr.strip()}", file=sys.stderr)
    return result


def cmd_status() -> None:
    """Show pending changes in sync-managed directories."""
    print(f"📂 Repo: {REPO_ROOT}")
    print(f"📁 Memory: {MEMORY_DIR}")
    print(f"📁 Sessions: {SESSIONS_DIR}")
    print()

    # Overall status
    result = git("status", "--porcelain", "--", ".aurelio/memory/", "sessions/", check=False)
    lines = [l for l in result.stdout.strip().split("\n") if l.strip()]

    if not lines:
        print("✅ No pending changes in sync-managed directories.")
    else:
        print(f"📝 {len(lines)} pending change(s):")
        for line in lines:
            status_code = line[:2].strip()
            filepath = line[3:]
            icon = {"M": "📝", "A": "➕", "D": "🗑️", "??": "❓"}.get(status_code, "📄")
            print(f"  {icon} [{status_code}] {filepath}")

    # Branch info
    branch = git("branch", "--show-current", check=False)
    print(f"\n🌿 Branch: {branch.stdout.strip() or 'detached HEAD'}")

    # Remote status
    git("fetch", "--dry-run", check=False)
    behind = git("rev-list", "--count", "HEAD..@{u}", check=False)
    ahead = git("rev-list", "--count", "@{u}..HEAD", check=False)
    behind_n = int(behind.stdout.strip()) if behind.returncode == 0 else 0
    ahead_n = int(ahead.stdout.strip()) if ahead.returncode == 0 else 0

    if behind_n > 0:
        print(f"⬇️  {behind_n} commit(s) behind remote")
    if ahead_n > 0:
        print(f"⬆️  {ahead_n} commit(s) ahead of remote")
    if behind_n == 0 and ahead_n == 0:
        print("🔄 Up to date with remote")


def cmd_push() -> None:
    """Stage .aurelio/memory/ + sessions/, commit with prefix, push."""
    print("🚀 Wiki Push")

    # Stage memory changes
    mem_status = git("status", "--porcelain", "--", ".aurelio/memory/", check=False)
    mem_changes = [l for l in mem_status.stdout.strip().split("\n") if l.strip()]

    if mem_changes:
        git("add", ".aurelio/memory/")
        msg = f"{MEMORY_PREFIX} sync {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        git("commit", "-m", msg)
        print(f"  ✅ Committed {len(mem_changes)} memory file(s): {msg}")
    else:
        print("  ℹ️  No memory changes to commit.")

    # Stage session changes
    sess_status = git("status", "--porcelain", "--", "sessions/", check=False)
    sess_changes = [l for l in sess_status.stdout.strip().split("\n") if l.strip()]

    if sess_changes:
        git("add", "sessions/")
        msg = f"{SESSION_PREFIX} export {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        git("commit", "-m", msg)
        print(f"  ✅ Committed {len(sess_changes)} session file(s): {msg}")
    else:
        print("  ℹ️  No session changes to commit.")

    if mem_changes or sess_changes:
        result = git("push", "origin", "main", check=False)
        if result.returncode == 0:
            print("  🎯 Pushed to remote.")
        else:
            print(f"  ⚠️  Push failed: {result.stderr.strip()}")
    else:
        print("  ℹ️  Nothing to push.")


def cmd_pull() -> None:
    """Pull latest from origin with rebase."""
    print("⬇️  Wiki Pull")

    # Stash local changes
    status = git("status", "--porcelain", check=False)
    had_stash = bool(status.stdout.strip())

    if had_stash:
        git("stash", "push", "-m", "aurelio-sync-pull-stash")
        print("  📦 Stashed local changes.")

    result = git("pull", "--rebase", "origin", "main", check=False)
    if result.returncode == 0:
        print(f"  ✅ Pull successful: {result.stdout.strip()}")
    else:
        print(f"  ⚠️  Pull failed: {result.stderr.strip()}")

    if had_stash:
        pop_result = git("stash", "pop", check=False)
        if pop_result.returncode == 0:
            print("  📦 Re-applied stashed changes.")
        else:
            print("  ⚠️  Stash conflict — keeping local (last-write-wins).")
            git("checkout", "--theirs", ".", check=False)
            git("stash", "drop", check=False)


def cmd_export_session(json_path: str) -> None:
    """Import a JSON session file into sessions/<id>/."""
    print(f"📓 Export Session: {json_path}")

    if not os.path.isfile(json_path):
        print(f"  ❌ File not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    with open(json_path, "r") as f:
        data = json.load(f)

    # Extract session ID
    session_id = data.get("metadata", {}).get("sessionId") or data.get("sessionId")
    if not session_id:
        print("  ❌ No sessionId found in JSON.", file=sys.stderr)
        sys.exit(1)

    # Create sessions/<id>/ directory
    session_dir = SESSIONS_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    # Write the TOON JSON
    toon_path = session_dir / "session.json"
    with open(toon_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Wrote {toon_path.relative_to(REPO_ROOT)}")

    # Stage + commit
    git("add", str(session_dir.relative_to(REPO_ROOT)))
    title = data.get("metadata", {}).get("title", session_id)
    msg = f"{SESSION_PREFIX} {title[:60]}"
    git("commit", "-m", msg)
    print(f"  ✅ Committed: {msg}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aurélio Wiki Sync Bridge — olivrododesassossego",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--push", action="store_true", help="Stage, commit, and push memory + sessions")
    group.add_argument("--pull", action="store_true", help="Pull latest from origin (rebase)")
    group.add_argument("--status", action="store_true", help="Show pending changes")
    group.add_argument("--export-session", metavar="JSON_FILE", help="Import JSON session into sessions/")

    args = parser.parse_args()

    if args.push:
        cmd_push()
    elif args.pull:
        cmd_pull()
    elif args.status:
        cmd_status()
    elif args.export_session:
        cmd_export_session(args.export_session)


if __name__ == "__main__":
    main()
