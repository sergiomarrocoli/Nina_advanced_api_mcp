"""Right Ascension in hours or degrees, and filters by name or id."""
import asyncio

import pytest

import nina_advanced_mcp as m

WHEEL = [{"Name": n, "Id": i} for i, n in enumerate(["Luminance", "Red", "Green", "Blue", "H-alpha", "SII", "O3"])]


def test_hours_pass_through():
    assert m.resolve_ra_hours(0.7122, None) == (0.7122, None)


def test_degrees_are_converted_to_hours():
    hours, problem = m.resolve_ra_hours(None, 10.68)
    assert problem is None and hours == pytest.approx(0.712)


def test_an_out_of_range_ra_names_both_ways_out_and_does_not_guess():
    hours, problem = m.resolve_ra_hours(42.44, None)
    assert hours is None and "ra_degrees" in problem and "ra_hms" in problem and "2.82" not in problem


@pytest.mark.parametrize("text", ["00h 42m 44s", "00:42:44", "0 42 44", "0h42m44s"])
def test_hours_minutes_seconds_are_read_in_any_common_form(text):
    hours, problem = m.resolve_ra_hours(None, None, text)
    assert problem is None and hours == pytest.approx(0.7122, abs=1e-3)


@pytest.mark.parametrize("text", ["Andromeda", "25h 00m 00s", "00h 61m 00s", "", "1 2 3 4"])
def test_something_that_is_not_hours_minutes_seconds_is_refused(text):
    assert m.resolve_ra_hours(None, None, text)[1]


def test_ra_out_of_every_range_is_refused_plainly():
    assert m.resolve_ra_hours(500, None)[1] and m.resolve_ra_hours(None, 400)[1] and m.resolve_ra_hours(-1, None)[1]


def test_both_or_neither_is_refused():
    assert "only one" in m.resolve_ra_hours(1.0, 15.0)[1] and "only one" in m.resolve_ra_hours(1.0, None, "1h")[1]
    assert "Give the Right Ascension" in m.resolve_ra_hours(None, None)[1]


def test_a_filter_is_found_by_name_ignoring_case():
    assert m.pick_filter(WHEEL, None, "green")[0]["Id"] == 2


def test_a_filter_is_found_by_a_unique_part_of_its_name():
    assert m.pick_filter(WHEEL, None, "alpha")[0]["Name"] == "H-alpha"


def test_a_filter_is_found_by_id():
    assert m.pick_filter(WHEEL, 1, None)[0]["Name"] == "Red"


def test_an_unknown_name_lists_the_filters():
    filt, problem = m.pick_filter(WHEEL, None, "Cyan")
    assert filt is None and "Green (id 2)" in problem


def test_an_unknown_id_lists_the_filters():
    filt, problem = m.pick_filter(WHEEL, 9, None)
    assert filt is None and "Red (id 1)" in problem


def test_an_ambiguous_part_of_a_name_is_not_guessed():
    assert m.pick_filter([{"Name": "Red", "Id": 0}, {"Name": "Red 2", "Id": 1}], None, "re")[0] is None


class FakeClient:
    _connected = True

    def __init__(self, filters):
        self.requests, self.filters = [], filters

    async def _send_request(self, method, endpoint, timeout=None):
        self.requests.append(endpoint)
        if endpoint == "equipment/filterwheel/info":
            if isinstance(self.filters, Exception):
                raise self.filters
            return {"Success": True, "Response": {"AvailableFilters": self.filters}}
        return {"Success": True}


def change(monkeypatch, filters, **args):
    client = FakeClient(filters)

    async def get_client():
        return client

    monkeypatch.setattr(m, "get_client", get_client)
    result = asyncio.run(m.nina_change_filter(**args))
    return result, [r for r in client.requests if "change-filter" in r]


def test_changing_by_name_sends_that_filters_id(monkeypatch):
    result, sent = change(monkeypatch, WHEEL, filter_name="Green")
    assert result["Success"] and sent == ["equipment/filterwheel/change-filter?filterId=2"] and "Green" in result["Message"]


def test_a_wrong_id_is_refused_and_nothing_is_sent(monkeypatch):
    result, sent = change(monkeypatch, WHEEL, filter_id=12)
    assert result["Success"] is False and "Red (id 1)" in result["Error"] and sent == []


def test_if_the_list_cannot_be_read_an_id_still_goes_through(monkeypatch):
    result, sent = change(monkeypatch, RuntimeError("down"), filter_id=2)
    assert result["Success"] and sent == ["equipment/filterwheel/change-filter?filterId=2"]


def test_if_the_list_cannot_be_read_a_name_is_refused(monkeypatch):
    result, sent = change(monkeypatch, RuntimeError("down"), filter_name="Green")
    assert result["Success"] is False and sent == []
