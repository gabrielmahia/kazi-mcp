"""KaziMCP server — 6 tools for Kenya labor market coordination."""
from __future__ import annotations

import hashlib
from typing import Annotated, Optional

from fastmcp import FastMCP
from pydantic import Field

from .data import EMPLOYMENT_RIGHTS, SKILLS_MAP, WAGE_BENCHMARKS

# Annotations tell clients which tools are safe to auto-approve (read-only, no side effects).
READ_ONLY = {"readOnlyHint": True, "idempotentHint": True, "openWorldHint": False}

mcp = FastMCP(name="kazi-mcp", instructions="Kenya labor market coordination. DEMO data only.")

@mcp.tool(name="job_match", description="Suggest sample Kenyan jobs for a list of skills with an indicative monthly wage range. Use when someone asks what work fits their skills. Each skill of three or more characters is matched against a small skills table; the score is the number of skills that pointed at the job, and at most 8 jobs are returned, with a note when nothing matches. county is only echoed back. Returns the source label, the skills, county and matches (job, match_score, wage_range_kes). Indicative wages labelled DEMO, not live vacancies. Read-only; no side effects.", annotations=READ_ONLY)
def job_match(skills: Annotated[list[str], Field(description="List of skills such as ['welding', 'python']; entries shorter than 3 characters are ignored.")], county: Annotated[str | None, Field(description="Optional county; only echoed back.")] = None) -> dict:
    matches: dict[str, int] = {}
    if isinstance(skills, str):
        skills = [skills]
    for skill in [s.strip().lower() for s in skills if len(s.strip()) >= 3]:
        for k, jobs in SKILLS_MAP.items():
            if k in skill or skill in k:
                for job in jobs:
                    matches[job] = matches.get(job, 0) + 1
    ranked = sorted(matches.items(), key=lambda x: x[1], reverse=True)[:8]
    results = [{"job": job.replace("_"," ").title(), "match_score": score,
                "wage_range_kes": f"KES {WAGE_BENCHMARKS[job]['entry']:,}–{(WAGE_BENCHMARKS[job]['senior'] or WAGE_BENCHMARKS[job]['mid']):,}/month"
                if job in WAGE_BENCHMARKS else "see wage_benchmark"} for job, score in ranked]
    return {"source": "DEMO", "skills": skills, "county": county, "matches": results, "note": None if results else "No sample jobs match these skills."}

@mcp.tool(name="wage_benchmark", description="Indicative monthly wage in KES for a job title and experience level (entry, mid or senior). Use when someone asks what a role usually pays. job_title is matched against a small table; an unknown title returns the list of available roles. An unrecognised experience level falls back to mid. county is only echoed back. Returns the job, level, kes_month and the entry, mid and senior figures. Indicative figures labelled DEMO, not survey data: check current sources. Read-only; no side effects.", annotations=READ_ONLY)
def wage_benchmark(job_title: Annotated[str, Field(description="Job title such as nurse or software engineer.")], experience_level: Annotated[str | None, Field(description="entry, mid (default) or senior.")] = "mid", county: Annotated[str | None, Field(description="Optional county; only echoed back.")] = None) -> dict:
    key = job_title.lower().replace(" ", "_")
    bench = WAGE_BENCHMARKS.get(key) or next((v for k, v in WAGE_BENCHMARKS.items() if key in k or k in key), None)
    if not bench:
        return {"source": "DEMO", "job": job_title, "available_roles": list(WAGE_BENCHMARKS.keys())}
    level = (experience_level or "mid").lower()
    return {"source": "DEMO", "job": job_title, "level": level, "kes_month": bench.get(level) or bench.get("mid"),
            "entry": bench["entry"], "mid": bench["mid"], "senior": bench.get("senior"), "county": county}

@mcp.tool(name="skills_gap_analysis", description="Compare a person's skills with a target job's required skills and suggest training providers. Use when someone asks what they need to learn for a role. target_job is matched against a small table of jobs; an unknown job returns an error listing the available targets instead of a readiness of 0. Returns the target, missing and present skills, suggested training with provider and readiness_pct. Based on a small table labelled DEMO: readiness is the share of listed skills matched by name, not a competence assessment. Read-only; no side effects.", annotations=READ_ONLY)
def skills_gap_analysis(current_skills: Annotated[list[str], Field(description="List of skills the person has.")], target_job: Annotated[str, Field(description="Target job such as data_analyst; unknown jobs return an error.")]) -> dict:
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
    req = REQUIRED.get(key) or next((v for k, v in REQUIRED.items() if key in k or k in key), None)
    if req is None:
        return {"source": "DEMO", "error": f"No skills profile for {target_job!r}.", "available_targets": list(REQUIRED)}
    if isinstance(current_skills, str):
        current_skills = [current_skills]
    cur = [s.lower() for s in current_skills]
    missing = [r for r in req if not any(r in c or c in r for c in cur)]
    present = [r for r in req if any(r in c or c in r for c in cur)]
    PROVIDERS = {"python":"Moringa/ALX Africa","nursing":"KMTC","accounting":"KASNEB","farming":"KALRO","teaching":"KTTC","welding":"NITA VTC","driving":"NTSA school"}
    training = [{"skill": s, "provider": next((v for k,v in PROVIDERS.items() if k in s), "NITA VTC")} for s in missing]
    return {"source": "DEMO", "target": target_job, "missing": missing, "present": present, "training": training,
            "readiness_pct": round(len(present) / max(len(req), 1) * 100) if req else 0}

@mcp.tool(name="informal_sector_registry", description="Demonstration of an informal-sector worker registry: list the trade categories or produce a demo worker ID. Use when someone wants to see how a registry could work, not to register anyone for real. Nobody is registered: action register returns status demo_registered, a deterministic demo ID and stored false, and nothing is saved anywhere. An action other than list_trades or register returns the valid actions and no worker_id. Returns the source label and the trades or the demo record. Labelled DEMO: there is no registry behind this tool. Read-only; no side effects.", annotations=READ_ONLY)
def informal_sector_registry(action: Annotated[str, Field(description="list_trades or register.")], name: Annotated[str | None, Field(description="Worker name, used only to derive the demo ID.")] = None, trade: Annotated[str | None, Field(description="Trade such as tailor.")] = None, county: Annotated[str | None, Field(description="County; its first three letters prefix the demo ID.")] = None) -> dict:
    if action == "list_trades":
        return {"source": "DEMO", "trades": ["jua_kali","boda_rider","domestic_worker","hawker","mama_mboga","salon_barber","tailor","electrician","plumber","fundi"]}
    if action == "register":
        num = int(hashlib.sha256((str(name) + str(trade)).encode()).hexdigest(), 16) % 90000 + 10000
        did = f"KZI-{(county or 'NBI')[:3].upper()}-{num}"
        return {"source": "DEMO", "status": "demo_registered", "stored": False, "worker_id": did, "name": name, "trade": trade, "county": county,
                "next_steps": ["Visit county Jua Kali office", "Join a SACCO", "Register for NSSF"]}
    return {"source": "DEMO", "note": "Nothing is looked up: no registry is connected.", "valid_actions": ["list_trades", "register"], "worker_id": None}

@mcp.tool(name="contract_template", description="Generate employment contract text for Kenya from the parties' details and monthly gross pay, with the statutory terms the template states (leave, sick leave, maternity, notice, severance) and the employee NSSF deduction. Use when an employer wants a starting draft. contract_type only changes the title; any value is accepted and no legal check is made. Negative pay is treated as zero for the NSSF line. Returns the source label, contract_type, the template text and a not-legal-advice disclaimer. A template labelled DEMO: have a Kenyan advocate review it before use. Read-only; no side effects.", annotations=READ_ONLY)
def contract_template(contract_type: Annotated[str, Field(description="Contract type such as permanent; only changes the title.")], employer_name: Annotated[str, Field(description="Employer's name.")], employee_name: Annotated[str, Field(description="Employee's name.")], job_title: Annotated[str, Field(description="Job title.")], monthly_gross_kes: Annotated[float, Field(description="Gross monthly pay in KES.")], start_date: Annotated[str | None, Field(description="Optional start date text.")] = None) -> dict:
    nssf = round(0.06 * min(max(monthly_gross_kes, 0), 108_000))  # employee 6% of pensionable pay, capped at the Feb-2026 upper limit (max KES 6,480)
    tmpl = (f"EMPLOYMENT CONTRACT — {contract_type.upper()}\nKenya Employment Act 2007\n\n"
            f"Employer: {employer_name}\nEmployee: {employee_name}\nJob Title: {job_title}\n"
            f"Start Date: {start_date or '[DATE]'}\nGross Monthly Pay: KES {monthly_gross_kes:,.0f}\n"
            f"NSSF employee (6%, capped at KES 6,480/month from Feb 2026): KES {nssf:,.0f}\n\nLeave: 21 days/yr | Sick: 7 full+7 half | Maternity 3mo | Paternity 14d\n"
            f"Notice: 28 days | Severance: 15 days/yr on redundancy\n\n[Review with qualified Kenyan advocate]")
    return {"source": "DEMO", "contract_type": contract_type, "template": tmpl, "disclaimer": "Not legal advice"}

@mcp.tool(name="labor_rights_query", description="Employment rights in Kenya under the Employment Act 2007 on a topic, with a not-legal-advice disclaimer. Use when a worker or employer asks what the law says. Keywords in topic select entries; an unmatched topic returns only a general pointer to the Act on kenyalaw.org. Returns the source label, topic, rights and a disclaimer. A short summary labelled DEMO and not legal advice: verify with the Ministry of Labour or an advocate. Read-only; no side effects.", annotations=READ_ONLY)
def labor_rights_query(topic: Annotated[str, Field(description="Topic such as termination, leave or overtime.")]) -> dict:
    tl = topic.lower()
    matches = {k: v for k, v in EMPLOYMENT_RIGHTS.items() if any(w in tl for w in k.split("_")) or any(w in k for w in tl.split())}
    if not matches:
        matches = {k: v for k, v in EMPLOYMENT_RIGHTS.items() if k[:4] in tl or tl[:4] in k}
    return {"source": "DEMO — Kenya Employment Act 2007", "topic": topic,
            "rights": matches or {"general": "Review Employment Act 2007 at kenyalaw.org"},
            "disclaimer": "Not legal advice", "all_topics": list(EMPLOYMENT_RIGHTS.keys())}

def main() -> None:
    """Console entry point."""
    mcp.run()
