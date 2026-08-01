"""AI Day event constants — the conference days, their sumvadis codes, the agenda.

One survey campaign instance per day (created in the sumvadis /admin console).
"""

SURVEY_BASE = "https://app.sumvadis.ai"

DEBATES_URL = "https://postair-debates.streamtex.org"

# The day as the room will live it. ``kind`` drives the visual treatment, not a
# hard-coded colour in the block: ``stage`` = a session, ``debate`` = the
# discussion (human/debate accent), ``break`` = the single focal accent.
# The session titles are those of the official agenda (PROJECT.md).
AGENDA = [
    ("Welcome", "20'", "stage"),
    ("Survey", "30'", "stage"),
    ("Survey results", "20'", "stage"),
    ("Survey discussion", "20'", "debate"),
    ("Break", "20'", "break"),
    ("Introduction to AI & Generative AI", "30'", "stage"),
    ("Using Mistral models & agents to study", "20'", "stage"),
    ("The UL AI guidelines", "15'", "stage"),
    ("Closing", "5'", "stage"),
]

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
