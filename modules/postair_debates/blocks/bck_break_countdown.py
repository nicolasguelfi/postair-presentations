"""Break screen — « Break » in big letters, Kuri on the left, the live countdown on the right.

Recomposed on NG's request (2026-08-30): the company of eighteen left this
screen (it comes back on the re-welcome slide); one mascot holds the stage —
Kuri, the meerkat standing tall, nose in the wind, the one who cannot wait
for what comes next. The countdown fills the right half.

The break duration comes from the agenda, not from a constant typed here: if
the programme changes, the screen follows. The countdown starts when the
slide is shown, so it is right whenever the presenter actually reaches it.

Bug fixed the same day: the agenda declares the break as « 15'+5' » (fifteen
minutes of break, five of re-welcome — NG 2026-08-19) and the former parser
concatenated every digit into ONE number: the room was promised a 155-minute
break. The countdown now takes the FIRST duration of the entry — the break
itself — never the sum, never the digits glued together.

SPEAKER NOTES:
Say the time out loud as well as showing it — half the room is already
standing and looking at the person next to them, not at the screen. Point at
the countdown once so people know where to look from the corridor, and say
what comes back after: generative AI, how it actually works. Then stop
talking; the screen does the rest.
"""
# @guideline: postair-minimal

import re

from custom.styles import Styles as s
from postair_data import mascot
from postair_event import AGENDA
from postair_lang import T
from shared_widgets import st_countdown, st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.hero + s.center_txt
    mascot_name = s.project.body.mascot_name


bs = BlockStyles

#: La mascotte de l'écran de pause — nommée, jamais un fichier.
_MASCOT = "Kuri"

# ── Le texte projeté (règle R-i18n) ──────────────────────────────────────────
_MARKER = {"en": "Break", "fr": "Pause"}
_LABEL = {"en": "Break", "fr": "Pause"}
_TIP_TITLE = {"en": "After the break", "fr": "Après la pause"}
_TIP = [
    ({"en": "Introduction to AI & Generative AI", "fr": "Introduction à l'IA et à l'IA générative"},
     {"en": ("How a large language model actually works, what it can and cannot do, "
             "and why it makes things up with such confidence."), "fr": "Comment un grand modèle de langage fonctionne vraiment, ce qu'il sait et ne sait pas faire, et pourquoi il invente avec tant d'assurance."}),
    ({"en": "Using Mistral models & agents to study", "fr": "Étudier avec les modèles et agents Mistral"},
     {"en": ("Building a revision agent step by step — including the mistakes that "
             "make one useless."), "fr": "Construire un agent de révision pas à pas — y compris les erreurs qui le rendent inutile."}),
    ({"en": "The UL AI guidelines", "fr": "Les lignes directrices IA de l'UL"},
     {"en": ("The university's rules: permitted by default, the syllabus prevails, "
             "disclose your use, three levels of risk, ten red lines, and the one test "
             "that settles the rest."), "fr": "Les règles de l'université : permise par défaut, le syllabus prime, déclarez votre usage, trois niveaux de risque, dix lignes rouges, et le test qui tranche le reste."}),
    ({"en": "Keep your device", "fr": "Gardez votre appareil"},
     {"en": ("The second half is lighter on the phone, but keep it within reach "
             "anyway."), "fr": "La seconde partie sollicite moins le téléphone, mais gardez-le à portée de main."}),
]


def _break_minutes() -> int:
    """The break itself, read from the agenda: the FIRST duration of the
    « break » entry (« 15'+5' » → 15 — the five minutes are the re-welcome)."""
    for _session, duration, kind in AGENDA:
        if kind == "break":
            found = re.search(r"\d+", duration)
            if not found:
                raise ValueError(f"unreadable break duration in the agenda: {duration!r}")
            return int(found.group())
    raise LookupError("the agenda declares no break")


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    m = mascot(_MASCOT)
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, (s.project.titles.keyword, T(_LABEL, lang)),
                         tag=t.div, toc_lvl="1", label=T(_LABEL, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", "1vh")
        # ONE flat grid: the mascot on the left, the countdown on the right.
        with st_grid(cols="45% 55%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_image(s.project.cards.media_center, width="min(36vw, 60vh)",
                         uri=m["image"],
                         alt=f"{m['name']}, mascot of the {m['pole']} posture, waiting for the second half",
                         overlay=dd35_overlay())
                st_write(bs.mascot_name, m["name"], tag=t.div)
            with g.cell():
                # `scale` est LE levier de taille : le widget est une iframe dimensionnée
                # en vw, un st_zoom autour serait inerte (R-zoom). La hauteur ne
                # fait que loger les chiffres agrandis.
                st_countdown(_break_minutes(), height=620, scale=1.8)
