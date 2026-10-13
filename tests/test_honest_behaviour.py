from kazi_mcp import server

_fn = lambda name: (getattr(server, name).fn if hasattr(getattr(server, name), "fn") else getattr(server, name))


def test_very_short_skill_tokens_do_not_match_jobs_by_accident():
    r = _fn("job_match")(["z", "a"], None)
    assert r["matches"] == [] and r["note"]


def test_a_real_skill_still_matches_and_a_bare_string_is_one_skill_not_many_letters():
    key = next(iter(server.SKILLS_MAP))
    assert _fn("job_match")([key], None)["matches"] and _fn("job_match")(key, None)["matches"]


def test_an_unknown_target_job_is_an_error_not_a_readiness_of_zero():
    r = _fn("skills_gap_analysis")(["python"], "astronaut")
    assert "error" in r and "readiness_pct" not in r and "data_analyst" in r["available_targets"]
    assert isinstance(_fn("skills_gap_analysis")(["python"], "data_analyst")["readiness_pct"], int)


def test_the_demo_worker_id_is_stable_across_calls_and_says_it_is_not_stored():
    a, b = _fn("informal_sector_registry")("register", "Amina", "tailor", "Nairobi"), _fn("informal_sector_registry")("register", "Amina", "tailor", "Nairobi")
    assert a["worker_id"] == b["worker_id"] and a["stored"] is False
    r = _fn("informal_sector_registry")("lookup", None, None, None)
    assert r["worker_id"] is None and "register" in r["valid_actions"]
