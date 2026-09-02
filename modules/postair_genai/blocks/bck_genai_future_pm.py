"""Your place: project manager of your assistants (G10bis).

La slide de la vision NG (2026-08-13) : les assistants génératifs avancés
entrent dans la production professionnelle — la place de l'humain remonte
d'un cran (diriger, juger, assumer) et cette place S'APPREND pendant les
études. La maxime est projetée dans les deux langues : la version anglaise
en ambre porte le message, l'originale française reste sous elle — c'est la
formule de l'auteur, elle se lit telle quelle.

Le FAIT vit ici (règle NG 2026-08-18) : message, maxime et réponse s'éditent
dans ce bloc. EXCEPTION (revue genaipat 2026-09-01) : le fait WEF (55
économies · 39 % · 2030, clé wef2025-jobs) est PARTAGÉ avec
``bck_genai_careers`` — il vit dans ``facts.json`` (section ``jobs``), la
slide garde sa formulation autour de lui. La phrase bibliographique reste
dérivée de ``references.bib`` par ``citation()``/``cite`` — clé inconnue =
erreur bruyante.

SPEAKER NOTES:
Two minutes, right after the careers cards — this is their consequence. Ask
the room the amber question and WAIT three full seconds. Then give the only
honest answer: you cannot. You can only direct what you can judge, and
judgement is built by learning the craft — which is why handing your degree
to the assistant would saw off the branch you will stand on. Bridge to the
actor slide: choosing your posture is choosing how you will direct.
"""
# @guideline: postair-minimal

from custom.facts import citekeys, section, text
from custom.prompts import AI_PREFIX, AI_SUFFIX_LANDSCAPE
from custom.refs import citation
from custom.styles import Styles as s
from custom.visuals import staged_hero_image
from postair_lang import T, TF
from shared_widgets import st_info_tooltip
from streamtex import *
from streamtex.enums import Tags as t

from postair_pack.components.hero_split import hero_split


class BlockStyles:
    title = s.project.titles.slide_title + s.center_txt
    message = s.project.body.bullet + s.center_txt
    punch = s.project.titles.subtitle + s.project.colors.amber + s.center_txt + s.bold
    punch_original = s.project.body.caption + s.center_txt
    answer = s.project.body.body + s.project.colors.keyword + s.center_txt


bs = BlockStyles

_HERO_PROMPT = (
    AI_PREFIX
    + "One abstract paper human silhouette seen from behind, standing on a "
      "small paper podium like an orchestra conductor, arms raised, directing "
      "a team of glowing warm amber paper orbs — plain spheres with no "
      "bodies, no limbs and no faces — each orb floating above its own "
      "little paper desk, and from every desk colourful cut-out paper sheets "
      "fly upward into the luminous sky."
    + AI_SUFFIX_LANDSCAPE
)

# ── La place de l'humain (message projeté ; phrase complète au survol) ──────
_MARKER = {"en": "Your place", "fr": "Votre place"}
_TITLE = {"en": ("All ", (s.project.titles.keyword, "project managers")), "fr": ("Tous ", (s.project.titles.keyword, "chefs de projet"))}
_LABEL = {"en": "You will all be project managers", "fr": "Vous serez tous chefs de projet"}
_MESSAGE = {"en": ("Generative assistants → professional production · your "
                   "place: DIRECT · JUDGE · OWN IT"), "fr": "Assistants génératifs → production professionnelle · votre place : DIRIGER · JUGER · ASSUMER"}
#: La maxime dans les deux langues — l'anglaise en ambre porte le message,
#: l'originale française de l'auteur se lit telle quelle.
_PUNCH = {"en": "How do you have it done, if you do not know how to do it?", "fr": "Comment faire faire, si nous ne savons pas faire ?"}
#: PAS une feuille : la formule ORIGINALE de l'auteur, projetée telle quelle
#: dans les deux langues (comme un nom propre — les données ne se traduisent
#: pas).
_PUNCH_ORIGINAL = "« Comment faire faire, si nous ne savons pas faire ? »"
_ANSWER = {"en": ("You can only direct what you can judge → learn the craft "
                  "DURING your studies"), "fr": "On ne dirige que ce qu’on sait juger → apprenez le métier PENDANT vos études"}
_TIP_HEAD = {"en": "Why this is the hard part", "fr": "Pourquoi c’est la partie difficile"}
#: La suite LOCALE de la phrase du survol — le chiffre WEF et sa phrase
#: viennent du fait partagé ``jobs``/``wef-outlook`` de facts.json.
_DETAIL_LOCAL = {"en": ("Directing an assistant that produces in seconds "
                        "requires exactly what a degree builds: knowing the "
                        "domain well enough to specify, to judge the output, "
                        "and to take responsibility for it."), "fr": "Diriger un assistant qui produit en quelques secondes exige exactement ce qu’un diplôme construit : connaître le domaine assez bien pour spécifier, juger le résultat et en assumer la responsabilité."}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    wef = next(f for f in section("jobs") if f["id"] == "wef-outlook")
    with st_block(s.project.containers.page_fill_top):
        with st_grid(cols="92% 8%", cell_styles=s.project.containers.grid_cell_centered) as g:
            with g.cell():
                st_write(bs.title, *TF(_TITLE, lang), tag=t.div,
                         toc_lvl="+1", label=T(_MARKER, lang))
            with g.cell():
                st_info_tooltip(title=T(_LABEL, lang),
                                entries=[(T(_TIP_HEAD, lang),
                                          text(wef["claim"], lang) + " "
                                          + T(_DETAIL_LOCAL, lang))])
        st_space("v", s.project.spacing.title_gap)
        with hero_split(s, image=lambda: staged_hero_image(
                "genai_conductor", _HERO_PROMPT,
                "images/genai_conductor_fallback.svg",
                alt_ready=("Papercut silhouette on a podium conducting plain amber "
                           "orbs floating above empty paper desks, colourful sheets "
                           "flying upward"),
                alt_fallback=("Papercut conductor silhouette directing amber orbs "
                              "producing paper sheets"),
                variant="sq")):
            st_write(bs.message, T(_MESSAGE, lang), " ",
                     citation(*citekeys(wef)), tag=t.div)
            st_space("v", "1vh")
            with st_block(s.project.cards.amber):
                st_write(bs.punch, T(_PUNCH, lang), tag=t.div)
                # La caption « formule originale » ne s'affiche que si elle
                # DIFFÈRE de la maxime projetée — en FR la feuille EST
                # l'originale, la répéter serait un doublon (i18n 2026-09-02).
                if T(_PUNCH, lang) not in _PUNCH_ORIGINAL:
                    st_write(bs.punch_original, _PUNCH_ORIGINAL, tag=t.div)
            st_space("v", "1vh")
            st_write(bs.answer, T(_ANSWER, lang), tag=t.div)
