# Decision Ecosystem — decision-ecosystem-integration-harness
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Integration harness: pipeline (run_one_step) + platform layer (gateway, store, catalog, control, adapters).
Pipeline SSOT: harness.run_one_step. Platform lives under harness.platform (INV-PLAT-ISOLATION-1).
"""

from harness.packet_builder import build_packet_v2
from harness.run_one_step import run_one_step
from harness.platform import (
    clear_memory_buffer,
    clear_ops_override,
    get_context_overrides,
    get_memory_buffer,
    get_ops_state,
    get_policy_defaults,
    merge_context,
    set_green,
    set_ops_state,
    set_red,
    store_save,
)

__version__ = "0.1.0"
__all__ = [
    "run_one_step",
    "build_packet_v2",
    "get_context_overrides",
    "get_policy_defaults",
    "merge_context",
    "get_ops_state",
    "set_ops_state",
    "set_red",
    "set_green",
    "clear_ops_override",
    "store_save",
    "get_memory_buffer",
    "clear_memory_buffer",
    "create_app",
    "serve",
    "__version__",
]


def create_app(*args: object, **kwargs: object):  # noqa: ANN001, ANN002
    """Create FastAPI app; requires pip install .[gateway] (INV-DEPS-OPTIONAL-1). Deprecated (INV-API-SURFACE-1): use harness.platform.gateway.create_app."""
    import warnings

    warnings.warn(
        "from harness import create_app is deprecated (deprecated_in: 0.2, remove_in: 1.0). "
        "Use: from harness.platform.gateway import create_app. See DEPRECATION_POLICY.md (INV-API-SURFACE-1).",
        DeprecationWarning,
        stacklevel=2,
    )
    from harness.platform.gateway import create_app as _create_app

    return _create_app(*args, **kwargs)


def serve(*args: object, **kwargs: object):  # noqa: ANN001, ANN002
    """Run gateway with uvicorn; requires pip install .[gateway] (INV-DEPS-OPTIONAL-1). Deprecated (INV-API-SURFACE-1): use harness.platform.gateway.serve."""
    import warnings

    warnings.warn(
        "from harness import serve is deprecated (deprecated_in: 0.2, remove_in: 1.0). "
        "Use: from harness.platform.gateway import serve (or python -m harness). See DEPRECATION_POLICY.md (INV-API-SURFACE-1).",
        DeprecationWarning,
        stacklevel=2,
    )
    from harness.platform.gateway import serve as _serve

    return _serve(*args, **kwargs)
