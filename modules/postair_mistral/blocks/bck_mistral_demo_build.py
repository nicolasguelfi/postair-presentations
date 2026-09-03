"""Démo A — Construire l'agent (M5, 4' en direct) — la slide relais.

La slide projetée pendant que l'orateur bascule sur Le Chat : les trois
gestes, gros, et le badge LIVE. Le plan B (réseau d'amphi non fiable) : les
3 captures annotées de chaque geste, à produire PENDANT LA RÉPÉTITION dans
Le Chat sur le cours-exemple (décision cours-exemple : NG) — elles rejoindront
l'annexe backup à côté du RAG. D'ici là, cette slide relais EST le secours :
les trois gestes se racontent.

Le FAIT vit ici (règle NG 2026-08-18) : les gestes s'éditent dans ce bloc.
EXCEPTION : le rappel « droits sur les supports » est le fait PARTAGÉ
``charter``/``data`` de facts.json.

SPEAKER NOTES:
Four minutes MAX — the agent is pre-created in duplicate in case anything
fails. Narrate the three gestures while doing them in Le Chat: create the
agent, paste the instructions (the full prompt from the method slide), upload
the course. If the network dies, stay on this slide and tell it — the room
loses nothing essential, the published step-by-step has every click.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, fact, text
from custom.refs import citation
from custom.styles import Styles as s
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    live = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    icon = s.project.titles.subtitle + s.center_txt
    label = s.project.body.bullet + s.center_txt + s.bold
    line = s.project.body.caption + s.center_txt
    warn = s.project.body.caption + s.project.colors.coral + s.center_txt


bs = BlockStyles

_MARKER = {"en": "Demo: build", "fr": "Démo : construire"}
_TITLE = {"en": ("Live: ", (s.project.titles.keyword, "creating the agent")), "fr": ("En direct : ", (s.project.titles.keyword, "créer l’agent"))}
_LIVE = {"en": "▶ LIVE — Le Chat", "fr": "▶ EN DIRECT — Le Chat"}

#: Les trois gestes — tout ce que la salle doit retenir de la manipulation.
_GESTURES = [
    {"icon": "🤖", "label": {"en": "Create the agent", "fr": "Créer l’agent"},
     "line": {"en": "name it after the course", "fr": "nommez-le comme le cours"}},
    {"icon": "📋", "label": {"en": "Paste the instructions", "fr": "Coller les instructions"},
     "line": {"en": "the full text defining the role", "fr": "le texte complet définissant le rôle"}},
    {"icon": "📁", "label": {"en": "Upload the course", "fr": "Téléverser le cours"},
     "line": {"en": "your notes · permitted material only", "fr": "vos notes · matériel permis seulement"}},
]

_WARN = {"en": "⚠ only material you have the right to upload", "fr": "⚠ seulement du matériel que vous avez le droit de téléverser"}

_TIP_TITLE = {"en": "The demo, precisely", "fr": "La démo, précisément"}
_TIP_PATH = ({"en": "The exact path in Mistral", "fr": "Le chemin exact dans Mistral"},
             {"en": ("Le Chat → Agents → Create an agent → name, "
                     "instructions, upload documents → deploy to Le Chat. "
                     "Interfaces move: this path is RE-VERIFIED the week of "
                     "the event, and the published step-by-step follows the "
                     "UI of that week."), "fr": "Le Chat → Agents → Créer un agent → nom, instructions, téléversement des documents → déployer dans Le Chat. Les interfaces bougent : ce chemin est RE-VÉRIFIÉ la semaine de l’événement, et le pas-à-pas publié suit l’interface de cette semaine-là."})
_TIP_FORMATS = ({"en": "Accepted documents", "fr": "Documents acceptés"},
                {"en": ("PDF and text files work everywhere; slides export "
                        "to PDF first. Big scanned PDFs read poorly — your "
                        "own typed notes are the best source the agent can "
                        "get."), "fr": "Les PDF et fichiers texte passent partout ; les slides s’exportent d’abord en PDF. Les gros PDF scannés se lisent mal — vos propres notes tapées sont la meilleure source possible pour l’agent."})
_TIP_RIGHTS_HEAD = {"en": "Whose material? (UL guidelines)", "fr": "Le matériel de qui ? (lignes directrices UL)"}
_TIP_RIGHTS_TAIL = {"en": " Your own notes: always. The professor's slides: ask permission first.", "fr": " Vos propres notes : toujours. Les slides du professeur : demandez d’abord la permission."}

# ── La main de l'artiste ────────────────────────────────────────────────────
TUNING = {
    "card_zoom": 130,
}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    charter = fact("charter", "data")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with st_zoom(150), g.cell():
                st_write(bs.title, *TF(_TITLE, lang),
                         tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(
                    title=T(_TIP_TITLE, lang),
                    entries=[(T(_TIP_PATH[0], lang), T(_TIP_PATH[1], lang)),
                             (T(_TIP_FORMATS[0], lang), T(_TIP_FORMATS[1], lang)),
                             (T(_TIP_RIGHTS_HEAD, lang),
                              text(charter["claim"], lang) + T(_TIP_RIGHTS_TAIL, lang))],
                )
        st_space("v", "1vh")
        with st_zoom(120):
            st_write(bs.live, T(_LIVE, lang), tag=t.div)
        st_space("v", s.project.spacing.title_gap)
        with st_grid(cols=s.project.grids.balanced(len(_GESTURES)), gap="1.2vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            for gesture in _GESTURES:
                with g.cell(), st_block(s.project.cards.blue):
                    with st_zoom(130):
                        st_write(bs.icon, gesture["icon"], tag=t.div)
                    st_space("v", "1.5vh")
                    with st_zoom(TUNING["card_zoom"]):
                        st_write(bs.label, T(gesture["label"], lang), tag=t.div)
                        st_space("v", "1vh")
                        st_write(bs.line, T(gesture["line"], lang), tag=t.div)
        # L'avertissement reste GROS (geste NG) mais borné (porte projection
        # 2026-09-02 : ×1.09/×1.17 — le 250 débordait aux deux références).
        st_space("v", "1.5vh")
        with st_zoom(200):
            st_write(bs.warn, T(_WARN, lang), " ",
                     citation(*citekeys(charter)), tag=t.div)
