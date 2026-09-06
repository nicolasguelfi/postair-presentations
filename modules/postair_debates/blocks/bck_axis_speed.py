"""Speed ⇄ Prudence — the two poles, their figures, their arguments.

Up to thirteen sub-slides rendered by ``custom.render.axis_slides`` (rhythm
NG 2026-08-31): the two pole identities with their three survey statements,
the debate stage, then per pole the waves that chose it (if any), the three
historical figures who held it (or the absence slide) and three sourced
contemporary arguments. The closing face-off is retired.
Nothing on these slides is written here — everything comes from the frozen
manifest.

SPEAKER NOTES:
The most familiar axis and the one with the sharpest split in a first-year
room. Keep it concrete: not 'should we go fast' but 'who pays if we are
wrong, and can it be undone'. The prudence bench wins on irreversible
harms, the speed bench wins on the cost of waiting — let both land.
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
# - a = pôle ACCÉLÉRATEUR = Vitesse (Speed), b = pôle RALENTISSEUR = Prudence
#   (Prudence) ; waves_* ne se rend que si le
#   gel porte des vagues pour ce pôle. Détail : docstring d'axis_slides.
TUNING: dict = {
    # Identité = la slide des 3 QUESTIONS du sondage (les cartes d'énoncés) + les
    # 2 mascottes du pôle. Réduire les cartes de texte : statement_zoom_scale
    # (ex. 0.85 = calcul auto ×0,85) ou statement_zoom absolu (ex. 95) —
    # l'absolu prime, le laisser à None pour que le facteur agisse.
    "identity_a": {                 # Vitesse (accélérateur)
        "statement_zoom": None,        # auto : 116 (≤6 lignes) / 106 (≤8) / 98
        "statement_zoom_scale": 0.9,  # ex. 1.15 = calcul auto ×1,15
        "mascot_vh": 27.0,             # hauteur des 2 mascottes (vh)
        "mascot_vh_scale": None,
    },
    "identity_b": {                 # Prudence (ralentisseur)
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
        "portrait_width": None,        # auto : min(100 % de la cellule, 75vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie le budget de hauteur (75vh → 75k vh)
    },
    "figure_a2": {
        "quote_zoom": None,            # auto : 100 (≤180 car.) / 90 (≤240) / 80
        "quote_zoom_scale": None,
        "portrait_width": None,        # auto : min(100 % de la cellule, 75vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie le budget de hauteur (75vh → 75k vh)
    },
    "figure_a3": {
        "quote_zoom": None,            # auto : 100 (≤180 car.) / 90 (≤240) / 80
        "quote_zoom_scale": None,
        "portrait_width": None,        # auto : min(100 % de la cellule, 75vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie le budget de hauteur (75vh → 75k vh)
    },
    "figure_b1": {
        "quote_zoom": None,            # auto : 100 (≤180 car.) / 90 (≤240) / 80
        "quote_zoom_scale": None,
        "portrait_width": None,        # auto : min(100 % de la cellule, 75vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie le budget de hauteur (75vh → 75k vh)
    },
    "figure_b2": {
        "quote_zoom": None,            # auto : 100 (≤180 car.) / 90 (≤240) / 80
        "quote_zoom_scale": None,
        "portrait_width": None,        # auto : min(100 % de la cellule, 75vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie le budget de hauteur (75vh → 75k vh)
    },
    "figure_b3": {
        "quote_zoom": None,            # auto : 100 (≤180 car.) / 90 (≤240) / 80
        "quote_zoom_scale": None,
        "portrait_width": None,        # auto : min(100 % de la cellule, 75vh × ratio du FICHIER) — R4d
        "portrait_scale": None,        # k multiplie le budget de hauteur (75vh → 75k vh)
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
    # « Et aujourd'hui pour l'IA ? » = DEUX slides, une par pôle (pas les trois
    # cartes) : arguments_a = la slide de Vitesse, arguments_b = celle de
    # Prudence. Sur une slide, les 3 cartes partagent UN SEUL zoom (règle NG
    # 2026-08-30 : même taille de texte partout) — pas de réglage par carte.
    # zoom absolu (ex. 120) OU zoom_scale (facteur sur l'auto ; laisser zoom à
    # None) ; badge_scale ne touche que le badge de nature.
    "arguments_a": {                # Vitesse (accélérateur)
        "zoom": None,                  # auto : min(240, palier 130/120/110 selon le titre le plus long) ; un absolu passe outre le plafond
        "zoom_scale": 0.95,
        "badge_scale": None,           # facteur du badge de nature (None = taille du DS)
    },
    "arguments_b": {                # Prudence (ralentisseur)
        "zoom": None,                  # auto : min(240, palier 130/120/110 selon le titre le plus long) ; un absolu passe outre le plafond
        "zoom_scale": 0.9,
        "badge_scale": None,           # facteur du badge de nature (None = taille du DS)
    },
}


def build(lang: str = "en", **_):
    axis_slides("speed", lang=lang, tuning=TUNING)
