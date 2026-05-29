"""Tests for get_eco_home() profile-mode fallback warning.

Regression test for https://github.com/NousResearch/hermes-agent-agent-agent/issues/18594.

When HERMES_HOME is unset but an active_profile file indicates a non-default
profile is active, get_eco_home() should:
  1. STILL return ~/.eco (raising would brick 30+ module-level callers)
  2. Emit a loud one-shot warning to stderr so operators can diagnose
     cross-profile data contamination after the fact.

The warning goes to stderr directly (not through logging) because this
function is called at module-import time from 30+ sites, often before the
logging subsystem has been configured.
"""

from pathlib import Path

import pytest


@pytest.fixture
def fresh_constants(monkeypatch, tmp_path):
    """Import eco_constants fresh and reset the one-shot warn flag."""
    import importlib
    import eco_constants
    importlib.reload(eco_constants)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.delenv("HERMES_HOME", raising=False)
    return eco_constants


class TestGetECOHomeProfileWarning:
    def test_classic_mode_no_active_profile_no_warning(
        self, fresh_constants, tmp_path, capsys
    ):
        """Classic mode: no active_profile file → silent, returns ~/.eco."""
        result = fresh_constants.get_eco_home()
        assert result == tmp_path / ".eco"
        assert "HERMES_HOME fallback" not in capsys.readouterr().err

    def test_default_active_profile_no_warning(
        self, fresh_constants, tmp_path, capsys
    ):
        """active_profile=default → still no warning, returns ~/.eco."""
        eco_dir = tmp_path / ".eco"
        eco_dir.mkdir()
        (eco_dir / "active_profile").write_text("default\n")
        result = fresh_constants.get_eco_home()
        assert result == tmp_path / ".eco"
        assert "HERMES_HOME fallback" not in capsys.readouterr().err

    def test_named_profile_unset_home_warns_once(
        self, fresh_constants, tmp_path, capsys
    ):
        """active_profile=coder + HERMES_HOME unset → warn loudly, still return fallback."""
        eco_dir = tmp_path / ".eco"
        eco_dir.mkdir()
        (eco_dir / "active_profile").write_text("coder\n")

        result = fresh_constants.get_eco_home()

        # 1. Still returns the fallback — no import-time crash
        assert result == tmp_path / ".eco"
        # 2. Stderr got the warning exactly once
        err = capsys.readouterr().err
        assert err.count("HERMES_HOME fallback") == 1
        assert "'coder'" in err
        assert "#18594" in err

        # 3. One-shot: second and third calls don't re-warn
        fresh_constants.get_eco_home()
        fresh_constants.get_eco_home()
        err2 = capsys.readouterr().err
        assert "HERMES_HOME fallback" not in err2

    def test_eco_home_set_suppresses_warning(
        self, fresh_constants, tmp_path, capsys, monkeypatch
    ):
        """Even if active_profile is 'coder', setting HERMES_HOME suppresses warning."""
        profile_dir = tmp_path / ".eco" / "profiles" / "coder"
        profile_dir.mkdir(parents=True)
        (tmp_path / ".eco" / "active_profile").write_text("coder\n")
        monkeypatch.setenv("HERMES_HOME", str(profile_dir))

        result = fresh_constants.get_eco_home()

        assert result == profile_dir
        assert "HERMES_HOME fallback" not in capsys.readouterr().err

    def test_unreadable_active_profile_no_crash(
        self, fresh_constants, tmp_path, capsys
    ):
        """active_profile that can't be decoded → fall through silently."""
        eco_dir = tmp_path / ".eco"
        eco_dir.mkdir()
        # Write bytes that aren't valid utf-8
        (eco_dir / "active_profile").write_bytes(b"\xff\xfe\x00\x00")

        result = fresh_constants.get_eco_home()

        assert result == tmp_path / ".eco"
        # Shouldn't crash; shouldn't warn either (can't tell what profile was intended)
        assert "HERMES_HOME fallback" not in capsys.readouterr().err

    def test_empty_active_profile_no_warning(
        self, fresh_constants, tmp_path, capsys
    ):
        """Empty active_profile file → treated as default, no warning."""
        eco_dir = tmp_path / ".eco"
        eco_dir.mkdir()
        (eco_dir / "active_profile").write_text("")

        result = fresh_constants.get_eco_home()

        assert result == tmp_path / ".eco"
        assert "HERMES_HOME fallback" not in capsys.readouterr().err
