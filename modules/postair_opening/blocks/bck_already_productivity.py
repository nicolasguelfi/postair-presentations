"""Already here 2/4 — −40 % de temps, +18 % de qualité (série « A revolution already here »).

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
_VALUE = {"en": "−40 %"}
_CLAIM = {"en": "time on the task, and 18 % higher output quality, with generative AI"}
_COUNTERPOINT = {"en": "and 17 % lower once it is taken away"}
_ATTRIBUTION = {"en": "Science, July 2023"}
#: La source du chiffre PUIS celle du contrepoint — un chiffre projeté sans
#: la publication qui le nuance serait un chiffre arrangé. Population du
#: contrepoint (jamais projetée, gardée pour la vérifiabilité) : nearly 1,000
#: high-school mathematics students in Turkey, field experiment (vérifié
#: 2026-08-02).
_CITEKEYS = ["noy-zhang-2023", "bastani-guardrails-2025"]

# ── Le panneau « Where this figure comes from » ─────────────────────────────
_POPULATION = {"en": ("453 college-educated professionals in a pre-registered "
               "randomised controlled trial on occupation-specific writing "
               "tasks; half given ChatGPT")}
_TREND = {"en": ("The gain was largest for the weakest writers, compressing the "
          "spread between workers")}
_FRESHNESS = {"en": ("Three years old, and kept deliberately: it remains the "
              "peer-reviewed anchor in Science for generative-AI productivity "
              "in knowledge work, and no larger randomised replication has "
              "displaced it.")}
_COUNTERPOINT_LONG = {"en": ("The gain belongs to the task, not to the person. "
                      "School students given an unguarded GPT-4 tutor scored "
                      "48 % higher while it was available and 17 % lower than "
                      "the control group once it was taken away — a loss that "
                      "disappeared when the tutor was constrained to give "
                      "hints instead of answers.")}
_CAVEAT = {"en": ("The two studies answer different questions — professionals "
           "performing, students learning — and that is the point: performing "
           "well and learning are not the same measurement.")}


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
