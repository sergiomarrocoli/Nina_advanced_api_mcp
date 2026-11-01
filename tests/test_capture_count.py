"""nina_capture_image repeats the exposure `count` times."""
import asyncio

import pytest
from pydantic import ValidationError

import nina_advanced_mcp as m


def run(monkeypatch, results, **kwargs):
    calls = []

    async def fake(input):
        calls.append(input)
        return results[len(calls) - 1]

    monkeypatch.setattr(m, "_capture_one", fake)
    reply = asyncio.run(m.nina_capture_image(duration=5, **kwargs))
    return reply, calls


OK = {"Success": True, "Message": "Image captured successfully"}


def test_one_capture_by_default_returns_that_capture_unchanged(monkeypatch):
    reply, calls = run(monkeypatch, [OK])
    assert reply == OK and len(calls) == 1


def test_count_takes_that_many_exposures(monkeypatch):
    reply, calls = run(monkeypatch, [OK] * 5, count=5)
    assert len(calls) == 5 and reply["Success"] and len(reply["Frames"]) == 5 and "5 images" in reply["Message"]


def test_a_failed_frame_stops_the_run_and_says_how_many_were_taken(monkeypatch):
    bad = {"Success": False, "Error": "camera busy"}
    reply, calls = run(monkeypatch, [OK, OK, bad, OK, OK], count=5)
    assert len(calls) == 3 and not reply["Success"] and "Frame 3 of 5" in reply["Error"] and "2 were taken" in reply["Error"]


@pytest.mark.parametrize("count", [0, -1, m.MAX_CAPTURE_COUNT + 1])
def test_a_count_out_of_range_is_refused(count):
    with pytest.raises(ValidationError):
        m.CameraCaptureInput(duration=5, count=count)


def test_the_published_tool_takes_count_and_describes_it():
    tool = asyncio.run(m.mcp.get_tool("nina_capture_image"))
    assert "count" in tool.parameters["properties"] and tool.parameters["properties"]["count"].get("description")
