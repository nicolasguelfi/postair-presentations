"""Le seuil de l'annexe BACKUP — jamais présenté, ouvert à la demande.

Même pattern que l'annexe du deck genai (drafts1 ``annexe=p1``, NG
2026-09-01) : les slides de réserve vivent dans le MÊME book, après « Next
deck » et avant References. Cette slide-seuil donne à la barre latérale son
séparateur : tout ce qui suit ne fait pas partie des 20 minutes et ne se
projette que sur une question de la salle — le « pourquoi » du RAG derrière
l'erreur n°1, le cas NotebookLM derrière le récap.

SPEAKER NOTES:
Never shown on purpose. If you page into it by accident, you have finished
the deck — go back one, or jump to a backup the room asked for via the
sidebar search.
"""
# @guideline: postair-minimal

from custom.styles import Styles as s
from postair_lang import T, TF
from streamtex import st_block, st_marker, st_space, st_write
from streamtex.enums import Tags as t


class BlockStyles:
    word = s.project.titles.slide_title + s.center_txt
    hint = s.project.body.caption + s.center_txt


bs = BlockStyles

_MARKER = {"en": "— Backup —", "fr": "— Réserve —"}
_WORD = {"en": ((s.project.titles.keyword, "BACKUP"), " slides"), "fr": ((s.project.titles.keyword, "RÉSERVE"), " de slides")}
_HINT = {"en": "extra depth · opened on demand, never presented", "fr": "approfondissements · ouverts à la demande, jamais présentés"}


def build(lang: str = "en", **_):
    st_marker(T(_MARKER, lang))
    with st_block(s.project.containers.page_fill_top):
        st_space("v", "30vh")
        st_write(bs.word, *TF(_WORD, lang),
                 tag=t.div, toc_lvl="+1", label=T(_MARKER, lang))
        st_space("v", "4vh")
        st_write(bs.hint, T(_HINT, lang), tag=t.div)
