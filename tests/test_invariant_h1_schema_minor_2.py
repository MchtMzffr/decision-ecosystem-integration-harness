"""INVARIANT H1: Schema minor=2 compat gate (decision-schema 0.2.x)."""

import pytest


def test_schema_version_minor_2() -> None:
    """decision-schema must be 0.2.x for harness contract."""
    from decision_schema import __version__
    from decision_schema.compat import is_compatible
    assert is_compatible(__version__, expected_major=0, min_minor=2, max_minor=2), (
        f"Harness expects decision-schema 0.2.x, got {__version__}"
    )


def test_eval_calibration_contract_check() -> None:
    """If eval-calibration-core is present, its expected_minor=2 check aligns with H1."""
    pytest.importorskip("eval_calibration_core")
    from eval_calibration_core.contracts import check_expected_minor_range
    ok, details = check_expected_minor_range(expected_major=0, min_minor=2, max_minor=2)
    assert ok, details
