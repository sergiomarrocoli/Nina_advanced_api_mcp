"""Tool profiles: a named subset of the tools, chosen when the server starts."""
import asyncio
import re
from pathlib import Path

import pytest

import nina_advanced_mcp as m


@pytest.fixture(autouse=True)
def full_list_afterwards():
    yield
    m.apply_profile("full")


def listed():
    return {tool.name for tool in asyncio.run(m.mcp.list_tools())}


def test_the_full_profile_lists_every_tool():
    m.apply_profile("full")
    assert len(listed()) == 104


def test_core_lists_only_the_core_tools():
    m.apply_profile("core")
    assert listed() == m.PROFILES["core"]


def test_mono_is_core_plus_the_filter_wheel():
    m.apply_profile("mono")
    assert listed() == m.PROFILES["core"] | {"nina_get_filterwheel_info", "nina_get_filter_info", "nina_change_filter"}


def test_every_profile_tool_exists():
    m.apply_profile("full")
    assert (m.PROFILES["core"] | m.PROFILES["mono"]) <= listed()


def test_a_profile_leaves_out_tools_the_model_does_not_need():
    m.apply_profile("core")
    assert "nina_slew_mount" in listed() and "nina_get_plugins" not in listed()


def test_extra_tools_added_after_the_server_stay_in_the_profile():
    m.apply_profile("core", extra={"nina_get_plugins"})
    assert "nina_get_plugins" in listed()


def test_an_unknown_profile_is_refused_with_the_valid_ones():
    with pytest.raises(ValueError, match="core.*full.*mono"):
        m.apply_profile("tiny")


def test_a_hidden_tool_cannot_be_called():
    m.apply_profile("core")
    with pytest.raises(Exception, match="nina_get_plugins"):
        asyncio.run(m.mcp.call_tool("nina_get_plugins", {}))


def test_tools_md_agrees_with_the_profiles():
    rows = re.findall(r"\| `(\w+)` \| (core|mono) \|", (Path(__file__).parent.parent / "docs" / "tools.md").read_text())
    assert {n for n, p in rows if p == "core"} == m.PROFILES["core"]
    assert {n for n, p in rows if p == "mono"} == m.PROFILES["mono"]
