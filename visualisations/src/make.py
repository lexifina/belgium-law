"""Rebuild visualisations/belgisch-recht-in-20-grafieken.html from this repository.

    python visualisations/src/make.py [--repo PATH] [--ref REF] [--skip-extract]

Steps (all read-only on the repository; scratch output goes to visualisations/src/.build/):
  1. git log of REF, streamed: one line per commit with its author, dates, subject and the trailers the charts use
                                                    -> .build/log.tsv
  2. git log --name-status of REF, streamed: one line per file a commit adds, changes or deletes
                                                    -> .build/names.tsv
  3. the blobs the charts read, listed from the tree of REF:
     - the tables data/laws.csv and data/versions.json, and REPRODUCE.md        -> .build/repo/
     - record.json of every act of 2025 and of every law of 2026 (folders arrete/, decret/, loi/, ordonnance/,
       reglement/, norm/, convention/, circulaire/, accord/, loi-2026*/)       -> .build/records.jsonl
     - the text (text.md or texte.md) of those acts                            -> .build/texts.jsonl
     - the metadata of every court decision in caselaw/ (source.json, nl.json, fr.json) and the first 2,000
       characters of the Council of State's decision texts                    -> .build/caselaw.jsonl
     - the articles of the new Code pénal (code-penal-2024/)                   -> .build/penal2024.jsonl
  4. prep.py turns those into .build/data.json; build.py fills page.tpl.html with it.
In a partial (blobless) clone the missing blobs are fetched in one batch per step; nothing is held in memory at once:
the history and the texts are streamed line by line.
"""
import argparse, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--repo', default=os.path.abspath(os.path.join(HERE, '..', '..')))
ap.add_argument('--ref', default=None, help='default: origin/main if present, else HEAD')
ap.add_argument('--out', default=os.path.join(HERE, '..', 'belgisch-recht-in-20-grafieken.html'))
ap.add_argument('--skip-extract', action='store_true', help='reuse .build/ from a previous run (prep and build only)')
a = ap.parse_args()
B = os.path.join(HERE, '.build')
os.makedirs(B, exist_ok=True)
NOLAZY = dict(os.environ, GIT_NO_LAZY_FETCH='1')


def git(*args, **kw):
    return subprocess.run(['git', '-C', a.repo, *args], check=True, capture_output=True, env=NOLAZY, **kw).stdout


ref = a.ref
if not ref:
    ref = 'origin/main' if subprocess.run(['git', '-C', a.repo, 'rev-parse', '--verify', '-q', 'origin/main'], capture_output=True).returncode == 0 else 'HEAD'
sha = git('rev-parse', ref).decode().strip()
print('ref', ref, sha)


def fetch_missing(oids):
    """one batched fetch for the blobs a partial clone does not have yet"""
    oids = sorted(set(oids))
    chk = subprocess.run(['git', '-C', a.repo, 'cat-file', '--batch-check'], input=''.join(o + '\n' for o in oids).encode(),
                         capture_output=True, env=NOLAZY).stdout.decode().split('\n')
    missing = [l.split()[0] for l in chk if l.endswith(' missing')]
    if missing:
        print('fetching', len(missing), 'blobs')
        subprocess.run(['git', '-C', a.repo, '-c', 'fetch.negotiationAlgorithm=noop', 'fetch', 'origin', '--no-tags', '--no-write-fetch-head',
                        '--recurse-submodules=no', '--filter=blob:none', '--stdin'], input=''.join(m + '\n' for m in missing).encode(), check=False)


def read_blobs(items):
    """yield (path, bytes) for (oid, path) pairs, one blob at a time"""
    p = subprocess.Popen(['git', '-C', a.repo, 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=NOLAZY)
    for oid, path in items:
        p.stdin.write((oid + '\n').encode()); p.stdin.flush()
        head = p.stdout.readline().split()
        if len(head) < 3:
            sys.exit('cannot read ' + path)
        data = p.stdout.read(int(head[2])); p.stdout.read(1)
        yield path, data
    p.stdin.close(); p.wait()


def ls_tree(treeish, *paths):
    """(oid, path) of every blob under these paths; never reads a blob (so never fetches one)"""
    out = []
    for i in range(0, max(1, len(paths)), 80):
        for e in git('ls-tree', '-r', '-z', treeish, '--', *paths[i:i + 80]).split(b'\0'):
            if not e:
                continue
            meta, path = e.split(b'\t', 1)
            _, typ, oid = meta.split()
            if typ == b'blob':
                out.append((oid.decode(), path.decode('utf-8')))
    return out


TRAILERS = ['Kind', 'In-force', 'Enacted', 'Published', 'Law', 'Act', 'Provisions', 'Source', 'Also-amended-by']
ACT_KINDS = ('arrete', 'decret', 'loi', 'ordonnance', 'reglement', 'norm', 'convention', 'circulaire', 'accord')
if not a.skip_extract:
    # 1. the history, streamed (a trailer that occurs more than once, like Also-amended-by, is joined with " ; ")
    fmt = '%x1e%H%x1f%an%x1f%ad%x1f%s%x1f%(trailers:unfold,separator=%x1d)'
    lg = subprocess.Popen(['git', '-C', a.repo, 'log', ref, '--date=short', '--format=' + fmt], stdout=subprocess.PIPE, env=NOLAZY)
    n, buf = 0, b''
    with open(os.path.join(B, 'log.tsv'), 'w', encoding='utf-8', newline='\n') as out:
        out.write('\t'.join(['sha', 'author', 'date', 'subject'] + TRAILERS) + '\n')

        def emit(rec):
            global n
            rec = rec.decode('utf-8', 'replace').strip('\n')
            if not rec:
                return
            parts = rec.split('\x1f')
            tr = {}
            for t in (parts[4] if len(parts) > 4 else '').split('\x1d'):
                k, _, v = t.partition(': ')
                k = k.strip()
                if k:
                    tr.setdefault(k, []).append(v.strip())
            row = parts[:4] + [' ; '.join(tr.get(k, [])) for k in TRAILERS]
            out.write('\t'.join(x.replace('\t', ' ').replace('\n', ' ') for x in row) + '\n')
            n += 1
        for chunk in iter(lambda: lg.stdout.read(1 << 16), b''):
            buf += chunk
            *recs, buf = buf.split(b'\x1e')
            for r in recs:
                emit(r)
        emit(buf)
    lg.wait()
    print('commits', n)

    # 2. the files of each commit, streamed
    lg = subprocess.Popen(['git', '-C', a.repo, 'log', ref, '--format=@@C %H', '--name-status', '--no-renames'], stdout=subprocess.PIPE, env=NOLAZY)
    nf = 0
    with open(os.path.join(B, 'names.tsv'), 'w', encoding='utf-8', newline='\n') as out:
        cur = None
        for raw in lg.stdout:
            l = raw.decode('utf-8', 'replace').rstrip('\n')
            if l.startswith('@@C '):
                cur = l[4:]
                continue
            if l and cur:
                st, _, f = l.partition('\t')
                out.write(f'{cur}\t{st[:1]}\t{f}\n')
                nf += 1
    lg.wait()
    print('file changes', nf)

    # 3. the blobs the charts read
    root = [p.decode() for p in git('ls-tree', '--name-only', '-z', ref).split(b'\0') if p]
    tables = [(o, p) for o, p in ls_tree(ref, 'data', 'REPRODUCE.md') if p in ('data/laws.csv', 'data/versions.json', 'REPRODUCE.md')]
    acts = ls_tree(ref, *ACT_KINDS, *[d for d in root if re.match(r'^loi-20\d{8}$', d)])
    records = [(o, p) for o, p in acts if p.endswith('/record.json')]
    texts = [(o, p) for o, p in acts if p.endswith(('/text.md', '/texte.md'))]
    cl = ls_tree(ref, 'caselaw')
    cmeta = [(o, p) for o, p in cl if p.endswith(('/source.json', '/nl.json', '/fr.json'))]
    ctext = [(o, p) for o, p in cl if p.startswith('caselaw/conseil-etat/') and p.endswith('/decision.txt')]
    penal = [(o, p) for o, p in ls_tree(ref, 'code-penal-2024') if p.endswith('.md') and not p.endswith('README.md')]
    print('tables', len(tables), 'records', len(records), 'texts', len(texts), 'court records', len(cmeta), 'court texts', len(ctext), 'penal 2024', len(penal))
    fetch_missing([o for o, _ in tables + records + texts + cmeta + ctext + penal])
    R = os.path.join(B, 'repo')
    for path, data in read_blobs(tables):
        dst = os.path.join(R, *path.split('/'))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, 'wb') as fh:
            fh.write(data)

    def jsonl(name, items, conv):
        with open(os.path.join(B, name), 'w', encoding='utf-8', newline='\n') as out:
            for path, data in read_blobs(items):
                out.write(json.dumps({'p': path, **conv(path, data)}, ensure_ascii=False) + '\n')
    jsonl('records.jsonl', records, lambda p, d: {'r': json.loads(d.decode('utf-8'))})
    jsonl('texts.jsonl', texts, lambda p, d: {'t': d.decode('utf-8', 'replace')})
    jsonl('caselaw.jsonl', cmeta + ctext, lambda p, d: {'r': json.loads(d.decode('utf-8'))} if p.endswith('.json') else {'t': d.decode('utf-8', 'replace')[:2000]})
    jsonl('penal2024.jsonl', penal, lambda p, d: {'t': d.decode('utf-8', 'replace')})

# 4. prep + build
env = dict(os.environ, HEAD_SHA=sha)
subprocess.run([sys.executable, '-X', 'utf8', os.path.join(HERE, 'prep.py'), B], check=True, env=env)
subprocess.run([sys.executable, '-X', 'utf8', os.path.join(HERE, 'build.py'), os.path.join(B, 'data.json'), os.path.abspath(a.out)], check=True)
