"""Le seuil de l'annexe BACKUP — jamais présenté, ouvert à la demande.

Décision NG (planche drafts1 2026-09-01, ``annexe=p1`` + ``mecanisme=p1``) :
les slides de réserve vivent dans le MÊME book, après « Next deck » et avant
References — le pattern de ``bck_refs_bibliography`` (« never presented;
opened when challenged »), étendu en zone. Cette slide-seuil donne à la barre
latérale son séparateur : tout ce qui suit ne fait pas partie du fil de la
séance et ne se projette que sur une question de la salle.

Rien n'a été supprimé : les quatre slides « augmentation » (Diagnosis, The
twist, Justice, In the lab) ont DÉMÉNAGÉ ici, intactes, pour recentrer le
flux sur la compréhension du génératif (consigne NG du même jour : « ne
supprime aucun des slides actuels »).

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
