from __future__ import annotations

from pathlib import Path

CI_PATH = Path(".github/workflows/ci.yml")

# Canonical, deterministic workflow content (ASCII + LF only).
LINES = [
    "name: CI",
    "",
    "on:",
    "  push:",
    "    branches: [main, master]",
    "  pull_request:",
    "    branches: [main, master]",
    "",
    "jobs:",
    "  test:",
    "    runs-on: ubuntu-latest",
    "    strategy:",
    "      matrix:",
    '        python-version: ["3.11", "3.12"]',
    "",
    "    steps:",
    "      - name: Checkout",
    "        uses: actions/checkout@v4",
    "",
    "      - name: Set up Python",
    "        uses: actions/setup-python@v5",
    "        with:",
    "          python-version: ${{ matrix.python-version }}",
    "",
    "      - name: Install test tooling",
    "        run: pip install -U pip pytest",
    "",
    "      - name: Install decision-schema",
    "        run: |",
    '          pip install "decision-schema>=0.2,<0.3" || pip install "git+https://github.com/MchtMzffr/decision-schema.git"',
    "",
    "      - name: Install harness",
    "        run: pip install -e .",
    "",
    "      - name: Run tests",
    "        run: pytest tests/ -v",
    "",
]

FORBIDDEN_UNICODE_RANGES = [
    (0x202A, 0x202E),  # bidi embeddings/overrides
    (0x2066, 0x2069),  # bidi isolates
    (0x2028, 0x2029),  # line/paragraph separators
]
FORBIDDEN_UNICODE_CHARS = {0xFEFF, 0x200B, 0x200C, 0x200D, 0x2060}


def _contains_forbidden_unicode(text: str) -> list[str]:
    hits = []
    for ch in text:
        cp = ord(ch)
        if cp in FORBIDDEN_UNICODE_CHARS:
            hits.append(f"U+{cp:04X}")
        for a, b in FORBIDDEN_UNICODE_RANGES:
            if a <= cp <= b:
                hits.append(f"U+{cp:04X}")
    return sorted(set(hits))


def main() -> int:
    CI_PATH.parent.mkdir(parents=True, exist_ok=True)

    content = ("\n".join(LINES)).encode("utf-8")

    # Byte-level hygiene checks BEFORE writing (defensive)
    assert b"\r" not in content, "Generated content must not contain CR"
    lf = content.count(b"\n")
    assert lf >= 10, f"Generated content must be multi-line; LF={lf}"
    text = content.decode("utf-8")
    hits = _contains_forbidden_unicode(text)
    assert not hits, f"Generated content contains forbidden Unicode: {hits}"

    old = CI_PATH.read_bytes() if CI_PATH.exists() else b""
    if old != content:
        CI_PATH.write_bytes(content)
        print(f"[rewrite_ci_yml] wrote {CI_PATH} (bytes changed)")
    else:
        print(f"[rewrite_ci_yml] no change (already canonical)")

    # Post-write verify (what CI-0 will enforce)
    new = CI_PATH.read_bytes()
    print(f"[rewrite_ci_yml] CR={new.count(b'\r')} LF={new.count(b'\n')} bytes={len(new)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
