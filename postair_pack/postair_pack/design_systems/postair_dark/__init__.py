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
    hero = Style(
        "font-size: calc(var(--stx-scale-17, 72pt) * 1.5); font-weight: 800; letter-spacing: -0.5px; "
        "line-height: 1.1; color: #FFFFFF;",
        "postair_title_hero",
    )
    slide_title = Style(
        "font-size: calc(var(--stx-scale-15, 48pt) * 1.5); font-weight: 700; letter-spacing: -0.5px; "
        "line-height: 1.15; color: #FFFFFF;",
        "postair_title_slide",
    )
    subtitle = Style(
        "font-size: calc(var(--stx-scale-12, 32pt) * 1.5); font-weight: 400; line-height: 1.25; color: #7AB8F5;",
        "postair_title_subtitle",
    )
    register_title = Style(
        "font-size: calc(var(--stx-scale-16, 60pt) * 1.5); font-weight: 800; letter-spacing: -0.5px; "
        "line-height: 1.1; color: #F39C12;",
        "postair_title_register",
    )
    keyword = Style("color: #2EC4B6; font-weight: 700;", "postair_title_keyword")


class _Body:
    bullet = Style(
        "font-size: var(--stx-scale-13, 36pt); line-height: 1.5; color: #F2EEE6;",
        "postair_body_bullet",
    )
    body = Style(
        "font-size: var(--stx-scale-12, 32pt); line-height: 1.4; color: #F2EEE6;",
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
    mascot_name = Style(
        "font-size: clamp(12pt, 2.2vw, var(--stx-scale-9, 22pt)); color: #95A5A6; text-align: center;",
        "postair_body_mascot_name",
    )
    caption = Style(
        "font-size: var(--stx-scale-9, 22pt); font-style: italic; color: #95A5A6; opacity: 0.85;",
        "postair_body_caption",
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
    def balanced(count: int, cap: int = 6, min_px: int = 200) -> str:
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


class DesignSystem:
    """POSTAIR dark design system (navy canvas, saturated accents, mascot stage)."""

    name = "postair_dark"
    colors = _Colors
    titles = _Titles
    body = _Body
    containers = _Containers
    grids = _Grids
    cards = _Cards
    buttons = _Buttons
    stage = _Stage
