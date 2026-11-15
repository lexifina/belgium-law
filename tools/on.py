"""Prints the law as it stood on a day, read from this repository's history.

    python tools/on.py 2015-06-01                      # every act's commit in force that day
    python tools/on.py 2015-06-01 constitucion         # the whole act on that day
    python tools/on.py 2015-06-01 constitucion art-019 # one provision (a file name without .md)
    python tools/on.py 2015-06-01 constitucion 19      # the same, by article number
    python tools/on.py --law 2015-06-01 constitucion art-019  # also name the law behind the version shown

Each commit carries the day its change took effect in an `In-force:` trailer. That trailer, not the commit date, is
the source of truth: git cannot store dates before 1970, and reading the trailer avoids time-zone edge cases. The text
in force on a day is the last commit on or before it that touches the act. Laws published but not yet in force live on
the future branch, which is read for days after the newest commit on main. Merge commits are ignored. Standard library
only.
"""
import datetime as dt
import re
import subprocess
import sys


def git(*args: str) -> str:
    return subprocess.run(['git', *args], capture_output=True, text=True, encoding='utf-8', check=True).stdout


def branches() -> tuple[str, str | None]:
    """main, and the future branch named in data/repo.json (local or origin/), if it exists."""
    import json
    try:
        name = json.loads(git('show', 'main:data/repo.json')).get('future_branch')
    except (subprocess.CalledProcessError, ValueError):
        name = None
    if not name:
        return 'main', None
    for ref in (name, f'origin/{name}'):
        if subprocess.run(['git', 'rev-parse', '-q', '--verify', ref], capture_output=True).returncode == 0:
            return 'main', ref
    return 'main', None


def history(branch: str, path: str, repo=None) -> list[tuple[str, str, str]]:
    """(commit, in-force day, author) for every commit touching path, newest first. With the layout map on, under
    today's path and the path before the move, and without the layout commit (Kind: documentation: it moves folders,
    it changes no law)."""
    args = ('log', '--no-merges', '--format=%H%x09%(trailers:key=In-force,valueonly,separator=)%x09%an'
            + ('%x09%(trailers:key=Kind,valueonly,separator=)' if LAYOUT else ''), branch, '--',
            *dict.fromkeys((path, to_old(path))))
    out = git(*args) if repo is None else _g(repo, *args)
    rows = []
    for line in out.splitlines():
        h, d, a, k = (line.split('\t') + ['', '', ''])[:4]
        if d.strip() and not (LAYOUT and 'documentation' in k):
            rows.append((h, d.strip(), a))
    return rows


# Correction commits (Kind: correction). A published text found wrong later is not rewritten: a correction commit at
# the tip carries the corrected text, with the trailers In-force, Corrects (<act> <from>..<to>, open "<from>.." for
# the newest version), Supersedes, Reason, Act-path (the act's folder or file) and Files (one line per corrected
# path; a listed path the commit's tree lacks is removed). Reading rule: the act's text on a day is the commit the
# In-force trailer picks among the commits that touch its Act-path and are not corrections, then, file by file and in
# commit order, each correction whose Corrects range holds the day; an open range ends the day before the next such
# commit with a later In-force day. A history with no correction commit reads exactly as before.

def _g(repo, *args: str) -> str:
    return subprocess.run(['git', *args], cwd=repo, capture_output=True, text=True, encoding='utf-8').stdout


def _day_before(day: str) -> str:
    return (dt.date.fromisoformat(day) - dt.timedelta(days=1)).isoformat()


def _under(p: str, base: str) -> bool:
    return p == base or p.startswith(base + '/')


def _ls(repo, commit: str, path: str) -> dict[str, str]:
    """{path: blob id} of every file at or under `path` in `commit`. With the layout map on (the command line), a
    commit from before the layout change is read at the path the act had then, and its files named by today's paths."""
    out = {}
    for rec in _g(repo, '-c', 'core.quotePath=false', 'ls-tree', '-r', '-z', commit, '--',
                  *dict.fromkeys((path, to_old(path)))).split('\0'):
        meta, _, p = rec.partition('\t')
        if p and meta.split()[1] == 'blob':
            out[to_new(p)] = meta.split()[2]
    return out


# Layout change (data/paths.json, 2026-11-15): act folders moved into one folder per kind (code/, wetboek/, loi/, ...)
# and acts of more than 1,000 articles split into sub-folders. Commits before the change hold the old paths; with the
# map on, history() and _ls() read both, so a day before the change reads as it did. Act names stay as they were
# (`code-penal` in Corrects trailers and data/versions.json); either the name or the folder can be given. Off unless
# main() turns it on, so tools/check_repo.py reads the history exactly as built.
LAYOUT: dict = {}


def _load_layout(ref: str = 'main') -> None:
    """data/paths.json: "paths" {act id: folder} (as in gitlaw_common's on_layout.py), "split" {act id: rule} for the
    acts whose article files sit in sub-folders, "moved" {folder before: folder now} for other folders."""
    import json
    try:
        doc = json.loads(git('show', f'{ref}:data/paths.json'))
    except (subprocess.CalledProcessError, ValueError):
        return
    split = doc.get('split') or {}
    LAYOUT['acts'] = {a: {'path': p, 'split': split.get(a)} for a, p in (doc.get('paths') or {}).items()}
    LAYOUT['moved'] = dict(sorted((doc.get('moved') or {}).items(), key=lambda kv: -len(kv[0])))  # longest first
    LAYOUT['tops'] = {k.split('/', 1)[0] for k in [*LAYOUT['acts'], *LAYOUT['moved']]}


def _bucket(split: str | None, stem: str) -> str | None:
    """The sub-folder of a split act's article file: by 500 article numbers, or by book (livre)."""
    if split == 'range500':
        m = re.match(r'art-(\d+)', stem)
        if m:
            lo = int(m.group(1)) // 500 * 500
            return f'art-{max(lo, 1):04d}-{lo + 499:04d}'
    elif split == 'livre-roman':
        m = re.match(r'art-([ivxlc]+)-', stem)
        if m:
            return f'livre-{m.group(1)}'
    elif split == 'livre':
        m = re.match(r'art-(\d+)-', stem)
        if m:
            return f'livre-{int(m.group(1)):02d}'
    return None


def to_new(p: str) -> str:
    """Today's path of a path (file or folder) as it was before the layout change."""
    if not LAYOUT:
        return p
    top = p.split('/', 1)[0]
    if top not in LAYOUT['tops']:
        return p
    for old, a in LAYOUT.get('acts', {}).items():
        if _under(p, old):
            rest = p[len(old):]
            if a.get('split') and rest.count('/') == 1 and rest.endswith('.md') and rest != '/README.md':
                b = _bucket(a['split'], rest[1:-3])
                if b:
                    return f'{a["path"]}/{b}{rest}'
            return a['path'] + rest
    moved = LAYOUT.get('moved', {})
    for old in moved:
        if _under(p, old):
            return moved[old] + p[len(old):]
    return p


def to_old(p: str) -> str:
    """The path a path of today's layout had before the change (itself if it did not move)."""
    best = None
    for old, a in LAYOUT.get('acts', {}).items():
        if _under(p, a['path']) and (best is None or len(a['path']) > len(best[1])):
            best = (old, a['path'], a.get('split'))
    for old, new in LAYOUT.get('moved', {}).items():
        if _under(p, new) and (best is None or len(new) > len(best[1])):
            best = (old, new, None)
    if not best:
        return p
    old, new, split = best
    parts = p[len(new):].split('/')[1:]
    if split and len(parts) == 2 and parts[1].endswith('.md') and _bucket(split, parts[1][:-3]) == parts[0]:
        parts = parts[1:]
    return '/'.join([old, *parts])


def act_path(act: str) -> str:
    """An act's folder today, given its name (`code-penal`) or its folder (`code/penal`)."""
    act = act.rstrip('/')
    return LAYOUT.get('acts', {}).get(act, {}).get('path') or to_new(act)


def corrections(ref: str, repo=None) -> list[dict]:
    """The correction commits on ref, oldest first: {'commit', 'day', 'ranges': {act: (from, to or None)}, 'paths':
    {act: Act-path}, 'files': {act: {path: blob id, or None if removed}}}. An act's files are those its Files trailers
    name, read from the commit's tree; with no Files trailer, the .md files it changes under the act's path. With no
    Act-path, the folder its Files share, else the act's name."""
    out = _g(repo, 'log', '--no-merges', '--reverse', '--grep=^Kind: *correction', '--format=%H%x1e'
             '%(trailers:key=Kind,valueonly,separator=%x1f)%x1e%(trailers:key=Corrects,valueonly,separator=%x1f)%x1e'
             '%(trailers:key=Act-path,valueonly,separator=%x1f)%x1e%(trailers:key=Files,valueonly,separator=%x1f)%x1e'
             '%(trailers:key=In-force,valueonly,separator=)%x1d', ref)
    fixes = []
    for rec in out.split('\x1d'):
        h, kind, cor, apath, named, day = (rec.strip('\n').split('\x1e') + [''] * 5)[:6]
        if not h or 'correction' not in [k.strip() for k in kind.split('\x1f')]:
            continue
        ranges = {}
        for line in cor.split('\x1f'):
            parts = line.split()
            if len(parts) == 2 and '..' in parts[1]:
                a, _, b = parts[1].partition('..')
                ranges[parts[0]] = (a, b or None)
        acts = list(ranges)
        listed = [to_new(p.strip()) for p in named.split('\x1f') if p.strip()]
        given = [to_new(p.strip().rstrip('/')) for p in apath.split('\x1f') if p.strip()]
        paths = {}
        for i, a in enumerate(acts):
            if i < len(given):
                paths[a] = given[i]
            else:
                dirs = {p.rsplit('/', 1)[0] for p in listed if '/' in p}
                paths[a] = dirs.pop() if len(dirs) == 1 and len(acts) == 1 else act_path(a)
        files: dict[str, dict] = {}
        if listed:
            for a in acts:
                mine = [p for p in listed if _under(p, paths[a])]
                if mine:
                    have = _ls(repo, h, paths[a])
                    files[a] = {p: have.get(p) for p in mine}
        else:
            f = _g(repo, '-c', 'core.quotePath=false', 'diff-tree', '-r', '-z', '--no-renames', '--no-commit-id',
                   f'{h}^', h).split('\0')
            for meta, path in zip(f[0::2], f[1::2]):
                path = to_new(path)
                for a in acts:
                    if _under(path, paths[a]) and path.endswith('.md') and path != f'{paths[a]}/README.md':
                        m = meta.split()
                        files.setdefault(a, {})[path] = None if m[4] == 'D' else m[3]
        fixes.append({'commit': h, 'day': day.strip(), 'ranges': ranges, 'paths': paths, 'files': files})
    return fixes


class Reader:
    """An act's files on a day with correction commits applied (the reading rule above). `base(commit, path)` gives
    an act's files in an ordinary commit (default: the .md files under a folder, README.md excepted, or the one file
    a path names)."""

    def __init__(self, ref: str, repo=None, fixes: list[dict] | None = None, base=None):
        self.ref, self.repo = ref, repo
        self.fixes = corrections(ref, repo) if fixes is None else fixes
        self.skip = {f['commit'] for f in self.fixes}
        self.alias = {p: a for f in self.fixes for a, p in f['paths'].items()}  # Act-path -> act name
        self.base = base or self._base
        self._rows: dict[str, list] = {}

    def name(self, act: str) -> str:
        """The act's name in Corrects, for an act given by name or by path."""
        return self.alias.get(act.rstrip('/'), act)

    def path(self, act: str) -> str:
        n = self.name(act)
        return next((f['paths'][n] for f in self.fixes if n in f['paths']), act_path(act))

    def rows(self, act: str) -> list[tuple[str, str, str]]:
        """(commit, in-force day, author), newest first, of the act's ordinary commits (corrections left out)."""
        p = self.path(act)
        if p not in self._rows:
            self._rows[p] = [r for r in history(self.ref, p, self.repo) if r[0] not in self.skip]
        return self._rows[p]

    def _base(self, commit: str, path: str) -> dict[str, str]:
        files = _ls(self.repo, commit, path)
        if path.endswith('.md'):
            return files
        return {f: o for f, o in files.items() if f.endswith('.md') and not f.endswith('/README.md')}

    def files(self, act: str, day: str, rows: list | None = None) -> tuple[dict[str, str] | None, tuple | None, list]:
        """({path: blob id} on `day`, or None when nothing is in force; the ordinary commit's row; the corrections
        applied, in commit order). `rows`: the act's ordinary (commit, day, ...) rows, newest first, if known."""
        n, p = self.name(act), self.path(act)
        rows = self.rows(act) if rows is None else rows
        hit = next((r for r in rows if r[1] <= day), None)
        out = dict(self.base(hit[0], p)) if hit else None
        used = []
        for f in self.fixes:
            if n not in f['ranges']:
                continue
            a, b = f['ranges'][n]
            if b is None:
                b = _day_before(min((r[1] for r in rows if r[1] > a), default='9999-12-31'))
            if a <= day <= b:
                out = out if out is not None else {}
                for fp, o in f['files'].get(n, {}).items():
                    if o is None:
                        out.pop(fp, None)
                    else:
                        out[fp] = o
                used.append(f)
        return out, hit, used


def commit_on(day: str, path: str) -> tuple[str, str, str] | None:
    main, future = branches()
    rows = history(main, path)
    if future and (not rows or day > rows[0][1]):
        rows = history(future, path) or rows
    for h, d, a in rows:
        if d <= day:
            return h, d, a
    return None


def resolve(commit: str, act: str, unit: str, files: list[str] | None = None) -> str | None:
    """An act's file for a unit given by file name (`art-019`) or by number (`19`); the file may sit in a sub-folder
    of the act (an act split by article numbers or by book)."""
    if files is None:
        files = list(_ls(None, commit, act))
    files = [f for f in files if _under(f, act)]
    name = lambda f: f.rsplit('/', 1)[1]  # noqa: E731
    exact = [f for f in files if name(f) == f'{unit}.md']
    if len(exact) == 1:
        return exact[0]
    m = re.fullmatch(r'(\d+)(.*)', unit)
    if m:
        want = re.compile(rf'[a-z-]*0*{int(m.group(1))}{re.escape(m.group(2))}\.md')
        hits = [f for f in files if want.fullmatch(name(f))]
        # A bare number means the article: "19" is art-019, not a transitional provision numbered 19.
        arts = [f for f in hits if name(f).startswith(('art-', 'art'))]
        if len(arts) == 1:
            return arts[0]
        if len(hits) == 1:
            return hits[0]
        if hits:
            sys.exit(f'{unit} is ambiguous in {act}: {", ".join(name(h)[:-3] for h in hits)}. Give the file name.')
    return None


def _acts() -> list[str]:
    """What `on.py <day>` lists: every act folder of the layout map, and each other top-level folder."""
    paths = [p for p in git('-c', 'core.quotePath=false', 'ls-tree', '-r', '--name-only', 'main').split('\n') if '/' in p]
    acts = {a['path'] for a in LAYOUT.get('acts', {}).values()}
    top = {p.split('/')[0] for p in paths if not any(_under(p, a) for a in acts)}
    return sorted(acts | top - {'data', 'tools', 'visualisations', 'vulnerabilities'})


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = sys.argv[1:]
    show_law = '--law' in args
    args = [a for a in args if a != '--law']
    if not args:
        sys.exit(__doc__)
    day = args[0]
    try:
        dt.date.fromisoformat(day)
    except ValueError:
        sys.exit(f'{day!r} is not a date (YYYY-MM-DD).')
    _load_layout()
    main_ref, future = branches()
    readers = {r: Reader(r) for r in (main_ref, future) if r}
    if any(rd.fixes for rd in readers.values()):
        return corrected(day, args, show_law, readers[main_ref], readers.get(future))
    if len(args) == 1:
        for act in _acts():
            hit = commit_on(day, act)
            print(f'{act}\t' + (f'{hit[1]}\t{hit[0][:10]}\t{hit[2]}' if hit else 'not in force yet'))
        return
    act = act_path(args[1])
    hit = commit_on(day, act)
    if not hit:
        sys.exit(f'{act} is not in the record on {day}: it took effect later, or the name is wrong (see `python tools/on.py {day}`).')
    commit = hit[0]
    if len(args) > 2:
        path = resolve(commit, act, args[2])
        if not path:
            sys.exit(f'{act}/{args[2]} was not in the text on {day} (it may have been inserted later or removed earlier).')
        if show_law:
            last = commit_on(day, path)
            print(f'# in force from {last[1]}, last changed by {last[2]} ({last[0][:10]})\n')
        sys.stdout.write(git('cat-file', 'blob', _ls(None, commit, path)[path]))
        return
    files = {f: o for f, o in _ls(None, commit, act).items() if f.endswith('.md') and not f.endswith('/README.md')}
    for f in sorted(files):
        sys.stdout.write(git('cat-file', 'blob', files[f]) + '\n')


def corrected(day: str, args: list[str], show_law: bool, rd_main: Reader, rd_future: Reader | None) -> None:
    """main() for a history with correction commits: the same output, read by the reading rule."""
    def reader(act: str) -> Reader:
        rows = rd_main.rows(act)
        if rd_future and (not rows or day > rows[0][1]) and rd_future.rows(act):
            return rd_future
        return rd_main

    def mark(used: list) -> str:
        return f'\tcorrected by {used[-1]["commit"][:10]}' if used else ''

    if len(args) == 1:
        for act in _acts():
            files, hit, used = reader(act).files(act, day)
            if files is None:
                print(f'{act}\tnot in force yet')
            elif hit:
                print(f'{act}\t{hit[1]}\t{hit[0][:10]}\t{hit[2]}{mark(used)}')
            else:
                print(f'{act}\t{used[-1]["ranges"][reader(act).name(act)][0]}\t{used[-1]["commit"][:10]}\tcorrection')
        return
    act = args[1].rstrip('/')
    rd = reader(act)
    files, hit, used = rd.files(act, day)
    if not files:
        sys.exit(f'{act} is not in the record on {day}: it took effect later, or the name is wrong (see `python tools/on.py {day}`).')
    if len(args) > 2 or rd.path(act).endswith('.md'):
        path = rd.path(act) if len(args) == 2 else resolve('', rd.path(act), args[2], sorted(files))
        if not path or path not in files:
            sys.exit(f'{act}/{args[2]} was not in the text on {day} (it may have been inserted later or removed earlier).')
        if show_law:
            fix = next((f for f in reversed(used) if path in f['files'].get(rd.name(act), {})), None)
            if fix:
                print(f'# in force from {fix["ranges"][rd.name(act)][0]}, corrected by {fix["commit"][:10]}\n')
            else:
                last = next((r for r in history(rd.ref, path) if r[0] not in rd.skip and r[1] <= day), hit)
                print(f'# in force from {last[1]}, last changed by {last[2]} ({last[0][:10]})\n')
        sys.stdout.write(git('cat-file', 'blob', files[path]))
        return
    for f in sorted(files):
        sys.stdout.write(git('cat-file', 'blob', files[f]) + '\n')


if __name__ == '__main__':
    main()
