# Decision Ecosystem — decision-ecosystem-integration-harness
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Integration harness: single-step propose → ops → modulate → PacketV2 → report."""

from harness.packet_builder import build_packet_v2
from harness.run_one_step import run_one_step

__version__ = "0.1.0"
__all__ = ["run_one_step", "build_packet_v2", "__version__"]
