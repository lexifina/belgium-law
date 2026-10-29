"""Read legalize-be Markdown files (Justel consolidated text) into provisions and Justel's inline notes.

Justel marks every change in its consolidated text:
- inline notes `<L 1997-02-28/31, art. 1, 004; En vigueur : 01-03-1997>`: amending act (L = loi, LS = loi
  spéciale, AR = arrêté royal ...), its date and Justel serial number, the amending article, Justel's archived
  version number (3 digits) and the in-force day;
- numbered markers `[¹ new words]¹` with the note as footnote `(1)<L ...>` under a `----------` rule;
- older bare brackets `[new words]` followed by the note.
We keep the notes as data (dates and credits) and strip them, and the markers, from the text.
"""
from __future__ import annotations

import re
import unicodedata

SUP = '¹²³⁴⁵⁶⁷⁸⁹⁰'
LATIN = ['bis', 'ter', 'quater', 'quinquies', 'sexies', 'septies', 'octies', 'novies', 'nonies', 'decies',
         'undecies', 'duodecies', 'terdecies', 'quaterdecies', 'quinquiesdecies', 'sexiesdecies',
         'septiesdecies', 'octiesdecies', 'noviesdecies', 'vicies']
ROMAN = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
         'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15, 'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19,
         'XX': 20}

LINK = re.compile(r'\[([^\[\]]*)\]\((https?://[^)\s]*)\)')
# one Justel note: <[prefix] L|LS|AR... yyyy-mm-dd/nn[, art. x][, NNN][; En vigueur : D]>
NOTE = re.compile(r'<\s*([^<>]*?)\s*>')
REF = re.compile(r'(?:^|\s)(L|LS|LSP|LO|AR|ARR|A|LW|DCFL|DRW|DCFR|ORD|D|W|ACC|LP)\s*\[?(\d{4}-\d\d-\d\d/\d+)\]?')
OLDREF = re.compile(r'(?:^|\s)(L|LS|AR|A|AL)\s+(\d\d)-(\d\d)-(\d{4})')
VNUM = re.compile(r',\s*(\d{3})\s*;')
INFORCE = re.compile(r'En vigueur\s*:\s*(\d\d)[-/](\d\d)[-/](\d{4})')
INFORCE_ISO = re.compile(r'En vigueur\s*:\s*(\d{4})-(\d\d)-(\d\d)')
FOOTRULE = re.compile(r'^-{5,}\s*$')
FOOTNOTE = re.compile(r'^\((\d+)\)\s*<.*>\s*$')
PARENNOTE = re.compile(r'\((?:voir |NOTE|ACC |L \d|L \[|pour le livre)[^()]*(?:\([^()]*\)[^()]*)*\)', re.I)
# an old-style note in parentheses: "(inséré par L 1996-03-25/34, art. 1, En vigueur: 1996-04-29)"
PARENCHANGE = re.compile(r'\(\s*((?:ins[ée]r[ée]e?s?|abrog[ée]e?s?|remplac[ée]e?s?|modifi[ée]e?s?|r[ée]tablie?s?)'
                         r'\s+par\s+(?:L|LS|AR)\s+\d{4}-\d\d-\d\d/\d+[^()]*)\)', re.I)
HEAD = re.compile(r'^(#{1,6})\s+(.*)$')
ART = re.compile(r'^Article\s+([^\s.]+(?:\s*/\s*\d+)*)\.*\s*(.*)$')


def note_info(inner: str) -> dict | None:
    """Parse the inside of one <...> note. None if it is not a Justel change note."""
    s = LINK.sub(r'\1', inner).replace('**', '')
    m = REF.search(s)
    if m:
        kind, ref = m.group(1), m.group(2)
    else:
        m = OLDREF.search(s)
        if not m:
            return None
        kind, ref = m.group(1), f'{m.group(4)}-{m.group(3)}-{m.group(2)}/?'
    v = VNUM.search(s)
    d = INFORCE.search(s)
    date = f'{d.group(3)}-{d.group(2)}-{d.group(1)}' if d else None
    if not d:
        d = INFORCE_ISO.search(s)
        date = f'{d.group(1)}-{d.group(2)}-{d.group(3)}' if d else None
    low = s.lower()
    return {'kind': kind, 'ref': ref, 'vnum': v.group(1) if v else None, 'date': date,
            'undetermined': 'indéterminée' in low and not date,
            'insert': bool(re.match(r'\s*(ins[ée]r[ée]e?|r[ée]tabli)', low)),
            'repeal': bool(re.match(r'\s*abrog[ée]', low)), 'raw': s.strip()}


def strip_notes(body: str) -> tuple[str, list[dict]]:
    """Text without Justel's notes and markers, plus the notes found (in order)."""
    notes = []
    out_lines = []
    in_foot = False
    for line in body.split('\n'):
        if FOOTRULE.match(line):
            in_foot = True
            continue
        if in_foot:
            if not line.strip():
                continue
            if FOOTNOTE.match(line.strip()):
                inner = line.strip()[line.strip().index('<') + 1:-1]
                n = note_info(inner)
                if n:
                    n['foot'] = True
                    notes.append(n)
                continue
            in_foot = False
        out_lines.append(line)
    s = '\n'.join(out_lines)

    def drop(m):
        n = note_info(m.group(1))
        if n is None and not re.search(r'\d', m.group(1)):
            return m.group(0)
        if n:
            notes.append(n)
        return ' '
    s = LINK.sub(r'\1', s)
    # a note whose "<" Justel misplaced (old versions): "... exprimés. L 2005-02-25/40, art. 1, 019; En vigueur: D>"
    def reopen(m):
        before = s[:m.start()].rsplit('\n', 1)[-1]
        return m.group(0) if before.rfind('<') > before.rfind('>') else '<' + m.group(1)
    s = re.sub(r'(?<![<\w])((?:L|LS|AR) \d{4}-\d\d-\d\d/\d+,[^<>\n]*?En vigueur\s*:[^<>\n]*?>)', reopen, s)
    s = re.sub(r'\s<\s*(?=\n|$)', '', s)
    s = NOTE.sub(drop, s)
    s = PARENCHANGE.sub(drop, s)
    s = PARENNOTE.sub(' ', s)
    s = re.sub(r'\[\s*(\.\.\.|…)\s*\]', '(...)', s)
    s = re.sub(r'\[\s*(Abrog[ée]e?s?)\s*\]', r'(\1)', s)
    s = re.sub(r'\[[' + SUP + r']+\s?', '', s)
    s = re.sub(r'\][' + SUP + r']+', '', s)
    s = s.replace('[', '').replace(']', '').replace('**', '')
    paras = []
    for p in re.split(r'\n\s*\n', s):
        p = re.sub(r'\s+', ' ', p.replace(' ', ' ')).strip()
        p = p.replace('’', "'").replace('‘', "'").replace('…', '...')
        p = re.sub(r'\s+([.,;:])(?=\s|$)', r'\1', p)
        if p and not re.fullmatch(r'[.;,\s]+', p):
            paras.append(p)
    if not paras and any(n['repeal'] for n in notes):
        paras = ['(Abrogé)']
    return '\n'.join(paras) + ('\n' if paras else ''), notes


def canon(text: str) -> str:
    """Text compared without Justel's typesetting: older versions mark changed words with ( ) where newer use
    [ ], and Justel later fixed case, accents and final stops ("alinéa 3 abrogé" -> "Alinéa 3 abrogé.")."""
    t = unicodedata.normalize('NFKD', re.sub(r'[()\[\]]', '', text).lower())
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r'\s+', ' ', re.sub(r'\s+([.,;:])', r'\1', t)).strip()
    return t.rstrip('.;: ')


def art_key(label: str) -> tuple[str, str, str] | None:
    """('art-118-bis', 'Art. 118bis', 'art') from an article label; None if it is not a numbered article."""
    lab = re.sub(r'\s+', '', label).rstrip('.')
    m = re.fullmatch(r'(\d+)([A-Za-z]*)((?:/\d+)*)', lab)
    if m:
        num, suf, sl = m.groups()
        key = f'art-{int(num):03d}'
        if suf:
            key += '-' + suf.lower()
        for part in sl.split('/')[1:]:
            key += f'-{int(part):02d}'
        return key, f'Art. {num}{suf.lower()}{sl}', 'art'
    if lab in ROMAN:
        return f'disp-trans-{ROMAN[lab]:02d}', f'Disposition transitoire {lab}', 'transitional'
    return None


def units(md: str, sub_heads: set[str] | None = None) -> tuple[list[tuple[str, str, str, str]], list[str]]:
    """[(key, label, kind, raw body)] in file order, and the labels we could not key.

    The article heading `##### Article 59. first paragraph` opens a unit, which runs to the next heading.
    A `## Disposition transitoire.` heading right inside an article (whose key is in sub_heads, if given) is a
    paragraph of that article; anywhere else (legalize-be repeats such blocks after section headings) it is dropped."""
    if md.startswith('---'):
        md = md.split('\n---', 1)[1].split('\n', 1)[1]
    out: list[list] = []
    skipped = []
    cur = None
    prev = None
    for line in md.split('\n'):
        h = HEAD.match(line)
        if h:
            title = h.group(2).strip()
            a = ART.match(title)
            prev, cur = cur, None
            if a and len(h.group(1)) == 5:
                lab, rest = a.group(1), a.group(2)
                # legalize-be sometimes doubles the label: "Article 112/1.. 112/1. text"
                rest = re.sub(r'^' + re.escape(lab) + r'\.\s*', '', rest)
                k = art_key(lab)
                if k is None:
                    skipped.append(lab)
                    continue
                cur = [k[0], k[1], k[2], [rest]]
                out.append(cur)
            elif (re.match(r'Dispositions? transitoires?\.?$', title, re.I) and prev is not None
                  and (sub_heads is None or prev[0] in sub_heads) and len(prev) == 4
                  and not any(re.fullmatch(r'Dispositions? transitoires?\.?', x.strip(), re.I) for x in prev[3])):
                # a paragraph of the article that legalize-be rendered as a heading (once: legalize-be
                # repeats the block)
                cur = prev
                cur[3] += ['', title, '']
                cur.append('sub')
            continue
        if cur is not None:
            cur[3].append(line)
    res = [(u[0], u[1], u[2], '\n'.join(u[3]).strip('\n')) for u in out]
    return res, skipped
