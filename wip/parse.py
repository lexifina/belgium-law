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
        diff = sorted(k for k in set(ours) & set(theirs)
                      if ours[k] != PLACEHOLDER and lmd.canon(ours[k]) != lmd.canon(theirs[k]))
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


def main() -> None:
    which = sys.argv[1:] or ['10']
    if '10' in which:
        part = constitution()
        log = part.pop('_log')
        write_part('10-constitution', part)
        print('constitution:', len(part['acts'][0]['versions']), 'versions,', len(part['laws']), 'laws;',
              {k: len(v) for k, v in log.items()})


if __name__ == '__main__':
    main()
