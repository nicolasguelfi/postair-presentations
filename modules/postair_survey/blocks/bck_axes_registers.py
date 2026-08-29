"""The nine axes, three by three (Knowing / Acting / Becoming).

Three sub-slides (one per register), fully data-driven from the frozen
mascot manifest (postair_data → cast_final.json). Each axis is rendered by
the pack component ``axis_stack``: accelerator pole (teal) on top,
decelerator pole below, same font size for both labels, no nested
responsive grids — the register slide is ONE flat 3-column grid.

SPEAKER NOTES:
One register per slide, ~2 minutes each. Present each axis as a legitimate
tension, not a defect: both poles are respectable postures, and each has a
mascot so nobody has to defend an opinion in person — the mascots carry the
postures. On Becoming, insist that 'accelerator' does not mean 'good'.
"""
# @guideline: postair-minimal

from custom.styles import DS
from custom.styles import Styles as s
from postair_data import REGISTERS, register_axes, register_name
from postair_i18n import ui
from postair_lang import T
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.axis_stack import axis_stack


class BlockStyles:
    register = s.project.titles.register_title + s.center_txt
    subtitle = s.project.titles.subtitle + s.center_txt


bs = BlockStyles

#: Le nom d'un registre vient du glossaire du hub (``register_name``, par
#: clé), son sous-titre de la feuille ``postair_data.REGISTERS`` ; les
#: tooltips ci-dessous sont indexés par CODE. Les têtes « Mascots » viennent
#: du lexique.
_MARKER = {"en": "Axes — {name}", "fr": "Axes — {name}"}
_TIP_TITLE = {"en": "Register: {name}", "fr": "Registre : {name}"}
_TOOLTIPS = {
    "know": [
        ({"en": "Trust vs Self-reliance", "fr": "Confiance vs Autonomie de jugement"},
         {"en": ("Do I rely on institutions, experts and tools — or only on "
                 "my own verified judgement?"), "fr": "Est-ce que je m'appuie sur les institutions, les experts et les outils — ou seulement sur mon propre jugement vérifié ?"}),
        ({"en": "Optimism vs Pessimism", "fr": "Optimisme vs Pessimisme"},
         {"en": "Do I expect AI to improve our lives — or to degrade them?", "fr": "Est-ce que j'attends de l'IA qu'elle améliore nos vies — ou qu'elle les dégrade ?"}),
        ({"en": "Rationality vs Emotion", "fr": "Rationalité vs Émotion"},
         {"en": ("Do I want decisions about AI grounded in measures and "
                 "proofs — or do feelings and intuitions count as much?"), "fr": "Est-ce que je veux des décisions sur l'IA fondées sur des mesures et des preuves — ou les sentiments et les intuitions comptent-ils autant ?"}),
        ("mascots",
         {"en": ("Fido & Solo · Solyo & Nimbo · Logos & Pathos — each mascot carries one "
                 "posture, so opinions are depersonalised: a figure holds a posture, "
                 "not a person."), "fr": "Fido & Solo · Solyo & Nimbo · Logos & Pathos — chaque mascotte porte une posture, ce qui dépersonnalise les opinions : c'est un personnage qui tient une posture, pas une personne."}),
    ],
    "act": [
        ({"en": "Speed vs Prudence", "fr": "Vitesse vs Prudence"},
         {"en": ("Deploy AI as fast as possible — or step by step, only after "
                 "each risk is understood?"), "fr": "Déployer l'IA aussi vite que possible — ou pas à pas, seulement une fois chaque risque compris ?"}),
        ({"en": "Openness vs Resistance", "fr": "Ouverture vs Résistance"},
         {"en": "Welcome AI into my practices — or protect them from it?", "fr": "Accueillir l'IA dans mes pratiques — ou les en protéger ?"}),
        ({"en": "Freedom vs Control", "fr": "Liberté vs Contrôle"},
         {"en": ("Let everyone use AI as they see fit — or regulate its uses "
                 "strictly?"), "fr": "Laisser chacun utiliser l'IA comme il l'entend — ou en réglementer strictement les usages ?"}),
        ("mascots", {"en": "Rapo & Lento · Kuri & Piko · Libero & Guardo.", "fr": "Rapo & Lento · Kuri & Piko · Libero & Guardo."}),
    ],
    "become": [
        ({"en": "Centralisation vs Decentralisation", "fr": "Centralisation vs Décentralisation"},
         {"en": ("Should AI power be concentrated in a few large "
                 "actors — or distributed among many small ones?"), "fr": "Le pouvoir de l'IA doit-il être concentré chez quelques grands acteurs — ou réparti entre de nombreux petits ?"}),
        ({"en": "Individualism vs Altruism", "fr": "Individualisme vs Altruisme"},
         {"en": ("Is AI first a personal advantage — or a common good to "
                 "share?"), "fr": "L'IA est-elle d'abord un avantage personnel — ou un bien commun à partager ?"}),
        ({"en": "Transhumanism vs Humanism", "fr": "Transhumanisme vs Humanisme"},
         {"en": ("Should AI augment and transform the human condition — or "
                 "preserve it?"), "fr": "L'IA doit-elle augmenter et transformer la condition humaine — ou la préserver ?"}),
        ({"en": "Note", "fr": "Note"},
         {"en": ("'Accelerator' never means 'good' — the poles are neutral descriptions of "
                 "postures. Mascots: Balo & Sardo · Ego & Unio · Ultra & Vita."), "fr": "« Accélérateur » ne veut jamais dire « bon » — les pôles décrivent des postures, sans jugement. Mascottes : Balo & Sardo · Ego & Unio · Ultra & Vita."}),
    ],
}


def _entries(code: str, lang: str):
    """Les entrées ``(tête, détail)`` du tooltip d'un registre : une tête
    écrite ``"mascots"`` est une clé du lexique, les autres sont des feuilles.
    (Pas d'annotation générique : règle R14, ``list`` est masqué ici.)"""
    return [(ui(head, lang) if isinstance(head, str) else T(head, lang),
             T(detail, lang)) for head, detail in _TOOLTIPS[code]]


def _register_slide(code: str, subtitle: str, lang: str) -> None:
    name = register_name(code, lang)
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.register, name, tag=t.div, toc_lvl="+1",
                         label=T(_MARKER, lang).format(name=name))
                st_write(bs.subtitle, subtitle, tag=t.div)
            with g.cell():
                st_info_tooltip(title=T(_TIP_TITLE, lang).format(name=name),
                                entries=_entries(code, lang))
        st_space("v", "1.5vh")
        # ONE flat responsive grid — 3 columns on a projector, stacking on
        # narrow windows; each cell is a self-contained axis stack.
        axes_here = register_axes(code, lang=lang)
        # align-start (NG 2026-08-13) : le centrage vertical décalait les
        # colonnes en escalier quand leurs étiquettes n'avaient pas le même
        # nombre de lignes.
        with st_grid(cols=s.project.grids.balanced(len(axes_here)), gap="1.5vw",
                     grid_style=s.project.grids.stretch,
                     cell_styles=s.project.containers.grid_cell_top) as g:
            for axis in axes_here:
                with g.cell():
                    with st_zoom(115):
                        axis_stack(axis, DS, image_width="min(10vw, 13.5vh)")


def build(lang: str = "en", **_):
    first = True
    for code, subtitle, _nums in REGISTERS:
        name = register_name(code, lang)
        if not first:
            st_slide_break(marker_label=T(_MARKER, lang).format(name=name),
                           config=SlideBreakConfig(mode=SlideBreakMode.MARKER_ONLY))
        else:
            st_marker(T(_MARKER, lang).format(name=name))
        _register_slide(code, T(subtitle, lang), lang)
        first = False
