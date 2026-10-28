"""The below-horizon check on nina_slew_mount: pure maths, and the tool against a fake client."""
import asyncio

import pytest

import nina_advanced_mcp as m

# The benchmark site: latitude 53 N. At sidereal time 23.0 h, M31 (RA 0.71 h, Dec +41.3) is well up.
SITE = {"SiteLatitude": 53, "SiderealTime": 23.0}
M31 = (0.7122, 41.27)
ALPHA_CEN = (14.66, -60.83)    # never rises from 53 N
ORION_BELT = (5.6, -1.2)        # rises and sets; below the horizon at sidereal time 23 h


def test_a_target_on_the_meridian_has_its_highest_altitude():
    assert m.target_altitude_deg(5.0, 20.0, 50.0, 5.0) == pytest.approx(m.highest_altitude_deg(20.0, 50.0))


def test_the_pole_star_altitude_is_the_latitude():
    assert m.target_altitude_deg(2.5, 90.0, 53.0, 11.0) == pytest.approx(53.0)


def test_m31_is_up_and_gets_no_refusal():
    assert m.below_horizon_message(*M31, SITE) is None


def test_a_target_that_never_rises_is_refused_and_says_so():
    msg = m.below_horizon_message(*ALPHA_CEN, SITE)
    assert "never rises" in msg and "below the horizon" in msg


def test_a_target_that_rises_later_is_refused_with_a_hint():
    msg = m.below_horizon_message(*ORION_BELT, SITE)
    assert "rises later" in msg


def test_no_site_in_the_mount_info_means_no_check():
    assert m.below_horizon_message(*ALPHA_CEN, {}) is None


class FakeClient:
    _connected = True

    def __init__(self, info):
        self.requests, self.info = [], info

    async def _send_request(self, method, endpoint, timeout=None):
        self.requests.append(endpoint)
        if endpoint == "equipment/mount/info":
            if isinstance(self.info, Exception):
                raise self.info
            return {"Success": True, "Response": self.info}
        return {"Success": True}


def slew(monkeypatch, info, ra, dec, **kwargs):
    client = FakeClient(info)

    async def get_client():
        return client

    monkeypatch.setattr(m, "get_client", get_client)
    result = asyncio.run(m.nina_slew_mount(ra=ra, dec=dec, **kwargs))
    return result, [r for r in client.requests if r.startswith("equipment/mount/slew")]


def test_a_slew_below_the_horizon_is_refused_and_never_sent(monkeypatch):
    result, sent = slew(monkeypatch, SITE, *ALPHA_CEN)
    assert result["Success"] is False and "Not slewing" in result["Error"] and sent == []


def test_allow_below_horizon_sends_the_slew(monkeypatch):
    result, sent = slew(monkeypatch, SITE, *ALPHA_CEN, allow_below_horizon=True)
    assert result["Success"] is True and len(sent) == 1


def test_a_target_that_is_up_is_slewed_to(monkeypatch):
    result, sent = slew(monkeypatch, SITE, *M31)
    assert result["Success"] is True and len(sent) == 1


def test_if_the_mount_info_cannot_be_read_the_slew_goes_ahead(monkeypatch):
    result, sent = slew(monkeypatch, RuntimeError("down"), *ALPHA_CEN)
    assert result["Success"] is True and len(sent) == 1
