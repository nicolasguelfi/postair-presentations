"""AI Day event constants — the three conference days and their sumvadis codes.

One survey campaign instance per day (created in the sumvadis /admin console).
"""

SURVEY_BASE = "https://app.sumvadis.ai"

# (label shown on stage, 6-digit sumvadis join code)
DAYS = [
    ("Monday 8 September", "260908"),
    ("Tuesday 9 September", "260909"),
    ("Wednesday 10 September", "260910"),
]


def join_url(code: str) -> str:
    return f"{SURVEY_BASE}/s/{code}"


def live_url(code: str) -> str:
    return f"{SURVEY_BASE}/live/{code}"


def present_url(code: str) -> str:
    return f"{SURVEY_BASE}/present/{code}"
