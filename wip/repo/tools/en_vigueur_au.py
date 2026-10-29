"""Prints Belgian law as it stood on a given day, read from this repository's history.

    python tools/en_vigueur_au.py 2014-01-30 constitution 151       # art. 151 the day before the 2014 revision
    python tools/en_vigueur_au.py 2014-01-31 constitution 151       # the same article, as revised
    python tools/en_vigueur_au.py 2024-06-03 constitution 7bis      # an inserted article (7bis, 22ter, 157bis)
    python tools/en_vigueur_au.py 2000-01-01 constitution           # the whole Constitution on 1 January 2000
    python tools/en_vigueur_au.py --law 2020-01-01 constitution 41  # also name the act behind that wording

A thin wrapper around tools/on.py: the version is chosen by each commit's `In-force:` trailer, never by its commit
date, and branches named wip* are ignored. An article number (`41`, `7bis`, `112/1`) becomes the file key
(`art-041`, `art-007-bis`, `art-112-01`); Roman numbers (`I`, `IV`) are the transitional provisions of the
Constitution (`disp-trans-01`, `disp-trans-04`). Standard library only.
"""
import re
import runpy
import sys
from pathlib import Path

ROMAN = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}


def article(unit: str) -> str:
    u = unit.strip()
    if u.upper() in ROMAN:
        return f'disp-trans-{ROMAN[u.upper()]:02d}'
    m = re.fullmatch(r'(\d+)([A-Za-z]*)((?:/\d+)*)', u.replace(' ', ''))
    if not m:
        return unit
    key = f'art-{int(m.group(1)):03d}'
    if m.group(2):
        key += '-' + m.group(2).lower()
    for part in m.group(3).split('/')[1:]:
        key += f'-{int(part):02d}'
    return key


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    args = [a for a in sys.argv[1:] if a != '--law']
    if len(args) == 3:
        i = len(sys.argv) - 1 - sys.argv[::-1].index(args[2])
        sys.argv[i] = article(args[2])
    sys.argv[0] = str(Path(__file__).with_name('on.py'))
    runpy.run_path(sys.argv[0], run_name='__main__')
