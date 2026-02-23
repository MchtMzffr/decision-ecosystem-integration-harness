# Decision Ecosystem - decision-ecosystem-integration-harness
# Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Run gateway: python -m harness [--host 0.0.0.0] [--port 8000] [--store file] [--store-path path]."""

from __future__ import annotations

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Decision Ecosystem Gateway")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    parser.add_argument("--port", type=int, default=8000, help="Bind port")
    parser.add_argument(
        "--store",
        default="memory",
        choices=("memory", "file", "off"),
        help="Store backend",
    )
    parser.add_argument(
        "--store-path", default=None, help="Store path (for file backend)"
    )
    args = parser.parse_args()
    store_backend = "off" if args.store == "off" else args.store
    try:
        from harness.platform.gateway import serve

        serve(
            host=args.host,
            port=args.port,
            store_backend=store_backend,
            store_path=args.store_path,
        )
    except ImportError:
        print(
            "Gateway requires [gateway] extra: pip install decision-ecosystem-integration-harness[gateway]",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
