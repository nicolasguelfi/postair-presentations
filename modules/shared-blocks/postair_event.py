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
    ("Break", "15'+5'", "break"),
    ("Introduction to AI & Generative AI", "30'", "stage"),
    ("Using Mistral models & agents to study", "20'", "stage"),
    ("The UL AI guidelines", "15'", "stage"),
    ("Closing", "5'", "stage"),
]

# (label shown on stage, 6-digit sumvadis join code)
# Les codes ont été choisis par l'auteur (NG 2026-08-03) ; ils ne se déduisent
# volontairement PAS de la date — un code devinable serait un code que la salle
# de la veille peut essayer. Ils doivent correspondre exactement aux campagnes
# créées dans la console /admin de sumvadis.
DAYS = [
    ("BEFORE AIDAY", "650001"),
    ("Tuesday 8 September", "201048"),
    ("Wednesday 9 September", "101048"),
    ("Thursday 10 September", "091048"),
]

#: Ce que le sélecteur affiche tant qu'aucun jour n'est choisi. La slide montre
#: alors la PLACE du QR et un code masqué : elle s'explique sans rien livrer.
#: Un étudiant de la séance de mardi ne doit pas repartir avec le code de mercredi.
#: (Jours corrigés le 2026-08-30 : l'AI Day tombe mardi 8, mercredi 9, jeudi 10.)
NO_DAY = "Survey Date"


def join_url(code: str) -> str:
    return f"{SURVEY_BASE}/s/{code}"


def live_url(code: str) -> str:
    return f"{SURVEY_BASE}/live/{code}"


def present_url(code: str) -> str:
    return f"{SURVEY_BASE}/present/{code}"
