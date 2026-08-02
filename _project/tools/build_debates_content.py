"""Build the content manifest of the `postair_debates` module.

The debate deck is **entirely data-driven** (design-guideline rule "data-driven"):
no figure name, quote, reference or argument is ever typed into a block. This
tool joins the four upstream sources and freezes the join into

    modules/postair_debates/static/data/content.json

It lives inside the module, not in the shared static tree: only this document
consumes it, and the deploy workflow redeploys ALL services when a shared file
changes but only one when the change is under ``modules/postair_<name>/``. The
manifest is regenerated at every upstream correction — sharing it would mean
redeploying five production services for a bibliographic fix.

Sources (all read-only, paths from ``debates-hub.config.local.json``):

  ai-social-profiles/questionnaire/debate-deck.json
      The 54 statements, each with its axis, its two poles and their
      accelerator/decelerator effect, and — per statement — the sourced
      arguments for and against. Generated from ``debate.json``, the same
      source as the ``debate-annex-*.tex`` annexes.
  great-figures/profiles/<id>.json
      Each figure's 54 inferred answers. The axis scores recomputed here
      reproduce ``great-figures/report/gen-master-table.tex`` exactly.
  great-figures/quote-ledger.json + editorial/<id>.json
      Verbatim quotes, each mapped to the statements it documents; the
      editorial layer adds a French translation and a precise reference.
  great-figures/media-manifest.json
      Portrait and presentation-video renditions, with clearance.

Selection rule — see `_project/plans/plan-postair_debates.md`.

Usage
-----
    uv run python _project/tools/build_debates_content.py            # write the manifest
    uv run python _project/tools/build_debates_content.py --report   # markdown dry run
"""

from __future__ import annotations

import argparse
import collections
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

_TOOLS = Path(__file__).parent
_REPO = _TOOLS.parent.parent
_OUT = _REPO / "modules" / "postair_debates" / "static" / "data" / "content.json"

# Pedagogical order of the axes — the three registers of the instrument.
AXIS_ORDER = ["trust", "optimism", "rationality",          # Knowing
              "speed", "openness", "control",              # Acting
              "centralisation", "altruism", "transhumanism"]  # Becoming
REGISTER = {a: r for r, axes in (("Knowing", AXIS_ORDER[:3]),
                                 ("Acting", AXIS_ORDER[3:6]),
                                 ("Becoming", AXIS_ORDER[6:])) for a in axes}

FIGURES_PER_POLE = 3
ARGUMENTS_PER_POLE = 3
#: A figure may carry at most this many poles, so the deck spreads over the
#: whole study instead of replaying the same half-dozen extreme profiles.
MAX_POLES_PER_FIGURE = 2
#: Beyond this distance to the pole (0 = perfectly on it) a figure no longer
#: "represents" it. Relaxed, with a warning, when a pole cannot be filled.
MAX_DISTANCE = 40
#: Quotes must read on a slide seen from the back of an auditorium. This one IS
#: ours: a length limit is a property of the room, not of the corpus.
QUOTE_MIN, QUOTE_MAX = 60, 300

#: Some ledger entries are an analyst's synthesis rather than a quotation. The
#: hub decides that — ``quote-ledger.json`` >= 1.1.0 flags them ``analyst_note``
#: and counts them in ``coverage.analyst_note_suspect``. We only read the flag;
#: re-deriving it here would be a second opinion on someone else's data.
_LEDGER_MIN_VERSION = "1.3.0"
#: Caption budget for a reference under a portrait, in characters. Median of the
#: displayed references is 29; six ran past 120 before this cap existed.
REFERENCE_MAX = 90


def load_config() -> dict[str, str]:
    local = _TOOLS / "debates-hub.config.local.json"
    if not local.exists():
        raise SystemExit(f"missing {local} — copy debates-hub.config.example.json and fill it in")
    return json.loads(local.read_text(encoding="utf-8"))


#: Hub paths whose uncommitted state would be frozen into the manifest.
_HUB_GATE_PATHS = ["questionnaire", "great-figures"]


def warn_if_hub_dirty(hub_root: str) -> None:
    """Say so when the join would photograph work in progress.

    ``sync_upstream.py`` (hub -> sumvadis) REFUSES on a dirty upstream, because
    it publishes to an application. This tool only freezes a slide deck, and the
    campaign sessions that correct the corpus regenerate ``quote-ledger.json``
    dozens of times before committing — refusing would make the mandatory
    before/after control unusable. So: warn, loudly, and let the author decide.
    A silent freeze is the failure mode worth preventing, not a dirty tree.
    """
    try:
        r = subprocess.run(["git", "-C", hub_root, "status", "--porcelain", "--"]
                           + _HUB_GATE_PATHS, capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return                       # not a git tree here: nothing to assert
    dirty = [ln for ln in r.stdout.splitlines() if ln.strip()]
    if not dirty:
        return
    print(f"! hub has {len(dirty)} uncommitted change(s) on {'/'.join(_HUB_GATE_PATHS)} — "
          "this build freezes work in progress:", file=sys.stderr)
    for line in dirty[:10]:
        print(f"    {line}", file=sys.stderr)
    if len(dirty) > 10:
        print(f"    … and {len(dirty) - 10} more", file=sys.stderr)


def _norm(text: str) -> str:
    return "".join(c for c in text.lower() if c.isalnum())[:60]


def _verification_tier(v: str | None) -> int:
    v = (v or "").lower()
    if "source verified" in v or "verified via" in v:
        return 0
    return 1 if v.startswith("verbatim") else 2


def _local_media(url: str | None) -> str | None:
    """L'URI locale d'une image du CDN, telle que la slide doit la demander.

    Le conteneur doit être autonome pendant la séance : les images sont
    matérialisées sous ``static/media/figures/`` par ``sync_media.py`` et servies
    par le conteneur lui-même. L'URI reste RELATIVE et introuvable via les
    sources statiques — sans quoi ``st_image`` encoderait le fichier en base64 et
    les 54 portraits pèseraient ~23 Mo dans la page, contre 2,7 Ko en URL.

    L'URL du CDN est conservée à côté (``*_cdn``) : c'est la provenance, et le
    repli si la matérialisation n'a pas eu lieu.
    """
    if not url:
        return None
    return "figures/" + url.rsplit("/", 1)[-1]


def _reference(q: dict, match: dict | None) -> str | None:
    """The complete reference of a quote, in order of authority.

    Curated editorial source first; then, when the dossier cited a source by
    key, the definition the hub resolved — never the bare key. Prose spilled
    into the ref field counts as no reference at all: it goes out as None so
    the slide shows the reserve and the work order picks it up, exactly like a
    reference still to be found.
    """
    src = q.get("source") or {}
    return ((match or {}).get("source")
            or src.get("resolved")
            or (None if q.get("source_status") == "prose" else src.get("ref")))


def _short_reference(reference: str | None, limit: int = REFERENCE_MAX) -> str | None:
    """The caption form: what fits under a portrait, read from the back row.

    A dossier's ``## Sources`` entry is written to be complete, not to be
    projected — the longest of the displayed references runs to 187 characters,
    against a median of 29. Cutting at the first clause boundary past the limit
    keeps the identifying head (work, venue, date) and drops the qualifying
    tail. Nothing is lost: the slide carries the full form in its tooltip.
    """
    if not reference or len(reference) <= limit:
        return reference
    head = reference[:limit]
    cut = max(head.rfind(", "), head.rfind(" ("), head.rfind(" — "), head.rfind("; "))
    if cut < limit // 2:                      # no usable boundary: fall back to a word
        cut = head.rfind(" ")
    return reference[:cut].rstrip(" ,;—(") + " …"


class Hub:
    """Read-only view over the four upstream sources."""

    def __init__(self, hub: str) -> None:
        root, gf = Path(hub), Path(hub) / "great-figures"
        deck = json.loads((root / "questionnaire" / "debate-deck.json").read_text(encoding="utf-8"))
        self.deck_version = deck["debate_version"]
        self.instrument_version = deck["questionnaire_version"]
        self.cards = {c["id"]: c for c in deck["cards"]}
        self.axis_of = {i: c["axis"]["id"] for i, c in self.cards.items()}
        self.axis = {c["axis"]["id"]: c["axis"] for c in self.cards.values()}
        self.items = collections.defaultdict(list)
        for i, c in self.cards.items():
            self.items[c["axis"]["id"]].append(i)
        for a in self.items:
            self.items[a].sort()

        figures = json.loads((gf / "figures.json").read_text(encoding="utf-8"))
        self.figure = {f["id"]: f for f in figures["figures"]}
        self.wave = {w["id"]: w for w in figures["waves"]}
        self.media = json.loads((gf / "media-manifest.json").read_text(encoding="utf-8"))["figures"]
        ledger = json.loads((gf / "quote-ledger.json").read_text(encoding="utf-8"))
        version = ledger.get("version", "0")
        if tuple(int(n) for n in version.split(".")) < tuple(
                int(n) for n in _LEDGER_MIN_VERSION.split(".")):
            # Silently falling back would mean re-deriving the hub's own
            # judgements here — exactly what this version brought to an end.
            raise SystemExit(
                f"quote-ledger.json is v{version}, this tool needs >= v{_LEDGER_MIN_VERSION} "
                f"(publication-readiness fields). Regenerate it in the hub: "
                f"python3 great-figures/tools/quote_ledger.py")
        self.ledger_coverage = ledger.get("coverage", {})
        self.ledger = {f["id"]: f["quotes"] for f in ledger["figures"]}
        self.editorial = {}
        for path in sorted((gf / "editorial").glob("*.json")):
            e = json.loads(path.read_text(encoding="utf-8"))
            self.editorial[e["id"]] = e
        self.scores = {}
        for path in sorted((gf / "profiles").glob("*.json")):
            p = json.loads(path.read_text(encoding="utf-8"))
            self.scores[p["figure"]] = self._axis_scores(p["responses"])

    def _axis_scores(self, responses: dict[str, Any]) -> dict[str, float]:
        """0 = fully the left pole, 100 = fully the right pole (master-table scale)."""
        acc = collections.defaultdict(list)
        for item, value in responses.items():
            if value == "NSP" or item not in self.cards:
                continue
            acc[self.axis_of[item]].append(value if self.cards[item]["polarity"] == 1 else 5 - value)
        return {a: sum(v) / len(v) / 5 * 100 for a, v in acc.items() if len(v) >= 3}

    def pole_items(self, axis: str, side: str) -> list[str]:
        """The three statements whose *agreement* pushes toward `side`."""
        return [i for i in self.items[axis]
                if ("right" if self.cards[i]["polarity"] == 1 else "left") == side]

    def quote(self, fid: str, axis: str, side: str) -> dict | None:
        """The figure's best displayable quote documenting this pole."""
        curated = {_norm(q["text"]["en"]): q
                   for q in (self.editorial.get(fid, {}).get("quotes") or [])
                   if q.get("text", {}).get("en")}
        on_pole, ranked = set(self.pole_items(axis, side)), []
        for q in self.ledger.get(fid, []):
            text = q["text"]
            items = {i for i in (q.get("axis_items") or []) if self.axis_of.get(i) == axis}
            if not items or q.get("grade") != "verbatim":
                continue
            if q.get("extraction_confidence") != "exact" or q.get("analyst_note"):
                continue
            if not QUOTE_MIN <= len(text) <= QUOTE_MAX:
                continue
            # A reference that is merely pending can still be selected — it is
            # reported as a warning and resolved upstream; prose spilled into
            # the ref field is that same case, a repair job, so it must not cost
            # the corpus its best quote. Only a key pointing at nothing is
            # unusable. A key the hub resolved is a complete reference.
            if q.get("source_status") == "unresolved-key":
                continue
            match = curated.get(_norm(text))
            ranked.append(((0 if items & on_pole else 1),      # documents THIS pole
                           (0 if match else 1),                # bilingual + precise reference
                           _verification_tier(q.get("verification")),
                           abs(len(text) - 150),               # closest to the ideal slide length
                           q, match, sorted(items)))
        if not ranked:
            return None
        ranked.sort(key=lambda r: r[:4])
        *_, q, match, items = ranked[0]
        full = _reference(q, match)
        return {"en": (match or {}).get("text", {}).get("en") or q["text"],
                "fr": (match or {}).get("text", {}).get("fr"),
                "reference": _short_reference(full),
                "reference_full": full,
                "curated": bool(match), "documents": items,
                "verification": q.get("verification")}

    def assets(self, fid: str, lang: str = "en") -> dict | None:
        """Portrait + presentation video, only if both are cleared for public use.

        Two kinds of presentation video coexist upstream, and the difference is
        editorial, not technical: a historical figure gets a synthetic *talk*
        (``<id>__talk__<lang>.mp4``), whereas a **living** person is never made
        to speak by generative AI — they are *presented* by the author instead
        (``ng__presente__<id>__<lang>.mp4``). The kind is carried through to the
        slide so the caption can state which one the audience is watching.
        """
        entry = self.media.get(fid)
        if not entry:
            return None
        out: dict[str, Any] = {}
        for a in entry["assets"]:
            if a.get("clearance", {}).get("channel") != "public-ok":
                continue
            if a["role"] == "portrait":
                out["portrait"] = _local_media(a["renditions"].get("web-512"))
                out["portrait_cdn"] = a["renditions"].get("web-512")
                out["portrait_source"] = a["source"]
            elif a["role"] == "video" and a["source"].endswith(f"__{lang}.mp4"):
                name = a["source"].rsplit("/", 1)[-1]
                kind = "presented" if name.startswith("ng__presente__") else "talk"
                if out.get("video") and out.get("video_kind") == "talk":
                    continue                      # a figure's own talk wins
                # Les vidéos restent au CDN : 51 masters de 12 Mo, ouverts deux
                # ou trois fois dans la séance. Les embarquer coûterait 612 Mo
                # pour une interaction ponctuelle — les images, elles, sont à
                # l'écran en permanence et valent leurs 35 Mo.
                out["video"] = a.get("url")
                out["video_kind"] = kind
                out["video_light"] = (a.get("renditions") or {}).get("video-050")
                out["poster"] = _local_media(a.get("poster"))
                out["poster_cdn"] = a.get("poster")
        return out if out.get("portrait") and out.get("video") else None

    def arguments(self, axis: str, side: str, k: int) -> tuple[list[dict], int]:
        """Contemporary arguments supporting this pole, from the debate annex material.

        A statement's "in favour" box supports the pole its polarity points to;
        its "against" box supports the opposite pole.
        """
        pool = []
        for cid, card in self.cards.items():
            if card["axis"]["id"] != axis:
                continue
            agrees_with = "right" if card["polarity"] == 1 else "left"
            box = "pro" if agrees_with == side else "contra"
            for e in (card.get(box) or []):
                pool.append({"statement": cid, "category": e["category"],
                             "title": e["title"], "person": e.get("person"),
                             "text": e["text"], "reference": e.get("source_detail"),
                             "citekey": e.get("ref"), "paraphrase": e.get("paraphrase"),
                             "quote": ((e.get("quotes") or [{}])[0]).get("text")})
        # One argument per category, so the three are of three different natures.
        picked: list[dict] = []
        speakers: set[str] = set()
        for category in ("policy", "case", "quote", "historical", "tradition"):
            for e in pool:
                if len(picked) == k:
                    break
                if e["category"] != category or any(p["category"] == category for p in picked):
                    continue
                if e["person"] and e["person"] in speakers:
                    continue
                picked.append(e)
                speakers.add(e["person"] or "")
        for e in pool:                                   # top up if a category was absent
            if len(picked) == k:
                break
            if e in picked or (e["person"] and e["person"] in speakers):
                continue
            picked.append(e)
            speakers.add(e["person"] or "")
        return picked, len(pool)


def build(hub: Hub) -> dict:
    used: collections.Counter[str] = collections.Counter()
    poles, warnings = [], []
    for axis in AXIS_ORDER:
        meta = hub.axis[axis]
        for side in ("left", "right"):
            pole = meta[f"pole_{side}"]
            candidates = []
            for fid, scores in hub.scores.items():
                if axis not in scores:
                    continue
                distance = (100 - scores[axis]) if side == "right" else scores[axis]
                quote, assets = hub.quote(fid, axis, side), hub.assets(fid)
                if quote and assets:
                    candidates.append((distance, fid, quote, assets))
            candidates.sort(key=lambda c: c[0])

            for limit in (MAX_DISTANCE, 100):
                picked: list[dict] = []
                for cap in range(1, MAX_POLES_PER_FIGURE + 1):
                    for distance, fid, quote, assets in candidates:
                        if len(picked) == FIGURES_PER_POLE:
                            break
                        if distance > limit or used[fid] >= cap:
                            continue
                        if any(p["id"] == fid for p in picked):
                            continue
                        f = hub.figure[fid]
                        picked.append({
                            "id": fid, "name": f["name"], "dates": f.get("dates"),
                            "origin": f.get("origin"), "stance": f.get("stance"),
                            "wave": (hub.wave.get(f.get("wave"), {}).get("name") or {}).get("en"),
                            "score": round(100 - distance if side == "right" else distance),
                            "quote": quote, "media": assets,
                        })
                    if len(picked) == FIGURES_PER_POLE:
                        break
                if len(picked) == FIGURES_PER_POLE:
                    break
            if limit != MAX_DISTANCE:
                warnings.append(f"{axis}/{pole['abbr']['en']}: no figure within "
                                f"{MAX_DISTANCE} points of the pole — threshold relaxed")
            if len(picked) < FIGURES_PER_POLE:
                warnings.append(f"{axis}/{pole['abbr']['en']}: only {len(picked)} figures")
            for p in picked:
                used[p["id"]] += 1
                if not p["quote"]["reference"]:
                    warnings.append(f"{axis}/{pole['abbr']['en']}/{p['id']}: quote has no "
                                    f"printable reference — resolve it from the dossier")

            arguments, pool_size = hub.arguments(axis, side, ARGUMENTS_PER_POLE)
            poles.append({
                "axis": axis, "axis_name": meta["name"], "register": REGISTER[axis],
                "side": side, "pole": pole, "effect": pole["effect"],
                "statements": [{"id": i, "text": hub.cards[i]["question"],
                                "guidance": hub.cards[i]["guidance"]}
                               for i in hub.pole_items(axis, side)],
                "figures": picked, "arguments": arguments, "argument_pool": pool_size,
            })
    # Ecosystem convention (NG, 2026-08-01): a shared or translated resource
    # declares the languages it actually carries, and every translatable leaf
    # is an object keyed by language code — the shape of questionnaire.json,
    # debate-deck.json, editorial/<id>.json and the mascot i18n.json.
    langs = ["en"]
    if any(f["quote"].get("fr") for p in poles for f in p["figures"]):
        langs.append("fr")
    return {"metadata": {"id": "postair-debates-content",
                         "version": 1,
                         "languages": langs,
                         "default_language": "en",
                         "generated_by": "_project/tools/build_debates_content.py",
                         "instrument_version": hub.instrument_version,
                         "debate_version": hub.deck_version},
            "version": 1,
            "generated_by": "_project/tools/build_debates_content.py",
            "instrument_version": hub.instrument_version,
            "debate_version": hub.deck_version,
            "poles": poles, "warnings": warnings,
            "figures_used": len(used), "figures_reused": sum(1 for n in used.values() if n > 1)}


_CATEGORY_FR = {"quote": "parole publique", "case": "cas concret",
                "policy": "politique publique", "historical": "précédent historique",
                "tradition": "tradition"}


def _clip(text: str | None, n: int = 150) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + "…"


def report(data: dict) -> str:
    out = ["# Sélection de contenu — `postair_debates` (essai à blanc)", "",
           "> **Fichier généré** par `_project/tools/build_debates_content.py --report`.",
           "> Ce n'est pas la source : c'est ce que la règle de sélection du plan produit",
           "> **aujourd'hui**, pour que la règle soit validable sur du concret. À régénérer",
           "> à chaque évolution des données amont.", "",
           f"> Instrument v{data['instrument_version']} · matériau de débat v{data['debate_version']} ·",
           f"> {data['figures_used']} figures distinctes mobilisées, dont {data['figures_reused']} sur deux pôles.", ""]
    for pole in data["poles"]:
        if pole["side"] == "left":
            out += ["---", "",
                    f"## Axe — {pole['axis_name']['en']} · {pole['axis_name']['fr']}"
                    f"  ({pole['register']})", ""]
        p = pole["pole"]
        effect = "accélérateur" if pole["effect"] == "accelerator" else "ralentisseur"
        out += [f"### Pôle {p['en']} · {p['fr']} — `{p['abbr']['en']}`, {effect}", "",
                "Questions du sondage : "
                + " · ".join(f"**{s['id']}**" for s in pole["statements"]), ""]
        for s in pole["statements"]:
            out.append(f"- `{s['id']}` — {s['text']['en']}")
        out += ["", "| Figure | Score | Citation | Référence |", "|---|--:|---|---|"]
        for f in pole["figures"]:
            q = f["quote"]
            mark = "" if q["curated"] else " ¹"
            ref = q["reference"] or "⚠️ *à résoudre depuis le dossier*"
            out.append(f"| **{f['name']}**{mark}<br>*{f['origin']}, {f['dates']}* | {f['score']} "
                       f"| « {_clip(q['en'])} » | {_clip(ref, 90)} |")
        out += ["", "| Argument aujourd'hui | Nature | Porte-parole | Source |", "|---|---|---|---|"]
        for a in pole["arguments"]:
            out.append(f"| {_clip(a['title']['en'], 80)} "
                       f"| {_CATEGORY_FR.get(a['category'], a['category'])} "
                       f"| {_clip(a['person'] or '—', 45)} "
                       f"| {_clip(a['reference'] or a['citekey'] or '—', 70)} |")
        out += ["", f"*Réservoir : {pole['argument_pool']} arguments sourcés pour ce pôle.*", ""]
    out += ["---", "",
            "¹ Citation issue du registre (`quote-ledger.json`) et pas encore promue dans la",
            "couche éditoriale : texte anglais vérifié, **traduction française et référence",
            "bibliographique complète à produire** avant l'amphi.", ""]
    if data["warnings"]:
        out += ["", "## Avertissements du générateur", ""]
        out += [f"- {w}" for w in data["warnings"]]
        out.append("")
    return "\n".join(out)


def work_order(data: dict) -> str:
    """The quotes this deck displays that are not yet publishable, on stdout.

    Deliberately **not** a file. Every field below already exists upstream: a
    committed copy would only duplicate the hub and go stale the moment a quote
    is fixed or the selection moves. What is genuinely local — *which* quotes
    this deck shows — is recomputed here on demand, from the same rule that
    builds the manifest, and pasted into the correcting session.
    """
    seen, rows = set(), []
    for pole in data["poles"]:
        for f in pole["figures"]:
            q = f["quote"]
            key = (f["id"], q["en"][:60])
            if key in seen:
                continue
            seen.add(key)
            needs = [n for n, missing in (("référence", not q["reference"]),
                                          ("traduction FR", not q["fr"])) if missing]
            if needs:
                rows.append((f, pole, q, needs))
    out = [f"# Citations à compléter — {len(rows)} sur {len(seen)} affichées",
           "",
           "> Sortie de `build_debates_content.py --work-order`, à recopier dans la session",
           "> de correction. **Éphémère par construction** : la vérité est dans le hub, cette",
           "> liste ne fait que désigner ce que ce document affiche aujourd'hui.", "",
           f"> Instrument v{data['instrument_version']} · matériau de débat v{data['debate_version']}",
           ""]
    for f, pole, q, needs in rows:
        out += [f"## {f['name']} (`{f['id']}`) — {', '.join(needs)}",
                f"- {f['origin']}, {f['dates']} · axe **{pole['axis']}**, "
                f"pôle **{pole['pole']['abbr']['en']}** · documente {', '.join(q['documents'])}",
                f"- vérification actuelle : {q['verification'] or '—'}",
                f"- référence actuelle : {q['reference'] or '**aucune**'}",
                f"- texte : « {' '.join(q['en'].split())} »", ""]
    missing_ref = sum(1 for *_, needs in rows if "référence" in needs)
    out += ["---", "",
            f"**{missing_ref} sans référence imprimable · "
            f"{sum(1 for *_, n in rows if 'traduction FR' in n)} sans traduction française.**", ""]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", metavar="PATH", nargs="?", const="-",
                    help="write the markdown dry run instead of the manifest")
    ap.add_argument("--work-order", action="store_true",
                    help="print the quotes still missing a reference or a translation")
    args = ap.parse_args()

    hub_root = load_config()["hub"]
    warn_if_hub_dirty(hub_root)
    hub = Hub(hub_root)
    data = build(hub)

    if args.work_order:
        print(work_order(data))
        return

    if args.report:
        text = report(data)
        if args.report == "-":
            print(text)
        else:
            Path(args.report).write_text(text, encoding="utf-8")
            print(f"wrote {args.report}")
        return

    _OUT.parent.mkdir(parents=True, exist_ok=True)
    _OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {_OUT.relative_to(_REPO)} — {len(data['poles'])} poles, "
          f"{data['figures_used']} figures, {len(data['warnings'])} warning(s)")
    for w in data["warnings"]:
        print("  !", w)


if __name__ == "__main__":
    main()
