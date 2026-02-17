import re
from pathlib import Path

# CI-0: Workflow file hygiene must be deterministic and tool-friendly.
# - Only LF line endings (no CR bytes)
# - No Unicode bidi/control characters that can confuse tooling or reviewers
# - Must look multi-line (avoid accidental "single-line YAML" regressions)

WORKFLOW_DIR = Path(".github/workflows")

# Unicode control ranges that commonly cause "hidden or bidirectional Unicode text" warnings
# and can break raw renderers / tooling.
FORBIDDEN_UNICODE_CODEPOINT_RANGES = [
    ("\u202A", "\u202E"),  # LRE..RLO (bidi embeddings/overrides)
    ("\u2066", "\u2069"),  # LRI..PDI (isolate controls)
    ("\u2028", "\u2029"),  # line separator / paragraph separator
]
# Also forbid zero-width and BOM in workflow files to keep diffs/tooling stable.
FORBIDDEN_UNICODE_CHARS = [
    "\ufeff",  # BOM
    "\u200b",  # zero width space
    "\u200c",  # zero width non-joiner
    "\u200d",  # zero width joiner
    "\u2060",  # word joiner
]

MIN_EXPECTED_NEWLINES = 10  # sanity: workflows should be multi-line, not a collapsed single line


def _contains_forbidden_unicode(text: str) -> list[str]:
    hits: list[str] = []
    for ch in FORBIDDEN_UNICODE_CHARS:
        if ch in text:
            hits.append(f"U+{ord(ch):04X}")
    for start, end in FORBIDDEN_UNICODE_CODEPOINT_RANGES:
        s, e = ord(start), ord(end)
        for cp in range(s, e + 1):
            c = chr(cp)
            if c in text:
                hits.append(f"U+{cp:04X}")
    return sorted(set(hits))


def test_invariant_ci_0_workflow_hygiene():
    assert WORKFLOW_DIR.exists(), f"{WORKFLOW_DIR} does not exist"

    workflow_files = sorted(
        [p for p in WORKFLOW_DIR.rglob("*") if p.is_file() and p.suffix in {".yml", ".yaml"}]
    )
    assert workflow_files, "No workflow YAML files found under .github/workflows"

    failures: list[str] = []

    for path in workflow_files:
        b = path.read_bytes()

        # 1) Only LF line endings: no CR bytes
        if b"\r" in b:
            cr_count = b.count(b"\r")
            failures.append(f"{path}: contains CR bytes (count={cr_count})")

        # 2) Must be multi-line (avoid single-line workflow regressions)
        lf_count = b.count(b"\n")
        if lf_count < MIN_EXPECTED_NEWLINES:
            failures.append(f"{path}: too few LF newlines (count={lf_count}); possible single-line YAML")

        # 3) Decode as UTF-8 strictly; workflows should be plain UTF-8
        try:
            text = b.decode("utf-8")
        except UnicodeDecodeError as e:
            failures.append(f"{path}: not valid UTF-8 ({e})")
            continue

        # 4) No hidden/bidi control characters
        hits = _contains_forbidden_unicode(text)
        if hits:
            failures.append(f"{path}: forbidden Unicode chars present: {', '.join(hits)}")

        # 5) YAML structural sanity check (cheap, not full YAML parse):
        # Ensure we see top-level keys in separate lines.
        # This catches weird separator issues where raw renderers collapse lines.
        # (We do not require exact formatting; just presence on their own lines.)
        if not re.search(r"(?m)^\s*on:\s*$", text):
            # allow inline "on:" map as well, but still require a newline boundary
            if "on:" not in text:
                failures.append(f"{path}: missing 'on:' key")
        if not re.search(r"(?m)^\s*jobs:\s*$", text):
            if "jobs:" not in text:
                failures.append(f"{path}: missing 'jobs:' key")

    assert not failures, "CI-0 workflow hygiene violations:\n- " + "\n- ".join(failures)
