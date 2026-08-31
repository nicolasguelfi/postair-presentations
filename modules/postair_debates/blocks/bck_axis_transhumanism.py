"""Transhumanism ⇄ Humanism — the two poles, their figures, their arguments.

Seven sub-slides rendered by ``custom.render.axis_slides``: for each pole its
identity and three survey statements, the three historical figures who held
it, and three sourced contemporary arguments; then the two poles face to face.
Nothing on these slides is written here — everything comes from the frozen
manifest.

SPEAKER NOTES:
The axis that makes a room go quiet, so give it room. Avoid science
fiction: start from what already exists — a prosthesis, a pacemaker, a
model that writes in your voice. The line each student draws, and their
reason for drawing it there, is the whole content of this debate.
"""
# @guideline: postair-minimal

from custom.render import axis_slides



# ── Réglages visuels de CET axe (NG 2026-08-31) — la main de l'artiste.
# Gabarit EXHAUSTIF à valeurs NEUTRES (NG 2026-08-31 soir) : tel quel, ce
# dictionnaire ne change RIEN au rendu — éditer librement les champs.
# - None = calcul AUTO de la brique (pour les zooms qui suivent la longueur
#   du texte, aucune valeur fixe n'est neutre ; les paliers auto sont donnés
#   en commentaire à côté) ; les valeurs chiffrées sont les défauts exacts.
# - Chaque paramètre absolu a un jumeau facteur `*_scale` qui multiplie le
#   calcul auto — MAIS l'absolu a priorité : pour utiliser un facteur,
#   remettre l'absolu correspondant à None.
# - a = pôle accélérateur, b = ralentisseur ; waves_* ne se rend que si le
#   gel porte des vagues pour ce pôle. Détail : docstring d'axis_slides.
TUNING: dict = {
    # Identité (les 3 énoncés + les 2 mascottes du pôle).
    "identity_a": {
        "statement_zoom": None,        # auto : 116 (≤6 lignes) / 106 (≤8) / 98
        "statement_zoom_scale": None,  # ex. 1.15 = calcul auto ×1,15
        "mascot_vh": 27.0,             # hauteur des 2 mascottes (vh)
        "mascot_vh_scale": None,
    },
    "identity_b": {
        "statement_zoom": None,        # auto : 116 (≤6 lignes) / 106 (≤8) / 98
        "statement_zoom_scale": None,  # ex. 1.15 = calcul auto ×1,15
        "mascot_vh": 27.0,             # hauteur des 2 mascottes (vh)
        "mascot_vh_scale": None,
    },
    # Scène du débat (mascottes des 2 pôles, énoncés synthétiques, Voxo).
    "stage": {
        "synth_zoom": None,            # auto : 122 (≤100 car.) / 108 (≤130) / 100
        "synth_zoom_scale": None,
        "mascot_vh": 16.0,             # hauteur des mascottes de pôle (vh)
        "mascot_vh_scale": None,
        "voxo_width": "min(15.4vw, 32.2vh)",
        "voxo_scale": None,            # k → min(15.4k vw, 32.2k vh) (voxo_width doit être None)
    },
    # « When society chose » (cartes-titres des vagues).
    "waves_a": {
        "stage_vh": 62.0,              # hauteur max d'une carte-titre (vh)
        "stage_vh_scale": None,
        "caption_zoom": 180,           # zoom de la ligne de légende
        "caption_zoom_scale": None,
    },
    "waves_b": {
        "stage_vh": 62.0,              # hauteur max d'une carte-titre (vh)
        "stage_vh_scale": None,
        "caption_zoom": 180,           # zoom de la ligne de légende
        "caption_zoom_scale": None,
    },
    # « Before us » — une slide par figure (3 par pôle).
    "figure_a1": {
        "quote_zoom": None,            # auto : 100 (≤180 car.) / 90 (≤240) / 80
        "quote_zoom_scale": None,
        "portrait_width": None,        # auto : min(38vw, 66vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie les deux bornes (portrait_width doit être None)
    },
    "figure_a2": {
        "quote_zoom": None,            # auto : 100 (≤180 car.) / 90 (≤240) / 80
        "quote_zoom_scale": None,
        "portrait_width": None,        # auto : min(38vw, 66vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie les deux bornes (portrait_width doit être None)
    },
    "figure_a3": {
        "quote_zoom": None,            # auto : 100 (≤180 car.) / 90 (≤240) / 80
        "quote_zoom_scale": None,
        "portrait_width": None,        # auto : min(38vw, 66vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie les deux bornes (portrait_width doit être None)
    },
    "figure_b1": {
        "quote_zoom": None,            # auto : 100 (≤180 car.) / 90 (≤240) / 80
        "quote_zoom_scale": None,
        "portrait_width": None,        # auto : min(38vw, 66vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie les deux bornes (portrait_width doit être None)
    },
    "figure_b2": {
        "quote_zoom": None,            # auto : 100 (≤180 car.) / 90 (≤240) / 80
        "quote_zoom_scale": None,
        "portrait_width": None,        # auto : min(38vw, 66vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie les deux bornes (portrait_width doit être None)
    },
    "figure_b3": {
        "quote_zoom": None,            # auto : 100 (≤180 car.) / 90 (≤240) / 80
        "quote_zoom_scale": None,
        "portrait_width": None,        # auto : min(38vw, 66vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie les deux bornes (portrait_width doit être None)
    },
    # Pôle sans champion (gel no_champion) : la slide d'absence qui REMPLACE
    # les trois figures — rendue seulement si le gel la déclare.
    "absence_a": {
        "zoom": None,                  # auto : 130 (zoom de la carte d'absence)
        "zoom_scale": None,
    },
    "absence_b": {
        "zoom": None,
        "zoom_scale": None,
    },
    # « And today for AI? » (grille 2+1 des arguments).
    "arguments_a": {
        "zoom": None,                  # auto : min(240, palier 130/120/110 selon le titre le plus long) ; un absolu passe outre le plafond
        "zoom_scale": None,
        "badge_scale": None,           # facteur du badge de nature (None = taille du DS)
    },
    "arguments_b": {
        "zoom": None,                  # auto : min(240, palier 130/120/110 selon le titre le plus long) ; un absolu passe outre le plafond
        "zoom_scale": None,
        "badge_scale": None,           # facteur du badge de nature (None = taille du DS)
    },
}


def build(lang: str = "en", **_):
    axis_slides("transhumanism", lang=lang, tuning=TUNING)
