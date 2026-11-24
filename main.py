#!/usr/bin/env python3
"""Dad Joke Showdown entry — writes the joke to /output/entry.txt.

The joke (134 characters, one dad joke, told the way a father tells it):

    My kids asked why the moon is always broke. I said, "It goes through
    too many phases — and quarters are the only change it ever gets."

Why this one: a triple pun that lands on the first read — the moon's
*phases*, its *quarters*, and *change* as both loose coins and personal
growth. Kids asking dad a question is the classic dinner-table setup,
the punchline ("change") arrives in the last word, and the groan is
built in: the moon is broke precisely because of the things that define
it. Fresh wording on a traditional structure, tight enough that every
word earns its place.

The program copies joke.txt verbatim to the output as entry.txt, after
checking it against the gate: UTF-8 text of 1 to 200 characters, not
only white space. Standard library only, no network, deterministic.
"""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOKE_FILE = HERE / "joke.txt"


def load_joke() -> str:
    raw = JOKE_FILE.read_bytes()
    # Strict decode: a joke file that is not clean UTF-8 fails here,
    # before anything is written, rather than at the gate.
    text = raw.decode("utf-8", errors="strict")
    if not (1 <= len(text) <= 200):
        raise ValueError(f"joke must be 1-200 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("joke must not be only white space")
    if text != text.strip():
        raise ValueError("joke must not carry leading/trailing white space")
    return text


def main() -> int:
    text = load_joke()
    payload = text.encode("utf-8")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    # Atomic write: a reader (or the gate) never sees a partial file.
    tmp = out_dir / ".entry.txt.tmp"
    tmp.write_bytes(payload)
    os.replace(tmp, target)
    # Round-trip check: what landed on disk is exactly the joke, byte
    # for byte, so the two harness runs can only ever agree.
    if target.read_bytes() != payload:
        raise IOError("entry.txt on disk does not match the joke bytes")
    print(f"wrote {target} ({len(payload)} bytes, {len(text)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
