#!/usr/bin/env python3
"""Check local Markdown and HTML links without making network requests."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: set[str] = set()
        self.references: list[tuple[int, str]] = []
        self.code_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"pre", "code"}:
            self.code_depth += 1
        if self.code_depth:
            return
        attributes = dict(attrs)
        if attributes.get("id"):
            self.anchors.add(attributes["id"])
        if tag == "a" and attributes.get("name"):
            self.anchors.add(attributes["name"])
        for attribute in ("href", "src"):
            value = attributes.get(attribute)
            if value:
                self.references.append((self.getpos()[0], value))

    def handle_endtag(self, tag: str) -> None:
        if tag in {"pre", "code"} and self.code_depth:
            self.code_depth -= 1


def _without_fenced_code(text: str) -> str:
    lines = text.splitlines()
    result: list[str] = []
    fence: tuple[str, int] | None = None
    for line in lines:
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence:
            closing = re.match(r"^\s{0,3}(`{3,}|~{3,})\s*$", line)
            if closing and closing.group(1)[0] == fence[0] and len(closing.group(1)) >= fence[1]:
                fence = None
            result.append("")
        elif match:
            fence = (match.group(1)[0], len(match.group(1)))
            result.append("")
        else:
            result.append(line)
    return "\n".join(result)


def _without_code(text: str) -> str:
    return "\n".join(re.sub(r"(`+).*?\1", "", line) for line in _without_fenced_code(text).splitlines())


def _slugify(heading: str) -> str:
    heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
    heading = re.sub(r"<[^>]*>", "", heading)
    heading = re.sub(r"[`*_~]", "", heading).strip().lower()
    slug = "".join(
        char if char == "-" or char.isspace() or unicodedata.category(char)[0] in "LMN" else ""
        for char in heading
    )
    slug = re.sub(r"\s+", "-", slug)
    return unicodedata.normalize("NFC", slug)


def _document_data(path: Path) -> tuple[set[str], list[tuple[int, str]]]:
    text = path.read_text(encoding="utf-8")
    markdown = path.suffix.lower() == ".md"
    content = _without_code(text) if markdown else text
    parser = LinkParser()
    parser.feed(content)

    anchors = parser.anchors
    if markdown:
        used_slugs: dict[str, int] = {}
        for line in _without_fenced_code(text).splitlines():
            match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
            if match:
                slug = _slugify(match.group(1))
                count = used_slugs.get(slug, 0)
                used_slugs[slug] = count + 1
                anchors.add(f"{slug}-{count}" if count else slug)

    references = parser.references
    if markdown:
        link_pattern = re.compile(r"!?\[[^\]]*\]\(\s*(<[^>\n]*>|(?:\\.|[^)\s])*)")
        reference_pattern = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>\n]*>|[^\s]+)")
        for line_number, line in enumerate(content.splitlines(), start=1):
            references.extend(
                (line_number, match.group(1)[1:-1] if match.group(1).startswith("<") else match.group(1))
                for match in link_pattern.finditer(line)
            )
            definition = reference_pattern.match(line)
            if definition:
                target = definition.group(1)
                references.append(
                    (line_number, target[1:-1] if target.startswith("<") else target)
                )
    return anchors, references


def check_links(root: Path) -> list[str]:
    root = root.resolve()
    documents = sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".html"}
        and ".git" not in path.relative_to(root).parts
    )
    document_data = {path: _document_data(path) for path in documents}
    errors: list[str] = []

    for source, (_, references) in document_data.items():
        for line, reference in references:
            reference = reference.strip()
            parsed = urlsplit(reference)
            if parsed.scheme or parsed.netloc:
                continue

            target_path = unquote(parsed.path)
            target = (source.parent / target_path).resolve() if target_path else source.resolve()
            if not target.is_relative_to(root):
                errors.append(f"{source.relative_to(root)}:{line}: link escapes repository: {reference}")
                continue
            if not target.exists():
                errors.append(f"{source.relative_to(root)}:{line}: missing target: {reference}")
                continue
            if parsed.fragment:
                fragment = unquote(parsed.fragment)
                anchors = document_data.get(target, (set(), []))[0]
                if fragment not in anchors:
                    errors.append(f"{source.relative_to(root)}:{line}: missing anchor: {reference}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root (default: current directory)")
    args = parser.parse_args()
    errors = check_links(args.root)
    if errors:
        print("\n".join(errors))
        return 1
    print("Local Markdown and HTML links are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
