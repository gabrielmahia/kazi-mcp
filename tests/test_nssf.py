from kazi_mcp import server as s

tpl = s.contract_template.fn if hasattr(s.contract_template, "fn") else s.contract_template


def _nssf_line(gross):
    text = tpl("permanent", "E", "W", "Clerk", gross)["template"]
    return next(line for line in text.splitlines() if line.startswith("NSSF"))


def test_nssf_below_the_cap_is_six_percent():
    assert "KES 3,000" in _nssf_line(50_000)


def test_nssf_is_capped_at_6480_above_the_2026_upper_limit():
    """The template charged 6% of everything: 12,000 on a 200,000 salary. The Feb-2026 maximum is 6,480."""
    assert "KES 6,480" in _nssf_line(200_000)


def test_nssf_is_exactly_the_cap_at_the_upper_limit():
    assert "KES 6,480" in _nssf_line(108_000)
