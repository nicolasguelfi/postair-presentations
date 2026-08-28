"""Already here 3/4 — 61 % de non-natifs lus « IA » (série « A revolution already here »).

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
_VALUE = {"en": "61 %"}
_CLAIM = {"en": "of essays by non-native writers are detected as AI"}
_COUNTERPOINT = {"en": "the vendors report under 1 %"}
_ATTRIBUTION = {"en": "Patterns, July 2023"}
#: La source du chiffre, celle du contrepoint (les revendications publiées de
#: Turnitin — la page FAQ elle-même bloque la lecture automatisée, vérifiée
#: 2026-08-02), et la confirmation 2026 (``also``).
_CITEKEYS = ["liang2023-bias", "turnitin-detection-faq", "giray-detectors-2026"]

# ── Le panneau « Where this figure comes from » ─────────────────────────────
_POPULATION = {"en": ("91 human-written TOEFL essays by non-native English writers, "
               "against 88 essays by US eighth-graders which the same "
               "detectors classified almost perfectly")}
_TREND = {"en": ("42 % of students say fear of being accused of cheating makes them "
          "less likely to use AI at all, down from 53 % a year earlier "
          "(HEPI 2026)")}
_FRESHNESS = {"en": ("Three years old and still load-bearing: the peer-reviewed "
              "position in 2026 is unchanged. Detection is a fast-moving "
              "field — re-check before citing this in any policy document.")}
_COUNTERPOINT_LONG = {"en": ("The vendors dispute it. Turnitin reports a "
                      "document-level false-positive rate below 1 % and its "
                      "own study finds no statistically significant bias "
                      "against English-language learners; the newest "
                      "detectors claim to have closed the gap.")}
_CAVEAT = {"en": ("The authors call it a pilot on small samples, and most detectors "
           "tested were built on GPT-2. Turnitin's own detector was not among "
           "the seven. What the study establishes is the mechanism: detectors "
           "read plain vocabulary as machine-like — rewriting the same essays "
           "in richer English dropped the false-positive rate to 12 %. That "
           "mechanism is the one that matters in a multilingual university.")}


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
