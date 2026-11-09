"""A trimmed profile lists two extra tools that find and enable what it hid."""
import asyncio
import json

import pytest
from fastmcp import Client

import nina_advanced_mcp as m


@pytest.fixture(autouse=True)
def full_list_afterwards():
    yield
    m.apply_profile("full")


def run(call):
    async def go():
        async with Client(m.mcp) as client:
            return await call(client)
    return asyncio.run(go())


async def names(client):
    return {t.name for t in await client.list_tools()}


async def tool(client, name, args=None):
    result = await client.call_tool(name, args or {}, raise_on_error=False)
    return json.loads(result.content[0].text)


def test_a_trimmed_profile_lists_the_two_discovery_tools_and_full_does_not():
    m.apply_profile("core")
    assert set(m.DISCOVERY_TOOLS) <= run(names)
    m.apply_profile("full")
    assert not set(m.DISCOVERY_TOOLS) & run(names)


def test_groups_cover_every_tool_exactly_once():
    m.apply_profile("full")
    grouped = [name for _, tools in m.GROUPS.values() for name in tools]
    assert len(grouped) == len(set(grouped))
    assert set(grouped) == run(names) - set(m.DISCOVERY_TOOLS)


def test_list_tool_groups_names_each_group_and_its_tools():
    m.apply_profile("core")
    reply = run(lambda c: tool(c, "nina_list_tool_groups"))
    groups = {g["group"]: g["tools"] for g in reply["Groups"]}
    assert "nina_open_dome_shutter" in groups["dome"] and set(groups) == set(m.GROUPS)


def test_enabling_a_group_makes_its_tools_appear_in_this_session():
    m.apply_profile("core")

    async def call(client):
        before = await names(client)
        reply = await tool(client, "nina_enable_tools", {"group": "dome"})
        return before, reply, await names(client)

    before, reply, after = run(call)
    assert "nina_open_dome_shutter" not in before and reply["Success"]
    assert set(m.GROUPS["dome"][1]) <= after and "nina_get_plugins" not in after


def test_apply_profile_hides_an_enabled_group_again():
    m.apply_profile("core")
    run(lambda c: tool(c, "nina_enable_tools", {"group": "dome"}))
    m.apply_profile("core")
    assert "nina_open_dome_shutter" not in run(names)


def test_an_unknown_group_lists_the_real_ones():
    m.apply_profile("core")
    reply = run(lambda c: tool(c, "nina_enable_tools", {"group": "telescope"}))
    assert not reply["Success"] and "dome" in reply["Error"] and "mount" in reply["Error"]
