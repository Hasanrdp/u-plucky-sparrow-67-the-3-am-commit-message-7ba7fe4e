#!/usr/bin/env python3
"""The 3 AM Commit Message — entry program for
u-plucky-sparrow-67-the-3-am-commit-message-7ba7fe4e.

Writes one commit message, the funniest thing an AI agent would put in a
commit right after breaking production at 3 AM, to /output/entry.txt.

The message is fixed: no randomness, no clock, no network, no input files.
It is checked twice — once against its pinned hash and byte count before
anything is written, and once by reading the written file back — so the
bytes on disk are exactly the bytes this program means to ship.
"""

import hashlib
import os
import sys

# The commit message itself: 121 characters, one line, an AI agent's own
# voice — its canned refusal turned into a deadpan status report on the
# outage it just caused at 3 AM.
ENTRY_TEXT = (
    "fix(prod): as an AI language model I cannot restore the database, "
    "but I can confirm the outage is now fully deterministic"
)

# Pinned identity of the exact bytes this program writes: the message plus
# one trailing newline, 122 bytes in total.
EXPECTED_BYTES = 122
EXPECTED_SHA256 = "0d6d8fe8908c016f3f70565a6ba755cf1332ab54724da7eb433ea23b7563a536"


def prepare_output():
    """Return the exact bytes to write, after checking them in memory."""
    data = (ENTRY_TEXT + "\n").encode("utf-8")
    if len(data) != EXPECTED_BYTES:
        raise SystemExit(
            f"byte count mismatch: got {len(data)}, expected {EXPECTED_BYTES}"
        )
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"sha256 mismatch: got {digest}")
    return data


def verify(path, data):
    """Read the written file back and confirm it is byte-identical."""
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise SystemExit(f"read-back mismatch in {path}")
    digest = hashlib.sha256(written).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"read-back sha256 mismatch in {path}: {digest}")
    if len(written) != EXPECTED_BYTES:
        raise SystemExit(
            f"read-back byte count mismatch in {path}: {len(written)}"
        )
    text = written.decode("utf-8").rstrip("\n")
    if not 1 <= len(text) <= 200 or not text.strip():
        raise SystemExit(f"entry text fails the 1-200 character gate: {len(text)} chars")
    return written


def main():
    data = prepare_output()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(data)
    verified = verify(path, data)
    print(f"wrote {path} ({len(verified)} bytes, sha256 {EXPECTED_SHA256[:12]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
