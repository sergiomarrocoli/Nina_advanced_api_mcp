"""A tool called with an argument it doesn't have says which arguments it does have."""
import asyncio

import pytest
from fastmcp.exceptions import ToolError

import nina_advanced_mcp as m

CAPTURE = {"properties": {"duration": {}, "gain": {}, "solve": {}}}


def test_an_unknown_argument_is_named_with_the_real_ones():
    message = m.unknown_argument_message("nina_capture_image", CAPTURE, {"duration": 5, "frames": 5})
    assert "frames" in message and "duration, gain, solve" in message


def test_a_repeat_count_is_told_the_tool_does_one_thing_per_call():
    message = m.unknown_argument_message("nina_capture_image", CAPTURE, {"count": 5})
    assert "call it again" in message


def test_other_unknown_names_get_no_repeat_hint():
    assert "call it again" not in m.unknown_argument_message("nina_capture_image", CAPTURE, {"colour": "red"})


def test_known_arguments_pass():
    assert m.unknown_argument_message("nina_capture_image", CAPTURE, {"duration": 5}) is None


def test_a_tool_with_no_arguments_says_so():
    assert "takes no arguments" in m.unknown_argument_message("nina_connect", {"properties": {}}, {"x": 1})


def test_the_server_returns_the_message_instead_of_the_raw_pydantic_error():
    with pytest.raises(ToolError) as caught:
        asyncio.run(m.mcp.call_tool("nina_capture_image", {"duration": 5, "frames": 5}))
    text = str(caught.value)
    assert "frames" in text and "duration" in text and "validation error" not in text
