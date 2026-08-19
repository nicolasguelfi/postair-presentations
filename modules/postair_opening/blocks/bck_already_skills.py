"""Already here 4/4 — 68 % « vital » + la ligne long-wave (série « A revolution already here »).

Composition de série (ex-gabarit ``already_slide``, NG 2026-08-13) : la valeur
en très grand (ambre — LE point focal), la lecture télégraphique, le
contrepoint corail À CÔTÉ du chiffre, l'attribution + code de citation. Les 4
blocs ``bck_already_*`` partagent cette composition : toute évolution s'y
réplique à la main. Ce dernier chiffre porte aussi la ligne « long-wave » qui
fermait l'ancienne slide.

Le FAIT vit ici (règle NG 2026-08-18) : textes, chiffres et choix des citekeys
s'éditent dans ce bloc, structurés (claim / population / trend / freshness /
counterpoint / caveat) pour que le panneau crédite toujours la source ET son
contrepoint. La phrase bibliographique reste dérivée de ``references.bib`` par
``citation()`` — clé inconnue = erreur bruyante. La ligne long-wave vit ici
aussi depuis la suppression de l'ancienne slide 2×2 qui la partageait
(2026-08-18).
"""
# @guideline: postair-minimal

from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_write, st_zoom
from streamtex.enums import Tags as t

from custom.refs import citation
from custom.styles import Styles as s


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    value = s.project.titles.register_title + s.center_txt
    claim = s.project.body.bullet_giant + s.center_txt
    counterpoint = s.project.body.bullet + s.project.colors.coral + s.center_txt + s.bold + s.text_6xl
    attribution = s.project.body.caption + s.center_txt
    closing = s.project.titles.subtitle + s.project.colors.amber + s.center_txt


bs = BlockStyles

_ZOOM = 110

# ── Le fait (source primaire, vérifiée 2026-08-02) ──────────────────────────
_VALUE = "68 %"
_CLAIM = "say AI skills are essential — only 48 % feel helped to build them"
_COUNTERPOINT = "yet only half want it provided"
_ATTRIBUTION = "HEPI, March 2026"
#: La source du chiffre ET celle du contrepoint, dédupliquées.
_CITEKEYS = ["hepi-survey-2026"]

# ── Le panneau « Where this figure comes from » ─────────────────────────────
_POPULATION = ("1,054 full-time UK undergraduates, polled by Savanta in "
               "December 2025; weighted; margin of error approximately 3 %")
_TREND = ("Institutions are moving: 38 % now provide AI tools to their "
          "students, against 9 % two years earlier")
_FRESHNESS = "Six months before this event."
_COUNTERPOINT_LONG = ("The demand is not unanimous either. Half of students "
                      "think their institution should provide AI tools — "
                      "which means half do not — and a quarter disagree "
                      "outright.")
_CAVEAT = ("Self-reported perception, not an audit of what is actually "
           "provided. The gap is widest in Arts and Humanities, where 26 % "
           "feel supported against 53 % in STEM.")

# ── La ligne long-wave qui ferme la série ───────────────────────────────────
#: Déclaration qualitative sourcée, pas un chiffre : une année de publication
#: n'a pas de population. Contexte (jamais projeté, gardé pour la
#: vérifiabilité) : le repère des deux sigmas de Bloom date de 1984, et les
#: revues systématiques de l'IA en enseignement supérieur précèdent ChatGPT ;
#: ce qui a rompu en 2022 est l'échelle, pas l'idée.
_CLOSING = "AI in education did not begin in 2022"
_CLOSING_CITEKEYS = ["bloom-2sigma", "zawacki-richter-2019",
                     "chiu-systematic-2023"]


def build():
    st_marker(_VALUE)
    with st_zoom(_ZOOM):
        with st_block(s.project.containers.page_fill_top):
            with st_grid(cols="92% 8%",
                         cell_styles=s.project.containers.grid_cell_centered) as g:
                with g.cell():
                    st_write(bs.title, "Already here — ",
                             (s.project.titles.keyword, _ATTRIBUTION),
                             tag=t.div, toc_lvl="+1", label=_VALUE)
                with g.cell():
                    st_info_tooltip(
                        title="Where this figure comes from",
                        entries=[(_VALUE, " ".join([
                            _CLAIM + ".", _POPULATION + ".",
                            _TREND, _FRESHNESS, _COUNTERPOINT_LONG, _CAVEAT]))])
            st_space("v", s.project.spacing.title_gap)
            st_write(bs.value, _VALUE, tag=t.div)
            st_space("v", "1vh")
            st_write(bs.claim, _CLAIM, tag=t.div)
            st_space("v", "2vh")
            st_write(bs.counterpoint, _COUNTERPOINT, tag=t.div)
            st_space("v", "1vh")
            st_write(bs.attribution, _ATTRIBUTION, " ",
                     citation(*_CITEKEYS), tag=t.div)
            # La ligne long-wave ferme la série.
            st_space("v", "2vh")
            st_write(bs.closing, _CLOSING, " ",
                     citation(*_CLOSING_CITEKEYS), tag=t.div)
