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
LAW_KINDS = {'L': ('L', 'law'), 'LS': ('LS', 'law'), 'LSP': ('LSP', 'law'), 'LO': ('LO', 'law'),
             'AR': ('AR', 'decree'), 'ARR': ('ARR', 'decree'), 'A': ('A', 'decree'), 'AL': ('AL', 'decree'),
             'LW': ('LW', 'law'), 'W': ('W', 'law'), 'ACC': ('ACC', 'court'), 'LP': ('LP', 'law'),
             'DCFL': ('DCFL', 'law'), 'DRW': ('DRW', 'law'), 'DCFR': ('DCFR', 'law'), 'ORD': ('ORD', 'law'),
             'D': ('D', 'law')}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def cached(url: str) -> bytes:
    return (CACHE / sha(url.encode())).read_bytes()


def legalize_rows(numac: str) -> list[dict]:
    idx = json.loads((CACHE / 'legalize' / 'index.json').read_text(encoding='utf-8'))
    rows = []
    for r in idx['commits']:
        if r['numac'] != numac:
            continue
        url = f'https://raw.githubusercontent.com/{REPO}/{r["commit"]}/be/{numac}.md'
        raw = cached(url)
        m = re.search(r'^Source-Id: \S+?@v(\d+):(\d{4}-\d\d-\d\d)', r['message'], re.M)
        rows.append({'commit': r['commit'], 'url': url, 'sha256': sha(raw), 'md': raw.decode('utf-8'),
                     'vnum': m.group(1) if m else '001', 'vdate': m.group(2) if m else None,
                     'src': f'legalize-be {r["commit"][:12]}'})
    return rows


def note_key(n: dict) -> tuple:
    art = re.search(r'\bart\.?\s*([^,;]+)', n['raw'])
    return (n['kind'], n['ref'], art.group(1).strip() if art else '')


def law_key(n: dict) -> str | None:
    if n['ref'].endswith('/?'):
        return None
    label, _ = LAW_KINDS.get(n['kind'], (n['kind'], 'law'))
    return f'{label.lower()}-{n["ref"].replace("/", "-")}'


class History:
    """Successive wordings of each provision of one act, from several sources in order."""

    def __init__(self, sub_heads=None):
        self.seq: dict[str, list[dict]] = {}
        self.labels: dict[str, tuple[str, str]] = {}
        self.sources: list[dict] = []
        self.skipped: set[str] = set()
        self.sub_heads = sub_heads

    def add(self, md: str, src: dict, only: set[str] | None = None, full: bool = False) -> set[str]:
        """Add one source text (all of it, or only units in `only`). Returns the unit keys it holds."""
        i = len(self.sources)
        self.sources.append(src)
        us, sk = lmd.units(md, self.sub_heads)
        self.skipped |= set(sk)
        got = {}
        for k, lab, kind, raw in us:
            if only is not None and k not in only:
                continue
            text, notes = lmd.strip_notes(raw)
            if k in got:   # legalize-be repeats some articles; keep the fuller copy
                if len(text) <= len(got[k][0]):
                    continue
            got[k] = (text, notes, lab, kind)
        for k, (text, notes, lab, kind) in got.items():
            s = self.seq.setdefault(k, [])
            self.labels[k] = (lab, kind)
            if not s or s[-1]['text'] != text:
                s.append({'i': i, 'text': text, 'notes': notes})
            else:
                s[-1]['notes_last'] = notes
        if full:
            src['full'] = set(got)
        return set(got)


def final_dates(h: History) -> dict:
    """The in-force day of every note, from its latest appearance (Justel corrects some dates later)."""
    out = {}
    for s in h.seq.values():
        for w in s:
            for n in w['notes'] + w.get('notes_last', []):
                if n['date']:
                    out[note_key(n)] = n['date']
                elif n['undetermined']:
                    out.setdefault(note_key(n), None)
    return out


def normalise_markup(h: History) -> int:
    """Older Justel versions mark changed words with ( ) where newer ones use [ ] (both stripped here, but not
    the parentheses). Where a paragraph's words equal a later paragraph's, take the later rendering; then merge
    wordings that became identical. Returns the number of wordings merged."""
    merged = 0
    for k, s in h.seq.items():
        for j in range(len(s) - 2, -1, -1):
            later = {lmd.canon(p): p for p in s[j + 1]['text'].splitlines()}
            paras = [later.get(lmd.canon(p), p) for p in s[j]['text'].splitlines()]
            s[j]['text'] = '\n'.join(paras) + ('\n' if paras else '')
        out = []
        for w in s:
            if out and out[-1]['text'] == w['text']:
                out[-1]['notes_last'] = w['notes']
                out[-1].setdefault('merged', []).append(w['i'])
                merged += 1
                continue
            out.append(w)
        h.seq[k] = out
    return merged


def timeline(h: History, start: str, decisions: list, laws: dict) -> dict[str, list[tuple]]:
    """Per unit: [(day, text or None, [law keys], why)], dated by the notes each wording gained."""
    fd = final_dates(h)
    tl: dict[str, list] = {}
    unexplained = []
    backwards = []

    def credit(ns):
        ks = []
        for n in ns:
            k = law_key(n)
            if k:
                ks.append(k)
                if k not in laws:
                    label, kind = LAW_KINDS.get(n['kind'], (n['kind'], 'law'))
                    num = n['ref'].replace('-', '').split('/')
                    laws[k] = {'label': f'{label} {n["ref"]}', 'kind': kind, 'title': None,
                               'enacted': n['ref'][:10], 'published': None,
                               'url': JUSTEL_CN.format(num[0] + num[1].zfill(2)) if kind != 'court' else None,
                               'temporary_until': None, 'restores': None, 'note': None}
        return sorted(set(ks))

    for k, s in h.seq.items():
        ev = []
        first = s[0]
        late = [n for n in first['notes'] if fd.get(note_key(n)) and fd[note_key(n)] > start]
        if h.sources[first['i']].get('first', False) is False and first['i'] > 0:
            # the unit first appears in a later source: inserted, dated by its notes
            late = [n for n in first['notes'] if fd.get(note_key(n))]
        if late:
            ds = sorted({fd[note_key(n)] for n in late})
            dmax = ds[-1]
            ins = [n for n in late if n['insert']]
            if first['i'] > 0 or ins:
                if ins and fd[note_key(ins[0])] < dmax:
                    ev.append((fd[note_key(ins[0])], PLACEHOLDER, credit(ins), 'inserted, wording not in source'))
            else:
                ev.append((start, PLACEHOLDER, [], 'text in source is later'))
                if ds[0] > start and ds[0] < dmax:
                    pass
            ev.append((dmax, first['text'], credit([n for n in late if fd[note_key(n)] == dmax]), 'notes'))
        elif first['i'] == 0:
            ev.append((start, first['text'], [], 'first'))
        else:
            unexplained.append((k, first['i'], 'appears without a dated note'))
            ev.append((h.sources[first['i']]['date'], first['text'], [], 'unexplained'))
        for j in range(1, len(s)):
            w, prev = s[j], s[j - 1]
            old = {note_key(n) for n in prev['notes'] + prev.get('notes_last', [])}
            new = [n for n in w['notes'] if note_key(n) not in old]
            ds = sorted({fd[note_key(n)] for n in new if fd.get(note_key(n))})
            last_day = ev[-1][0]
            if ds:
                dmax = ds[-1]
                if dmax <= last_day:
                    backwards.append((k, w['i'], dmax, last_day))
                    if dmax < last_day:
                        dmax = last_day
                earlier = [n for n in new if fd.get(note_key(n)) and fd[note_key(n)] < dmax
                           and fd[note_key(n)] > last_day]
                if earlier:
                    d0 = min(fd[note_key(n)] for n in earlier)
                    ev.append((d0, PLACEHOLDER, credit([n for n in earlier if fd[note_key(n)] == d0]),
                               'two in-force days in one wording'))
                ev.append((dmax, w['text'], credit([n for n in new if fd.get(note_key(n)) == ds[-1]]), 'notes'))
            else:
                day = h.sources[w['i']]['date']
                if day <= last_day:
                    day = last_day
                unexplained.append((k, w['i'], 'changed without a new dated note'))
                ev.append((day, w['text'], [], 'unexplained'))
        # same day twice: keep the last
        out = []
        for e in ev:
            if out and out[-1][0] == e[0]:
                out[-1] = (e[0], e[1], sorted(set(out[-1][2]) | set(e[2])), e[3])
            else:
                out.append(e)
        tl[k] = out
    h.unexplained = unexplained
    h.backwards = backwards
    return tl


def versions(h: History, tl: dict, act_slug: str) -> list[dict]:
    days = sorted({e[0] for evs in tl.values() for e in evs})
    state: dict[str, str] = {}
    out = []
    for d in days:
        units, credits, changed = {}, {}, False
        for k, evs in tl.items():
            for e in evs:
                if e[0] == d:
                    if state.get(k) != e[1]:
                        changed = True
                        if e[2]:
                            credits[k] = e[2]
                    state[k] = e[1]
        for k in sorted(state):
            if state[k] is not None:
                lab, kind = h.labels[k]
                units[k] = {'label': lab, 'kind': kind, 'text': state[k]}
        if changed or not out:
            srcs = sorted({h.sources[e_i]['url'] for k, evs in tl.items() for e in evs if e[0] == d
                           for e_i in [0]})
            out.append({'from': d, 'units': units, 'credits': credits})
    return out


def finish_versions(h: History, tl: dict) -> list[dict]:
    """Versions as `changes` against the one before (the first holds every unit)."""
    days = sorted({e[0] for evs in tl.values() for e in evs})
    state: dict[str, str | None] = {}
    out = []
    for d in days:
        changes, credits, srcs = {}, {}, set()
        for k in sorted(tl):
            for e in tl[k]:
                if e[0] != d:
                    continue
                if state.get(k) != e[1]:
                    lab, kind = h.labels[k]
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


def write_part(name: str, part: dict) -> None:
    OUT.mkdir(exist_ok=True)
    p = OUT / f'{name}.json'
    tmp = p.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=1, sort_keys=False) + '\n', encoding='utf-8',
                   newline='\n')
    os.replace(tmp, p)
