"""What it gets wrong — your data is the raw material (G8c). Série « the other side ».

Réécriture NG (2026-09-02, audit demandé par NG lui-même) : l'ancienne slide
projetait « "Free" = paid with your conversations » SANS SOURCE — le cliché
« si c'est gratuit, c'est vous le produit », faux dans les deux sens (les
abonnements grand public ChatGPT Plus/Pro entraînent AUSSI par défaut ; des
offres gratuites ne monétisent pas les données — objection d'entrepreneur de
NG : d'autres modèles de financement existent et respectent leurs
utilisateurs). Le fait DOCUMENTABLE aux sources PRIMAIRES (les politiques
elles-mêmes, vérifiées le 2026-09-02) : les offres GRAND PUBLIC entraînent
par défaut, gratuites ou payantes, avec opt-out ; les offres API/ENTREPRISE
n'entraînent pas par défaut. La ligne de partage n'est pas l'argent — c'est
le CONTRAT. Le punch (« Read what you sign ») en sort renforcé : c'est
littéralement la leçon des sources.

Composition de série (ex-gabarit ``limit_slide``, NG 2026-08-11) : UNE image
papier découpé dominante à gauche (``hero_split``), UN message en gros, UNE
ligne punch. Les 4 blocs ``bck_genai_limit_*`` partagent cette composition.

Le FAIT vit ici (règle NG 2026-08-18) : label, message, punch, entrées du
panneau et choix des citekeys s'éditent dans ce bloc. La phrase
bibliographique reste dérivée de ``references.bib`` par ``citation()`` — clé
inconnue = erreur bruyante.

SPEAKER NOTES:
One minute. The image says it: your conversations flow into the funnel. Read
the message and let the codes carry the proof — these are the vendors' OWN
policy pages, not a commentary: consumer tiers train by default, free or
PAID, opt-out in the settings; enterprise and API contracts do not. So the
rule is not « avoid free tools » — it is « read what you sign », and keep
personal and sensitive data out of consumer tiers. Echo the coral maxim from
two slides ago: marketing bias — check the claims. Bridge to the
UL-supported tools in the guidelines session.
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
    cite = s.project.body.caption + s.center_txt


bs = BlockStyles

# ── Le revers ───────────────────────────────────────────────────────────────
_MARKER = {"en": "Your data"}
_ICON = "🔐"
_LABEL = {"en": "Your data is the raw material"}
_MESSAGE = {"en": ("Consumer chats train the model — by DEFAULT, "
                   "free or paid")}
_PUNCH = {"en": "Read what you sign · personal / sensitive = OUT"}
_CITEKEYS = ["openai2026-datause", "google2026-gemini-privacy"]

_TOOLTIP = [
    ({"en": "OpenAI, primary source"},
     {"en": ("Personal accounts — Free, Go, Plus AND Pro — train the models "
             "by default; opt-out lives in the privacy portal, Temporary "
             "Chat is excluded. API and enterprise offers do NOT train by "
             "default. Checked 2026-09-02.")}),
    ({"en": "Google, primary source"},
     {"en": ("Consumer Gemini conversations can be read by human reviewers "
             "and used to improve the models; reviewed content is kept up to "
             "three years. Google's own warning: do not enter confidential "
             "information you would not want a reviewer to see. Checked "
             "2026-09-02.")}),
    ({"en": "Free ≠ sold — the honest divide"},
     {"en": ("« Free means you are the product » is a cliché, wrong both "
             "ways: paid consumer tiers train by default too, and some free "
             "offers fund themselves without monetising users. The real "
             "divide is CONSUMER versus ENTERPRISE/API contract — which is "
             "why the rule is « read what you sign », not « avoid free ». "
             "Marketing bias, again: check the claims.")}),
]

# ── L'image papercut ────────────────────────────────────────────────────────
_IMAGE = "genai_data"
_FALLBACK = "images/genai_data_fallback.svg"
_ALT = ("Papercut river of speech bubbles pouring into a funnel feeding an "
        "amber orb, one silhouette watching")
_SCENE = ("A river of colourful paper speech bubbles flowing across the "
          "frame and pouring into a large paper funnel that feeds a glowing "
          "warm amber paper orb; one abstract paper silhouette seen from "
          "behind watches its own speech bubble float away.")


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
        # message + punch empilés à droite — plus rien sous le pli.
        with hero_split(s, image=lambda: staged_hero_image(
                _IMAGE, prompt, _FALLBACK, alt_ready=_ALT, alt_fallback=_ALT,
                variant="sq")):
            st_write(bs.message, T(_MESSAGE, lang), tag=t.div)
            st_write(bs.cite, citation(*_CITEKEYS), tag=t.div)
            st_space("v", "1vh")
            st_write(bs.punch, T(_PUNCH, lang), tag=t.div)
