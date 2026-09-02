"""What it gets wrong — bias (G8a). Série « the other side ».

Ligne éditoriale NG (planche biasline ``bias=p1 perimetre=p1``, 2026-09-02) :
le biais se raconte par le DÉSÉQUILIBRE DES DONNÉES D'ENTRAÎNEMENT —
représentation culturelle et linguistique — l'angle académique, et le plus
pertinent pour un deck sur l'IA GÉNÉRATIVE. L'ancien exemple (Gender Shades,
Buolamwini & Gebru 2018) reste une étude de référence revue par les pairs,
mais c'est une étude de classifieurs de visages 2018 : remplacée ici par un
chiffre PRIMAIRE du constructeur (≈ 93 % de mots anglais dans le corpus
d'entraînement de GPT-3 — statistiques publiées avec l'article) et le
contrepoint honnête formulé par NG : ce n'est pas un biais pour un lecteur
américain — c'est un décalage pour un lecteur chinois, japonais ou iranien.
Cohérence de deck : la slide « détecteurs » d'opening (61 % de non-natifs
lus « IA ») raconte déjà ce déséquilibre linguistique.

Composition de série (ex-gabarit ``limit_slide``, NG 2026-08-11) : UNE image
papier découpé dominante à gauche (``hero_split``), UN message en gros, UNE
ligne de preuve sourcée (code de citation visible). Les blocs
``bck_genai_limit_*`` partagent cette composition. L'image balance
déséquilibrée est CONSERVÉE : un plateau surchargé dit exactement la
sur-représentation d'un monde dans le corpus.

Le FAIT vit ici (règle NG 2026-08-18) : label, message, punch, contrepoint,
détail et choix des citekeys s'éditent dans ce bloc. La phrase
bibliographique reste dérivée de ``references.bib`` par ``citation()`` — clé
inconnue = erreur bruyante.

SPEAKER NOTES:
One minute. Read the 93 % slowly — it is OpenAI's own dataset statistic, not
a commentary. Then the honest turn, in NG's words: for an American reader
this is not even a bias — for a Chinese, Japanese or Iranian reader the
model speaks someone else's world. Make it felt locally: invite the room to
ask the same question in Luxembourgish tonight and compare. Hover the codes
if challenged — the cultural-alignment measurements are in the panel.
"""
# @guideline: postair-minimal

from postair_lang import T
from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_write, st_zoom
from streamtex.enums import Tags as t

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    message = s.project.titles.subtitle + s.center_txt
    punch = s.project.body.body + s.project.colors.amber + s.center_txt + s.bold
    #: La maxime de NG — en gros, corail (rouge visible sans être criard,
    #: le jeton « humain » de la palette), demande NG 2026-09-02.
    maxim = s.project.titles.subtitle + s.project.colors.coral + s.center_txt + s.bold
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Le revers ───────────────────────────────────────────────────────────────
_MARKER = {"en": "Bias"}
_ICON = "⚖️"
_LABEL = {"en": "Trained on WHOSE world?"}
_MESSAGE = {"en": "Mostly the English-speaking, Western web"}
_PUNCH = {"en": "≈ 93 % of GPT-3's training words: English"}
#: LA maxime de NG, projetée en corail (remplace la ligne « mismatch »,
#: demande NG 2026-09-02 — l'ancienne formulation vit au panneau) ; les
#: mesures d'alignement qui la fondent gardent leurs codes visibles dessous.
_MAXIM = {"en": ("Beware of “marketing bias” — the AI is not always aligned "
                 "with its sellers' claims")}
_CITE_PUNCH = ["brown2020-gpt3"]
_CITE_MAXIM = ["santurkar2023-opinions", "cao2023-culture"]

_TOOLTIP = [
    # L'entrée d'ouverture — la phrase de NG (variante B validée 2026-09-02) :
    # le biais vit dans l'écart entre la prétention commerciale et la cible
    # réelle de l'outil, pas dans les poids (fidèles à leur corpus).
    ({"en": "Marketing bias"},
     {"en": ("The pitch says « the world »; the corpus says « the English-"
             "speaking web » — the gap is the bias. Not a bias for an "
             "American reader — a mismatch for a Chinese, Japanese or "
             "Iranian one.")}),
    ({"en": "The primary number — documented, not speculative"},
     {"en": ("92.65 % of GPT-3's training words were English — OpenAI's own "
             "dataset statistics, published with the paper. Recent frontier "
             "corpora are less documented publicly; that opacity is itself "
             "worth saying on stage.")}),
    ({"en": "Culture, measured"},
     {"en": ("On value surveys, aligned models answer closest to US/Western "
             "respondents and diverge from Chinese or Japanese answers "
             "(Hofstede-style probes); on opinion polls, they reflect some "
             "populations far more than others.")}),
    ({"en": "Feel it locally"},
     {"en": ("Ask the same question in Luxembourgish, then in English, and "
             "compare depth and accuracy — under-represented languages get "
             "the leftovers of the training corpus.")}),
    ({"en": "Same story, earlier slide"},
     {"en": ("The opening deck's detector slide (61 % of non-native English "
             "essays flagged as « AI ») is the same data imbalance, seen "
             "from the student's side.")}),
]

# ── L'image papercut ────────────────────────────────────────────────────────
#: L'image balance CONSERVÉE (biasline bias=p1) : le plateau surchargé dit la
#: sur-représentation d'un monde dans le corpus — même scène, autre lecture.
_IMAGE = "genai_bias"
_FALLBACK = "images/genai_mirror_fallback.svg"
_ALT = ("Papercut tilted balance scale, one pan loaded with amber spheres, "
        "a warped paper mirror behind")
_SCENE = ("A large paper balance scale, clearly tilted: one pan low, loaded "
          "with many warm amber paper spheres, the other pan high with a "
          "single small teal sphere. Behind it, a slightly warped paper "
          "mirror leaning against the luminous sky, reflecting the scene "
          "imperfectly.")


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    prompt = AI_PREFIX + _SCENE + AI_SUFFIX_LANDSCAPE
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, _ICON, " ",
                         (s.project.titles.keyword, T(_LABEL, lang)),
                         tag=t.div, toc_lvl="+1", label=T(_LABEL, lang))
            with g.cell():
                st_info_tooltip(title=T(_LABEL, lang),
                                entries=[(T(h, lang), T(d, lang))
                                         for h, d in _TOOLTIP])
        st_space("v", s.project.spacing.title_gap)
        # Gabarit par défaut (NG 2026-08-13) : image carrée à gauche ~50 %,
        # message + punch + contrepoint empilés à droite — rien sous le pli.
        with hero_split(s, image=lambda: staged_hero_image(
                _IMAGE, prompt, _FALLBACK, alt_ready=_ALT, alt_fallback=_ALT,
                variant="sq")):
            st_write(bs.message, T(_MESSAGE, lang), tag=t.div)
            st_space("v", "1vh")
            st_write(bs.punch, T(_PUNCH, lang), " ",
                     citation(*_CITE_PUNCH), tag=t.div)
            st_space("v", "2vh")
            st_write(bs.maxim, T(_MAXIM, lang), tag=t.div)
            st_write(bs.cite, citation(*_CITE_MAXIM), tag=t.div)
