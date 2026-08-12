"""Affichage POSTAIR — échelle amphi/mobile et profils auto-sélectionnés.

Constat NG (2026-08-12, capture iPhone) : les books POSTAIR calibrent le texte
pour l'amphithéâtre (``base_pt_desktop=30``, ×1,67 du défaut) mais les facteurs
de rétrécissement tablette/mobile de la librairie restaient ceux d'un document
18pt — sur téléphone, les titres sortaient à ~75 px CSS : cinq caractères par
ligne, pendant que les images (en %/vw) se redimensionnaient normalement.

Deux mécanismes COMBINÉS, calibrés ensemble parce qu'ils se multiplient :

1. ``SCALE`` — les facteurs d'échelle par palier (``@media`` 1024/480 px de la
   librairie), ramenés à 0,70/0,55 : couvre tout appareil, même quand la
   détection échoue ou que l'utilisateur reste sur le profil Auditorium.
2. ``PROFILES`` + ``auto_profile()`` — les profils commutables de streamtex
   (le mécanisme de docs.streamtex.org), avec sélection AUTOMATIQUE à
   l'ouverture de session : la librairie n'en a pas (activation par clic
   sidebar uniquement), on la construit avec ``st.context.headers`` —
   ``Sec-CH-UA-Mobile: ?1`` (Chromium) puis repli sur le user-agent (Safari
   iOS). L'utilisateur peut toujours changer de profil à la main ensuite ;
   l'auto ne s'applique qu'UNE fois, jamais par-dessus un choix.

La vraie sélection par résolution (media query côté client) est une évolution
à demander à la librairie — un en-tête HTTP ne connaît pas la largeur d'écran.
"""

from __future__ import annotations

import re

import streamlit as st
from streamtex import ScaleConfig
from streamtex.presentation_profile import (
    _ACTIVE_PROFILE_KEY,
    PageLayout,
    PresentationProfile,
    apply_profile,
)

#: L'échelle des decks : base amphi 30pt, rétrécissement mobile renforcé.
#: 0,55×30 = 16,5pt de corps mobile (~22 px) SANS le profil Mobile ; avec le
#: profil (zoom 60 %), ~13 px effectifs — taille de lecture téléphone normale.
SCALE = ScaleConfig(base_pt_desktop=30, tablet_scale=0.70, mobile_scale=0.55)

#: Auditorium = exactement les réglages historiques des books (pleine largeur,
#: zoom 100). Mobile = pleine largeur, zoom 60 — le préréglage des docs.
PROFILES = [
    PresentationProfile(name="Auditorium", layout=PageLayout(width=100, zoom=100)),
    PresentationProfile(name="Mobile", layout=PageLayout(width=100, zoom=60)),
]

_MOBILE_UA = re.compile(r"iPhone|iPod|Android.+Mobile|Windows Phone", re.I)


def _is_mobile() -> bool:
    try:
        headers = st.context.headers
    except Exception:
        return False
    if headers is None:
        return False
    hint = headers.get("Sec-CH-UA-Mobile") or headers.get("sec-ch-ua-mobile")
    if hint:
        return hint.strip() == "?1"
    return bool(_MOBILE_UA.search(headers.get("User-Agent")
                                  or headers.get("user-agent") or ""))


def auto_profile() -> None:
    """Applique UNE fois le profil adapté à l'appareil — avant ``st_book``.

    Ne fait rien si un profil est déjà actif dans la session : le choix
    manuel de l'utilisateur (sidebar) prime toujours sur la détection.
    """
    if _ACTIVE_PROFILE_KEY in st.session_state:
        return
    if _is_mobile():
        apply_profile(PROFILES[1])
