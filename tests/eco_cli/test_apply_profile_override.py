"""Regression tests for _apply_profile_override ECO_HOME guard (issue #22502).

When ECO_HOME is set to the eco root (e.g. systemd hardcodes
ECO_HOME=/root/.eco), _apply_profile_override must still read
active_profile and update ECO_HOME to the profile directory.

When ECO_HOME is already a profile directory (.../profiles/<name>),
_apply_profile_override must trust it and return without re-reading
active_profile (child-process inheritance contract).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path



def _run_apply_profile_override(
    tmp_path, monkeypatch, *, eco_home: str | None, active_profile: str | None,
    argv: list[str] | None = None,
):
    """Run _apply_profile_override in isolation.

    Returns the value of os.environ["ECO_HOME"] after the call,
    or None if unset.
    """
    eco_root = tmp_path / ".eco"
    eco_root.mkdir(parents=True, exist_ok=True)

    if active_profile is not None:
        (eco_root / "active_profile").write_text(active_profile)

    if active_profile and active_profile != "default":
        (eco_root / "profiles" / active_profile).mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    if eco_home is not None:
        monkeypatch.setenv("ECO_HOME", eco_home)
    else:
        monkeypatch.delenv("ECO_HOME", raising=False)

    monkeypatch.setattr(sys, "argv", argv or ["eco", "gateway", "start"])

    from eco_cli.main import _apply_profile_override
    _apply_profile_override()

    return os.environ.get("ECO_HOME")


class TestApplyProfileOverrideECOHomeGuard:
    """Regression guard for issue #22502.

    Verifies that ECO_HOME pointing to the eco root does NOT suppress
    the active_profile check, while ECO_HOME already pointing to a
    profile directory IS trusted as-is.
    """

    def test_eco_home_at_root_with_active_profile_is_redirected(
        self, tmp_path, monkeypatch
    ):
        """ECO_HOME=/root/.eco + active_profile=coder must redirect
        ECO_HOME to .../profiles/coder.

        Bug scenario from #22502: systemd sets ECO_HOME to the eco root
        and the user switches to a profile via `eco profile use`.
        Before the fix, the guard returned early and active_profile was ignored.
        """
        eco_root = tmp_path / ".eco"
        eco_root.mkdir(parents=True, exist_ok=True)

        result = _run_apply_profile_override(
            tmp_path,
            monkeypatch,
            eco_home=str(eco_root),
            active_profile="coder",
        )

        assert result is not None, "ECO_HOME must be set after profile redirect"
        assert "profiles" in result, (
            f"Expected ECO_HOME to point into profiles/ dir, got: {result!r}"
        )
        assert result.endswith("coder"), (
            f"Expected ECO_HOME to end with 'coder', got: {result!r}"
        )

    def test_eco_home_already_profile_dir_is_trusted(self, tmp_path, monkeypatch):
        """ECO_HOME=.../profiles/coder must not be overridden even when
        active_profile says something different.

        Preserves the child-process inheritance contract: a subprocess spawned
        with ECO_HOME already set to a specific profile must stay in that
        profile.
        """
        eco_root = tmp_path / ".eco"
        profile_dir = eco_root / "profiles" / "coder"
        profile_dir.mkdir(parents=True, exist_ok=True)

        (eco_root / "active_profile").write_text("other")

        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        monkeypatch.setenv("ECO_HOME", str(profile_dir))
        monkeypatch.setattr(sys, "argv", ["eco", "gateway", "start"])

        from eco_cli.main import _apply_profile_override
        _apply_profile_override()

        assert os.environ.get("ECO_HOME") == str(profile_dir), (
            "ECO_HOME must remain unchanged when already pointing to a profile dir"
        )

    def test_eco_home_unset_reads_active_profile(self, tmp_path, monkeypatch):
        """Classic case: ECO_HOME unset + active_profile=coder must set
        ECO_HOME to the profile directory (existing behaviour must not regress).
        """
        result = _run_apply_profile_override(
            tmp_path,
            monkeypatch,
            eco_home=None,
            active_profile="coder",
        )

        assert result is not None
        assert "coder" in result

    def test_eco_home_unset_default_profile_no_redirect(self, tmp_path, monkeypatch):
        """active_profile=default must not redirect ECO_HOME."""
        eco_root = tmp_path / ".eco"
        eco_root.mkdir(parents=True, exist_ok=True)

        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        monkeypatch.delenv("ECO_HOME", raising=False)
        monkeypatch.setattr(sys, "argv", ["eco", "gateway", "start"])
        (eco_root / "active_profile").write_text("default")

        from eco_cli.main import _apply_profile_override
        _apply_profile_override()

        assert os.environ.get("ECO_HOME") is None
