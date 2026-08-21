"""The consent screen (03) — nothing personal, and it is written on screen.

Slide Q14 (NG 2026-08-20) : la capture RÉELLE du consentement à gauche, et à
droite les messages utiles à la place de l'ancienne légende — ce que l'écran
demande, ce qu'il ne demande PAS, et ce que « anonyme » veut dire ici.
Remplace, avec ``bck_screens_statement``, l'ancienne paire « The first
screens · 3-4 » du bloc « How to answer » (supprimé le même jour).

SPEAKER NOTES:
Thirty seconds. Say out loud that nothing on this screen identifies anyone —
the room heard it on the context slide, it must SEE it once on the real
screen. Consent is a tap, stopping is allowed at any time.
"""
# @guideline: postair-minimal

from custom.screen_slide import screen_slide
from custom.styles import Styles as s
from streamtex import *


def build():
    st_marker("Consent")
    with st_zoom(130):
        screen_slide(
            ["Consent — ", (s.project.titles.keyword, "nothing personal")],
            "03-consentement",
            "Mobile screen of the survey journey: the consent step, dark theme",
            [
                ("Nothing personal is asked",
                "No name, no email, no account — nothing on this screen can "
                "identify you."),
                ("Your explicit consent",
                "The survey starts only after you accept — participation is "
                "voluntary, and you can stop at any time."),
                ("Anonymous by construction",
                "Your report is computed on YOUR device; only anonymous answers "
                "reach the room's averages."),
            ],
            toc_label="Consent",
            tooltip=("This screen",
                    [("Real capture", "The actual application, mobile facet, dark "
                    "theme — frozen from the sumvadis media registry, never "
                    "redrawn."),
                    ("Under 18", "You can play and see your own results — your "
                    "record is simply excluded from the research analysis.")]),
        )
