"""Resolve ECO_HOME for standalone skill scripts.

Skill scripts may run outside the ECO process (e.g. system Python,
nix env, CI) where ``eco_constants`` is not importable.  This module
provides the same ``get_eco_home()`` and ``display_eco_home()``
contracts as ``eco_constants`` without requiring it on ``sys.path``.

When ``eco_constants`` IS available it is used directly so that any
future enhancements (profile resolution, Docker detection, etc.) are
picked up automatically.  The fallback path replicates the core logic
from ``eco_constants.py`` using only the stdlib.

All scripts under ``google-workspace/scripts/`` should import from here
instead of duplicating the ``ECO_HOME = Path(os.getenv(...))`` pattern.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from eco_constants import display_eco_home as display_eco_home
    from eco_constants import get_eco_home as get_eco_home
except (ModuleNotFoundError, ImportError):

    def get_eco_home() -> Path:
        """Return the ECO home directory (default: ~/.eco).

        Mirrors ``eco_constants.get_eco_home()``."""
        val = os.environ.get("ECO_HOME", "").strip()
        return Path(val) if val else Path.home() / ".eco"

    def display_eco_home() -> str:
        """Return a user-friendly ``~/``-shortened display string.

        Mirrors ``eco_constants.display_eco_home()``."""
        home = get_eco_home()
        try:
            return "~/" + str(home.relative_to(Path.home()))
        except ValueError:
            return str(home)
