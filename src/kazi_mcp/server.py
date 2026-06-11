"""KaziMCP server — 6 tools for Kenya labor market coordination."""
from __future__ import annotations
from typing import Optional
from fastmcp import FastMCP
from .data import WAGE_BENCHMARKS, EMPLOYMENT_RIGHTS, SKILLS_MAP

mcp = FastMCP(name="kazi-mcp", description="Kenya labor market coordination. DEMO data only.")

@mcp.tool(name="job_match", description="Match worker skills to Kenyan job categories. Returns ranked matches with wage ranges. DEMO.")
def job_match(skills: list[str], county: Optional[str] = None) -> dict:
    matches: dict[str, int] = {}
    for skill in [s.lower() for s in skills]:
        for k, jobs in SKILLS_MAP.items():
            if k in skill or skill in k:
                for job in jobs:
                    matches[job] = matches.get(job, 0) + 1
    ranked = sorted(matches.items(), key=lambda x: x[1], reverse=True)[:8]
    results = [{"job": job.replace("_"," ").title(), "match_score": score,
                "wage_range_kes": f"KES {WAGE_BENCHMARKS[job]['entry']:,}–{(WAGE_BENCHMARKS[job]['senior'] or WAGE_BENCHMARKS[job]['mid']):,}/month"
                if job in WAGE_BENCHMARKS else "see wage_benchmark"} for job, score in ranked]
    return {"source": "DEMO", "skills": skills, "county": county, "matches": results}

@mcp.tool(name="wage_benchmark", description="Monthly wage benchmark for a Kenyan job (entry/mid/senior in KES). DEMO — verify against KNBS data.")
def wage_benchmark(job_title: str, experience_level: Optional[str] = "mid", county: Optional[str] = None) -> dict:
    key = job_title.lower().replace(" ", "_")
    bench = WAGE_BENCHMARKS.get(key) or next((v for k, v in WAGE_BENCHMARKS.items() if key in k or k in key), None)
    if not bench:
        return {"source": "DEMO", "job": job_title, "available_roles": list(WAGE_BENCHMARKS.keys())}
    level = (experience_level or "mid").lower()
    return {"source": "DEMO", "job": job_title, "level": level, "kes_month": bench.get(level) or bench.get("mid"),
            "entry": bench["entry"], "mid": bench["mid"], "senior": bench.get("senior"), "county": county}

@mcp.tool(name="skills_gap_analysis", description="Identify skills gap between current skills and target job. Returns missing skills + Kenya training pathways.")
def skills_gap_analysis(current_skills: list[str], target_job: str) -> dict:
    REQUIRED = {
        "software_engineer": ["python","javascript","git","api","databases"],
        "data_analyst":      ["python","excel","sql","statistics"],
        "nurse":             ["nursing","patient_care","triage"],
        "accountant":        ["accounting","excel","quickbooks","tax"],
        "agri_extension_officer": ["farming","agronomy","extension","swahili"],
        "boda_rider":        ["driving","motorcycle","customer_service"],
        "jua_kali_mechanic": ["welding","carpentry","tools"],
        "teacher_primary":   ["teaching","swahili","english"],
    }
    key = target_job.lower().replace(" ", "_")
    req = REQUIRED.get(key) or next((v for k, v in REQUIRED.items() if key in k or k in key), [])
    cur = [s.lower() for s in current_skills]
    missing = [r for r in req if not any(r in c or c in r for c in cur)]
    present = [r for r in req if any(r in c or c in r for c in cur)]
    PROVIDERS = {"python":"Moringa/ALX Africa","nursing":"KMTC","accounting":"KASNEB","farming":"KALRO","teaching":"KTTC","welding":"NITA VTC","driving":"NTSA school"}
    training = [{"skill": s, "provider": next((v for k,v in PROVIDERS.items() if k in s), "NITA VTC")} for s in missing]
    return {"source": "DEMO", "target": target_job, "missing": missing, "present": present, "training": training,
            "readiness_pct": round(len(present) / max(len(req), 1) * 100) if req else 0}

@mcp.tool(name="informal_sector_registry", description="Register or look up informal sector worker (jua kali, boda rider, domestic worker). DEMO.")
def informal_sector_registry(action: str, name: Optional[str] = None, trade: Optional[str] = None, county: Optional[str] = None) -> dict:
    if action == "list_trades":
        return {"source": "DEMO", "trades": ["jua_kali","boda_rider","domestic_worker","hawker","mama_mboga","salon_barber","tailor","electrician","plumber","fundi"]}
    if action == "register":
        did = f"KZI-{(county or 'NBI')[:3].upper()}-{abs(hash(str(name)+str(trade)))%90000+10000}"
        return {"source": "DEMO", "status": "demo_registered", "worker_id": did, "name": name, "trade": trade, "county": county,
                "next_steps": ["Visit county Jua Kali office", "Join a SACCO", "Register for NSSF"]}
    return {"source": "DEMO", "note": "Production queries county registry", "worker_id": None}

@mcp.tool(name="contract_template", description="Generate Kenya Employment Act 2007 contract template (permanent/casual/fixed_term). NOT legal advice.")
def contract_template(contract_type: str, employer_name: str, employee_name: str, job_title: str, monthly_gross_kes: float, start_date: Optional[str] = None) -> dict:
    nssf = round(monthly_gross_kes * 0.06)
    tmpl = (f"EMPLOYMENT CONTRACT — {contract_type.upper()}\nKenya Employment Act 2007\n\n"
            f"Employer: {employer_name}\nEmployee: {employee_name}\nJob Title: {job_title}\n"
            f"Start Date: {start_date or '[DATE]'}\nGross Monthly Pay: KES {monthly_gross_kes:,.0f}\n"
            f"NSSF (6%): KES {nssf:,.0f}\n\nLeave: 21 days/yr | Sick: 7 full+7 half | Maternity 3mo | Paternity 14d\n"
            f"Notice: 28 days | Severance: 15 days/yr on redundancy\n\n[Review with qualified Kenyan advocate]")
    return {"source": "DEMO", "contract_type": contract_type, "template": tmpl, "disclaimer": "Not legal advice"}

@mcp.tool(name="labor_rights_query", description="Query Kenya Employment Act 2007 rights by topic (maternity, overtime, termination, etc). DEMO summary — not legal advice.")
def labor_rights_query(topic: str) -> dict:
    tl = topic.lower()
    matches = {k: v for k, v in EMPLOYMENT_RIGHTS.items() if any(w in tl for w in k.split("_")) or any(w in k for w in tl.split())}
    if not matches:
        matches = {k: v for k, v in EMPLOYMENT_RIGHTS.items() if k[:4] in tl or tl[:4] in k}
    return {"source": "DEMO — Kenya Employment Act 2007", "topic": topic,
            "rights": matches or {"general": "Review Employment Act 2007 at kenyalaw.org"},
            "disclaimer": "Not legal advice", "all_topics": list(EMPLOYMENT_RIGHTS.keys())}
