"""Refresh only the upstream-work section from public GitHub pull requests."""

import argparse
import html
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- UPSTREAM:START -->"
END = "<!-- UPSTREAM:END -->"
USER = "Ritesh17rb"


def escape_cell(value: str) -> str:
    escaped = html.escape(" ".join(value.split()), quote=True)
    return re.sub(r"([\\`*_\[\]])", r"\\\1", escaped).replace("|", "&#124;")


def render(items: list[dict]) -> str:
    rows = []
    for item in items:
        match = re.fullmatch(
            r"https://github\.com/([A-Za-z0-9-]+)/([A-Za-z0-9_.-]+)/pull/(\d+)",
            item["html_url"],
        )
        if match is None:
            raise ValueError("Unexpected pull-request URL")
        owner, repo, number = match.groups()
        if owner.lower() == USER.lower():
            continue
        status = (
            "🟣&nbsp;Merged" if item["pull_request"].get("merged_at")
            else "🟢&nbsp;Open" if item["state"] == "open"
            else "⚪&nbsp;Closed"
        )
        rows.append(
            f'| **{escape_cell(owner)}/{escape_cell(repo)}** '
            f'| [{escape_cell(item["title"])} · #{number}]({item["html_url"]}) '
            f"| {status} |"
        )
        if len(rows) == 4:
            break
    if not rows:
        raise ValueError("No upstream pull requests returned; keeping existing content")
    return "\n".join([
        "| Project | Contribution | Status |",
        "| :--- | :--- | :--- |",
        *rows,
    ])


def replace_section(readme: str, section: str) -> str:
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("Expected exactly one upstream section")
    before, rest = readme.split(START)
    _, after = rest.split(END)
    return f"{before}{START}\n{section}\n{END}{after}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Use a saved GitHub search response")
    parser.add_argument("--check", action="store_true", help="Check without writing")
    args = parser.parse_args()
    if args.input:
        result = json.loads(args.input.read_text(encoding="utf-8"))
    else:
        process = subprocess.run([
            "gh", "api", "search/issues", "--method", "GET",
            "-f", f"q=is:pr is:public author:{USER} -user:{USER}",
            "-f", "sort=updated", "-f", "order=desc", "-f", "per_page=30",
        ], check=True, capture_output=True, text=True, encoding="utf-8")
        result = json.loads(process.stdout)
    if result.get("incomplete_results"):
        raise ValueError("Incomplete GitHub search; keeping existing content")
    readme_path = ROOT / "README.md"
    current = readme_path.read_text(encoding="utf-8")
    updated = replace_section(current, render(result["items"]))
    if args.check:
        if current != updated:
            raise SystemExit("Upstream section needs a refresh")
        print("Upstream section is current")
    elif current != updated:
        readme_path.write_text(updated, encoding="utf-8")
        print("Updated upstream work")
    else:
        print("No changes; no update needed")


if __name__ == "__main__":
    main()
