#!/usr/bin/env python3
"""Check the docs' navigation front matter.

Fails (exit code 1) if:
  - a .md file has no front matter (Jekyll would publish it as raw text)
  - a page's `parent` doesn't exactly match the title of a top-level page,
    or `parent` + `grand_parent` don't match a section within that product
  - a page with children is missing `has_children: true`
  - two pages under the same parent share a `nav_order` or a title
  - `nav_order` is not a number
  - `keywords` is not a list of words/phrases (or a single string)

Run from the repository root:  python3 .github/scripts/check_nav.py
"""
import os
import sys
from collections import defaultdict

import yaml

SKIP_DIRS = {".git", ".github", "_site", "node_modules", "vendor"}
SKIP_FILES = {"README.md"}


def front_matter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return yaml.safe_load("\n".join(lines[1:i])) or {}
    return None


def main():
    pages = []
    errors = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if not name.endswith(".md") or name in SKIP_FILES:
                continue
            path = os.path.relpath(os.path.join(root, name))
            fm = front_matter(path)
            if fm is None:
                errors.append(f"{path}: no front matter (would be published as raw text)")
                continue
            kw = fm.get("keywords")
            if kw is not None and not (isinstance(kw, str) or
                                       (isinstance(kw, list) and all(isinstance(k, str) for k in kw))):
                errors.append(f"{path}: keywords must be a list of strings, "
                              'e.g. keywords: ["AD CS", "Microsoft CA"]')
            fm["_path"] = path
            pages.append(fm)

    titled = [p for p in pages if p.get("title") is not None and not p.get("nav_exclude")]
    top = {p["title"]: p for p in titled if not p.get("parent")}
    second = {(p["title"], p["parent"]): p for p in titled
              if p.get("parent") and not p.get("grand_parent")}

    siblings = defaultdict(list)
    for p in titled:
        path, parent, grand = p["_path"], p.get("parent"), p.get("grand_parent")
        if parent and grand:
            owner = second.get((parent, grand))
            if owner is None:
                errors.append(f"{path}: no page titled '{parent}' with parent '{grand}'")
        elif parent:
            owner = top.get(parent)
            if owner is None:
                errors.append(f"{path}: no top-level page titled '{parent}' "
                              "(parent must match a title exactly, including case)")
        else:
            owner = None
        if owner is not None and owner.get("has_children") is not True:
            errors.append(f"{owner['_path']}: has child pages but no 'has_children: true'")

        order = p.get("nav_order")
        if order is not None and not isinstance(order, (int, float)):
            errors.append(f"{path}: nav_order '{order}' is not a number")
        siblings[(parent, grand)].append(p)

    for (parent, grand), group in siblings.items():
        where = " > ".join(x for x in (grand, parent) if x) or "top level"
        by_order, by_title = defaultdict(list), defaultdict(list)
        for p in group:
            if isinstance(p.get("nav_order"), (int, float)):
                by_order[p["nav_order"]].append(p["_path"])
            by_title[str(p["title"])].append(p["_path"])
        for order, paths in sorted(by_order.items()):
            if len(paths) > 1:
                errors.append(f"[{where}] nav_order {order} used by: {', '.join(sorted(paths))}")
        for title, paths in by_title.items():
            if len(paths) > 1:
                errors.append(f"[{where}] title '{title}' used by: {', '.join(sorted(paths))}")

    if errors:
        print(f"Navigation check found {len(errors)} problem(s):\n")
        for e in sorted(set(errors)):
            print("  - " + e)
        return 1
    print(f"Navigation check passed ({len(pages)} pages).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
