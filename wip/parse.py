"""Belgium: build corpus.d/<part>.json from the cache only (no network).

Text: legalize-be's reconstructions of Justel's archived consolidated versions (fetch_legalize.py), plus archived
Justel pages (Internet Archive `id_` captures, fetch_justel.py) for the newest text. Dates and credits: Justel's
own inline notes, `<L 1997-02-28/31, art. 1, 004; En vigueur : 01-03-1997>`, which name the amending act and
the day the change took effect.

Why notes and not legalize-be's commit order: legalize-be's later files hold only the articles touched so far,
and an article's new wording often shows up several archived versions after the version that made it (see
README). So each article's successive wordings are taken in order and each wording is dated by the notes it
gained (the latest of their in-force days), never by legalize-be's commit date.

    python -X utf8 scripts/belgium-law/parse.py
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import justel  # noqa: E402
import lmd  # noqa: E402

CACHE = HERE / '.cache'
OUT = HERE / 'corpus.d'
REPO = 'legalize-dev/legalize-be'
PLACEHOLDER = '[La source ne donne pas le texte en vigueur à cette date.]\n'
JUSTEL_CN = 'https://www.ejustice.just.fgov.be/cgi_loi/article.pl?language=fr&lg_txt=f&cn_search={}'
LAW_KINDS = {'AR': 'decree', 'ARR': 'decree', 'A': 'decree', 'AL': 'decree', 'ACC': 'court'}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def cached(url: str) -> bytes:
    return (CACHE / sha(url.encode())).read_bytes()


def legalize_sources(numac: str) -> list[dict]:
    idx = json.loads((CACHE / 'legalize' / 'index.json').read_text(encoding='utf-8'))
    out = []
    for r in idx['commits']:
        if r['numac'] != numac:
            continue
        url = f'https://raw.githubusercontent.com/{REPO}/{r["commit"]}/be/{numac}.md'
        raw = cached(url)
        m = re.search(r'^Source-Id: \S+?@v(\d+):(\d{4}-\d\d-\d\d)', r['message'], re.M)
        out.append({'kind': 'legalize', 'commit': r['commit'], 'url': url, 'sha256': sha(raw),
                    'md': raw.decode('utf-8'), 'vnum': m.group(1) if m else '001',
                    'date': m.group(2) if m else None})
    return out


def justel_source(url: str, day: str) -> dict:
    raw = cached(url)
    return {'kind': 'justel', 'url': url, 'sha256': sha(raw), 'md': justel.to_md(raw), 'date': day}


def note_key(n: dict) -> tuple:
    art = re.search(r'\bart\.?\s*([^,;]+)', n['raw'])
    return (n['kind'], n['ref'], art.group(1).strip() if art else '')


class Act:
    """Successive wordings of each provision of one act, read from several sources in order."""

    def __init__(self, sub_heads: set[str] | None = None):
        self.seq: dict[str, list[dict]] = {}
        self.labels: dict[str, tuple[str, str]] = {}
        self.sources: list[dict] = []
        self.skipped: set[str] = set()
        self.sub_heads = sub_heads

    def add(self, src: dict, rename: dict | None = None) -> set[str]:
        i = len(self.sources)
        self.sources.append(src)
        us, sk = lmd.units(src['md'], self.sub_heads)
        self.skipped |= set(sk)
        got: dict[str, tuple] = {}
        for k, lab, kind, raw in us:
            if rename and k in rename:
                k, lab = rename[k]
            text, notes = lmd.strip_notes(raw)
            if not text:   # a heading-only block (legalize-be lost the body); not a wording
                continue
            if k in got and len(text) <= len(got[k][0]):   # legalize-be repeats some articles
                continue
            got[k] = (text, notes, lab, kind)
        for k, (text, notes, lab, kind) in got.items():
            s = self.seq.setdefault(k, [])
            self.labels[k] = (lab, kind)
            if not s or s[-1]['text'] != text:
                s.append({'i': i, 'text': text, 'notes': notes, 'seen': [i]})
            else:
                s[-1]['seen'].append(i)
                s[-1]['notes_last'] = notes
        src['units'] = set(got)
        return set(got)

    def final_dates(self, k: str) -> dict:
        """In-force day of every note in unit k, from its latest appearance there (Justel corrected some dates
        later; the same amending article can carry different days in different provisions)."""
        out = {}
        for w in self.seq[k]:
            for n in w['notes'] + w.get('notes_last', []):
                if n['date']:
                    out[note_key(n)] = n['date']
                elif n['undetermined']:
                    out[note_key(n)] = None
        return out

    def normalise_markup(self) -> int:
        """Older Justel versions mark changed words with ( ) where newer ones use [ ] (brackets are stripped,
        parentheses cannot be). Where a paragraph's words equal a later paragraph's, use the later rendering;
        then merge wordings that became identical. Returns how many were merged."""
        merged = 0
        for k, s in self.seq.items():
            for j in range(len(s) - 2, -1, -1):
                later = {lmd.canon(p): p for p in s[j + 1]['text'].splitlines()}
                paras = [later.get(lmd.canon(p), p) for p in s[j]['text'].splitlines()]
                s[j]['text'] = '\n'.join(paras) + ('\n' if paras else '')
            out = []
            for w in s:
                if out and out[-1]['text'] == w['text']:
                    out[-1]['seen'] += w['seen']
                    out[-1]['notes_last'] = w['notes']
                    merged += 1
                    continue
                out.append(w)
            self.seq[k] = out
        return merged


class Laws:
    def __init__(self):
        self.laws: dict[str, dict] = {}

    def key(self, n: dict) -> str | None:
        if n['ref'].endswith('/?'):
            return None
        k = f'{n["kind"].lower()}-{n["ref"].replace("/", "-")}'
        if n.get('court'):
            if k not in self.laws:
                yr, num = n['ref'].split('/')
                self.laws[k] = {'label': f'C. const. {int(num)}/{yr}', 'kind': 'court',
                                'title': f'Cour constitutionnelle, arrêt n° {int(num)}/{yr} du {n["ruling"]}',
                                'enacted': n['ruling'], 'published': n['published'],
                                'url': f'https://www.const-court.be/public/f/{yr}/{yr}-{int(num):03d}f.pdf',
                                'temporary_until': None, 'restores': None,
                                'note': 'The Constitutional Court annulled words of this provision; Justel prints '
                                        'them in italics, and they are removed here from the day the ruling was '
                                        'published in the Moniteur belge.'}
            return k
        if k not in self.laws:
            kind = LAW_KINDS.get(n['kind'], 'law')
            d, num = n['ref'].split('/')
            self.laws[k] = {'label': f'{n["kind"]} {n["ref"]}', 'kind': kind, 'title': None, 'enacted': d,
                            'published': None,
                            'url': JUSTEL_CN.format(d.replace('-', '') + num.zfill(2)) if kind != 'court' else None,
                            'temporary_until': None, 'restores': None, 'note': None}
        return k

    def credit(self, notes: list[dict]) -> list[str]:
        return sorted({k for k in (self.key(n) for n in notes) if k})


def timeline(act: Act, start: str, laws: Laws, log: dict) -> dict[str, list[tuple]]:
    """Per unit: [(day, text or None, [law keys], why)], each wording dated by the notes it gained.

    - A wording whose notes all took effect on one day D is in force from D, credited to the act(s) named.
    - A wording that gained notes with two in-force days D1 < D2 is in force only from D2; from D1 the
      source does not give the wording (PLACEHOLDER), credited to the act(s) of D1.
    - The first wording of a unit is in force from `start` unless it carries notes in force after `start`:
      then the unit is absent before an insertion note's day, or reads PLACEHOLDER (publisher) before the
      latest note's day, when the wording arrives credited to that note's act.
    - A change with no new dated note is "unexplained" (publisher), dated by the source that first shows it.
    """
    tl: dict[str, list] = {}

    for k, s in act.seq.items():
        fd = act.final_dates(k)

        def day(n):
            return fd.get(note_key(n))

        ev: list[tuple] = []
        first = s[0]
        base = act.sources[first['i']]
        is_base = first['i'] == 0 or base.get('base')
        st = max(start, base.get('start') or start) if is_base else start
        bcredit = list(base.get('credit') or []) if is_base else []
        late = [n for n in first['notes'] if day(n) and day(n) > st]
        if late:
            dmax = max(day(n) for n in late)
            ins = sorted((n for n in late if n['insert']), key=day)
            if ins:
                if day(ins[0]) < dmax:
                    ev.append((day(ins[0]), PLACEHOLDER, laws.credit([ins[0]]), 'inserted; first wording not in source'))
            else:
                ev.append((st, PLACEHOLDER, bcredit, 'source wording is later than this day'))
                log['placeholder_start'].append(k)
            ev.append((dmax, first['text'], laws.credit([n for n in late if day(n) == dmax]), 'notes'))
        elif is_base:
            ev.append((st, first['text'], bcredit, 'first'))
        else:
            d = act.sources[first['i']]['date']
            log['unexplained'].append((k, first['i'], d, 'appears without a dated note'))
            ev.append((d, first['text'], [], 'unexplained'))
        for j in range(1, len(s)):
            w, prev = s[j], s[j - 1]
            old = {note_key(n) for n in prev['notes'] + prev.get('notes_last', [])}
            new = [n for n in w['notes'] if note_key(n) not in old]
            ds = sorted({day(n) for n in new if day(n)})
            last = ev[-1][0]
            ds_after = [d for d in ds if d > last]
            if ds_after:
                dmax = ds_after[-1]
                if len(ds_after) > 1:
                    d0 = ds_after[0]
                    ev.append((d0, PLACEHOLDER, laws.credit([n for n in new if day(n) == d0]),
                               'two in-force days in one wording'))
                    log['split'].append((k, ds_after))
                ev.append((dmax, w['text'], laws.credit([n for n in new if day(n) == dmax]), 'notes'))
            elif ds:
                # the notes it gained took effect on or before the last change we placed: same day as that
                log['backwards'].append((k, w['i'], ds, last))
                ev.append((last, w['text'], laws.credit([n for n in new if day(n)]), 'notes (same day)'))
            else:
                d = max(act.sources[w['i']]['date'], last)
                log['unexplained'].append((k, w['i'], d, 'changed without a new dated note'))
                ev.append((d, w['text'], [], 'unexplained'))
        out: list[tuple] = []
        for e in ev:
            if out and out[-1][0] == e[0]:
                out[-1] = (e[0], e[1], sorted(set(out[-1][2]) | set(e[2])), e[3])
            else:
                out.append(e)
        tl[k] = out
    return tl


def drop_missing(act: Act, tl: dict, snaps: list[tuple[str, set]], log: dict) -> None:
    """legalize-be's files never drop an article, and Justel removes some repealed ones from its page. A provision
    absent from the newest full Justel page (snaps: [(day, unit keys)] of full pages, oldest first) is removed: on
    the day a provision with its words first appears under another number (renumbered; credited like that
    appearance), else on the day of the first page from which it is missing for good (unexplained)."""
    final_keys = snaps[-1][1]
    for k in sorted(tl):
        evs = tl[k]
        if k in final_keys or evs[-1][1] is None:
            continue
        seen = [i for i, (d, ks) in enumerate(snaps) if k in ks]
        day = snaps[seen[-1] + 1][0] if seen else snaps[0][0]
        words = lmd.canon(evs[-1][1])
        hit = None
        for k2 in sorted(final_keys) if len(words) > 40 and not words.startswith('(abroge') else []:
            if k2 == k or k2 not in tl:
                continue
            for e in tl[k2]:
                if e[1] and e[0] >= evs[-1][0] and lmd.canon(e[1]) == words:
                    hit = (e[0], e[2], k2)
                    break
            if hit:
                break
        if hit:
            d = max(hit[0], evs[-1][0])
            evs.append((d, None, hit[1], f'renumbered as {hit[2]}'))
            log['renumbered'].append((k, hit[2], d))
        else:
            evs.append((max(day, evs[-1][0]), None, [], 'not on the newest full Justel page'))
            log['dropped'].append((k, day))
        if len(evs) > 1 and evs[-1][0] == evs[-2][0]:
            evs[-2:] = [evs[-1]]


def build_versions(act: Act, tl: dict) -> list[dict]:
    """Versions as `changes` against the one before (the first holds every unit)."""
    days = sorted({e[0] for evs in tl.values() for e in evs})
    state: dict[str, str | None] = {}
    out = []
    for d in days:
        changes, credits = {}, {}
        for k in sorted(tl):
            for e in tl[k]:
                if e[0] != d:
                    continue
                if state.get(k) != e[1]:
                    lab, kind = act.labels[k]
                    changes[k] = {'label': lab, 'kind': kind, 'text': e[1]} if e[1] is not None else None
                    if e[2]:
                        credits[k] = e[2]
                state[k] = e[1]
        if not changes:
            continue
        v = {'from': d}
        if not out:
            v['units'] = {k: u for k, u in changes.items() if u is not None}
        else:
            v['changes'] = changes
        v['credits'] = credits
        out.append(v)
    return out


def state_on(versions: list[dict], day: str) -> dict[str, str]:
    st: dict[str, str] = {}
    for v in versions:
        if v['from'] > day:
            break
        for k, u in (v.get('units') or v.get('changes') or {}).items():
            if u is None:
                st.pop(k, None)
            else:
                st[k] = u['text']
    return st


def captures(cn: str) -> list[dict]:
    """The archived Justel captures of text cn that are in the cache, oldest first."""
    p = CACHE / 'justel' / 'captures.json'
    if not p.exists():
        return []
    out = []
    for r in json.loads(p.read_text(encoding='utf-8')).get(cn, []):
        f = CACHE / sha(r['wb'].encode())
        if f.exists():
            out.append(dict(r, day=f'{r["ts"][:4]}-{r["ts"][4:6]}-{r["ts"][6:8]}'))
    return out


def verify(versions: list[dict], caps: list[dict], sub_heads=None, rename=None) -> dict:
    """Compare our state on each capture's day with that capture, provision by provision, ignoring Justel's
    typesetting (lmd.canon). Provisions that read PLACEHOLDER on that day are not compared."""
    rows = []
    for c in caps:
        md = justel.to_md(cached(c['wb']))
        us, _ = lmd.units(md, sub_heads)
        theirs = {}
        for k, lab, kind, raw in us:
            if rename and k in rename:
                k = rename[k][0]
            t = lmd.strip_notes(raw)[0]
            if k not in theirs or len(t) > len(theirs[k]):
                theirs[k] = t
        if len(theirs) < 20:
            continue
        ours = state_on(versions, c['day'])
        def cl(t):
            return [lmd.canon(x) for x in t.splitlines()]
        diff = sorted(k for k in set(ours) & set(theirs)
                      if ours[k] != PLACEHOLDER and cl(ours[k]) != cl(theirs[k]))
        rows.append({'capture': c['ts'], 'day': c['day'], 'units': len(theirs), 'differ': diff,
                     'only_ours': sorted(k for k in set(ours) - set(theirs) if ours[k] not in (PLACEHOLDER,)),
                     'only_justel': sorted(set(theirs) - set(ours))})
    return {'captures': len(rows), 'exact': sum(1 for r in rows if not r['differ'] and not r['only_justel']),
            'rows': rows}


def legalize_source_entry(numacs: list[str], n_files: int) -> dict:
    idx = json.loads((CACHE / 'legalize' / 'index.json').read_text(encoding='utf-8'))
    return {'name': 'legalize-be (Legalize, github.com/legalize-dev/legalize-be): Justel archived versions as Markdown',
            'url': f'https://github.com/{REPO}/tree/{idx["pin"]}',
            'retrieved': '2026-10-29', 'requests': n_files + 1,
            'licence': 'Data: "Licence ouverte / open data fédéral belge (CC0 par défaut)"; pipeline MIT '
                       '(github.com/legalize-dev/legalize-pipeline). Each file\'s YAML front matter names its official '
                       'source, a Justel ELI page.',
            'notes': f'Pinned at commit {idx["pin"]}. Files be/{{NUMAC}}.md for NUMAC {", ".join(numacs)}, one per '
                     'legalize-be commit, read from raw.githubusercontent.com; commit list from a treeless clone.'}


def justel_source_entry(caps: list[dict], used: str) -> dict:
    return {'name': 'Justel (SPF Justice, Moniteur belge), consolidated text, read through Internet Archive captures',
            'url': 'https://www.ejustice.just.fgov.be/cgi_loi/welcome.pl?language=fr',
            'retrieved': '2026-10-29', 'requests': len(caps),
            'licence': 'Official acts: no copyright (Code de droit économique, art. XI.172, § 2). Justel\'s '
                       'robots.txt disallows /cgi_loi/, /eli/ and /mopdf/, so Justel was read only through '
                       'web.archive.org `id_` captures.',
            'notes': used}


def write_part(name: str, part: dict) -> None:
    OUT.mkdir(exist_ok=True)
    p = OUT / f'{name}.json'
    tmp = p.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    os.replace(tmp, p)


COUNTRY = {
    'code': 'BE', 'name': 'Belgium', 'slug': 'belgium', 'lang': 'fr', 'tz': 'Europe/Brussels',
    'future_branch': 'futur',
    'publisher': {'name': 'Justel (SPF Justice, Moniteur belge)', 'email': 'justel@ejustice.just.fgov.be.invalid'},
    'default_in_force_rule': {
        'text': 'Loi du 31 mai 1961, art. 4, al. 2: les lois "sont obligatoires dans tout le royaume le dixième jour '
                'après celui de leur publication, à moins que la loi n\'ait fixé un autre délai". Every date here '
                'is the in-force day Justel prints in its note on the change, which applies that rule or the '
                'law\'s own clause.',
        'source': 'https://www.ejustice.just.fgov.be/eli/loi/1961/05/31/1961053107/justel'},
    'licence_note': 'Texts: Justel, the consolidated legislation database of the SPF Justice (Moniteur belge), as '
                    'reconstructed by legalize-be (data CC0 by default; pipeline MIT) and as archived by the '
                    'Internet Archive. Official acts are not protected by copyright in Belgium (CDE art. XI.172 § 2).',
}
AI_USE = ['Claude Code (claude-opus-5-5) wrote fetch_legalize.py, fetch_justel.py, lmd.py, justel.py and parse.py, '
          'and chose the sources. No model output is used as legal text, dates or credits: every word comes from '
          'the cached legalize-be files or Justel captures, and every date and credit from Justel\'s own notes.']
MONTHS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre',
          'novembre', 'décembre']


def fr_date(iso: str) -> str:
    y, m, d = iso.split('-')
    return f'{int(d)}{"er" if d == "01" else ""} {MONTHS[int(m) - 1]} {y}'


def common_decisions(log: dict, title: str) -> list[str]:
    d = []
    if log['placeholder_start']:
        d.append(f'{title}: {len(log["placeholder_start"])} provisions read "{PLACEHOLDER.strip()}" in the oldest '
                 'version, because the only wording the source gives for them carries a note in force later: '
                 f'{", ".join(sorted(log["placeholder_start"]))}.')
    if log['split']:
        d.append(f'{title}: {len(log["split"])} wordings gained notes with two in-force days at once; they read '
                 f'"{PLACEHOLDER.strip()}" from the first day to the second: '
                 + '; '.join(f'{k} {"/".join(ds)}' for k, ds in sorted(log['split'])) + '.')
    if log['unexplained']:
        d.append(f'{title}: {len(log["unexplained"])} changes have no new dated note; they are committed as '
                 'unexplained (publisher), dated by the Justel version (legalize-be Source-Id date) or capture '
                 'that first shows them: '
                 + '; '.join(f'{k} ({day})' for k, i, day, why in sorted(log['unexplained'])) + '.')
    if log.get('renumbered'):
        d.append(f'{title}: {len(log["renumbered"])} provisions renumbered away are removed on the day their words '
                 'first appear under the new number: '
                 + '; '.join(f'{k} -> {k2} ({day})' for k, k2, day in sorted(log['renumbered'])) + '.')
    if log.get('dropped'):
        d.append(f'{title}: {len(log["dropped"])} provisions that legalize-be still carries are absent from the '
                 'newest full Justel page and are removed on that page\'s day (unexplained): '
                 + ', '.join(k for k, day in sorted(log['dropped'])) + '.')
    if log['backwards']:
        d.append(f'{title}: {len(log["backwards"])} wordings gained notes whose in-force day is earlier than a '
                 'change already placed (Justel recorded the change late); they are committed on that later '
                 'change\'s day, credited to the act the note names: '
                 + '; '.join(f'{k} ({"/".join(ds)} after {last})' for k, i, ds, last in sorted(log['backwards']))
                 + '.')
    return d


def constitution() -> dict:
    from collections import defaultdict
    act = Act(sub_heads={'art-143'})
    src = legalize_sources('1994021048')
    for s in src:
        act.add(s)
    caps = captures('1994021730')
    newest = 'https://web.archive.org/web/20260824161257id_/https://www.ejustice.just.fgov.be/cgi_loi/article.pl?' \
             'language=fr&lg_txt=f&type=&sort=&numac_search=&cn_search=1994021730&caller=SUM&&view_numac=1994021730f'
    act.add(justel_source(newest, '2026-08-24'))
    merged = act.normalise_markup()
    laws = Laws()
    log = defaultdict(list)
    tl = timeline(act, '1994-02-27', laws, log)
    vs = build_versions(act, tl)
    for v in vs:
        v['source_url'] = 'https://www.ejustice.just.fgov.be/eli/constitution/1994/02/17/1994021048/justel'
    vs[0]['note'] = ('The coordinated Constitution as published on 17 February 1994 (Justel: in force 27 February '
                     '1994), from legalize-be\'s first file for NUMAC 1994021048.')
    for law in laws.laws.values():
        law['title'] = f'Révision de la Constitution du {fr_date(law["enacted"])}'
    laws.laws['constitution-1994'] = {
        'label': 'Constitution coordonnée 1994', 'kind': 'law',
        'title': 'La Constitution coordonnée (17 février 1994)', 'enacted': '1994-02-17', 'published': '1994-02-17',
        'url': 'https://www.ejustice.just.fgov.be/eli/constitution/1994/02/17/1994021048/justel',
        'temporary_until': None, 'restores': None, 'note': None}
    ver = verify(vs, caps, {'art-143'})
    (HERE / 'verification').mkdir(exist_ok=True)
    (HERE / 'verification' / 'constitution.json').write_text(json.dumps(ver, indent=1), encoding='utf-8')
    act_d = {'slug': 'constitution', 'short': 'Const.', 'title': 'La Constitution coordonnée',
             'url': 'https://www.ejustice.just.fgov.be/eli/constitution/1994/02/17/1994021048/justel',
             'first_law': 'constitution-1994', 'earlier_laws': [], 'versions': vs}
    dec = [
        'Constitution: text from legalize-be (78 files for NUMAC 1994021048, one per Justel archived version, '
        'pinned commit) and, for the revisions after legalize-be\'s last file (L 2025-06-12/07 and L 2026-07-15/04), '
        'the archived Justel page of 24 August 2026 (Internet Archive capture 20260824161257).',
        'Constitution: legalize-be\'s files after the first hold only the articles touched so far, and an article\'s '
        'new wording often appears several archived versions after the version that made it; so each article\'s '
        'successive wordings are taken in file order and each is dated by the Justel notes it gained (their '
        'in-force day), never by legalize-be\'s commit date (which is often the publication date plus ten days).',
        'Constitution: the first version (27 February 1994, Justel\'s in-force date for the coordinated text) is '
        'legalize-be\'s first file. Articles inserted later appear in that file with their later wording; each is '
        'left out until the in-force day of its "Inséré par" note (7bis, 11bis, 14bis, 22bis, 22ter, 39bis, 39ter, '
        '118bis, 135bis, 168bis).',
        f'Constitution: {merged} wordings differed from the next only in Justel\'s typesetting (older versions mark '
        'changed words with parentheses, later ones with brackets; case, accents and final stops tidied later); '
        'each paragraph takes Justel\'s latest rendering of the same words.',
        'Constitution: Justel\'s inline notes and change markers ([¹ ]¹, older bare brackets) are removed from the '
        'text; a provision that Justel shows only as a repeal note reads "(Abrogé)". The anchors M, M1, M2 '
        '(structure) and N1, N2 (the 1994 correspondence tables, which Justel does not reproduce) are not provisions.',
        'Constitution: law labels are Justel\'s citations, "L <date of the act>/<Justel serial>"; every one here is a '
        'revision of the Constitution, and the link opens its Justel record. Their Moniteur belge publication dates '
        'are not in the source data, so "published" is left empty.',
        f'Constitution: compared with {ver["captures"]} archived Justel pages (2009-2026): {ver["exact"]} match '
        'provision for provision on their capture day, ignoring typesetting; see verification/constitution.json.',
    ] + common_decisions(log, 'Constitution')
    return {'country': COUNTRY,
            'sources': [legalize_source_entry(['1994021048'], len(src)),
                        justel_source_entry(caps or [newest], 'Constitution (Justel cn 1994021730): the capture of '
                                            '2026-08-24 supplies the newest text; every capture is compared with '
                                            'our text in verification/constitution.json.')],
            'laws': laws.laws, 'acts': [act_d], 'applies': [], 'decisions': dec, 'ai_use': AI_USE,
            '_log': dict(log)}


def code_penal() -> dict:
    from collections import defaultdict
    act = Act()
    src = legalize_sources('1867060850')
    for s in src:
        act.add(s)
    caps = captures('1867060801')
    # the newest real Justel page after legalize-be's last file (2026-02-26); later captures are bot challenges
    newest = [c for c in caps if c['day'] == '2026-05-03']
    for c in newest:
        act.add(justel_source(c['wb'], c['day']))
    merged = act.normalise_markup()
    laws = Laws()
    log = defaultdict(list)
    tl = timeline(act, '1990-04-05', laws, log)
    if newest:
        drop_missing(act, tl, [(newest[0]['day'], act.sources[-1]['units'])], log)
    vs = build_versions(act, tl)
    for v in vs:
        v['source_url'] = 'https://www.ejustice.just.fgov.be/eli/loi/1867/06/08/1867060850/justel'
    vs[0]['note'] = ('The oldest text Justel keeps: its archived versions start on 5 April 1990. Not the Code as '
                     'enacted in 1867.')
    ver = verify(vs, caps)
    (HERE / 'verification').mkdir(exist_ok=True)
    (HERE / 'verification' / 'code-penal.json').write_text(json.dumps(ver, indent=1), encoding='utf-8')
    late = [r for r in ver['rows'] if r['day'] >= '2024-01-01']
    act_d = {'slug': 'code-penal', 'short': 'C. pén.', 'title': 'Code pénal (8 juin 1867)',
             'url': 'https://www.ejustice.just.fgov.be/eli/loi/1867/06/08/1867060850/justel',
             'first_law': None, 'earlier_laws': [], 'versions': vs}
    dec = [
        'Code pénal: text from legalize-be (166 files for NUMAC 1867060850, one per Justel archived version, from '
        '5 April 1990, the start of Justel\'s archive) and, after legalize-be\'s last file (Justel update of '
        '18 February 2026), the archived Justel page of 3 May 2026 (Internet Archive capture '
        f'{newest[0]["ts"] if newest else "-"}). The first version is the oldest text available (5 April 1990), '
        'credited to the publisher, not the Code as enacted in 1867.',
        'Code pénal: each article\'s successive wordings are dated by the Justel notes they gained, as for the '
        'Constitution; legalize-be\'s commit dates are not used.',
        'Code pénal: the new Code pénal (lois du 29 février 2024, livres I et II) replaces the 1867 Code. Its '
        'in-force day was first set at two years after publication (8 April 2026); Justel\'s note on art. 38 of '
        'the livre I law records its postponement to 1 September 2026 by L 2026-03-30/01, art. 252, and Justel\'s '
        'page of 3 May 2026 still shows the 1867 Code in force. No source used here gives the clause for livre II, '
        'so the replacement is not committed: the 1867 Code ends with its last sourced version. The new Code is '
        'not built: legalize-be\'s files for the two laws mix the laws\' own articles with the Code\'s, under the '
        'same numbers.',
        'Code pénal: Justel added the euro conversion (L 2000-06-26/42, in force 1 January 2002) to many articles '
        'only in 2010; those articles carry euros from 1 January 2002 here, so Justel\'s pages of 2009 and early '
        '2010 differ from this history in about 200 articles, all but 5 of them by francs and euros only.',
        'Code pénal: words the Constitutional Court annulled (Justel prints them in italics with a note naming the '
        'ruling) are removed from the day the ruling was published in the Moniteur belge, credited to the ruling '
        '(kind "court"), e.g. arrêt n° 148/2017.',
        'Code pénal: seven articles legalize-be labels "auto-NNN" (its parser lost the article number) are left '
        'out; their articles are read from the other files that label them.',
        f'Code pénal: {merged} wordings differed from the next only in Justel\'s typesetting and take its latest '
        'rendering.',
        f'Code pénal: compared with {ver["captures"]} archived Justel pages (2009-2026); the {len(late)} pages from '
        f'2024 on match provision for provision in {sum(1 for r in late if not r["differ"])}; see '
        'verification/code-penal.json.',
    ] + common_decisions(log, 'Code pénal')
    return {'sources': [legalize_source_entry(['1867060850'], len(src)),
                        justel_source_entry(caps, 'Code pénal (Justel cn 1867060801): the capture of 2026-05-03 '
                                            'supplies the newest text; every capture is compared with our text in '
                                            'verification/code-penal.json.')],
            'laws': laws.laws, 'acts': [act_d], 'applies': [], 'decisions': dec, 'ai_use': AI_USE,
            '_log': dict(log)}


OLD_CC = {'1804032130': 'Titre préliminaire, livre I (art. 1-515)', '1804032131': 'livre II (art. 516-710bis)',
          '1804032132': 'livre III, titres I-II (art. 711-1100)', '1804032133': 'livre III, titres III-V (art. 1101-1581)',
          '1804032134': 'livre III, titres VI-XIII (art. 1582-2010)', '1804032135': 'livre III, titres XIV-XX'}
# not used: Justel text 1804032136, "[ANCIEN] CODE CIVIL. - LIVRE III - TITRE V. Du régime en Communauté", the
# pre-1976 wording of arts. 1399-1581 that Justel keeps beside the current one (same article numbers)
# the new Code civil: Justel's consolidated book -> the law that enacted it (legalize-be NUMAC), book label
NEW_CC = [('2019A12168', '2019012168', 'livre 8'), ('2020A20347', '2020020347', 'livre 3'),
          ('2022A30600', '2022030600', 'livre 2, titre 3'), ('2022B30600', '2022030600', 'livre 4'),
          ('2022A32057', '2022032057', 'livre 1'), ('2022A32058', '2022032058', 'livre 5'),
          ('2024A01600', '2024001600', 'livre 6'), ('2025A05089', '2025005089', 'livre 9, titre 1')]
MONTH_N = {m.replace('é', 'e').replace('û', 'u'): i + 1 for i, m in enumerate(MONTHS)}


def fr_iso(s: str) -> str:
    s = s.lower().replace('é', 'e').replace('û', 'u')
    m = re.match(r'\s*(\d+)(?:er)?\s+(\S+)\s+(\d{4})', s)
    return f'{m.group(3)}-{MONTH_N[m.group(2)]:02d}-{int(m.group(1)):02d}'


def front(numac: str) -> dict:
    """legalize-be's YAML front matter (Justel's record) for the newest file of an act."""
    md = legalize_sources(numac)[-1]['md']
    return dict(re.findall(r'^(\w+): "(.*)"$', md.split('\n---', 1)[0], re.M))


def full_captures(cn: str) -> list[dict]:
    """Captures that hold a consolidated text (later ones are Justel's bot challenge)."""
    out = []
    for c in captures(cn):
        if len(lmd.units(justel.to_md(cached(c['wb'])))[0]) >= 5:
            out.append(c)
    return out


def code_civil() -> dict:
    from collections import defaultdict
    # --- the old Code civil (1804), from Justel's pages, part by part
    old = Act()
    part_caps = {}
    for cn in OLD_CC:
        caps = full_captures(cn)
        part_caps[cn] = caps
        for j, c in enumerate(caps):
            s = justel_source(c['wb'], c['day'])
            s.update(base=(j == 0), start=c['day'], part=cn)
            old.add(s)
    merged_old = old.normalise_markup()
    laws = Laws()
    log_old = defaultdict(list)
    start = min(c[0]['day'] for c in part_caps.values() if c)
    tl = timeline(old, start, laws, log_old)
    for cn, caps in part_caps.items():
        if caps:
            snaps = [(s['date'], s['units']) for s in old.sources if s.get('part') == cn]
            mine = {k for k in tl if any(old.sources[w['i']].get('part') == cn for w in old.seq[k])}
            drop_missing(old, {k: tl[k] for k in mine}, snaps, log_old)
    vs_old = build_versions(old, tl)
    for v in vs_old:
        v['source_url'] = 'https://www.ejustice.just.fgov.be/eli/loi/1804/03/21/1804032150/justel'
    vs_old[0]['note'] = (f'The oldest text available: Justel\'s consolidated old Code civil as archived on {start}. '
                         'Not the Code as enacted in 1804.')
    ver_old = {cn: verify(vs_old, caps) for cn, caps in part_caps.items() if caps}
    # --- the new Code civil (2019-), book by book
    new = Act()
    book_laws = {}
    for cn, numac, book in NEW_CC:
        fm = front(numac)
        key = f'loi-{numac}'
        books = [b for c2, n2, b in NEW_CC if n2 == numac]
        enacted = fr_iso(fm['title'].split('.')[0])
        laws.laws[key] = {'label': f'Loi du {fr_date(enacted)} (C. civ., {" et ".join(books)})', 'kind': 'law',
                          'title': fm['title'].split(' (NOTE')[0].split('(NOTE')[0].strip(),
                          'enacted': enacted, 'published': fm.get('publication_date'),
                          'url': fm.get('source'), 'temporary_until': None, 'restores': None, 'note': None}
        book_laws[cn] = (key, fr_iso(fm['entry_into_force']), book)
    first_book = min(NEW_CC, key=lambda b: book_laws[b[0]][1])[0]
    new_caps = {}
    for cn, numac, book in sorted(NEW_CC, key=lambda b: book_laws[b[0]][1]):
        caps = full_captures(cn)
        new_caps[cn] = caps
        key, day, _ = book_laws[cn]
        for j, c in enumerate(caps):
            s = justel_source(c['wb'], c['day'])
            s.update(base=(j == 0), start=day, part=cn,
                     credit=[] if (j or cn == first_book) else [key])
            new.add(s)
    merged_new = new.normalise_markup()
    log_new = defaultdict(list)
    tl2 = timeline(new, book_laws[first_book][1], laws, log_new)
    vs_new = build_versions(new, tl2)
    for v in vs_new:
        v['source_url'] = 'https://www.ejustice.just.fgov.be/cgi_loi/welcome.pl?language=fr'
    ver_new = {cn: verify(vs_new, caps) for cn, caps in new_caps.items() if caps}
    (HERE / 'verification').mkdir(exist_ok=True)
    (HERE / 'verification' / 'code-civil.json').write_text(json.dumps({'ancien': ver_old, 'nouveau': ver_new},
                                                                      indent=1), encoding='utf-8')
    acts = [
        {'slug': 'ancien-code-civil', 'short': 'anc. C. civ.', 'title': 'Code civil (21 mars 1804), dit ancien Code civil',
         'url': 'https://www.ejustice.just.fgov.be/eli/loi/1804/03/21/1804032150/justel', 'first_law': None,
         'earlier_laws': [], 'versions': vs_old},
        {'slug': 'code-civil', 'short': 'C. civ.', 'title': 'Code civil (loi du 13 avril 2019 et livres suivants)',
         'url': laws.laws[book_laws[first_book][0]]['url'], 'first_law': book_laws[first_book][0],
         'earlier_laws': [], 'versions': vs_new},
    ]
    n_old = sum(len(c) for c in part_caps.values())
    n_new = sum(len(c) for c in new_caps.values())

    def vsum(ver):
        return ', '.join(f'{cn}: {v["exact"]}/{v["captures"]}' for cn, v in ver.items())
    dec = [
        'Ancien Code civil: legalize-be has no file for the 1804 Code civil, so it is read only from Justel\'s '
        f'consolidated pages (Justel splits it into parts, text numbers 1804032130-1804032136), {n_old} Internet '
        'Archive captures from 2009 to 2026 (about two a year per part, plus the newest). The first version is '
        f'the oldest capture ({start}), credited to the publisher; it is not the Code as enacted in 1804.',
        'Ancien Code civil: each article\'s successive wordings across the captures are dated by the Justel notes '
        'they gained, as for the Constitution; a capture\'s own date is used only for a change with no new dated '
        'note (unexplained). A change made and replaced between two captures is not seen.',
        'Ancien Code civil: the books of the new Code civil replace parts of it; Justel marks the replaced '
        'articles repealed, with the in-force day, and they read "(Abrogé)" from that day.',
        'Code civil (2019-): each book is read from Justel\'s consolidated page of that book (Internet Archive '
        f'captures, {n_new} in all, 2022-2026). Its articles enter on the book\'s in-force day as Justel records it '
        '(legalize-be front matter "entry_into_force"), credited to the law that enacted it; an article whose '
        'oldest captured wording carries a later note reads the placeholder from that day until the note\'s day. '
        'Livre 7 does not exist yet; livre 2 titres 1-2 are not yet enacted.',
        f'Code civil: {merged_old + merged_new} wordings differed from the next only in Justel\'s typesetting and '
        'take its latest rendering.',
        f'Code civil: every capture compared with this history on its own day (exact/total): ancien {vsum(ver_old)}; '
        f'nouveau {vsum(ver_new)}; see verification/code-civil.json.',
    ] + common_decisions(log_old, 'Ancien Code civil') + common_decisions(log_new, 'Code civil (2019-)')
    caps_all = [c for v in part_caps.values() for c in v] + [c for v in new_caps.values() for c in v]
    return {'sources': [justel_source_entry(caps_all, 'Ancien Code civil (Justel cn 1804032130-36) and the books '
                                            'of the new Code civil (Justel NUMAC 2019A12168, 2020A20347, '
                                            '2022A30600, 2022B30600, 2022A32057, 2022A32058, 2024A01600, '
                                            '2025A05089): every word of this part comes from these captures.'),
                        legalize_source_entry([n for _, n, _ in NEW_CC], 0) | {
                            'notes': 'Used only for the enacting laws\' titles, publication and in-force days (YAML '
                                     'front matter of be/<NUMAC>.md, a copy of Justel\'s record).'}],
            'laws': laws.laws, 'acts': acts, 'applies': [], 'decisions': dec, 'ai_use': AI_USE,
            '_log': {**{f'old_{k}': v for k, v in log_old.items()}, **{f'new_{k}': v for k, v in log_new.items()}}}


def main() -> None:
    which = sys.argv[1:] or ['10', '20', '30']
    for key, name, fn in (('10', '10-constitution', constitution), ('20', '20-code-penal', code_penal),
                          ('30', '30-code-civil', code_civil)):
        if key in which:
            part = fn()
            log = part.pop('_log')
            write_part(name, part)
            print(name, len(part['acts'][0]['versions']), 'versions,', len(part['laws']), 'laws;',
                  {k: len(v) for k, v in log.items()})


if __name__ == '__main__':
    main()
