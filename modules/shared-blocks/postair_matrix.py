"""La matrice de fonctionnalités — LE mode tableau graphique réutilisable.

Demande NG (plan-services-etudiants §2bis, 2026-09-03) : « un mode tableau
générique réutilisable […] graphique et bien visuel avec des icônes /
symboles / étoiles / médailles dans les cellules et synthétique, et que les
détails apparaissent en tooltip ou en hover […] ou sur une petite icône i
cliquable en dernière colonne ». Concrètement :

- **une ligne = un outil** : logo (fichier servi de ``images/brands/`` ou
  emoji) + nom ; le nom porte le résumé de la ligne au survol (``title``) ;
- **une cellule = UN symbole**, jamais une phrase — le vocabulaire commun :
  ✅ inclus · 💰 payant · 🎓 offre étudiante · ⚠️ limité/nuancé · ❌ absent ·
  ❓ non vérifié à la source (politique « ? » de NG : jamais un ✅/❌ de
  confiance moyenne) · 🥇🥈🥉 médailles · ★★★ niveaux. Chaque cellule porte
  son détail au survol (``title`` natif — lisible aussi dans l'export) ;
- **dernière colonne : ⓘ cliquable/survolable** (``st_hover_tooltip`` maison)
  qui déroule le détail COMPLET de la ligne — chiffres exacts, conditions,
  source officielle datée.

R-zoom : les symboles et textes sont dimensionnés sur les variables d'échelle
(``--stx-scale-N``) — un ``st_zoom`` englobant les suit ; la taille des logos
se règle par ``logo_vh`` (largeur = ratio × vh, leçon R4d).

⚠ Module PARTAGÉ (shared-blocks) : une édition ici exige un redémarrage du
serveur Streamlit (hors du rechargement à chaud des blocs).
"""

from __future__ import annotations

import html as _html

from streamtex import st_grid, st_html, st_image, st_space, st_zoom
from postair_lang import T
from shared_widgets import st_info_tooltip

#: Le vocabulaire des symboles — feuilles {en, fr} pour la légende.
SYMBOLS = [
    ("✅", {"en": "included", "fr": "inclus"}),
    ("💰", {"en": "paid plan", "fr": "abonnement payant"}),
    ("🎓", {"en": "student offer", "fr": "offre étudiante"}),
    ("⚠️", {"en": "limited / nuanced", "fr": "limité / nuancé"}),
    ("❌", {"en": "not available", "fr": "absent"}),
    ("❓", {"en": "unverified at the source", "fr": "non vérifié à la source"}),
]

_CELL_CSS = ("font-size: calc(var(--stx-scale-13, 36pt) * 1.15); "
             "line-height: 1.1; text-align: center; cursor: default;")
_HEAD_CSS = ("font-size: calc(var(--stx-scale-10, 26pt) * 1.0); font-weight: 700; "
             "color: #7AB8F5; text-align: center; line-height: 1.15; cursor: default;")
_NAME_CSS = ("font-size: calc(var(--stx-scale-9, 22pt) * 0.95); font-weight: 700; "
             "color: #F2EEE6; text-align: center; line-height: 1.1; cursor: default;")
_LEGEND_CSS = ("font-size: calc(var(--stx-scale-8, 20pt) * 0.85); color: #95A5A6; "
               "text-align: center;")


#: Le 🎓 sur pastille claire (remarque NG 2026-09-03 : le chapeau noir se
#: perd sur le thème sombre) — appliqué APRÈS échappement, sûr par
#: construction.
_GRAD_CHIP = ('<span style="display:inline-block;background:#F2EEE6;'
              'border-radius:0.45em;padding:0 0.14em;line-height:1.2;">🎓</span>')


def _span(css: str, text: str, hover: str = "") -> str:
    """Un fragment ``st_html`` : texte échappé + détail au survol (title)."""
    title = f' title="{_html.escape(hover, quote=True)}"' if hover else ""
    body = _html.escape(text).replace("🎓", _GRAD_CHIP)
    return f'<div style="{css}"{title}>{body}</div>'


def st_feature_matrix(s, cols, rows, lang: str = "en", *,
                      zoom: int = 100, logo_vh: int = 7,
                      name_col: str = "16%", info_col: str = "7%",
                      row_gap: str = "1.6vh", legend: bool = True,
                      head_zoom: int = 100, col_widths: list | None = None,
                      legend_zoom: int = 100) -> None:
    """La matrice : lignes d'outils × colonnes de fonctionnalités/accès.

    :param s: la façade ``Styles`` du module appelant.
    :param cols: en-têtes de colonnes — feuille ``{en, fr}`` (ou str), tuple
        ``(feuille, feuille_hover)``, ou dict ``{"head": feuille,
        "hover": feuille, "zoom": 120}`` (tune1 h1 : zoom PAR colonne).
    :param rows: une entrée par outil : ``{"name": str, "icon": uri|emoji,
        "icon_ratio": float, "icon_vh": int (option — tune1 l1),
        "hover": feuille, "cells": [...],
        "details": [(feuille_titre, feuille_corps), …]}`` ; une cellule est un
        symbole ``str`` (ou feuille ``{en, fr}``) ou ``(symbole, feuille_hover)``.
    :param lang: la langue projetée, reçue par ``build(lang)``.
    :param zoom: le levier de taille GLOBALE (variables d'échelle).
    :param logo_vh: hauteur des logos (largeur = ratio × vh, R4d) —
        surchargeable par ligne via ``icon_vh``.
    :param legend: imprime la légende des symboles UTILISÉS sous la matrice.
    :param head_zoom: taille des EN-TÊTES de colonnes, en % (tune1 h1) —
        multipliée par le ``zoom`` éventuel de chaque colonne.
    :param col_widths: largeurs CSS des colonnes de features (tune1 w1),
        ex. ``["1fr", "1.4fr", "0.8fr"]`` — ``None`` = toutes égales ;
        erreur bruyante si la longueur ne correspond pas à ``cols``.
    :param legend_zoom: taille de la LÉGENDE, en % (tune1 l1) — découplée du
        zoom de la matrice.
    """
    if col_widths is not None and len(col_widths) != len(cols):
        raise ValueError(
            f"st_feature_matrix : col_widths a {len(col_widths)} largeur(s) "
            f"pour {len(cols)} colonne(s) de features — les deux listes "
            f"doivent correspondre une à une (tune1 w1).")
    features = " ".join(col_widths) if col_widths else f"repeat({len(cols)}, 1fr)"
    grid_cols = f"{name_col} {features} {info_col}"

    def _col_spec(col):
        """(feuille, hover, zoom%) quelle que soit la forme de la colonne."""
        if isinstance(col, dict):
            return col.get("head"), col.get("hover"), col.get("zoom", 100)
        if isinstance(col, tuple):
            return col[0], col[1], 100
        return col, None, 100

    used: list[str] = []
    with st_zoom(zoom):
        with st_grid(cols=grid_cols, gap=f"{row_gap} 0.6vw",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            # ── En-têtes ────────────────────────────────────────────────────
            with g.cell():
                st_space("v", "0.1vh")
            for col in cols:
                head, head_hover, col_zoom = _col_spec(col)
                factor = head_zoom * col_zoom / 10_000
                head_css = (_HEAD_CSS if factor == 1 else _HEAD_CSS.replace(
                    "* 1.0)", f"* {factor:.3f})"))
                with g.cell():
                    st_html(_span(head_css, T(head, lang),
                                  T(head_hover, lang) if head_hover else ""))
            with g.cell():
                st_space("v", "0.1vh")
            # ── Une ligne par outil : l'ICÔNE SEULE quand elle existe, le nom
            # sinon (remarque NG 2026-09-03) — le détail de la ligne vit dans
            # le ⓘ, dont le titre EST le nom de l'outil.
            for row in rows:
                with g.cell():
                    icon = row.get("icon", "")
                    url = row.get("url", "")
                    if icon and ("/" in icon or icon.endswith(".svg")
                                 or icon.endswith(".png") or icon.endswith(".webp")):
                        # tune1 l1 : icon_vh de LA ligne surcharge logo_vh.
                        # Le logo est CLIQUABLE vers la page de l'outil
                        # (demande NG 2026-09-03) — nouvel onglet (LinkConfig).
                        vh = row.get("icon_vh") or logo_vh
                        st_image(s.project.cards.media_center,
                                 width=(f'min({row.get("icon_ratio", 1.0) * vh:.1f}vh,'
                                        f' 12vw)'),
                                 uri=icon, alt=row["name"],
                                 link=url, hover=False)
                    elif icon:
                        st_html(_span(_CELL_CSS, icon))
                    else:
                        name_html = _span(_NAME_CSS, row["name"],
                                          T(row["hover"], lang) if row.get("hover") else "")
                        if url:
                            name_html = (f'<a href="{_html.escape(url, quote=True)}" '
                                         f'target="_blank" rel="noopener" '
                                         f'style="text-decoration: none; color: inherit;">'
                                         f'{name_html}</a>')
                        st_html(name_html)
                for cell in row["cells"]:
                    sym, hover = cell if isinstance(cell, tuple) else (cell, None)
                    # Une cellule porteuse d'unités est une FEUILLE {en, fr}
                    # (remarque NG 2026-09-03 : « 512 Mo » fuyait en anglais).
                    sym = T(sym, lang) if isinstance(sym, dict) else sym
                    if sym and sym not in used:
                        used.append(sym)
                    with g.cell():
                        st_html(_span(_CELL_CSS, sym,
                                      T(hover, lang) if hover else ""))
                with g.cell():
                    # Le ⓘ de la ligne : résumé (l'ex-hover du nom) + détail.
                    entries = ([(row["name"], T(row["hover"], lang))]
                               if row.get("hover") else [])
                    entries += [(T(h, lang), T(b, lang))
                                for h, b in row.get("details", [])]
                    st_info_tooltip(title=row["name"], entries=entries)
        if legend:
            st_space("v", "1.5vh")
            parts = [f"{sym} {T(label, lang)}"
                     for sym, label in SYMBOLS
                     if any(sym in u for u in used)]
            if parts:
                # tune1 l1 : la légende se règle indépendamment de la matrice.
                factor = 0.85 * legend_zoom / 100
                legend_css = (_LEGEND_CSS if legend_zoom == 100 else
                              _LEGEND_CSS.replace("* 0.85)", f"* {factor:.3f})"))
                st_html(_span(legend_css, " · ".join(parts)))
