"""AI in the faculty 3/3 — FHSE (série « AI concerns the whole University »).

Composition de série (ex-gabarit ``faculty_slide``, NG 2026-08-13, 1 idée =
1 slide) : l'image papier découpé carrée à gauche (``hero_split``), à droite
les constats télégraphiques avec leurs codes de citation, et la réserve
d'honnêteté EN CLAIR sur chaque slide de la série. Les 3 blocs
``bck_faculty_*`` partagent cette composition : toute évolution s'y réplique
à la main.

Le FAIT vit ici (règle NG 2026-08-18) : constats, caveats et choix des
citekeys s'éditent dans ce bloc. La phrase bibliographique reste dérivée de
``references.bib`` par ``citation()`` — clé inconnue = erreur bruyante.
Exception : la réserve « no faculty data » est PARTAGÉE par les 3 slides et
reste servie par ``facts.json`` — ce qui sert plusieurs slides vit dans
``custom/``.
"""
# @guideline: postair-minimal

from shared_widgets import st_info_tooltip
from streamtex import st_block, st_grid, st_marker, st_space, st_write, st_zoom
from streamtex.enums import Tags as t

from custom.facts import no_faculty_data, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import hero_image
from postair_i18n import ui
from postair_lang import T
from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    headline = s.project.body.bullet + s.center_txt
    reserve = s.project.body.caption + s.project.colors.amber + s.center_txt


bs = BlockStyles

# ── Réglages de la slide ────────────────────────────────────────────────────
_TITLE_ZOOM = 120   # le sigle en titre
_RATIO = 40         # part de largeur de la colonne image, en %
_ZOOM = 120         # st_zoom de la colonne des constats

# ── La faculté et sa scène ──────────────────────────────────────────────────
_MARKER = {"en": "FHSE"}
_FACULTY = {"en": "Humanities, Education and Social Sciences"}
_SCENE = ("A papercut humanities scene: a pile of colourful paper books, a "
          "paper quill, speech bubbles cut from bright cardstock rising like "
          "a conversation, a glowing warm amber paper orb among them; one "
          "abstract paper silhouette seen from behind.")

# ── Les constats (headline projetée ; detail + caveat dans le tooltip) ──────
_EXAMPLES = [
    {
        "headline": {"en": "non-native writers are detected as AI"},
        "detail": {"en": ("Writing in a second language is read as writing by a "
                   "machine. Seven detectors wrongly flagged 61 % of essays "
                   "by non-native English writers while classifying US "
                   "eighth-grade essays almost perfectly — and rewriting the "
                   "very same essays in richer vocabulary dropped the rate to "
                   "12 %. In a university where most students write in a "
                   "language that is not their first, this is not an "
                   "abstract concern.")},
        "caveat": {"en": ("Pilot study, small samples, detectors mostly built on "
                   "GPT-2. The mechanism it identifies — plain vocabulary "
                   "read as machine-like — is what carries.")},
        "citekeys": ["liang2023-bias"],
        "reported": False,
    },
    {
        "headline": {"en": "Higher scores, lower learning"},
        "detail": {"en": ("Access can raise the score and lower the learning. "
                   "Nearly a thousand school students gained 48 % on "
                   "practice problems with an unguarded GPT-4 tutor and then "
                   "scored 17 % below the control group on the exam they sat "
                   "without it. Constraining the same tutor to hints instead "
                   "of answers removed the loss.")},
        "caveat": {"en": ("School mathematics in Turkey, over weeks. Whether it "
                   "holds over a degree, nobody has measured yet.")},
        "citekeys": ["bastani-guardrails-2025"],
        "reported": False,
    },
    # Rééquilibrage NG 2026-08-19 : le bénéfice vit dans la MÊME étude que la
    # mise en garde au-dessus — le remède mesuré, pas une promesse.
    {
        "headline": {"en": "Hints driven AI tutor: the gain without the loss"},
        "detail": {"en": ("The same field experiment also measured the fix: when "
                   "the GPT-4 tutor was constrained to give hints instead of "
                   "answers, students kept the practice gains and the exam "
                   "loss disappeared.")},
        "caveat": {"en": ("Same population and horizon as the caution beside it: "
                   "school mathematics in Turkey, over weeks.")},
        "citekeys": ["bastani-guardrails-2025"],
        "reported": False,
    },
    {
        "headline": {"en": "Least convinced, least supported"},
        "detail": {"en": ("Arts and humanities students are the most sceptical and "
                   "the least supported: 25 % think AI-written work would "
                   "earn a good grade in their subject, against 46 % in STEM "
                   "— and only 26 % feel their teaching staff help them "
                   "build AI skills, against 53 % in STEM.")},
        "caveat": {"en": ("UK subject areas, which do not map cleanly onto this "
                   "university’s three faculties. Read as a disciplinary "
                   "gradient, not as a faculty measurement.")},
        "citekeys": ["hepi-survey-2026"],
        "reported": False,
    },
]

def build(lang: str = "en", **_):
    marker = T(_MARKER, lang)
    st_marker(marker)
    prompt = AI_PREFIX + _SCENE + AI_SUFFIX_LANDSCAPE
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%",
                     cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                # Le sigle en titre (une ligne) — le nom complet de la
                # faculté vit dans le titre du tooltip.
                with st_zoom(_TITLE_ZOOM):
                    st_write(bs.title, ui("ai_in", lang),
                             (s.project.titles.keyword, marker),
                             tag=t.div, toc_lvl="+1", label=marker)
            with g.cell():
                entries = [(T(ex["headline"], lang),
                            " ".join([T(ex["detail"], lang), T(ex["caveat"], lang)]
                                     + ([ui("reported_note", lang)]
                                        if ex["reported"] else [])))
                           for ex in _EXAMPLES]
                entries.append((ui("no_figures_university", lang),
                                text(no_faculty_data(), lang)))
                st_info_tooltip(
                    title=ui("faculty_evidence", lang).format(
                        faculty=T(_FACULTY, lang)),
                    entries=entries)
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, ratio=_RATIO, zoom=_ZOOM,
                        image=lambda: hero_image(
                            "faculty_fhse", prompt,
                            "images/postair_radar_question.svg",
                            alt_ready=f"Papercut scene for {marker}",
                            alt_fallback=f"Papercut scene for {marker}",
                            variant="sq", width="100%")):
            for ex in _EXAMPLES:
                st_write(bs.headline, "▸ ",
                         T(ex["headline"], lang) + " " + citation(*ex["citekeys"]),
                         tag=t.div)
            st_space("v", "0.5vh")
            st_write(bs.reserve, text(no_faculty_data()["headline"], lang), tag=t.div)
