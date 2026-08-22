"""Une slide « écran du parcours » — capture mobile à gauche, messages à droite.

Mise en page Q14 (NG 2026-08-14) : la capture MOBILE (portrait) occupe la
moitié gauche (~38 %), la moitié droite porte deux à quatre MESSAGES UTILES en
cartes — ce que l'écran montre, le geste à faire, le piège à éviter — et le
titre garde la cellule tooltip de 8 % du gabarit maison. Même pattern de
fabrique de slide que ``faculty_slide.py`` d'opening : les blocs ``bck_screens_*``
ne décrivent que leur contenu, jamais la géométrie.

Les captures sont des écrans RÉELS de l'application (aucune marque DD-35 :
la liste blanche de ``check_export_media.py`` couvre ``media/captures/``),
demandés par slug via ``custom.captures.capture`` — jamais par fichier.
"""

from __future__ import annotations

from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from custom.captures import capture
from custom.styles import Styles as s


class _Styles:
    title = s.project.titles.slide_title + s.center_txt
    head = s.project.body.bullet + s.center_txt + s.bold
    detail = s.project.body.caption + s.center_txt
    caption = s.project.body.mascot_name + s.center_txt


#: La capture mobile est PORTRAIT (~9:19,5) : c'est la HAUTEUR qui borne —
#: à ~62vh de haut, la largeur retombe vers 29vh. Le plafond en vw ne joue
#: que sur une fenêtre étroite, où la carte de droite reprend la place.
CAPTURE_WIDTH = "min(22vw, 29vh)"

#: La capture desktop du diaporama est PAYSAGE (2560×1800, ratio ~1,42) :
#: elle prend toute la scène et les messages passent DESSOUS, en ligne —
#: la moitié gauche de Q14 ne vaut que pour un écran de téléphone. La
#: hauteur borne encore : à 72vh de large, la capture fait ~51vh de haut,
#: ce qui laisse le titre et la ligne de cartes à l'écran.
CAPTURE_WIDTH_LANDSCAPE = "min(44vw, 72vh)"


def screen_slide(title_parts, slug: str, alt: str, messages, *,
                 tooltip: tuple[str, list[tuple[str, str]]] | None = None,
                 toc_label: str | None = None, toc_lvl: str = "+1",
                 device: str = "mobile", theme: str = "sombre",
                 lang: str = "en", caption: str | None = None,
                 landscape: bool = False,
                 zoomImage: int = 100,
                 zoomText: int = 100,
                 crop: tuple[float, float, float, float] | None = None) -> None:
    """Le corps d'une slide écran : titre (+ tooltip), capture, cartes.

    ``title_parts`` suit la convention ``st_write`` (chaînes et couples
    ``(style, texte)``) ; ``messages`` est une liste de ``(tête, détail)`` —
    deux à quatre, pas plus : la salle lit la capture, les cartes la guident.
    ``landscape=True`` (écrans d'opérateur, Q15) : capture pleine scène en
    haut, messages en ligne dessous.

    ``device``/``theme``/``lang`` suivent jusqu'à ``capture()`` (matrice
    complète au catalogue depuis la décision D, NG 2026-08-21) : ``device``
    dit la FORME de la capture (``mobile`` portrait, ``desktop`` paysage — à
    accorder avec ``landscape``), ``theme`` (``sombre``/``clair``) et ``lang``
    (``en``/``fr``/``de``) disent sa peau. Combinaison absente du catalogue =
    KeyError bruyant, comme toujours.

    ``crop`` (streamtex >= 0.7.24) : découpe de la capture par pourcentages,
    ordre CSS ``inset`` — ``(haut, droite, bas, gauche)``. La largeur affichée
    (``CAPTURE_WIDTH``/``_LANDSCAPE``) désigne la zone VISIBLE après découpe.
    Typique : rogner la barre de statut d'une capture mobile ``crop=(4,0,0,0)``.
    """
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                toc = {"toc_lvl": toc_lvl, "label": toc_label} if toc_label else {}
                st_write(_Styles.title, *title_parts, tag=t.div, **toc)
            with g.cell():
                if tooltip:
                    st_info_tooltip(title=tooltip[0], entries=tooltip[1])
        st_space("v", "1vh")
        if landscape:
            with st_zoom(zoomImage):
                st_image(s.project.cards.media_center, width=CAPTURE_WIDTH_LANDSCAPE,
                        uri=capture(slug, device=device, theme=theme, lang=lang),
                        alt=alt, crop=crop)
            if caption:
                st_write(_Styles.caption, caption, tag=t.div)
            st_space("v", "1vh")
            with st_grid(cols=s.project.grids.balanced(len(messages)), gap="1.5vw",
                         grid_style=s.project.grids.stretch,
                         cell_styles=s.project.containers.grid_cell_top) as g:
                for head, detail in messages:
                    with g.cell(), st_block(s.project.cards.blue):
                        with st_zoom(zoomText):
                            st_write(_Styles.head, head, tag=t.div)
                            st_write(_Styles.detail, detail, tag=t.div)
            return
        with st_grid(cols="38% 62%", gap="1.5vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                with st_zoom(zoomImage):
                    st_image(s.project.cards.media_center, width=CAPTURE_WIDTH,
                            uri=capture(slug, device=device, theme=theme, lang=lang),
                            alt=alt, crop=crop)
                if caption:
                    st_write(_Styles.caption, caption, tag=t.div)
            with g.cell(), st_block(s.project.containers.column_stack):
                for head, detail in messages:
                    with st_block(s.project.cards.blue):
                        with st_zoom(zoomText):
                            st_write(_Styles.head, head, tag=t.div)
                            st_write(_Styles.detail, detail, tag=t.div)
