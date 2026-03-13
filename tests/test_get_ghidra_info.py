"""Tests for scripts/get_ghidra_info.py."""

from __future__ import annotations

import get_ghidra_info
import pytest


class TestTagRegex:
    @pytest.mark.parametrize(
        ("tag", "expected_version"),
        [
            ("Ghidra_12.0.3_build", "12.0.3"),
            ("Ghidra_11.2_build", "11.2"),
            ("Ghidra_10.0.0_build", "10.0.0"),
        ],
    )
    def test_valid_tags(self, tag: str, expected_version: str) -> None:
        m = get_ghidra_info._TAG_RE.match(tag)
        assert m is not None
        assert m.group(1) == expected_version

    @pytest.mark.parametrize(
        "tag",
        [
            "unknown",
            "v12.0.3",
            "Ghidra_12.0.3",
            "ghidra_12.0.3_build",
            "",
        ],
    )
    def test_invalid_tags(self, tag: str) -> None:
        assert get_ghidra_info._TAG_RE.match(tag) is None


class TestGetVersion:
    def test_valid_tag(self) -> None:
        assert get_ghidra_info.get_version("Ghidra_12.0.3_build") == "12.0.3"

    def test_unknown_tag_returns_fallback(self) -> None:
        assert get_ghidra_info.get_version("unknown") == "0.0.0.dev0"

    def test_none_tag_calls_get_tag(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(get_ghidra_info, "get_tag", lambda: "Ghidra_9.1.2_build")
        assert get_ghidra_info.get_version() == "9.1.2"
