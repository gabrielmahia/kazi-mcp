"""Live tools: parsing, provenance, validation and failure behaviour, with the network mocked (CI never depends on the services)."""
import urllib.error

from kazi_mcp import server


def _boom(url, params=None, timeout=20.0):
    raise urllib.error.URLError("down")

def test_labour_indicators_merge_series_newest_first(monkeypatch):
    data = {"SL.UEM.TOTL.ZS": [{"date": "2025", "value": 5.61}], "SL.UEM.1524.ZS": [{"date": "2025", "value": 12.04}], "SL.TLF.CACT.ZS": [{"date": "2025", "value": 74.0}, {"date": "2024", "value": 73.9}]}
    monkeypatch.setattr(server, "_live_get", lambda url, params=None, timeout=20.0: [{}, data[url.rsplit("/", 1)[1]]])
    r = server.kenya_labour_indicators(2)
    assert r["rows"][0] == {"year": "2025", "unemployment_pct": 5.61, "youth_unemployment_pct": 12.04, "labour_force_participation_pct": 74.0}
    assert r["rows"][1]["unemployment_pct"] is None and "CC BY 4.0" in r["attribution"]


def test_labour_indicators_failure_and_bad_input_never_give_figures(monkeypatch):
    monkeypatch.setattr(server, "_live_get", _boom)
    assert "error" in server.kenya_labour_indicators() and "rows" not in server.kenya_labour_indicators()
    assert "error" in server.kenya_labour_indicators(0)
