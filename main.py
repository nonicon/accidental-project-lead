#!/usr/bin/env python3
"""Accidental Project Lead — entry for make.fun's
"One-Line Office Joke: 24-Hour Sprint" bounty.

Writes one line (a joke about office life) to /output/entry.txt.
Deterministic, stdlib only.
"""

import os
import sys

ENTRY = (
    "I replied \"sounds good\" to a 47-email thread "
    "and somehow ended up leading the project."
)


def output_path() -> str:
    """Where the entry goes: MAKEFUN_OUTPUT_DIR first, then legacy
    OUTPUT_DIR, then the harness default /output."""
    base = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("OUTPUT_DIR") or "/output"
    return os.path.join(base, "entry.txt")


def validate_entry(text: str) -> str:
    """Enforce the kit gate from RULES.txt: UTF-8 text of 1-200
    characters, a single line, not only whitespace."""
    text.encode("utf-8")  # must be valid UTF-8
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry is {len(text)} chars, gate requires 1-200")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main() -> int:
    text = validate_entry(ENTRY.strip())
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Round-trip: the written file must hold exactly the validated entry.
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != text:
            raise RuntimeError("round-trip check failed: written entry differs")
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
