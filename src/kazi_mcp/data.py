"""Synthetic labor market reference data for Kenya. ALL DATA IS DEMO."""
from __future__ import annotations

WAGE_BENCHMARKS = {
    "software_engineer":      {"entry": 60000, "mid": 120000, "senior": 220000, "counties": ["Nairobi","Mombasa","Kisumu"]},
    "data_analyst":           {"entry": 45000, "mid": 90000,  "senior": 160000, "counties": ["Nairobi","Nakuru"]},
    "nurse":                  {"entry": 35000, "mid": 60000,  "senior": 100000, "counties": ["all"]},
    "teacher_primary":        {"entry": 25000, "mid": 40000,  "senior": 65000,  "counties": ["all"]},
    "boda_rider":             {"entry": 18000, "mid": 28000,  "senior": None,   "counties": ["all"]},
    "jua_kali_mechanic":      {"entry": 15000, "mid": 30000,  "senior": 55000,  "counties": ["all"]},
    "domestic_worker":        {"entry": 12000, "mid": 18000,  "senior": 28000,  "counties": ["all"]},
    "security_guard":         {"entry": 15000, "mid": 20000,  "senior": 30000,  "counties": ["all"]},
    "accountant":             {"entry": 40000, "mid": 80000,  "senior": 150000, "counties": ["Nairobi","Mombasa"]},
    "agri_extension_officer": {"entry": 30000, "mid": 50000,  "senior": 80000,  "counties": ["all"]},
}

EMPLOYMENT_RIGHTS = {
    "written_contract":  "Every employee is entitled to a written contract within 3 months.",
    "minimum_wage":      "Minimum wage varies by sector and county per current Wages Order.",
    "overtime":          "Overtime over 52 hrs/wk must be paid at 1.5x rate.",
    "annual_leave":      "At least 21 working days paid leave per year after 12 months.",
    "sick_leave":        "Up to 7 days full pay plus 7 days half pay per year.",
    "maternity_leave":   "3 months paid maternity leave.",
    "paternity_leave":   "2 weeks paid paternity leave.",
    "termination_notice":"28 days minimum notice or equivalent pay in lieu.",
    "severance_pay":     "15 days gross pay per completed year on redundancy.",
    "nssf_nhif":         "Employer must register and remit NSSF and NHIF contributions.",
}

SKILLS_MAP = {
    "python":     ["software_engineer","data_analyst","ml_engineer"],
    "javascript": ["software_engineer","web_developer","frontend_dev"],
    "accounting": ["accountant","finance_officer","auditor"],
    "swahili":    ["teacher","translator","customer_service"],
    "driving":    ["boda_rider","truck_driver","taxi_driver"],
    "farming":    ["agri_extension_officer","farm_manager"],
    "carpentry":  ["jua_kali_mechanic","furniture_maker"],
    "nursing":    ["nurse","clinical_officer","community_health_worker"],
    "teaching":   ["teacher_primary","tutor","training_coordinator"],
    "welding":    ["jua_kali_mechanic","construction","manufacturing"],
}
