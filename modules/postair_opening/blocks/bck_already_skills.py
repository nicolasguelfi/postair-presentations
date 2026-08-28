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
from postair_i18n import ui
from postair_lang import T


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
_VALUE = {"en": "68 %", "fr": "68 %"}
_CLAIM = {"en": "say AI skills are essential — only 48 % feel helped to build them", "fr": "jugent les compétences en IA essentielles — seuls 48 % se sentent accompagnés"}
_COUNTERPOINT = {"en": "yet only half want it provided", "fr": "mais seule la moitié le demande"}
_ATTRIBUTION = {"en": "HEPI, March 2026", "fr": "HEPI, mars 2026"}
#: La source du chiffre ET celle du contrepoint, dédupliquées.
_CITEKEYS = ["hepi-survey-2026"]

# ── Le panneau « Where this figure comes from » ─────────────────────────────
_POPULATION = {"en": ("1,054 full-time UK undergraduates, polled by Savanta in "
               "December 2025; weighted; margin of error approximately 3 %"), "fr": "1 054 étudiants britanniques de premier cycle, à temps plein, sondés par Savanta en décembre 2025 ; échantillon pondéré ; marge d'erreur d'environ 3 %"}
_TREND = {"en": ("Institutions are moving: 38 % now provide AI tools to their "
          "students, against 9 % two years earlier"), "fr": "Les établissements bougent : 38 % fournissent désormais des outils d'IA à leurs étudiants, contre 9 % deux ans plus tôt"}
_FRESHNESS = {"en": "Six months before this event.", "fr": "Six mois avant cet événement."}
_COUNTERPOINT_LONG = {"en": ("The demand is not unanimous either. Half of students "
                      "think their institution should provide AI tools — "
                      "which means half do not — and a quarter disagree "
                      "outright."), "fr": "La demande n'est pas unanime non plus. La moitié des étudiants pensent que leur établissement devrait fournir des outils d'IA — donc l'autre moitié non — et un quart s'y opposent franchement."}
_CAVEAT = {"en": ("Self-reported perception, not an audit of what is actually "
           "provided. The gap is widest in Arts and Humanities, where 26 % "
           "feel supported against 53 % in STEM."), "fr": "Une perception déclarée, pas un audit de ce qui est réellement fourni. L'écart est le plus large en lettres et sciences humaines, où 26 % se sentent soutenus, contre 53 % en STEM."}

# ── La ligne long-wave qui ferme la série ───────────────────────────────────
#: Déclaration qualitative sourcée, pas un chiffre : une année de publication
#: n'a pas de population. Contexte (jamais projeté, gardé pour la
#: vérifiabilité) : le repère des deux sigmas de Bloom date de 1984, et les
#: revues systématiques de l'IA en enseignement supérieur précèdent ChatGPT ;
#: ce qui a rompu en 2022 est l'échelle, pas l'idée.
_CLOSING = {"en": "AI in education did not begin in 2022", "fr": "L'IA dans l'éducation ne date pas de 2022"}
_CLOSING_CITEKEYS = ["bloom-2sigma", "zawacki-richter-2019",
                     "chiu-systematic-2023"]


def build(lang: str = "en", **_):
    st_marker(T(_VALUE, lang))
    with st_zoom(_ZOOM):
        with st_block(s.project.containers.page_fill_top):
            with st_grid(cols="92% 8%",
                         cell_styles=s.project.containers.grid_cell_centered) as g:
                with g.cell():
                    st_write(bs.title, ui("already_here", lang),
                             (s.project.titles.keyword, T(_ATTRIBUTION, lang)),
                             tag=t.div, toc_lvl="+1", label=T(_VALUE, lang))
                with g.cell():
                    st_info_tooltip(
                        title=ui("where_figure_from", lang),
                        entries=[(T(_VALUE, lang), " ".join([
                            T(_CLAIM, lang) + ".", T(_POPULATION, lang) + ".",
                            T(_TREND, lang), T(_FRESHNESS, lang),
                            T(_COUNTERPOINT_LONG, lang), T(_CAVEAT, lang)]))])
            st_space("v", s.project.spacing.title_gap)
            st_write(bs.value, T(_VALUE, lang), tag=t.div)
            st_space("v", "1vh")
            st_write(bs.claim, T(_CLAIM, lang), tag=t.div)
            st_space("v", "2vh")
            st_write(bs.counterpoint, T(_COUNTERPOINT, lang), tag=t.div)
            st_space("v", "1vh")
            st_write(bs.attribution, T(_ATTRIBUTION, lang), " ",
                     citation(*_CITEKEYS), tag=t.div)
            # La ligne long-wave ferme la série.
            st_space("v", "2vh")
            st_write(bs.closing, T(_CLOSING, lang), " ",
                     citation(*_CLOSING_CITEKEYS), tag=t.div)
