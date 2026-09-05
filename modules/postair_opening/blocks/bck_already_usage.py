"""Already here 1/4 — 94 % : l'usage étudiant (série « A revolution already here »).

Composition de série (ex-gabarit ``already_slide``, NG 2026-08-13) : la valeur
en très grand (ambre — LE point focal), la lecture télégraphique, le
contrepoint corail À CÔTÉ du chiffre, l'attribution + code de citation. Les 4
blocs ``bck_already_*`` partagent cette composition : toute évolution s'y
réplique à la main.

Le FAIT vit ici (règle NG 2026-08-18) : textes, chiffres et choix des citekeys
s'éditent dans ce bloc, structurés (claim / population / trend / freshness /
counterpoint / caveat) pour que le panneau crédite toujours la source ET son
contrepoint. La phrase bibliographique reste dérivée de ``references.bib`` par
``citation()`` — clé inconnue = erreur bruyante.
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


bs = BlockStyles

_ZOOM = 130

# ── Le fait (source primaire, vérifiée 2026-08-02) ──────────────────────────
_VALUE = {"en": "94 %", "fr": "94 %"}
_CLAIM = {"en": "of students use generative AI to help with assessed work", "fr": "des étudiants s'aident de l'IA générative pour leurs travaux notés"}
_COUNTERPOINT = {"en": "but only 12 % hand in AI-written text", "fr": "mais seuls 12 % rendent du texte d'IA"}
_ATTRIBUTION = {"en": "HEPI, March 2026", "fr": "HEPI, mars 2026"}
#: La source du chiffre ET celle du contrepoint, dédupliquées — un chiffre
#: projeté sans la publication qui le conteste serait un chiffre arrangé.
_CITEKEYS = ["hepi-survey-2026"]

# ── Le panneau « Where this figure comes from » ─────────────────────────────
_POPULATION = {"en": ("1,054 full-time UK undergraduates, polled by Savanta in "
               "December 2025; weighted for gender, institution type and year "
               "of study; margin of error approximately 3 %"), "fr": "1 054 étudiants britanniques de premier cycle à temps plein, sondés par Savanta en décembre 2025 ; pondérés par genre, type d'établissement et année d'études ; marge d'erreur d'environ 3 %"}
_TREND = {"en": "89 % one year earlier, 53 % two years earlier", "fr": "89 % un an plus tôt, 53 % deux ans plus tôt"}
_FRESHNESS = {"en": ("Six months before this event. The third annual edition of the "
              "same instrument, so the trend is measured, not assembled."), "fr": "Six mois avant cet événement. Troisième édition annuelle du même instrument : la tendance est donc mesurée, pas reconstituée."}
_COUNTERPOINT_LONG = {"en": ("Using it is not the same as handing it in. Only 12 % "
                      "include AI-generated text directly in assessed work; "
                      "the dominant uses are having concepts explained (61 %) "
                      "and articles summarised (49 %)."), "fr": "L'utiliser n'est pas le rendre. Seuls 12 % insèrent directement du texte généré par l'IA dans un travail noté ; les usages dominants : se faire expliquer des concepts (61 %) et faire résumer des articles (49 %)."}
_CAVEAT = {"en": "UK undergraduates. No equivalent survey exists for Luxembourg.", "fr": "Premier cycle britannique. Aucune enquête équivalente pour le Luxembourg."}


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
            st_space("v", "3vh")
            st_write(bs.value, T(_VALUE, lang), tag=t.div)
            st_space("v", "1vh")
            with st_zoom(90):
                st_write(bs.claim, T(_CLAIM, lang), tag=t.div)
            st_space("v", "2vh")
            st_write(bs.counterpoint, T(_COUNTERPOINT, lang), tag=t.div)
            st_space("v", "1vh")
            st_write(bs.attribution, T(_ATTRIBUTION, lang), " ",
                     citation(*_CITEKEYS), tag=t.div)
