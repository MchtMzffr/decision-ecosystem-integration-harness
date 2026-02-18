import pytest

pytestmark = pytest.mark.fullstack


def test_fullstack_run_one_step_produces_report_and_contract_ok() -> None:
    from harness import run_one_step

    state = {
        "signal_0": 0.5,
        "signal_1": 0.0,
        "state_scalar_a": 0.0,
    }
    context = {}
    now_ms = 1700000000000

    final_decision, packet, report = run_one_step(state, context, now_ms, run_id="fullstack", step=0)

    assert final_decision is not None
    assert packet is not None
    assert report is not None, "full-stack job must have evaluation-calibration-core installed"

    assert hasattr(report, "contract_matrix_check")
    assert report.contract_matrix_check is not None
    assert report.contract_matrix_check.get("compatible") is True
