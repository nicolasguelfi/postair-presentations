"""Title — The UL AI Guidelines (U1).

One dominant papercut image (the official document, sealed, under the amber
orb), the exact title, the version line. The full identity card of the
document — issuer, structure, nature, where to download — lives in the
tooltip.

Le FAIT vit ici (règle NG 2026-08-18) : la carte d'identité du document et le
choix des citekeys s'éditent dans ce bloc. La phrase bibliographique reste
dérivée de ``references.bib`` par ``citation()`` — clé inconnue = erreur
bruyante.

Conversion R-i18n (2026-09-03) : chaque texte projeté est une feuille
``{"en", "fr"}`` résolue par ``T``/``TF`` ; le titre exact du document reste
verbatim (document officiel en anglais).

SPEAKER NOTES:
One minute, positive tone: « these rules exist so that you CAN use AI, well ».
Say the three facts that matter: official document, for students AND teachers,
version 1.0 of February 2026. Fifteen minutes for the essential — the full
text is nineteen pages and its identity card is in the info panel.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    version = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Le fait : la carte d'identité du document officiel ──────────────────────
#: Le titre officiel du document, cité tel quel dans les deux langues.
_TITLE_EXACT = "Guidelines on the Use of Generative AI for Teaching and Learning"  # i18n: verbatim
_ISSUER = {"en": ("Institute for Innovative Teaching and Learning (I²TL), "
                  "University of Luxembourg — contact I2TL@uni.lu"),
           "fr": ("Institute for Innovative Teaching and Learning (I²TL), "
                  "Université du Luxembourg — contact I2TL@uni.lu")}
_VERSION_LINE = {"en": ("Version 1.0 · 16 February 2026 · 19 pages · for "
                        "students AND teachers"),
                 "fr": ("Version 1.0 · 16 février 2026 · 19 pages · pour "
                        "étudiants ET enseignants")}
_NATURE = {"en": ("A foundational framework, not a disciplinary code: it "
                  "explains how to use generative AI critically, ethically "
                  "and transparently, and refers misconduct to the existing "
                  "academic procedures. Anchored in the EU AI Act's approach: "
                  "risk levels, transparency, human oversight, bias "
                  "awareness."),
           "fr": ("Un cadre fondateur, pas un code disciplinaire : il "
                  "explique comment utiliser l’IA générative de façon "
                  "critique, éthique et transparente, et renvoie les "
                  "manquements aux procédures académiques existantes. Ancré "
                  "dans l’approche de l’AI Act européen : niveaux de risque, "
                  "transparence, supervision humaine, conscience des biais.")}
_STRUCTURE = {"en": ("1 Introduction (p.3) · 2 Guidelines for learning (p.4) "
                     "· 3 AI tools supported by UL (p.5) · 4 Using GenAI "
                     "effectively and responsibly (p.6) · 5 Guidelines for "
                     "teaching (p.9) · 6 Assessment adaptation (p.12) · "
                     "7 Resources (p.16) · Appendix 1 disclaimers (p.18) · "
                     "Appendix 2 student checklist (p.19). This session "
                     "covers the student sections: 2, 3, 4 and the two "
                     "appendices."),
              "fr": ("1 Introduction (p.3) · 2 Lignes directrices pour "
                     "l’apprentissage (p.4) · 3 Outils d’IA soutenus par "
                     "l’UL (p.5) · 4 Utiliser l’IA générative efficacement "
                     "et de façon responsable (p.6) · 5 Lignes directrices "
                     "pour l’enseignement (p.9) · 6 Adaptation de "
                     "l’évaluation (p.12) · 7 Ressources (p.16) · Annexe 1 "
                     "mentions types (p.18) · Annexe 2 check-list étudiante "
                     "(p.19). Cette session couvre les sections "
                     "étudiantes : 2, 3, 4 et les deux annexes.")}
_CITEKEYS = ["i2tl2026-guidelines"]

_MARKER = {"en": "Guidelines", "fr": "Lignes directrices"}
_TITLE = {"en": ("The UL ", (s.project.titles.keyword, "AI Guidelines")),
          "fr": ("Les ", (s.project.titles.keyword, "lignes directrices IA"),
                 " de l’UL")}
_SUBTITLE = {"en": "15 minutes for the essential",
             "fr": "15 minutes pour l’essentiel"}
_TIP_TITLE = {"en": "The document", "fr": "Le document"}
_LBL_EXACT = {"en": "Exact title", "fr": "Titre exact"}
_LBL_ISSUER = {"en": "Issuer", "fr": "Émetteur"}
_LBL_NATURE = {"en": "Nature", "fr": "Nature"}
_LBL_STRUCTURE = {"en": "Structure", "fr": "Structure"}

_COVER_PROMPT = (
    AI_PREFIX
    + "A large paper document standing upright like a monument, made of "
      "cream cardstock with layered paper pages, closed by a bright coral "
      "paper ribbon and a round paper wax seal, on a small paper pedestal. "
      "A warm glowing amber paper orb floats above it like a sun. Small "
      "abstract paper silhouettes seen from behind look up at the document."
    + AI_SUFFIX_LANDSCAPE
)


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150),g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[
                        (T(_LBL_EXACT, lang), _TITLE_EXACT),  # i18n: verbatim
                        (T(_LBL_ISSUER, lang), T(_ISSUER, lang)),
                        (T(_LBL_NATURE, lang), T(_NATURE, lang)),
                        (T(_LBL_STRUCTURE, lang), T(_STRUCTURE, lang)),
                    ],
                )
        st_space("v", s.project.spacing.title_gap)
        hero_image(
            "guide_cover", _COVER_PROMPT, "images/guide_cover_fallback.svg",
            alt_ready=("Papercut official document with coral ribbon and seal on a "
                       "pedestal, amber orb above, silhouettes watching"),
            alt_fallback=("Papercut sealed document under an amber orb"),
            width="50%",
        )
        st_space("v", "1vh")
        st_write(bs.subtitle, T(_SUBTITLE, lang), tag=t.div)
        st_write(bs.version, T(_VERSION_LINE, lang), " ",
                 citation(*_CITEKEYS), tag=t.div)
