# Check profile SVGs against GitHub camo sanitizer constraints.
# Run: python assets/profile/check_sanitizer.py
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["hero-dark", "hero-light", "hero-static", "typing-dark", "typing-light"]

PATTERNS = [
    (re.compile(r"<script", re.I), "script tag"),
    (re.compile(r"foreignObject", re.I), "foreignObject"),
    (re.compile(r"href\s*=\s*[\"']https?://", re.I), "external href"),
    (re.compile(r"url\((?![#'\" ])", re.I), "non-local url()"),
    (re.compile(r"<image", re.I), "image tag"),
]


def main() -> None:
    clean = True
    for f in FILES:
        with open(os.path.join(HERE, f + ".svg"), encoding="utf-8") as fh:
            svg = fh.read()
        problems = [name for pat, name in PATTERNS if pat.search(svg)]
        if problems:
            clean = False
            print(f, "-> FAIL:", problems)
        else:
            print(f, "-> clean")
    raise SystemExit(0 if clean else 1)


if __name__ == "__main__":
    main()
