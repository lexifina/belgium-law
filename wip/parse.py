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
        late = [n for n in first['notes'] if day(n) and day(n) > start]
        if late:
            dmax = max(day(n) for n in late)
            ins = sorted((n for n in late if n['insert']), key=day)
            if ins:
                if day(ins[0]) < dmax:
                    ev.append((day(ins[0]), PLACEHOLDER, laws.credit([ins[0]]), 'inserted; first wording not in source'))
            else:
                ev.append((start, PLACEHOLDER, [], 'source wording is later than this day'))
                log['placeholder_start'].append(k)
            ev.append((dmax, first['text'], laws.credit([n for n in late if day(n) == dmax]), 'notes'))
        elif first['i'] == 0:
            ev.append((start, first['text'], [], 'first'))
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


def write_part(name: str, part: dict) -> None:
    OUT.mkdir(exist_ok=True)
    p = OUT / f'{name}.json'
    tmp = p.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    os.replace(tmp, p)
