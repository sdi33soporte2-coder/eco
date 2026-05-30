"""Tests for the Nous-ECO-3/4 non-agentic warning detector.

Prior to this check, the warning fired on any model whose name contained
``"eco"`` anywhere (case-insensitive). That false-positived on unrelated
local Modelfiles such as ``eco-brain:qwen3-14b-ctx16k`` — a tool-capable
Qwen3 wrapper that happens to live under the "eco" tag namespace.

``is_nous_eco_non_agentic`` should only match the actual Nous Research
ECO-3 / ECO-4 chat family.
"""

from __future__ import annotations

import pytest

from eco_cli.model_switch import (
    _ECO_MODEL_WARNING,
    _check_eco_model_warning,
    is_nous_eco_non_agentic,
)


@pytest.mark.parametrize(
    "model_name",
    [
        "NousResearch/ECO-3-Llama-3.1-70B",
        "NousResearch/ECO-3-Llama-3.1-405B",
        "eco-3",
        "ECO-3",
        "eco-4",
        "eco-4-405b",
        "eco_4_70b",
        "openrouter/hermes3:70b",
        "openrouter/nousresearch/eco-4-405b",
        "NousResearch/Hermes3",
        "eco-3.1",
    ],
)
def test_matches_real_nous_eco_chat_models(model_name: str) -> None:
    assert is_nous_eco_non_agentic(model_name), (
        f"expected {model_name!r} to be flagged as Nous ECO 3/4"
    )
    assert _check_eco_model_warning(model_name) == _ECO_MODEL_WARNING


@pytest.mark.parametrize(
    "model_name",
    [
        # Kyle's local Modelfile — qwen3:14b under a custom tag
        "eco-brain:qwen3-14b-ctx16k",
        "eco-brain:qwen3-14b-ctx32k",
        "eco-honcho:qwen3-8b-ctx8k",
        # Plain unrelated models
        "qwen3:14b",
        "qwen3-coder:30b",
        "qwen2.5:14b",
        "claude-opus-4-6",
        "anthropic/claude-sonnet-4.5",
        "gpt-5",
        "openai/gpt-4o",
        "google/gemini-2.5-flash",
        "deepseek-chat",
        # Non-chat ECO models we don't warn about
        "eco-llm-2",
        "hermes2-pro",
        "nous-eco-2-mistral",
        # Edge cases
        "",
        "eco",  # bare "eco" isn't the 3/4 family
        "eco-brain",
        "brain-eco-3-impostor",  # "3" not preceded by /: boundary
    ],
)
def test_does_not_match_unrelated_models(model_name: str) -> None:
    assert not is_nous_eco_non_agentic(model_name), (
        f"expected {model_name!r} NOT to be flagged as Nous ECO 3/4"
    )
    assert _check_eco_model_warning(model_name) == ""


def test_none_like_inputs_are_safe() -> None:
    assert is_nous_eco_non_agentic("") is False
    # Defensive: the helper shouldn't crash on None-ish falsy input either.
    assert _check_eco_model_warning("") == ""
