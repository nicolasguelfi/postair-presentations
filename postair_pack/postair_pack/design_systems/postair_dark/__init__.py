"""POSTAIR dark design system — deep-navy auditorium canvas + saturated accents.

Visual line inherited from the FC-260507 deck (navy #1A1A2E, electric blue /
teal / amber / coral dimension accents, keyword-highlight discipline) and
tuned to host the 3D Pixar-style POSTAIR mascots on a dark stage.

All font sizes use ``var(--stx-scale-K, fallback)`` so the whole deck follows
the document ``ScaleConfig`` (auditorium projection uses base_pt_desktop=24,
which maps text_5xl → 48pt bullets and text_8xl → 96pt heroes).

Color semantics (one meaning everywhere — text, marker, wash, image):
- electric blue: primary / opening & framing
- teal: keyword highlight (exactly one per bullet)
- amber: THE single warm focal accent of a slide (never a background)
- coral: human / debate
"""

import math
from functools import lru_cache

from streamtex.styles import Style

# Tooltip palette + geometry (consumed by the shared st_info_tooltip wrapper).
# Auditorium rule (NG 2026-07-29): panel = 2/3 of the viewport in both
# dimensions, content font large enough for the back rows.
# ⚠ st_hover_tooltip REPLACES its default styles when title/term/def overrides
# are given — the font-size MUST therefore be part of these constants.
TOOLTIP_BG = "rgba(26, 34, 48, 0.96)"
TOOLTIP_SCALE = "1.5vw"
TOOLTIP_TITLE_CSS = f"font-size: calc(1.3 * {TOOLTIP_SCALE}); color: #7AB8F5; font-weight: 700;"
TOOLTIP_TERM_CSS = f"font-size: calc(1.1 * {TOOLTIP_SCALE}); color: #2EC4B6; font-weight: 700;"
TOOLTIP_DEF_CSS = f"font-size: calc(1.0 * {TOOLTIP_SCALE}); color: #F2EEE6; line-height: 1.45;"
TOOLTIP_WIDTH = "66vw"
TOOLTIP_MAX_HEIGHT = "66vh"

# Code de citation dans le texte visible (règle NG 2026-08-15) : plus petit
# que le texte PORTEUR (em, donc relatif), italique, gris « muted » de la
# palette. Consommé par le wrapper ``citation()`` de chaque module
# (custom/refs.py) qui l'INLINE dans le fragment HTML de ``cite()`` : le style
# doit voyager avec le fragment — le scaffold bib n'est injecté qu'en mode
# application, l'export HTML statique ne le reçoit pas, et la classe
# ``.stx-cite`` n'enveloppe que le libellé, jamais les parenthèses.
# ``font-weight: 400`` : un code de citation ne prend jamais le gras du texte
# qui le porte.
CITE_CODE_CSS = "font-size: 0.75em; font-style: italic; font-weight: 400; color: #95A5A6;"
# Par défaut le code va À LA LIGNE, en fin de phrase/paragraphe (règle NG
# 2026-08-15) — ``display: block`` suffit, l'alignement suit le porteur.
CITE_CODE_BLOCK_CSS = CITE_CODE_CSS + " display: block; margin-top: 0.2em;"


class _Spacing:
    #: Espace bloc-titre → contenu (règle NG 2026-08-15, calibrée 7vh le même
    #: jour à la projection) : sur toute slide courante — les slides très
    #: chargées (références, captures) gardent leur valeur locale, assumée
    #: dans le bloc.
    title_gap = "7vh"


class _Colors:
    bg_navy = Style("color: #1A1A2E;", "postair_color_bg_navy")
    white = Style("color: #FFFFFF;", "postair_color_white")
    text = Style("color: #F2EEE6;", "postair_color_text")
    primary = Style("color: #7AB8F5;", "postair_color_primary")        # electric blue
    keyword = Style("color: #2EC4B6;", "postair_color_keyword")        # teal
    amber = Style("color: #F39C12;", "postair_color_amber")
    coral = Style("color: #E07A6E;", "postair_color_coral")
    success = Style("color: #27AE60;", "postair_color_success")
    critical = Style("color: #E74C3C;", "postair_color_critical")
    muted = Style("color: #95A5A6;", "postair_color_muted")


class _Titles:
    # Titles and subtitles ×1.5 (NG 2026-07-29) — the multiplier is applied
    # on the responsive scale token so everything still follows ScaleConfig.
    # Chaque gros jeton porte AUSSI un plafond vw (NG 2026-08-12) : sur un
    # écran étroit, la taille devient proportionnelle à la largeur — en
    # projection le jeton pt reste seul maître (le plafond ne mord qu'en
    # dessous de ~1400 px).
    hero = Style(
        "font-size: min(9vw, calc(var(--stx-scale-17, 72pt) * 1.5)); font-weight: 800; letter-spacing: -0.5px; "
        "line-height: 1.1; color: #FFFFFF;",
        "postair_title_hero",
    )
    # Titre de slide sur UNE ligne (NG 2026-08-13) : le ×1.5 historique
    # mangeait 2 lignes et 12 % d'écran sur la moitié des slides — la hauteur
    # gagnée va à l'image. white-space nowrap N'est PAS posé : un titre trop
    # long doit se voir et se raccourcir dans les données, pas se tronquer.
    slide_title = Style(
        "font-size: min(4.6vw, calc(var(--stx-scale-15, 48pt) * 1.1)); font-weight: 700; letter-spacing: -0.5px; "
        "line-height: 1.15; color: #FFFFFF;",
        "postair_title_slide",
    )
    subtitle = Style(
        "font-size: min(5vw, calc(var(--stx-scale-12, 32pt) * 1.5)); font-weight: 400; "
        "line-height: 1.25; color: #7AB8F5;",
        "postair_title_subtitle",
    )
    register_title = Style(
        "font-size: min(8vw, calc(var(--stx-scale-16, 60pt) * 1.5)); font-weight: 800; letter-spacing: -0.5px; "
        "line-height: 1.1; color: #F39C12;",
        "postair_title_register",
    )
    keyword = Style("color: #2EC4B6; font-weight: 700;", "postair_title_keyword")
    # Minutage d'un créneau — sans couleur : elle vient du type de séance, et
    # se compose par-dessus. Bornée par la largeur pour rester dans sa colonne.
    duration = Style(
        "font-size: min(2.8vw, calc(var(--stx-scale-13, 36pt) * 1.4)); font-weight: 800; "
        "line-height: 1.1; text-align: center;",
        "postair_title_duration",
    )


class _Body:
    bullet = Style(
        "font-size: min(4.6vw, var(--stx-scale-13, 36pt)); line-height: 1.5; color: #F2EEE6;",
        "postair_body_bullet",
    )
    body = Style(
        "font-size: min(4.2vw, var(--stx-scale-12, 32pt)); line-height: 1.4; color: #F2EEE6;",
        "postair_body_text",
    )
    # Pole labels of an axis stack — SAME size for both poles (only the
    # color differs: accelerator teal, decelerator white). Responsive:
    # capped by the scale token, shrinks with the viewport, never below 16pt.
    pole_label = Style(
        "font-size: clamp(16pt, 4vw, var(--stx-scale-12, 32pt)); font-weight: 700; color: #FFFFFF; "
        "line-height: 1.2; text-align: center;",
        "postair_body_pole_label",
    )
    pole_label_accel = Style(
        "font-size: clamp(16pt, 4vw, var(--stx-scale-12, 32pt)); font-weight: 700; color: #2EC4B6; "
        "line-height: 1.2; text-align: center;",
        "postair_body_pole_label_accel",
    )
    # Variante compacte (NG 2026-08-13) : pour les grilles serrées — plancher
    # 11pt, plus de césures dans une carte d'un cinquième d'écran.
    pole_label_compact = Style(
        "font-size: clamp(11pt, 1.6vw, 22pt); font-weight: 700; color: #FFFFFF; "
        "line-height: 1.2; text-align: center; overflow-wrap: normal;",
        "postair_body_pole_label_c",
    )
    pole_label_accel_compact = Style(
        "font-size: clamp(11pt, 1.6vw, 22pt); font-weight: 700; color: #2EC4B6; "
        "line-height: 1.2; text-align: center; overflow-wrap: normal;",
        "postair_body_pole_label_accel_c",
    )
    mascot_name = Style(
        "font-size: clamp(12pt, 2.2vw, var(--stx-scale-9, 22pt)); color: #95A5A6; text-align: center;",
        "postair_body_mascot_name",
    )
    # Nom de créneau dans l'agenda : trois colonnes larges, donc plus grand que
    # le corps courant, mais toujours borné par la largeur de sa colonne.
    session_name = Style(
        "font-size: min(2.4vw, var(--stx-scale-13, 36pt)); font-weight: 700; "
        "line-height: 1.25; color: #F2EEE6; text-align: center;",
        "postair_body_session_name",
    )
    caption = Style(
        "font-size: min(3.4vw, var(--stx-scale-9, 22pt)); font-style: italic; color: #95A5A6; opacity: 0.85;",
        "postair_body_caption",
    )
    # Liste courte, sans commentaire, sur une demi-slide : la contrainte n'est
    # plus la place mais la dernière rangée. On monte donc au niveau d'un titre
    # de slide, et on borne par la largeur pour qu'une fenêtre étroite ne fasse
    # pas déborder la ligne.
    bullet_giant = Style(
        "font-size: min(4.2vw, calc(var(--stx-scale-15, 48pt) * 1.25)); font-weight: 700; "
        "line-height: 1.45; color: #F2EEE6;",
        "postair_body_bullet_giant",
    )
    # Nom d'archétype : le double du corps de texte (NG 2026-08-03). Six mots
    # sur une slide, ils doivent se lire depuis le dernier rang.
    name_double = Style(
        "font-size: min(3.6vw, calc(var(--stx-scale-12, 32pt) * 2)); font-weight: 800; "
        "line-height: 1.2; color: #FFFFFF; text-align: center;",
        "postair_body_name_double",
    )


class _Containers:
    page_fill_top = Style(
        "min-height: 88vh; display: flex; flex-direction: column; "
        "justify-content: flex-start; padding: 3vh 3vw 2vh 3vw;",
        "postair_page_fill_top",
    )
    page_fill_center = Style(
        "min-height: 88vh; display: flex; flex-direction: column; "
        "justify-content: center; align-items: center; padding: 3vh 3vw;",
        "postair_page_fill_center",
    )
    # Full-bleed stage (videos, projections): no side padding, children
    # keep 100% width (no align-items constraint).
    page_fill_full = Style(
        "min-height: 88vh; display: flex; flex-direction: column; "
        "justify-content: center; padding: 0;",
        "postair_page_fill_full",
    )
    grid_cell_centered = Style(
        "display: flex; align-items: center; justify-content: center;",
        "postair_grid_cell_centered",
    )
    grid_cell_top = Style(
        "display: flex; align-items: flex-start; justify-content: center;",
        "postair_grid_cell_top",
    )
    # Cellule dont le contenu prend toute la hauteur ET toute la largeur : la
    # colonne devient une vraie colonne, pas une pile posée en haut.
    grid_cell_stretch = Style(
        "display: flex; align-items: stretch; justify-content: stretch;",
        "postair_grid_cell_stretch",
    )
    # Colonne de cartes réparties sur toute la hauteur disponible. Le pendant
    # vertical de la règle d'amphi : on ne tasse pas quatre cartes en haut d'une
    # colonne en laissant les deux tiers du bas vides.
    column_stack = Style(
        "display: flex; flex-direction: column; justify-content: space-between; "
        "gap: 1vh; width: 100%;",
        "postair_column_stack",
    )
    column_stack_centered = Style(
        "display: flex; flex-direction: column; justify-content: center; "
        "gap: 1vh; width: 100%;",
        "postair_column_stack_centered",
    )
    # Média seul en scène, sur TOUTE la fenêtre : pas de titre, pas de marge,
    # rien d'autre à l'écran. Le repère de position sert à poser une mention
    # par-dessus le média sans lui reprendre un seul pixel de hauteur.
    media_fullscreen = Style(
        "position: relative; min-height: 100vh; width: 100%; display: flex; "
        "flex-direction: column; justify-content: center; align-items: center; "
        "padding: 0; margin: 0;",
        "postair_media_fullscreen",
    )
    media_hint_overlay = Style(
        "position: absolute; left: 0; right: 0; bottom: 1.5vh; text-align: center; "
        "pointer-events: none;",
        "postair_media_hint_overlay",
    )

    @staticmethod
    @lru_cache(maxsize=16)
    def media_stage(ratio: float = 1.0, height_vh: int = 84) -> Style:
        """Cadre d'un média projeté, borné par la HAUTEUR de la fenêtre.

        ``st.video`` et ``st.image`` ne se dimensionnent que par la LARGEUR de
        leur conteneur : la hauteur suit le rapport de forme, sans jamais
        consulter la fenêtre. Un clip carré servi sur toute la largeur d'un
        projecteur fait donc presque deux mille pixels de haut — il déborde,
        et redimensionner la fenêtre ne le remet jamais d'aplomb.

        On borne donc la largeur du conteneur par la hauteur disponible :
        ``ratio × height_vh``. Le média occupe alors au plus ``height_vh`` de
        haut, reste centré, et suit les DEUX dimensions de la fenêtre — le
        ``min(…, 100%)`` reprend la main dès que la fenêtre devient étroite.

        ``ratio`` = largeur / hauteur du média : 1 pour un carré, 16/9 pour un
        format large. C'est une propriété du fichier, pas un choix de mise en
        page : la passer fausse produit un cadre trop grand ou trop petit.
        """
        slug = f"{ratio:.3f}".replace(".", "_").replace("-", "_")
        return Style(
            f"width: min({ratio * height_vh:.2f}vh, 100%); "
            f"margin-left: auto; margin-right: auto;",
            f"postair_media_stage_{slug}_{height_vh}",
        )


class _Grids:
    """Grilles plates, réparties sur plusieurs lignes, qui remplissent l'écran.

    Règle d'amphi (NG 2026-08-02) : une slide ne doit jamais montrer **une
    seule ligne de nombreuses cellules minuscules** avec le reste de la hauteur
    vide. ``repeat(auto-fit, minmax(200px, 1fr))`` fait exactement cela sur un
    projecteur large — neuf éléments s'y rangent sur une ligne de 200 px.
    """

    #: Le conteneur de grille prend toute la hauteur restante et distribue ses
    #: lignes à parts égales : deux lignes de cinq occupent l'écran, elles ne se
    #: tassent pas en haut.
    stretch = Style(
        "flex: 1 1 auto; align-content: stretch; grid-auto-rows: 1fr;",
        "postair_grid_stretch",
    )

    @staticmethod
    def columns(count: int, cap: int = 6) -> int:
        """Le nombre de colonnes le plus équilibré pour ``count`` éléments.

        On part de la racine carrée — le rectangle le plus proche du carré —
        et on retient, entre elle et la colonne suivante, celle qui laisse le
        moins de vide sur la dernière ligne : dix-huit pôles donnent trois
        lignes de six, pas quatre lignes de cinq dont une de trois. À égalité
        on garde le moins de colonnes, donc les plus grandes cellules.

        La fenêtre de recherche s'arrête volontairement à la colonne suivante.
        Chercher un diviseur exact plus loin ferait ressortir les nombres
        premiers sur une seule ligne — cinq éléments donneraient cinq colonnes,
        très exactement le défaut qu'on corrige.

        Jusqu'à trois éléments, une seule ligne : les cellules y sont déjà
        larges d'un tiers d'écran, les répartir ne gagnerait rien.
        """
        if count <= 0:
            return 1
        if count <= 3:
            return count
        start = math.ceil(math.sqrt(count))
        candidates = [c for c in (start, start + 1) if c <= cap] or [cap]
        return min(candidates, key=lambda c: (c * math.ceil(count / c) - count, c))

    @staticmethod
    def balanced(count: int, cap: int = 6, min_px: int = 340) -> str:
        """Le ``cols`` d'une grille équilibrée et responsive.

        Le plancher en pourcentage **plafonne** le nombre de colonnes : posé
        entre ``100/n`` et ``100/(n+1)``, il laisse tenir ``n`` colonnes et pas
        une de plus, quelle que soit la largeur de l'écran. Le plancher en
        pixels reprend la main sur une fenêtre étroite et fait retomber la
        grille à moins de colonnes, puis à une seule — la mise en page reste
        donc responsive dans les deux sens, sans point de rupture codé en dur.
        """
        cols = _Grids.columns(count, cap)
        floor_pct = int((100 / cols + 100 / (cols + 1)) / 2)
        return f"repeat(auto-fit, minmax(max({min_px}px, {floor_pct}%), 1fr))"


class _Cards:
    # Reference-card washes: 10% wash + 4px dimension-colored left bar.
    blue = Style(
        "background-color: rgba(122, 184, 245, 0.10); border-left: 4px solid #7AB8F5; "
        "border-radius: 12px; padding: 2vh 1.5vw;",
        "postair_card_blue",
    )
    teal = Style(
        "background-color: rgba(46, 196, 182, 0.10); border-left: 4px solid #2EC4B6; "
        "border-radius: 12px; padding: 2vh 1.5vw;",
        "postair_card_teal",
    )
    amber = Style(
        "background-color: rgba(243, 156, 18, 0.10); border-left: 4px solid #F39C12; "
        "border-radius: 12px; padding: 2vh 1.5vw;",
        "postair_card_amber",
    )
    coral = Style(
        "background-color: rgba(224, 122, 110, 0.10); border-left: 4px solid #E07A6E; "
        "border-radius: 12px; padding: 2vh 1.5vw;",
        "postair_card_coral",
    )
    # Axis pole cell: subtle surface for the mascot tables (register slides).
    # Every child (text AND image) is horizontally centered.
    pole_cell = Style(
        "background-color: rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 1.2vh 0.8vw; "
        "display: flex; flex-direction: column; align-items: center; justify-content: flex-start; "
        "gap: 0.6vh; text-align: center;",
        "postair_card_pole_cell",
    )
    # Centered media inside a stack (images are block elements — flex
    # centering alone does not centre their inner content box).
    media_center = Style(
        "display: block; margin-left: auto; margin-right: auto; text-align: center;",
        "postair_card_media_center",
    )
    @staticmethod
    @lru_cache(maxsize=32)
    def scale_step(index: int, count: int) -> Style:
        """Une marche de l'échelle d'accord : corail à un bout, turquoise à l'autre.

        La couleur est INTERPOLÉE entre les deux accents de la palette, elle
        n'est pas choisie marche par marche : ajouter ou retirer un niveau ne
        demande alors aucune décision graphique, et surtout aucune marche ne
        peut passer pour « la bonne réponse » — le dégradé est continu, donc
        neutre. Il n'y a pas de milieu, et c'est le sujet de la slide.
        """
        span = max(count - 1, 1)
        ratio = min(max(index, 0), span) / span
        coral, teal = (224, 122, 110), (46, 196, 182)
        r, g, b = (round(a + (z - a) * ratio) for a, z in zip(coral, teal))
        return Style(
            f"background-color: rgba({r}, {g}, {b}, 0.16); "
            f"border-left: 6px solid rgb({r}, {g}, {b}); "
            f"border-radius: 10px; padding: 1.1vh 1vw; width: 100%;",
            f"postair_scale_step_{index}_{count}",
        )

    axis_frame = Style(
        "background-color: rgba(122, 184, 245, 0.06); border: 1px solid rgba(122, 184, 245, 0.25); "
        "border-radius: 16px; padding: 1.5vh 1vw;",
        "postair_card_axis_frame",
    )


class _Buttons:
    # Big stage-action button (opens an external operator page). One clear
    # action per line, readable from the presenter's position.
    action_big = Style(
        "display: block; background-color: #7AB8F5; color: #1A1A2E; font-weight: 800; "
        "font-size: calc(var(--stx-scale-12, 32pt) * 1.2); line-height: 1.2; text-align: center; "
        "padding: 2.2vh 1.6vw; border-radius: 18px; margin: 1.2vh 0; "
        "box-shadow: 0 6px 24px rgba(122, 184, 245, 0.35);",
        "postair_button_action_big",
    )
    action_amber = Style(
        "display: block; background-color: #F39C12; color: #1A1A2E; font-weight: 800; "
        "font-size: calc(var(--stx-scale-12, 32pt) * 1.2); line-height: 1.2; text-align: center; "
        "padding: 2.2vh 1.6vw; border-radius: 18px; margin: 1.2vh 0; "
        "box-shadow: 0 6px 24px rgba(243, 156, 18, 0.35);",
        "postair_button_action_amber",
    )
    # La date, à la ligne dans le bouton (NG 2026-08-03). ``display: block``
    # sur le fragment suffit à le faire passer à la ligne : le bouton reste UN
    # seul lien cliquable, ce que deux écritures superposées ne seraient pas.
    action_day = Style(
        "display: block; font-size: calc(var(--stx-scale-10, 26pt) * 1.1); "
        "font-weight: 700; opacity: 0.8; margin-top: 0.4vh;",
        "postair_button_action_day",
    )
    # Bouton unique d'une slide de passage : plus rien d'autre ne le concurrence,
    # il prend donc la place. Borné par la largeur pour ne jamais déborder de sa
    # cellule sur une fenêtre étroite.
    action_amber_giant = Style(
        "display: block; background-color: #F39C12; color: #1A1A2E; font-weight: 900; "
        "font-size: min(4vw, calc(var(--stx-scale-15, 48pt) * 1.3)); line-height: 1.15; "
        "text-align: center; padding: 5vh 2vw; border-radius: 24px; margin: 2vh 0; "
        "box-shadow: 0 10px 40px rgba(243, 156, 18, 0.45);",
        "postair_button_action_amber_giant",
    )


class _Stage:
    # Auditorium-giant tokens (join-code, short URLs).
    code_giant = Style(
        "font-size: calc(var(--stx-scale-17, 72pt) * 1.6); font-weight: 900; "
        "letter-spacing: 0.08em; line-height: 1.05; color: #F39C12; text-align: center;",
        "postair_stage_code_giant",
    )
    url_big = Style(
        "font-size: calc(var(--stx-scale-13, 36pt) * 1.1); font-weight: 700; color: #7AB8F5; "
        "text-align: center;",
        "postair_stage_url_big",
    )
    # Le code caché : même gabarit que le code géant, mais éteint. La slide de
    # démonstration montre la PLACE du code sans jamais montrer un code — un
    # étudiant qui la photographie n'emporte rien d'exploitable.
    code_masked = Style(
        "font-size: calc(var(--stx-scale-17, 72pt) * 1.6); font-weight: 900; "
        "letter-spacing: 0.08em; line-height: 1.05; color: #95A5A6; opacity: 0.55; "
        "text-align: center;",
        "postair_stage_code_masked",
    )
    # L'emplacement du QR sur la même slide : un cadre vide, aux dimensions du
    # vrai, pour que le passage d'une date à l'autre ne fasse pas sauter la
    # mise en page.
    qr_placeholder = Style(
        "width: min(30vw, 52vh); aspect-ratio: 1 / 1; border-radius: 16px; "
        "border: 4px dashed rgba(149, 165, 166, 0.45); "
        "background-color: rgba(255, 255, 255, 0.03); display: flex; "
        "align-items: center; justify-content: center; margin: 0 auto;",
        "postair_stage_qr_placeholder",
    )


class DesignSystem:
    """POSTAIR dark design system (navy canvas, saturated accents, mascot stage)."""

    name = "postair_dark"
    colors = _Colors
    spacing = _Spacing
    titles = _Titles
    body = _Body
    containers = _Containers
    grids = _Grids
    cards = _Cards
    buttons = _Buttons
    stage = _Stage
