"""Actor, not spectator (G11) — the loop back to the morning.

Composition NG 2026-09-02 (2e retouche) : la ligne des trois compagnons,
AUTONOME sous le titre, puis deux colonnes — l'image de l'horizon à GAUCHE,
et à droite les trois verbes en puces et la citation-boussole de NG avec son
code. The mascots are asked by NAME (``postair_data.mascot``), never by
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
from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    verbs = s.project.titles.subtitle + s.project.colors.amber + s.center_txt
    quote = s.project.titles.subtitle + s.center_txt
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
#: PROJETÉE depuis le 2026-09-02 (demande NG) : la ligne d'accroche de
#: l'ancienne section « actor » de facts.json remonte à l'écran, avec son
#: code de citation (clé ``guelfi-postair`` — la référence de NG).
#: Tri DD-113 (revue genaipat 2026-09-01) : rien sur cette slide ne CITE un
#: bouton ou un écran de l'application sumvadis — « retake the survey » est
#: une phrase du deck, pas un intitulé d'interface : feuilles simples, pas de
#: ``screen()``.
_MARKER = {"en": "Actor", "fr": "Acteur"}
_TITLE = {"en": ((s.project.titles.keyword, "Actor"), ", not spectator"), "fr": ((s.project.titles.keyword, "Acteur"), ", pas spectateur")}
_VERBS = [{"en": "Stay informed", "fr": "Restez informés"}, {"en": "Test things", "fr": "Testez les choses"}, {"en": "Keep doubting", "fr": "Gardez le doute"}]
_QUOTE = {"en": "The revolution is here. Your posture is your compass.", "fr": "La révolution est là. Votre posture est votre boussole."}
#: Les trois compagnons — demandés par leur NOM au cast gelé.
_MASCOTS = ["Kuri", "Solyo", "Lento"]
_MASCOT_WHY = {"en": "Curiosity · optimism · prudence — three postures, together", "fr": "Curiosité · optimisme · prudence — trois postures, ensemble"}
_TIP_TITLE = {"en": "Your posture is your compass", "fr": "Votre posture est votre boussole"}
_TIP = [
    ({"en": "The nine axes", "fr": "Les neuf axes"},
     {"en": ("Trust, optimism, rationality — speed, openness, control — "
             "centralisation, altruism, transhumanism. Your radar from this "
             "morning."), "fr": "Confiance, optimisme, rationalité — vitesse, ouverture, contrôle — centralisation, altruisme, transhumanisme. Votre radar de ce matin."}),
    ({"en": "Not frozen", "fr": "Pas figée"},
     {"en": ("A posture is a position, not an identity: it moves when the "
             "evidence moves. Retake the survey in a year."), "fr": "Une posture est une position, pas une identité : elle bouge quand les preuves bougent. Refaites le questionnaire dans un an."}),
]
_TIP_COMPANIONS = {"en": "Three companions", "fr": "Trois compagnons"}
_CITEKEYS = ["guelfi-postair"]

# ── La main de l'artiste (pattern TUNING debates, revue genaipat 2026-09-01) ─
#: ``ratio`` = part de largeur de l'image du hero_split (gabarit par défaut :
#: 50/50). ``hero_vh`` = budget hauteur de l'image DANS sa cellule (R4d).
#: ``mascot_width`` borne les DEUX dimensions — resserré à la recomposition
#: pyramide 2026-09-02 : DEUX rangées de mascottes dans la colonne droite
#: (l'ancien ``min(7vw, 13vh)`` valait pour une rangée pleine largeur).
#: À confirmer à la repasse visuelle NG.
TUNING = {
    "ratio": 50,
    #: L'image partage désormais la hauteur avec la ligne des compagnons
    #: au-dessus d'elle : budget resserré en conséquence.
    "hero_vh": 48,
    #: Zoom de la colonne de contenu (verbes + citation).
    "column_zoom": 90,
    "mascot_width": "min(6vw, 10vh)",
}


def _companion(name: str) -> None:
    """Une carte compagnon — demandé par son NOM au cast gelé."""
    m = mascot(name)
    st_image(s.project.cards.media_center, width=TUNING["mascot_width"],
             uri=m["image"], alt=f"Mascot {m['name']}",
             overlay=dd35_overlay())
    st_write(bs.mascot_name, m["name"], tag=t.div)


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
        st_space("v", s.project.spacing.title_gap)
        # La ligne des compagnons — AUTONOME, sous le titre (NG 2026-09-02).
        with st_grid(cols=s.project.grids.balanced(len(_MASCOTS)), gap="1vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for name in _MASCOTS:
                with g.cell():
                    _companion(name)
        st_space("v", "1.5vh")
        # Puis deux colonnes : image à GAUCHE, verbes + citation à droite.
        with hero_split(s, ratio=TUNING["ratio"], zoom=TUNING["column_zoom"],
                        image=lambda: staged_hero_image(
                "genai_horizon", _HORIZON_PROMPT, "images/genai_horizon_fallback.svg",
                alt_ready=("Papercut silhouette from behind walking toward a large amber "
                           "sun on the horizon, navy sky"),
                alt_fallback=("Silhouette from behind facing an amber sun on the horizon, "
                              "three small companions beside it"),
                stage_vh=TUNING["hero_vh"])):
            # Les trois verbes — en puces, une par ligne.
            for v in _VERBS:
                st_write(bs.verbs, "▸ ", T(v, lang), tag=t.div)
            st_space("v", "1vh")
            # La citation-boussole de NG, avec son code visible.
            st_write(bs.quote, "« ", T(_QUOTE, lang), " » ",
                     citation(*_CITEKEYS), tag=t.div)
