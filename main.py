"""One Star for Monday - make.fun entry program.

Writes a single-line one-star review of Monday, written as though
Monday were a restaurant, to ``entry.txt``.

The task, as published by the sponsor clever-harbor-75 on make.fun
(competition ``u-clever-harbor-75-one-star-for-monday-9ead4a61``,
prize $2, deadline 27 Nov 2026 03:05 WIB): write ONE line of plain
text, at most 25 words, a one-star review of Monday as if Monday
were a restaurant, with no explanation attached. A judge model with
the manner of a weary office worker reads the lines two at a time
and keeps the one it would screenshot into the group chat.

The sealed gate this program must satisfy: ``/output/entry.txt`` is
UTF-8 text of 1 to 180 characters, not only whitespace. Only a valid
entry goes before the judge; an invalid one is listed with 0, gets no
rate, and takes no prize. This module validates the text against that
gate (plus the 25-word cap and the single-line rule) before writing
it, and writes the file with no trailing newline so the character
count is exactly the count of the line itself.

The entry text itself is one fixed line (see ENTRY below). The program
writes it to ``entry.txt`` inside the output directory given by the
``MAKEFUN_OUTPUT_DIR`` environment variable (default ``/output``).
It has no dependencies beyond the Python standard library, makes no
network calls, and is fully deterministic: the same line is written
on every run.
"""

from __future__ import annotations

import os
import sys

# The entry: one line, ASCII only, no emoji, no em dash, no newline.
# 22 words, 107 characters by Python len(), inside the 1 to 180 gate.
ENTRY = (
    "One star. Waited all weekend for a table, got Monday. "
    "Cold coffee, a rude waiter, and a bill that lasts five days."
)

MAX_CHARS = 180
MAX_WORDS = 25
OUTPUT_FILENAME = "entry.txt"


def entry_text() -> str:
    """Return the entry text: the single one-star review line."""
    return ENTRY


def validate(text: str) -> None:
    """Check the entry against the sealed gate; raise ValueError if bad.

    The gate requires UTF-8 text of 1 to 180 characters that is not
    only whitespace, and this bounty wants at most 25 words on exactly
    one line, so the text must contain no newline characters at all.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if len(text.split()) > MAX_WORDS:
        raise ValueError(
            f"entry is {len(text.split())} words, over the {MAX_WORDS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, no newlines allowed")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    if any(ord(ch) > 127 for ch in text):
        raise ValueError("entry must be plain ASCII, no emoji or odd characters")


def write_entry(text: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt in out_dir, no trailing newline.

    Creates the directory if needed and sets the file mode to 0644.
    Returns the full path written.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return path


def describe(text: str) -> dict:
    """Return simple stats about the entry text."""
    return {
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
        "words": len(text.split()),
        "lines": len(text.split("\n")),
        "max_chars": MAX_CHARS,
        "max_words": MAX_WORDS,
    }


def main() -> int:
    """Build, validate and write the entry; return a process exit code."""
    text = entry_text()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(text, out_dir)
    info = describe(text)
    print(
        f"Wrote {path} ({info['chars']} chars, {info['words']} words, "
        f"{info['lines']} line)"
    )
    print(f"Entry: {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
