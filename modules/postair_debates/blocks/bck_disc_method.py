"""How we debate — the three rules, with the moderator between two poles.

Moved here from the opening deck (NG 2026-08-14, ss12-restructure) — the same
movement as bck_disc_wrapup (NG 2026-08-03): the rules of the debate belong
where the debate is run, and this slide now opens the deck's four-beat intro.

Opens the discussion sequence. The questions are not chosen by the speaker:
they come out of what this room answered, which is the whole point and the
reason the survey came first.

The host takes the third seat (NG 2026-08-30): Guardo is commented out of
the stage and the speaker's own portrait (the opening deck's illustration,
DD-35 marked) faces Libero beside the moderator.

Steps, not a stopwatch (NG 2026-08-29, cards rewritten 2026-08-30): the
three projected cards say what is debated (your concerns), how the room
takes part (hands on, arguments each way) and the thread of every axis
(past · present · future) — and no duration. In a hall of five hundred to
fifteen hundred, a short timer kills the debate before it starts; the
speaker keeps the twenty-minute slot by opening two axes instead of three
when the room is lively.

SPEAKER NOTES:
Three minutes. Insist on one thing above all: nobody defends a position in
their own name. The mascots carry the postures, so a student can argue for
prudence without being labelled a pessimist for the rest of the year — that
is what makes a room of this size willing to speak at all. Give the three
rules plainly, promise the microphone will come to them, and move on.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_data import mascot
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay

# Trois cartes, réécrites par NG le 2026-08-30 : ce que la salle débat, comment
# elle y prend part, et le fil de chaque axe. Aucune durée n'est projetée — des
# ÉTAPES, jamais un chronomètre (NG 2026-08-29) : devant 500 à 1500 personnes,
# un timing trop court étouffe le débat avant qu'il n'existe ; la durée reste à
# l'orateur, qui tient les 20' du créneau en ouvrant deux axes plutôt que trois
# si la salle s'anime.
# Chaque règle : (feuille du titre, tuple de feuilles — une par ligne).
_RULES = [
    # Les sujets viennent des réponses de la salle, jamais de l'orateur.
    ({"en": "Your concerns"}, ({"en": "the ones that split"},)),
    # La salle argumente elle-même, dans les deux sens ; le vote à main levée
    # vient après que les deux camps ont été entendus — jamais avant.
    # Deux lignes voulues (NG 2026-08-30) : un détail est un tuple de
    # lignes — `st_write` n'interprète pas « \n », chaque ligne est un écrit.
    ({"en": "Hands on"}, ({"en": "your arguments"}, {"en": "each way"})),
    # Le fil de chaque axe : les figures d'hier, les arguments d'aujourd'hui,
    # le face-à-face qui engage demain — l'ordre des sous-slides de la banque.
    ({"en": "DEBATE"}, ({"en": "past · present · future"},)),
]

# The moderator flanked by an opposed pair — the visual grammar of a debate.
# Guardo cède sa place à l'hôte (NG 2026-08-30) : le troisième siège est
# tenu par l'orateur lui-même, face à Libero — il défendra chaque posture.
_STAGE = ("Libero", "Medio")  # , "Guardo"
#: Portrait de l'hôte — illustration versionnée (copie de celle d'opening,
#: `ng__portrait__studio__v1`, public-ok, image de synthèse ⇒ DD-35), jamais au CDN.
_HOST_PORTRAIT = "images/host/host_portrait.webp"
_HOST_NAME = {"en": "Your host", "fr": "Votre hôte"}

# ── Le texte projeté (règle R-i18n) ──────────────────────────────────────────
_MARKER = {"en": "How we debate"}
_TITLE = {"en": ("Let's ", (s.project.titles.keyword, "debate"))}
_TIP_TITLE = {"en": "How the questions are chosen"}
_TIP = [
    ({"en": "Not by the speaker"},
     {"en": ("The debate questions come from your own answers: the selection ranks the "
             "statements by disagreement, by engagement and by response rate, and keeps "
             "the most divisive ones, at most two per axis so the debate does not collapse "
             "onto a single theme.")}),
    ({"en": "Hands on, no stopwatch"},
     {"en": ("You make the arguments, in both directions: one for, one against, then a "
             "show of hands. A round closes when both sides have been heard, not when a "
             "timer rings — the speaker keeps the slot by opening two axes rather than "
             "three when the room is lively.")}),
    ({"en": "Past, present, future"},
     {"en": ("Each axis runs the same way: who held this posture before us and in what "
             "words, what is argued today with sources, then the two poles face to face — "
             "where this room stands.")}),
    ({"en": "Nobody speaks in their own name"},
     {"en": ("The mascots carry the postures. You argue for prudence, not as a prudent "
             "person — which is what makes it possible to change your mind in public.")}),
    ({"en": "Microphones"},
     {"en": ("Roaming microphones; wait for one before speaking, so the whole "
             "amphitheatre hears you and not just your row.")}),
    ({"en": "Respect"},
     {"en": ("Attack the position, never the person holding it. Every posture in this "
             "instrument is defensible, and each one has been held by someone whose name "
             "you know.")}),
]


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    rule = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt
    mascot_name = s.project.body.mascot_name


bs = BlockStyles


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(h, lang), T(d, lang)) for h, d in _TIP],
                )
        st_space("v", "1vh")
        # ONE flat grid: pole · moderator · pole.
        with st_grid(cols="1fr 1.2fr 1fr", gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for name in _STAGE:
                m = mascot(name)
                with g.cell():
                    st_image(s.project.cards.media_center,
                             width="min(20vw, 40vh)" if name == "Medio" else "min(14vw, 30vh)",
                             uri=m["image"],
                             alt=f"{m['name']}, mascot of the {m['pole'] or 'moderator'} posture",
                             overlay=dd35_overlay())
                    st_write(bs.mascot_name, m["name"], tag=t.div)
            with g.cell():
                with st_zoom(140):
                    st_image(s.project.cards.media_center, width="min(14vw, 30vh)",
                            uri=_HOST_PORTRAIT,
                            alt="Portrait of the host of the AI Day, taking the third seat of the debate",
                            overlay=dd35_overlay())
                st_write(bs.mascot_name, T(_HOST_NAME, lang), tag=t.div)
        st_space("v", "0.5vh")
        with st_grid(cols=s.project.grids.balanced(len(_RULES)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for rule, detail in _RULES:
                with g.cell(), st_block(s.project.cards.coral):
                    with st_zoom(150):
                        st_write(bs.rule, T(rule, lang), tag=t.div)
                        for line in detail:
                            st_write(bs.detail, T(line, lang), tag=t.div)
