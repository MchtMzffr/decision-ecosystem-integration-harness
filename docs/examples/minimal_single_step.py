"""Minimal single-step E2E: run_one_step with minimal state/context."""

import sys
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from harness import run_one_step

def main() -> None:
    state = {"mid": 0.5, "imbalance": 0.1, "depth": 50.0, "spread_bps": 10.0}
    context = {}
    now_ms = 1700000000000
    final_decision, packet, report = run_one_step(state, context, now_ms, run_id="minimal", step=0)
    print("Final decision:", final_decision.action.value, "allowed:", final_decision.allowed)
    print("Packet run_id:", packet.run_id, "step:", packet.step, "latency_ms:", packet.latency_ms)
    if report:
        print("Report suite:", report.suite_name)
    else:
        print("Report: (eval-calibration-core not installed)")

if __name__ == "__main__":
    main()
