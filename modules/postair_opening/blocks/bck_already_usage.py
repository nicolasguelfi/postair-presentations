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


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    value = s.project.titles.register_title + s.center_txt
    claim = s.project.body.bullet_giant + s.center_txt
    counterpoint = s.project.body.bullet + s.project.colors.coral + s.center_txt + s.bold + s.text_6xl
    attribution = s.project.body.caption + s.center_txt


bs = BlockStyles

_ZOOM = 130

# ── Le fait (source primaire, vérifiée 2026-08-02) ──────────────────────────
_VALUE = "94 %"
_CLAIM = "of students use generative AI to help with assessed work"
_COUNTERPOINT = "but only 12 % hand in AI-written text"
_ATTRIBUTION = "HEPI, March 2026"
#: La source du chiffre ET celle du contrepoint, dédupliquées — un chiffre
#: projeté sans la publication qui le conteste serait un chiffre arrangé.
_CITEKEYS = ["hepi-survey-2026"]

# ── Le panneau « Where this figure comes from » ─────────────────────────────
_POPULATION = ("1,054 full-time UK undergraduates, polled by Savanta in "
               "December 2025; weighted for gender, institution type and year "
               "of study; margin of error approximately 3 %")
_TREND = "89 % one year earlier, 53 % two years earlier"
_FRESHNESS = ("Six months before this event. The third annual edition of the "
              "same instrument, so the trend is measured, not assembled.")
_COUNTERPOINT_LONG = ("Using it is not the same as handing it in. Only 12 % "
                      "include AI-generated text directly in assessed work; "
                      "the dominant uses are having concepts explained (61 %) "
                      "and articles summarised (49 %).")
_CAVEAT = "UK undergraduates. No equivalent survey exists for Luxembourg."


def build(lang: str = "en", **_):
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
