"""Keep the links into pypowerwall's docs pinned to the pypowerwall release we ship.

Links from README.md, AGENTS.md and docs/*.md into pypowerwall's own docs use the
release tag matching manifest.json's `pypowerwall==` pin (see AGENTS.md's
Conventions). tests/test_manifest.py checks the tag but can't check the anchors,
since that needs the network.

    python3 scripts/pypowerwall_doc_links.py           # check every link and anchor
    python3 scripts/pypowerwall_doc_links.py --write   # move links to the pin's tag, then check

The check downloads each linked file at the tag and fails if the file is missing
or an `#anchor` matches no heading (or explicit `<a name>`/`id`) in it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT_DIR / "custom_components" / "pypowerwall" / "manifest.json"
RAW_URL = "https://raw.githubusercontent.com/jasonacox/pypowerwall/{tag}/{path}"
LINK_RE = re.compile(
    r"https://github\.com/jasonacox/pypowerwall/blob/(?P<tag>[^/\s)]+)/"
    r"(?P<path>[^\s)#>\"']+)(?:#(?P<anchor>[^\s)>\"']+))?"
)


def doc_files() -> list[Path]:
    return [
        ROOT_DIR / "README.md",
        ROOT_DIR / "AGENTS.md",
        *sorted((ROOT_DIR / "docs").glob("*.md")),
    ]


def pinned_tag() -> str:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for requirement in manifest["requirements"]:
        match = re.fullmatch(r"pypowerwall==(.+)", requirement)
        if match:
            return f"v{match.group(1)}"
    raise SystemExit(f"No pinned pypowerwall requirement found in {MANIFEST_PATH}")


def github_anchors(markdown: str) -> set[str]:
    """Anchors GitHub generates for a Markdown file's headings, plus explicit ones."""
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    in_fence = False
    for line in markdown.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        match = None if in_fence else re.match(r" {0,3}#{1,6}\s+(.*?)\s*#*\s*$", line)
        if match:
            text = re.sub(r"<[^>]+>", "", match.group(1))
            text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
            slug = re.sub(r"[^\w\- ]", "", text.strip().lower()).replace(" ", "-")
            count = seen.get(slug, 0)
            seen[slug] = count + 1
            anchors.add(slug if count == 0 else f"{slug}-{count}")
    anchors.update(re.findall(r"<a\s+(?:name|id)=\"([^\"]+)\"", markdown))
    return anchors


def fetch(tag: str, path: str) -> str | None:
    try:
        with urllib.request.urlopen(RAW_URL.format(tag=tag, path=path), timeout=30) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None
        raise


def write_links(tag: str) -> int:
    changed = 0
    for doc in doc_files():
        text = doc.read_text(encoding="utf-8")
        new = re.sub(
            r"(https://github\.com/jasonacox/pypowerwall/blob/)[^/\s)]+/", rf"\g<1>{tag}/", text
        )
        if new != text:
            doc.write_text(new, encoding="utf-8")
            changed += 1
            print(f"{doc.relative_to(ROOT_DIR)}: links moved to {tag}")
    return changed


def check_links(tag: str) -> list[str]:
    problems: list[str] = []
    cache: dict[str, str | None] = {}
    for doc in doc_files():
        name = doc.relative_to(ROOT_DIR)
        for match in LINK_RE.finditer(doc.read_text(encoding="utf-8")):
            link_tag, path, anchor = match.group("tag", "path", "anchor")
            if link_tag != tag:
                problems.append(f"{name}: {match.group(0)} is not pinned to {tag}")
                continue
            if path not in cache:
                cache[path] = fetch(tag, path)
            content = cache[path]
            if content is None:
                problems.append(f"{name}: {path} does not exist at {tag}")
            elif anchor and anchor not in github_anchors(content):
                problems.append(f"{name}: #{anchor} matches no heading in {path} at {tag}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--write", action="store_true", help="move every link to the pinned tag first"
    )
    args = parser.parse_args()

    tag = pinned_tag()
    if args.write:
        write_links(tag)
    problems = check_links(tag)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1
    print(f"All pypowerwall doc links resolve at {tag}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
