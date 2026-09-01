"""Actor, not spectator (G11) — the loop back to the morning.

One dominant image — a silhouette facing the amber horizon — and three
mascots walking with it: curiosity, optimism, prudence. One line, three
verbs. The mascots are asked by NAME (``postair_data.mascot``), never by
file.

Le FAIT vit ici (règle NG 2026-08-18) : les trois verbes, les trois mascottes
et le choix des citekeys s'éditent dans ce bloc. La phrase bibliographique
reste dérivée de ``references.bib`` par ``citation()``/``cite`` — clé
inconnue = erreur bruyante.

SPEAKER NOTES:
One minute, almost no words. The morning asked « what is your posture? » ;
this slide answers « whatever it is, it is a compass, not a cage ». Say the
three verbs — stay informed, test things, keep doubting — and let the image
do the rest.
"""
# @guideline: postair-minimal

from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from postair_data import mascot
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.ai_mark import dd35_overlay


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    verbs = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    mascot_name = s.project.body.mascot_name + s.center_txt


bs = BlockStyles

_HORIZON_PROMPT = (
    AI_PREFIX
    + "A lone abstract paper silhouette seen from behind, walking toward a "
      "huge warm amber paper sun low on the horizon of a rolling papercut "
      "landscape, long soft shadows, a wide navy paper sky above."
    + AI_SUFFIX_LANDSCAPE
)

# ── La posture-boussole ─────────────────────────────────────────────────────
#: Jamais projeté, gardé pour la vérifiabilité — la ligne d'accroche de
#: l'ancienne section « actor » de facts.json (entrée ``line``, jamais
#: consommée par le rendu) : « The revolution is here. Your posture is your
#: compass. »
#: Tri DD-113 (revue genaipat 2026-09-01) : rien sur cette slide ne CITE un
#: bouton ou un écran de l'application sumvadis — « retake the survey » est
#: une phrase du deck, pas un intitulé d'interface : feuilles simples, pas de
#: ``screen()``.
_MARKER = {"en": "Actor"}
_TITLE = {"en": ((s.project.titles.keyword, "Actor"), ", not spectator")}
_VERBS = [{"en": "Stay informed"}, {"en": "Test things"}, {"en": "Keep doubting"}]
#: Les trois compagnons — demandés par leur NOM au cast gelé.
_MASCOTS = ["Kuri", "Solyo", "Lento"]
_MASCOT_WHY = {"en": "Curiosity · optimism · prudence — three postures, together"}
_TIP_TITLE = {"en": "Your posture is your compass"}
_TIP = [
    ({"en": "The nine axes"},
     {"en": ("Trust, optimism, rationality — speed, openness, control — "
             "centralisation, altruism, transhumanism. Your radar from this "
             "morning.")}),
    ({"en": "Not frozen"},
     {"en": ("A posture is a position, not an identity: it moves when the "
             "evidence moves. Retake the survey in a year.")}),
]
_TIP_COMPANIONS = {"en": "Three companions"}
_CITEKEYS = ["guelfi-postair"]

# ── La main de l'artiste (pattern TUNING debates, revue genaipat 2026-09-01) ─
#: ``hero_vh`` = budget hauteur de l'image héro (staged_hero_image, R4d) —
#: remplace l'ancien ``width="62%"``, inerte au zoom : titre + verbes +
#: rangée de mascottes doivent tenir sous elle. ``mascot_width`` borne les
#: DEUX dimensions (l'ancien ``7vw`` n'avait pas de borne verticale — geste
#: guidelines ``min(7vw, 13vh)``). À confirmer à la repasse visuelle NG.
TUNING = {
    "hero_vh": 50,
    "mascot_width": "min(7vw, 13vh)",
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[*[(T(h, lang), T(d, lang)) for h, d in _TIP],
                             (T(_TIP_COMPANIONS, lang), T(_MASCOT_WHY, lang))],
                )
        st_space("v", "1vh")
        staged_hero_image(
            "genai_horizon", _HORIZON_PROMPT, "images/genai_horizon_fallback.svg",
            alt_ready=("Papercut silhouette from behind walking toward a large amber "
                       "sun on the horizon, navy sky"),
            alt_fallback=("Silhouette from behind facing an amber sun on the horizon, "
                          "three small companions beside it"),
            stage_vh=TUNING["hero_vh"],
        )
        st_space("v", "1vh")
        st_write(bs.verbs,
                 " · ".join(T(v, lang) for v in _VERBS), "   ",
                 citation(*_CITEKEYS), tag=t.div)
        st_space("v", "1.5vh")
        # Les trois compagnons — demandés par leur NOM au cast gelé.
        with st_grid(cols=s.project.grids.balanced(len(_MASCOTS)), gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for name in _MASCOTS:
                m = mascot(name)
                with g.cell():
                    st_image(s.project.cards.media_center, width=TUNING["mascot_width"],
                             uri=m["image"], alt=f"Mascot {m['name']}",
                             overlay=dd35_overlay())
                    st_write(bs.mascot_name, m["name"], tag=t.div)
