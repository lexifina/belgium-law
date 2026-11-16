"""Compute every number for the 20 charts into <build>/data.json.

    python prep.py <build-dir>

Reads, from <build> (written by make.py): log.tsv (one line per commit), names.tsv (the files of each commit),
records.jsonl and texts.jsonl (record.json and text of every act of 2025 and every law of 2026), caselaw.jsonl
(court records and the first lines of the Council of State's texts), penal2024.jsonl (the articles of the new
Code pénal) and repo/data/ (laws.csv, versions.json). Every rule that reads a category out of a title or a text
is in this file.
"""
import collections, csv, json, os, re, statistics, sys
from datetime import date, timedelta

B = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '.build')
R = os.path.join(B, 'repo')
OUT, PROFILE = {}, {}
D = lambda s: date.fromisoformat(s[:10])
MED = lambda v: statistics.median(v) if v else None


def jl(name):
    """stream a .jsonl file"""
    with open(os.path.join(B, name), encoding='utf-8') as fh:
        for line in fh:
            yield json.loads(line)


def clean(s):
    return re.sub(r'\s+', ' ', s or '').strip()


def q(v, p):
    """the p-quantile of a sorted list (nearest rank, as the tables show whole days)"""
    v = sorted(v)
    return v[min(len(v) - 1, max(0, int(round(p * (len(v) - 1)))))] if v else None


MOIS = {'janvier': 1, 'fevrier': 2, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6, 'juillet': 7, 'aout': 8, 'août': 8,
        'septembre': 9, 'octobre': 10, 'novembre': 11, 'decembre': 12, 'décembre': 12}


def fr_date(s):
    """'1er octobre 2025' / '15 MAI 2025' -> date"""
    m = re.match(r'\s*(\d{1,2})(?:er)?\s+([a-zéû]+)\s+(\d{4})', s or '', re.I)
    if not m or m.group(2).lower() not in MOIS:
        return None
    try:
        return date(int(m.group(3)), MOIS[m.group(2).lower()], int(m.group(1)))
    except ValueError:
        return None


# ------------------------------------------------------------------ the history
C = []  # newest first
with open(os.path.join(B, 'log.tsv'), encoding='utf-8') as fh:
    head = fh.readline().rstrip('\n').split('\t')
    for line in fh:
        r = dict(zip(head, line.rstrip('\n').split('\t')))
        r['f'] = []
        C.append(r)
BY = {r['sha']: r for r in C}
with open(os.path.join(B, 'names.tsv'), encoding='utf-8') as fh:
    for line in fh:
        h, st, f = line.rstrip('\n').split('\t')
        BY[h]['f'].append((st, f))
print('commits', len(C))

# the French texts of the 24 acts of the codes' history (the Dutch texts repeat five of them and are left out)
CODES = ['constitution', 'code-penal', 'ancien-code-civil', 'code-civil', 'titre-preliminaire-code-procedure-penale',
         'code-instruction-criminelle-livre-1', 'code-instruction-criminelle-livre-2-titre-1', 'code-instruction-criminelle-livre-2-titre-2',
         'code-instruction-criminelle-livre-2-titre-3', 'code-instruction-criminelle-livre-2-titre-4', 'code-instruction-criminelle-livre-2-titres-5-6',
         'code-instruction-criminelle-livre-2-titre-7', 'code-judiciaire', 'code-nationalite', 'code-electoral', 'code-droit-international-prive',
         'loi-protection-donnees', 'loi-contrats-travail', 'loi-bien-etre-travailleurs', 'loi-sur-le-travail', 'loi-etrangers',
         'loi-accidents-travail', 'code-societes-associations', 'code-droit-economique']
NL_TEXTS = ['grondwet', 'strafwetboek', 'wetboek-van-strafvordering-boek-2-titel-2', 'wetboek-van-strafvordering-boek-2-titel-3',
            'wetboek-van-strafvordering-boek-2-titels-5-6']
CODESET = set(CODES)
GROUP = lambda a: 'cic' if a.startswith('code-instruction-criminelle') else a   # the Code d'instruction criminelle's seven texts
CHANGE_KINDS = ('law', 'decree', 'court')                                      # a change credited to an act that made it
PROV = lambda f: f.count('/') == 1 and f.endswith('.md') and not f.endswith('README.md')


def code_files(c):
    """the provision files of the French codes a commit touches: [(status, act folder, file)]"""
    out = []
    for st, f in c['f']:
        a = f.split('/')[0]
        if a in CODESET and PROV(f):
            out.append((st, a, f))
    return out


# ------------------------------------------------------------------ the acts of 2025 and the laws of 2026
ACT_KINDS = ('arrete', 'decret', 'loi', 'ordonnance', 'reglement', 'norm', 'convention', 'circulaire', 'accord')
REC = {}
for o in jl('records.jsonl'):
    folder = o['p'].rsplit('/', 1)[0]
    REC[folder] = o['r']
TXT = {}
for o in jl('texts.jsonl'):
    t = re.sub(r'<[^>]+>', '', o['t'])          # Justel's anchors and links
    TXT[o['p'].rsplit('/', 1)[0]] = t
# the authority that issued an act, from the issuer folder Justel files it under
AUTH = {'autorite-flamande': 'vl', 'wallonia-service': 'wa', 'brussels-capital': 'br', 'brussels-service': 'br', 'french-community': 'fwb',
        'communaute-germanophone': 'dg', 'cocof': 'cocof', 'cocom': 'cocom', 'ordre-barreaux-francophones-germanophone': 'other'}
auth_of = lambda folder: 'fed' if folder.startswith('loi-20') else AUTH.get(folder.split('/')[1], 'fed')


def form_of(title):
    """the kind of act, from the words after the date in its title ('1 OCTOBRE 2025. - Arrêté royal ...')"""
    t = re.sub(r'^.*?\d{4}\s*\.?\s*-\s*', '', title).strip()
    rules = [('wet', r'^Loi\b'), ('decreet', r'^D[ée]cret\b'), ('ordonnantie', r'^Ordonnance\b'), ('kb', r'^Arr[êe]t[ée] royal\b'),
             ('mb', r'^Arr[êe]t[ée] (?:minist[ée]riel\b|(?:du|de la|des) Ministres?\b|de Membres du Coll)'),
             ('regering', r"^Arr[êe]t[ée](?: [\d/]+)? (?:du|de la|de l')\s*(?:Gouvernement|Coll[èée]ge|Ex[ée]cutif)\b"),
             ('besluit', r'^Arr[êe]t[ée]\b'), ('reglement', r'^R[èe]glement\b'), ('cao', r'^Convention collective de travail\b'),
             ('omzendbrief', r'^Circulaire\b'), ('akkoord', r'^Accord de coop[ée]ration\b')]
    for k, rx in rules:
        if re.search(rx, t, re.I):
            return k
    return 'overig'


FORMGROUP = {'wet': 'leg', 'decreet': 'leg', 'ordonnantie': 'leg', 'kb': 'exec', 'mb': 'exec', 'regering': 'exec', 'besluit': 'exec'}
A25 = []  # the acts of 2025
for folder, r in REC.items():
    p_ = folder.split('/')
    if p_[0] not in ACT_KINDS or len(p_) != 4 or p_[2] != '2025':   # <kind>/<issuer>/2025/<number>; two older records filed elsewhere are left out
        continue
    sm = r.get('source_metadata') or {}
    pg = re.sub(r'\D', '', str(sm.get('page', '')))
    A25.append({'f': folder, 'a': auth_of(folder), 'form': form_of(r.get('title', '')), 't': clean(r.get('title', '')),
                'made': r.get('made'), 'pub': r.get('published'), 'inf': r.get('in_force'), 'page': int(pg) if pg else None,
                'amends': any(k.startswith('Ce texte modifie') for k in sm), 'issuer': folder.split('/')[1]})
print('acts of 2025', len(A25), collections.Counter(x['a'] for x in A25), collections.Counter(x['form'] for x in A25))
AUTHS = ['fed', 'vl', 'wa', 'br', 'fwb', 'dg', 'cocof', 'cocom']

# ------------------------------------------------------------------ c01: who makes the rules
rows = []
for k in AUTHS:
    v = [x for x in A25 if x['a'] == k]
    fc = collections.Counter(x['form'] for x in v)
    lag = [(D(x['pub']) - D(x['made'])).days for x in v if x['made'] and x['pub']]
    rows.append({'k': k, 'n': len(v), 'forms': dict(fc), 'leg': sum(1 for x in v if FORMGROUP.get(x['form']) == 'leg'),
                 'exec': sum(1 for x in v if FORMGROUP.get(x['form']) == 'exec'), 'amends': sum(1 for x in v if x['amends']),
                 'med': MED(lag)})
fed_issuers = collections.Counter(x['issuer'] for x in A25 if x['a'] == 'fed')
fed_by = collections.defaultdict(collections.Counter)
for x in A25:
    if x['a'] == 'fed':
        fed_by[x['issuer']][x['form']] += 1
OUT['c01'] = {'rows': rows, 'n': len(A25), 'other': sum(1 for x in A25 if x['a'] == 'other'), 'fed_issuers': fed_issuers.most_common(), 'fed_by': {k: dict(v) for k, v in fed_by.items()},
              'made': [min(x['made'] for x in A25 if x['made']), max(x['made'] for x in A25 if x['made'])],
              'made_q4': sum(1 for x in A25 if x['made'] and x['made'] >= '2025-10-01')}
print('c01', [(r['k'], r['n'], r['leg'], r['exec']) for r in rows], OUT['c01']['made'], OUT['c01']['made_q4'])

# ------------------------------------------------------------------ c02: from signature to the Moniteur belge
BK2 = [(0, 7), (8, 14), (15, 30), (31, 60), (61, 100000)]
rows = []
for k in AUTHS:
    lag = sorted((D(x['pub']) - D(x['made'])).days for x in A25 if x['a'] == k and x['made'] and x['pub'])
    rows.append({'k': k, 'n': len(lag), 'med': MED(lag), 'q1': q(lag, .25), 'q3': q(lag, .75), 'max': max(lag),
                 **{f'b{i}': sum(1 for d in lag if a_ <= d <= z) for i, (a_, z) in enumerate(BK2)}})
allag = [(D(x['pub']) - D(x['made'])).days for x in A25 if x['made'] and x['pub']]
slow = sorted([x for x in A25 if x['made'] and x['pub']], key=lambda x: -(D(x['pub']) - D(x['made'])).days)[:12]
OUT['c02'] = {'rows': rows, 'med': MED(allag), 'n': len(allag),
              'slow': [[x['a'], x['made'], x['pub'], x['t'][:160]] for x in slow]}
print('c02', [(r['k'], r['n'], r['med']) for r in rows], OUT['c02']['med'])

# ------------------------------------------------------------------ c03: when an act takes effect, counted from its publication
def inf_class(pub, inf):
    d = (D(inf) - D(pub)).days
    return 'before' if d < 0 else 'same' if d == 0 else 'd1' if d < 10 else 'd10' if d == 10 else 'd11' if d <= 31 else 'later'


ICL = ['before', 'same', 'd1', 'd10', 'd11', 'later']
rows = []
for k in AUTHS:
    v = [inf_class(x['pub'], x['inf']) for x in A25 if x['a'] == k and x['pub'] and x['inf']]
    c = collections.Counter(v)
    rows.append({'k': k, 'n': len(v), **{c_: c[c_] for c_ in ICL}})
jan1 = sum(1 for x in A25 if x['inf'] == '2026-01-01')
OUT['c03'] = {'rows': rows, 'jan1': jan1, 'n': sum(r['n'] for r in rows),
              'tot': {c_: sum(r[c_] for r in rows) for c_ in ICL}}
print('c03', [(r['k'], r['n'], r['before'], r['d10']) for r in rows], 'jan1', jan1)

# ------------------------------------------------------------------ c04: the page numbers of the Moniteur belge
pts = sorted([[x['pub'], x['page'], x['a'], x['t'][:110]] for x in A25 if x['page'] and x['pub']], key=lambda p: (p[0], p[1]))
OUT['c04'] = {'pts': pts}
y25 = [p for p in pts if p[0].startswith('2025')]
y26 = [p for p in pts if p[0].startswith('2026')]
print('c04', len(y25), len(y26), y25[-1][:2], y26[-1][:2])

# ------------------------------------------------------------------ the federal laws of 2026 (folders loi-2026...), from the history
L26 = {}
for c in C:
    for st, f in c['f']:
        fo = f.split('/')[0]
        if re.match(r'^loi-20\d{8}$', fo) and fo not in L26 and c['Kind'] == 'publisher':
            m = re.search(r'pd_search=(\d{4}-\d{2}-\d{2})', c['Source'])
            L26[fo] = {'t': clean(c['subject']), 'inf': c['In-force'], 'pub': m.group(1) if m else None, 'prov': int(c['Provisions'] or 0)}
for fo, v in L26.items():
    md = fr_date(v['t'])
    v['made'] = md.isoformat() if md else None
print('laws of 2026', len(L26))

# ------------------------------------------------------------------ c05: treaties, and the parliaments that assent to them
# each assent act (portant assentiment) to an international instrument; cooperation agreements between Belgian governments
# are left out. An act that assents to several instruments counts once for each.
PARTNERS = [('CD', r'r[ée]publique d[ée]mocratique du Congo'), ('CG', r'r[ée]publique du Congo'), ('CV', r'Cap-Vert'), ('GA', r'gabonaise'),
            ('SL', r'Sierra Leone'), ('LR', r'Liberia'), ('BR', r'Br[ée]sil'), ('TG', r'togolaise'), ('TZ', r'Tanzanie'), ('SN', r'S[ée]n[ée]gal'),
            ('NL', r'Pays-Bas'), ('MX', r'mexicains'), ('AU', r'Australie'), ('QA', r'Qatar'), ('DZ', r'alg[ée]rienne'), ('CI', r"C[ôo]te d.Ivoire"),
            ('GN', r'R[ée]publique de Guin[ée]e\b'), ('BJ', r'B[ée]nin'), ('BF', r'Burkina Faso'), ('ML', r'\bMali\b'), ('SG', r'Singapour'),
            ('VN', r'Vi[êe]t Nam'), ('IN', r"\bl'Inde\b"), ('TJ', r'Tadjikistan'), ('MY', r'Malaisie'), ('BW', r'Botswana'),
            ('LU', r'Grand-Duch[ée] de Luxembourg'), ('UA', r'Ukraine'), ('KZ', r'Kazakhstan')]
ORGS = [('ilo', r'Conf[ée]rence internationale du Travail|Organisation internationale du Travail'), ('un', r'Nations Unies'),
        ('nato', r"Trait[ée] de l'Atlantique Nord"), ('igad', r'Autorit[ée] intergouvernementale pour le d[ée]veloppement'),
        ('efta', r'Association europ[ée]enne de libre-[ée]change'), ('boip', r'Benelux de la propri[ée]t[ée] intellectuelle'),
        ('oacps', r"Etats d'Afrique, des Cara[ïi]bes et du Pacifique"), ('eurocontrol', r'navigation a[ée]rienne')]


def sign_date(t):
    """the day the instrument was made: 'fait à X le …', else 'signé…', 'adoptée…', 'tenue à … le …'"""
    for rx in [r"\bfaite?s?\s+(?:à|a)\s+[^;]*?\ble\s+(\d{1,2}(?:er)?\s+[a-zéû]+\s+\d{4})", r"\bsign[ée]e?s?\s+(?:à|a)\s+[^;]*?\ble\s+(\d{1,2}(?:er)?\s+[a-zéû]+\s+\d{4})",
               r"\badopt[ée]e?\s+(?:à|a)\s+\S+\s+le\s+(\d{1,2}(?:er)?\s+[a-zéû]+\s+\d{4})", r"\btenue\s+(?:à|a)\s+\S+\s+le\s+(\d{1,2}(?:er)?\s+[a-zéû]+\s+\d{4})"]:
        m = re.search(rx, t, re.I)
        if m:
            d = fr_date(m.group(1))
            if d:
                return d.isoformat()
    return None


def instrument(t):
    """(key, kind, partner) of the instrument a title assents to"""
    org = next((k for k, rx in ORGS if re.search(rx, t, re.I)), None)
    eu = bool(re.search(r"Union europ[ée]enne et ses Etats membres", t))
    pt = next((k for k, rx in PARTNERS if re.search(rx, t, re.I)), None)
    if re.search(r'transport a[ée]rien|services a[ée]riens|services de transport a[ée]rien', t, re.I) and pt:
        return 'air:' + pt, 'air', pt
    if re.search(r'double imposition', t, re.I) and pt:
        return 'tax:' + pt, 'tax', pt
    if eu and re.search(r'protection des investissements', t, re.I):
        return 'ipa:' + pt, 'eu', pt
    if eu and org == 'oacps':
        return 'oacps', 'eu', None
    if eu and re.search(r'partenariat et de coop[ée]ration', t, re.I):
        return 'pca:' + pt, 'eu', pt
    m = re.search(r'Convention n°\s*(\d+)', t)
    if org == 'ilo' and m:
        return 'ilo:' + m.group(1), 'multi', None
    if org == 'un':
        return 'bbnj', 'multi', None
    if org:
        return org, 'org', None
    if pt:
        return 'bi:' + pt, 'other', pt
    return 'other', 'other', None


treaties = []
srcs = [(f, REC[f].get('title', ''), REC[f].get('made'), auth_of(f), form_of(REC[f].get('title', ''))) for f in REC if f.split('/')[0] in ACT_KINDS]
srcs += [(f, v['t'], v['made'], 'fed', 'wet') for f, v in L26.items()]
for f, t, made, au, fm in srcs:
    t = clean(t)
    if not re.search(r'\bportant assentiment\b', t, re.I) or re.search(r'accord de coop[ée]ration du \d', t, re.I):
        continue
    parts = re.split(r';\s*\d°\s*', t) if 'actes internationaux suivants' in t else [t]
    for pt_ in parts:
        key, kind, partner = instrument(pt_)
        treaties.append({'f': f, 'a': au, 'form': fm, 'made': made, 'sign': sign_date(pt_), 'key': key, 'kind': kind, 'p': partner,
                         'transferred': bool(re.search(r"mati[èe]res dont l'exercice a [ée]t[ée] transf[ée]r[ée]", t)), 't': pt_[:400]})
inst = collections.OrderedDict()
for x in sorted(treaties, key=lambda x: (x['sign'] or '9999', x['made'] or '')):
    inst.setdefault(x['key'], []).append(x)
OUT['c05'] = {'acts': treaties, 'n_acts': len({x['f'] for x in treaties}), 'n_inst': len(inst)}
lags = [(D(x['made']) - D(x['sign'])).days / 365.25 for x in treaties if x['sign'] and x['made']]
print('c05', len(treaties), 'acts', OUT['c05']['n_acts'], 'instruments', len(inst), 'median years', round(MED(lags), 1), 'no sign date',
      [x['t'][:80] for x in treaties if not x['sign']])
for k, v in inst.items():
    print('   ', k, v[0]['kind'], v[0]['sign'], [(x['a'], x['made']) for x in v])

# ------------------------------------------------------------------ c06: EU directives, and which governments transpose them
# an act transposes a directive when it says so itself ('Le présent arrêté transpose (partiellement) la directive …',
# 'La présente loi assure la transposition …', a heading 'Dispositions transposant …', or its own title '… transposant la
# directive …'). Only the text before the act's first amending instruction is read, so a transposition clause the act
# writes into another act ('… est remplacé par ce qui suit : « Le présent arrêté transpose … »') does not count; in a
# directive's own title, the directives it amends, repeals or replaces are not counted.
DIRX = r"\bdirectives?\s+(?:d[ée]l[ée]gu[ée]e\s+|d'ex[ée]cution\s+)?(?:\((?:UE|CE|CEE)\)\s*)?(?:n°\s*)?(\d{2,4})\s*/\s*(\d{1,4})(?:\s*/\s*(?:UE|CE|CEE))?"
NUMX = r"(?:\((?:UE|CE|CEE)\)\s*)?(\d{2,4})\s*/\s*(\d{1,4})(?:\s*/\s*(?:UE|CE|CEE))?"
SELFX = (r"(?:(?:Le|La|Les)\s+pr[ée]sente?s?\s+(?:loi|d[ée]cret|arr[êe]t[ée](?:\s+royal|\s+minist[ée]riel)?|ordonnance|r[èe]glement|titre|chapitre|section|livre"
         r"|article|code|dispositions?|partie)\b[^.;:]{0,120}?|\barticle\s+\d+\w*\s+de\s+la\s+pr[ée]sente\s+loi\s+|\bDispositions?\s+)(transpos\w+|transposition)")
STOPX = (r"(?:par ce qui suit|r[ée]dig[ée]e?s?\s+comme suit|est remplac[ée]e?\s+par|sont remplac[ée]e?s\s+par|est ins[ée]r[ée]e?|sont ins[ée]r[ée]e?s"
         r"|est compl[ée]t[ée]e?|est r[ée]tabli)")
TITLEDOC = lambda y: ('19' if int(y) > 50 else '20') + y if len(y) == 2 else y


def dirs_in(seg):
    """the directives a transposition clause names: the first one, then any further numbered item or 'et la directive …'"""
    out = []
    for k, it in enumerate(re.split(r';\s*|\s(?=\d+°\s)', seg)):
        m = re.search(DIRX, it, re.I) or (re.search(r'^\s*\d+°\s*' + NUMX, it) if k else None)
        if not m or re.search(r'(modifiant|abrogeant|rempla[çc]ant|compl[ée]tant|en ce qui concerne|relative)', it[:m.start()], re.I):
            continue
        out.append((f'{TITLEDOC(m.group(1))}/{int(m.group(2))}', clean(it[m.end():m.end() + 260])))
        if k == 0:
            rest = it[m.end():]
            cut = re.search(r'(modifiant|abrogeant|rempla[çc]ant|compl[ée]tant|en ce qui concerne|relative|concernant|\bsur\s|[ée]tablissant|portant)', rest, re.I)
            for m2 in re.finditer(r'\bet\s+(?:la\s+|de\s+la\s+)?' + DIRX, rest[:cut.start()] if cut else rest, re.I):
                out.append((f'{TITLEDOC(m2.group(1))}/{int(m2.group(2))}', ''))
    return out


def title_of(f):
    return REC[f].get('title', '') if f in REC else L26.get(f, {}).get('t', '')


def is_2025_act(f):
    p = f.split('/')
    return p[0] in ACT_KINDS and len(p) == 4 and p[2] == '2025'


TR = []  # (act, authority, directive, words after the number)
for f, t in TXT.items():
    if not (is_2025_act(f) or f in L26):
        continue
    t = clean(t)
    st = re.search(STOPX, t, re.I)
    body = (t[:st.start()] if st else t)[:8000]
    hits = []
    for m in re.finditer(SELFX, body, re.I):
        seg = re.split(r'\.\s+(?:Art\.?\s|Article\s|CHAPITRE|Chapitre|TITRE|Titre|Section)', body[m.end():m.end() + 700])[0]
        hits += dirs_in(seg)
    if not hits:
        tl = clean(title_of(f))
        tm = re.search(r'\b(?:et\s+)?(transposant|portant transposition|visant [àa] transposer)\b', tl, re.I)
        if tm and not re.search(r"(?:de la loi|du d[ée]cret|de l'arr[êe]t[ée]|de l'ordonnance|du r[èe]glement)\s+(?:royal\s+)?du\s+\d[^,]{0,40}$", tl[:tm.start()], re.I):
            hits = dirs_in(tl[tm.end():tm.end() + 400])
    seen = set()
    for d, words in hits:
        if d not in seen:
            seen.add(d)
            TR.append({'f': f, 'a': auth_of(f), 'd': d, 'w': words, 'made': (REC.get(f) or {}).get('made') or L26.get(f, {}).get('made'),
                       't': clean(title_of(f))[:200]})
dauth = collections.defaultdict(lambda: collections.Counter())
for x in TR:
    dauth[x['d']][x['a']] += 1
drows = [{'d': d, 'by': dict(v), 'n': sum(v.values()), 'w': next((x['w'] for x in TR if x['d'] == d and x['w']), '')} for d, v in dauth.items()]
drows.sort(key=lambda r: (-len(r['by']), -r['n'], r['d']))
nacts = collections.Counter(x['a'] for x in {x['f']: x for x in TR}.values())
OUT['c06'] = {'rows': drows, 'acts': len({x['f'] for x in TR}), 'by_auth': dict(nacts), 'pairs': TR,
              'n_all': {k: sum(1 for x in A25 if x['a'] == k) + (len(L26) if k == 'fed' else 0) for k in AUTHS}}
print('c06', len(TR), 'pairs', OUT['c06']['acts'], 'acts', len(drows), 'directives', 'shared', [(r['d'], r['by']) for r in drows if len(r['by']) > 1], dict(nacts))

# ------------------------------------------------------------------ c07: the federal laws of 2025–2026: which chambers, and what they do
# article 1 of every law says which article of the Constitution governs its procedure: 74 (the Chamber alone), 77 (the
# Chamber and the Senate on an equal footing) or 78 (the Senate may examine it). The kind of law is read from its title;
# the words of a title that only name the law being amended ('… de la loi du … portant dispositions diverses') do not count.
KIND07 = [('revision', r'^R[ée]vision de\b', 0), ('special', r'^Loi sp[ée]ciale\b', 0), ('assent', r'\bportant (?:assentiment|approbation)\b', 0),
          ('penal', r"\bconcordance\b|\bharmonisation\b[^.]*Code p[ée]nal|Code p[ée]nal du 29 f[ée]vrier 2024|introduisant le livre I(?:er)? du Code p[ée]nal", 0),
          ('eu', r"\btranspos\w*|\bmettant en (?:oe|œ)uvre le r[èe]glement \((?:UE|CE)\)", 0),
          ('omnibus', r"^Loi-programme|^Loi-cadre|\b(?:portant|instaurant|contenant)\s+(?:des\s+)?(?:dispositions|mesures)\s+(?:[a-zéèû]+\s+)?(?:diverses|urgentes)\b"
                      r"|\bdiverses\s+(?:dispositions|mesures)\b|\bdispositions\s+(?:[a-zéèû]+\s+)?diverses\b", 1),
          ('budget', r"\bbudg[ée]t|\bVoies et Moyens\b|\bcontingent de l'arm[ée]e\b", 1), ('natur', r'\bnaturalisations?\b', 0),
          ('amend', r"\b(?:modifiant|portant modification|portant des modifications|portant abrogation|r[ée]tablissant|interpr[ée]tative|prorogation|prolongeant"
                    r"|portant ratification|portant confirmation|abrogeant|compl[ée]tant|portant l'insertion|ins[ée]rant)\b", 0)]


def kind07(title):
    t = re.sub(r'^.*?\d{4}\s*\.?\s*-\s*', '', title).strip()
    head = re.split(r"\b(?:la loi|les lois|le Code|l'arr[êe]t[ée]|le d[ée]cret|la loi-programme)\s+(?:du|de|coordonn|ordinaire|sp[ée]ciale)\b", t)[0]
    for k, rx, use_head in KIND07:
        if re.search(rx, head if use_head else t, re.I):
            return k
    return 'new'


PROV25 = {}
for c in C:
    if c['Kind'] == 'publisher' and c['Provisions']:
        for st, f in c['f']:
            fo = f.rsplit('/', 1)[0]
            if is_2025_act(fo) and fo not in PROV25:
                PROV25[fo] = int(c['Provisions'])
laws07 = []
for f, t, made, inf, prov in [(x['f'], x['t'], x['made'], x['inf'], PROV25.get(x['f'])) for x in A25 if x['form'] == 'wet'] + \
                             [(f, v['t'], v['made'], v['inf'], v['prov']) for f, v in L26.items()]:
    body = clean(TXT.get(f, ''))[:6000]
    arts = set()
    for m in re.finditer(r"r[èe]gl(?:e|ent)\s*,?\s*(?:en application de l.article \d+ de la Constitution,\s*)?une mati[èe]re vis[ée]e (?:à|aux|par) (?:l.)?articles?\s+([\d ,età]+)", body):
        arts |= {int(x) for x in re.findall(r'\d+', m.group(1)) if int(x) in (74, 77, 78)}
    proc = '/'.join(str(x) for x in sorted(arts)) or 'none'
    laws07.append({'f': f, 'made': made, 'inf': inf, 'prov': prov, 'proc': proc, 'k': kind07(t), 't': clean(t)[:240]})
laws07.sort(key=lambda x: x['made'] or '')
OUT['c07'] = {'laws': laws07}
print('c07', len(laws07), collections.Counter(x['proc'] for x in laws07), collections.Counter(x['k'] for x in laws07),
      [(x['t'][:60], x['proc']) for x in laws07 if x['proc'] in ('77', '78')])

# ------------------------------------------------------------------ the amending acts (data/laws.csv)
LAWS = list(csv.DictReader(open(os.path.join(R, 'data', 'laws.csv'), encoding='utf-8')))
is_law = lambda r: r['kind'] == 'law' and (r['label'].startswith('L ') or r['label'].startswith('Loi du'))
print('laws.csv', len(LAWS), sum(1 for r in LAWS if is_law(r)))

# ------------------------------------------------------------------ c08: the legislative calendar: amending laws by the month they were enacted
grid = collections.Counter()
for r in LAWS:
    if is_law(r) and r['enacted'] >= '1995':
        grid[(int(r['enacted'][:4]), int(r['enacted'][5:7]))] += 1
OUT['c08'] = {'grid': [[y, m, n] for (y, m), n in sorted(grid.items())], 'y0': 1995}
print('c08', sum(grid.values()), [(y, sum(grid[(y, m)] for m in range(1, 13))) for y in (2007, 2010, 2014, 2019, 2024)])

# ------------------------------------------------------------------ c09: from enactment to the Moniteur belge, and from there to entry into force
lag = collections.defaultdict(list)
icl = collections.defaultdict(collections.Counter)
for r in LAWS:
    if not is_law(r) or not r['published'] or not r['enacted']:
        continue
    y = int(r['enacted'][:4])
    lag[y].append((D(r['published']) - D(r['enacted'])).days)
    f = r['in_force_days'].split()
    if f:
        icl[y][inf_class(r['published'], f[0])] += 1
rows = []
for y in sorted(lag):
    v = sorted(lag[y])
    rows.append({'y': y, 'n': len(v), 'med': MED(v), 'q1': q(v, .25), 'q3': q(v, .75), **{k: icl[y][k] for k in ICL}})
OUT['c09'] = {'rows': rows}
print('c09', [(r['y'], r['n'], r['med']) for r in rows if r['n'] >= 5][:3], [(r['y'], r['n'], r['med']) for r in rows][-6:])

# ------------------------------------------------------------------ the provision files of each act over time, replayed from the history
OLDEST = list(reversed(C))
first_commit = {}
for c in OLDEST:
    for st, a, f in code_files(c):
        first_commit.setdefault(a, c['sha'])
FILES = collections.defaultdict(set)   # act -> provision files at REF
for c in OLDEST:
    for st, f in c['f']:
        a = f.split('/')[0]
        if (a in CODESET or a == 'code-penal-2024') and PROV(f):
            (FILES[a].discard if st == 'D' else FILES[a].add)(f)

# ------------------------------------------------------------------ c10: changes that took effect before the act that made them was published
# REPRODUCE.md lists them, act by act ("N changes took effect retroactively …: art-x in force D1, published D2 (laws)");
# the repository commits each on its day of publication
V = json.load(open(os.path.join(R, 'data', 'versions.json'), encoding='utf-8'))
TITLE2SLUG = {a['title']: a['slug'] for a in V['acts']}
TITLE2SLUG['Code pénal'] = 'code-penal'
retro = []
for line in open(os.path.join(R, 'REPRODUCE.md'), encoding='utf-8'):
    m = re.match(r'^- (.+?): (\d+) changes took effect retroactively', line)
    if not m:
        continue
    slug = TITLE2SLUG.get(m.group(1))
    if not slug or slug in NL_TEXTS:
        continue
    items = re.findall(r'(art-[\w-]+) in force (\d{4}-\d{2}-\d{2}), published (\d{4}-\d{2}-\d{2}) \(([^)]+)\)', line)
    assert len(items) == int(m.group(2)), (slug, len(items), m.group(2))
    for art, inf, pub, laws in items:
        # a day equal to the act's oldest text in the record may stand for an earlier one the record does not reach
        retro.append({'a': GROUP(slug), 'art': art[4:], 'inf': inf, 'pub': pub, 'laws': laws, 'days': (D(pub) - D(inf)).days,
                      'atstart': inf == (BY[first_commit[slug]]['In-force'] if slug in first_commit else '')})
OUT['c10'] = {'rows': retro}
print('c10', len(retro), collections.Counter(x['a'] for x in retro), 'median days', MED([x['days'] for x in retro]), 'max', max(retro, key=lambda x: x['days']))

# ------------------------------------------------------------------ c11: the acts changed most often: new versions a year
# the Code judiciaire's first texts of 1985 are incomplete (Justel's oldest archived pages lack many articles, which later
# pages add as 'unexplained' changes): its history counts from the first complete text
CUT = {'code-judiciaire': '1985-06-12'}
ver = collections.defaultdict(lambda: collections.defaultdict(set))   # act group -> year -> in-force days
start = {}
for c in OLDEST:
    if c['Kind'] in ('correction', ''):
        continue
    acts = {a for st, a, f in code_files(c)}
    for a in acts:
        g = GROUP(a)
        day = c['In-force'] or c['date']
        if c['sha'] == first_commit[a] or (a in CUT and day <= CUT[a]):
            start[g] = CUT.get(a) or min(start.get(g, day), day)
            continue
        ver[g][int(day[:4])].add(day)
rows = []
for g, v in ver.items():
    by = {y: len(d) for y, d in v.items()}
    rows.append({'k': g, 'start': start[g], 'n': sum(by.values()), 'by': by})
rows.sort(key=lambda r: -r['n'])
OUT['c11'] = {'rows': rows}
print('c11', [(r['k'], r['n'], r['start']) for r in rows][:8])

# ------------------------------------------------------------------ c12: the provisions changed most often
cnt = collections.Counter()
dec = collections.defaultdict(collections.Counter)
for c in C:
    if c['Kind'] not in CHANGE_KINDS:
        continue
    y = int((c['In-force'] or c['date'])[:4])
    for st, a, f in code_files(c):
        if st == 'M':
            cnt[f] += 1
            dec[f]['a' if y < 1995 else 'b' if y < 2005 else 'c' if y < 2015 else 'd'] += 1
top = cnt.most_common(20)
OUT['c12'] = {'rows': [{'f': f, 'n': n, **dec[f]} for f, n in top], 'n_files': len(cnt)}
print('c12', top[:5], 'last', top[-1])

# ------------------------------------------------------------------ c13: how acts grow: article numbers by the way they were numbered
def numbering(f):
    """'plain' (art. 37, art. 1er), 'latin' (art. 7bis), 'slash' (art. 112/1, art. 120octies/1) from the file name"""
    name = f.rsplit('/', 1)[1][4:-3]
    toks = name.split('-')
    if not toks[0].isdigit():
        return 'other'
    rest = [t for t in toks[1:] if t != 'er']
    if any(t.isdigit() for t in rest):
        return 'slash'
    if rest:
        return 'latin'
    return 'plain'


GROW = ['loi-etrangers', 'code-penal', 'loi-contrats-travail', 'loi-accidents-travail', 'loi-bien-etre-travailleurs', 'loi-sur-le-travail',
        'titre-preliminaire-code-procedure-penale', 'code-judiciaire']
series = {}
for a in GROW:
    cur, pts_ = set(), []
    for c in OLDEST:
        if c['Kind'] == 'correction':   # corrections restate earlier days' text at the tip and are undone by the last one
            continue
        fs = [(st, f) for st, a2, f in code_files(c) if a2 == a]
        if not fs:
            continue
        for st, f in fs:
            (cur.discard if st == 'D' else cur.add)(f)
        k = collections.Counter(numbering(f) for f in cur)
        day = c['In-force'] or c['date']
        if pts_ and day < pts_[-1][0]:
            continue
        p_ = [day, k['plain'] + k['other'], k['latin'], k['slash']]
        if pts_ and pts_[-1][0] == p_[0]:
            pts_[-1] = p_
        elif not pts_ or pts_[-1][1:] != p_[1:]:
            pts_.append(p_)
    series[a] = pts_
OUT['c13'] = {'series': series}
print('c13', {a: (s[0], s[-1], sum(s[-1][1:]), len(FILES[a])) for a, s in series.items()})

# ------------------------------------------------------------------ c14: the day of the year a change takes effect
ev = {}
for c in C:
    if c['Kind'] not in CHANGE_KINDS:
        continue
    acts = {GROUP(a) for st, a, f in code_files(c)}
    if not acts:
        continue
    day = c['In-force'] or c['date']
    key = (c['Law'], day)
    ev.setdefault(key, set()).update(acts)
cal = collections.Counter(d[5:] for (L, d) in ev)
cj = collections.Counter(d[5:] for (L, d), acts in ev.items() if 'code-judiciaire' in acts)
OUT['c14'] = {'cal': dict(cal), 'cj': dict(cj), 'n': len(ev), 'years': [min(d for L, d in ev)[:4], max(d for L, d in ev)[:4]]}
print('c14', len(ev), cal.most_common(5), 'cj on 09-01', cj['09-01'], 'first of month', sum(v for k, v in cal.items() if k.endswith('-01')))

# ------------------------------------------------------------------ c15: four new codes, book by book: from the law to entry into force
LAWBY = {r['label']: r for r in LAWS}
books = []
cde_first, bw_first = {}, {}
for c in OLDEST:
    if c['Kind'] != 'law':
        continue
    for st, a, f in code_files(c):
        if st != 'A':
            continue
        if a == 'code-droit-economique':
            m = re.match(r'art-([ivxl]+)-', f.split('/')[1])
            if m and m.group(1).upper() not in cde_first:
                cde_first[m.group(1).upper()] = (c['In-force'], c['Law'])
for b, (inf, L) in cde_first.items():
    r = LAWBY.get(L, {})
    n = sum(1 for f in FILES['code-droit-economique'] if re.match(r'art-' + b.lower() + r'-', f.split('/')[1]))
    books.append({'code': 'cde', 'b': b, 'law': L, 'enacted': r.get('enacted'), 'pub': r.get('published') or None, 'inf': inf, 'n': n})
for r in LAWS:
    m = re.match(r'^Loi du .*\(C\. civ\., (livre .+)\)$', r['label'])
    if m:
        bk = m.group(1)
        keys = re.findall(r'livre (\d+)(?:, titre (\d+))?', bk)
        n = 0
        for lb, ti in keys:
            pre = f'art-{lb}-{ti}-' if ti else f'art-{lb}-'
            n += sum(1 for f in FILES['code-civil'] if f.split('/')[1].startswith(pre) and (ti or not re.match(r'art-\d+-\d+-\d', f.split('/')[1]) or lb != '2'))
        books.append({'code': 'bw', 'b': bk, 'law': r['label'], 'title': r['title'], 'enacted': r['enacted'], 'pub': r['published'] or None,
                      'inf': r['in_force_days'].split()[0], 'n': n})
csa = next(c for c in OLDEST if c['Kind'] == 'law' and any(a == 'code-societes-associations' for st, a, f in code_files(c)))
r = LAWBY.get(csa['Law'], {})
books.append({'code': 'csa', 'b': '', 'law': csa['Law'], 'enacted': r.get('enacted'), 'pub': r.get('published') or None, 'inf': csa['In-force'],
              'n': len(FILES['code-societes-associations'])})
cp24 = next(c for c in OLDEST if any(f.startswith('code-penal-2024/') for st, f in c['f']))
m = re.search(r'/eli/loi/(\d{4})/(\d{2})/(\d{2})/', cp24['Source'])
books.append({'code': 'cp24', 'b': '', 'law': 'Code pénal 2024', 'enacted': f'{m.group(1)}-{m.group(2)}-{m.group(3)}' if m else None, 'pub': None,
              'inf': cp24['In-force'], 'n': len(FILES['code-penal-2024'])})
OUT['c15'] = {'books': books}
print('c15', [(b['code'], b['b'], b['enacted'], b['pub'], b['inf'], b['n']) for b in books])

# ------------------------------------------------------------------ c16: the new Code pénal: the level of penalty each offence carries
LV = []
for o in jl('penal2024.jsonl'):
    m = re.match(r'code-penal-2024/art-(\d+)', o['p'])
    if not m:
        continue
    n = int(m.group(1))
    t = o['t']
    lv = [int(x) for x in re.findall(r'punie?s?\s+d.une\s+peine\s+de\s+niveau\s+([1-8])', t)]
    LV.append({'a': n, 'cap': clean(t.split('\n', 1)[0])[:120], 'lv': lv})
LV.sort(key=lambda x: x['a'])
definition = next(x for x in LV if x['a'] == 36)
offences = [x for x in LV if x['lv'] and x['a'] >= 79]   # book II (offences) starts at art. 79; book I sets the rules
OUT['c16'] = {'arts': [[x['a'], x['cap'], max(x['lv']), min(x['lv'])] for x in offences], 'n_arts': len(LV),
              'mentions': dict(collections.Counter(l for x in offences for l in x['lv']))}
print('c16', len(LV), 'offence articles', len(offences), collections.Counter(max(x['lv']) for x in offences), 'first offence art', offences[0]['a'])

# ------------------------------------------------------------------ c17: the Constitution: the provisions each revision changed, by part
# the parts follow the Constitution's titles and chapters, by article number
CPARTS = [('t1', 1, 7.9), ('t2', 8, 32.9), ('t3', 33, 41.9), ('ch', 42, 73.9), ('leg', 74, 84.9), ('king', 85, 114.9), ('cr', 115, 140.9),
          ('cc', 141, 143.9), ('jud', 144, 159.9), ('ce', 160, 161.9), ('loc', 162, 166.9), ('int', 167, 169.9), ('fin', 170, 181.9),
          ('arm', 182, 186.9), ('gen', 187, 198.9)]


def cpart(f):
    name = f.split('/')[1][:-3]
    if name.startswith('disp-trans'):
        return 'trans'
    m = re.match(r'art-(\d+)(?:-(\w+))?', name)
    n = int(m.group(1)) + (0.5 if m.group(2) else 0)
    return next(k for k, a_, z in CPARTS if a_ <= n <= z)


revs = []
for c in OLDEST:
    if c['Kind'] != 'law' or c['sha'] == first_commit['constitution']:
        continue
    fs = [f for st, a, f in code_files(c) if a == 'constitution']
    if fs:
        revs.append({'law': c['Law'], 'inf': c['In-force'], 'parts': dict(collections.Counter(cpart(f) for f in fs)), 'arts': [f.split('/')[1][4:-3] for f in fs]})
other_c = [c for c in OLDEST if c['Kind'] not in ('law', '') and c['sha'] != first_commit['constitution'] and any(a == 'constitution' for st, a, f in code_files(c))]
OUT['c17'] = {'revs': revs, 'acts': len({r['law'] for r in revs}), 'unexplained': len(other_c), 'first': BY[first_commit['constitution']]['In-force']}
print('c17', len(revs), 'commits,', OUT['c17']['acts'], 'revision acts;', sum(sum(r['parts'].values()) for r in revs), 'provision changes; 2014:',
      sum(1 for r in revs if r['inf'].startswith('2014')), 'other kinds', len(other_c))

# ------------------------------------------------------------------ c18: the Constitutional Court in the codes
rul = collections.OrderedDict()
for c in OLDEST:
    if c['Kind'] != 'court':
        continue
    fs = [(a, f) for st, a, f in code_files(c)]
    if not fs:
        continue
    k = c['Law']
    r = rul.setdefault(k, {'k': k, 'ruling': c['Enacted'], 'pub': c['Published'] or None, 'inf': c['In-force'], 'arts': []})
    r['arts'] += [[GROUP(a), f.split('/')[1][4:-3]] for a, f in fs]
OUT['c18'] = {'rulings': list(rul.values())}
print('c18', len(rul), sum(len(r['arts']) for r in rul.values()), [(r['k'], r['ruling'], r['pub']) for r in rul.values()][:3])

# ------------------------------------------------------------------ c19 + c20: the courts' own records
CASS, CE, CETXT = [], [], {}
for o in jl('caselaw.jsonl'):
    p_ = o['p']
    if p_.startswith('caselaw/cour-cassation/') and 'r' in o:
        CASS.append(o['r'])
    elif p_.startswith('caselaw/conseil-etat/') and 'r' in o and p_.endswith('source.json'):
        CE.append(o['r'])
    elif p_.startswith('caselaw/conseil-etat/') and 't' in o:
        CETXT[p_.split('/')[-2]] = o['t']
cass = []
for r in CASS:
    if not r.get('role_number') or not r.get('published_on_juportal'):
        continue
    typ = r['ecli'].split(':')[4].split('.')[0]
    cass.append({'d': r['decision_date'], 'pub': r['published_on_juportal'], 'm': r['role_number'][0], 'lang': r.get('language'),
                 'typ': {'ARR': 'arr', 'CONC': 'conc'}.get(typ, 'other'), 'role': r['role_number'], 'days': (D(r['published_on_juportal']) - D(r['decision_date'])).days})
OUT['c19'] = {'rows': cass, 'n_all': len(CASS), 'pdf_only': sum(1 for r in CASS if not r.get('role_number'))}
print('c19', len(cass), collections.Counter((x['m'], x['typ']) for x in cass), collections.Counter(x['lang'] for x in cass))


def lang_of(t):
    """the language of a decision text, by its most common function words"""
    tl = t.lower()
    nl = len(re.findall(r'\b(?:het|van|de|een|en|verzoeker|verzoekende|arrest|tegen)\b', tl))
    fr = len(re.findall(r'\b(?:le|la|les|des|du|requérante?|arrêt|contre)\b', tl))
    return 'nl' if nl > fr else 'fr'


ce = []
for r in CE:
    ce.append({'n': int(r['number']), 'd': r['decision_date'], 'ch': r.get('chamber') or '', 'pg': r.get('pages'),
               'lang': lang_of(CETXT[str(r['number'])]) if str(r['number']) in CETXT else None})
chl = collections.defaultdict(collections.Counter)
for x in ce:
    if x['lang']:
        chl[x['ch']][x['lang']] += 1
OUT['c20'] = {'rows': sorted([[x['d'], x['n'], x['ch'], x['pg']] for x in ce]), 'chamber_lang': {k: dict(v) for k, v in chl.items()}, 'texts': len(CETXT)}
print('c20', len(ce), {k: dict(v) for k, v in chl.items()})
# the Council of State numbers its judgments in one series: the numbers held show how many it gave each month.
# A record whose number runs against the order of the dates (no. 60.959, dated 11 June 1996) is left out of the estimate.
seq = sorted(ce, key=lambda x: (x['d'], x['n']))
later_min, keep = 10 ** 9, []
for x in reversed(seq):
    if x['n'] <= later_min:
        keep.append(x)
        later_min = min(later_min, x['n'])
keep.reverse()
dropped = [[x['d'], x['n']] for x in seq if x not in keep]


def number_on(day):
    """the judgment number reached at the start of a day, interpolated between the judgments held before and after it"""
    before = [x for x in keep if x['d'] < day]
    after = [x for x in keep if x['d'] >= day]
    if not before or not after:
        return None
    b, a_ = before[-1], after[0]
    nb = max(x['n'] for x in keep if x['d'] == b['d'])
    na = min(x['n'] for x in keep if x['d'] == a_['d'])
    span = (D(a_['d']) - D(b['d'])).days
    return nb + (na - nb) * (D(day) - D(b['d'])).days / span


months = []
d0 = date(1994, 10, 1)
while d0 < date(1996, 7, 1):
    d1 = date(d0.year + (d0.month == 12), d0.month % 12 + 1, 1)
    s, e = number_on(d0.isoformat()), number_on(d1.isoformat())
    last = d1 > D(keep[-1]['d'])
    if last:
        e = keep[-1]['n']
    held = sum(1 for x in ce if x['d'][:7] == d0.isoformat()[:7])
    months.append({'m': d0.isoformat()[:7], 'est': round(e - s) if s is not None and e is not None else None, 'held': held, 'partial': last})
    d0 = d1
lang_ch = {k: max(v, key=v.get) for k, v in chl.items()}
OUT['c20'].update({'months': months, 'dropped': dropped, 'lang_ch': lang_ch, 'first': [seq[0]['d'], seq[0]['n']], 'last': [keep[-1]['d'], keep[-1]['n']],
                   'by_ch': dict(collections.Counter(x['ch'] for x in ce)), 'pages_med': MED([x['pg'] for x in ce if x['pg']]),
                   'pages': dict(collections.Counter(min(x['pg'], 21) for x in ce if x['pg'])), 'old_format': sum(1 for o in jl('caselaw.jsonl') if o['p'].endswith(('/nl.json', '/fr.json')))})
print('c20 months', [(m['m'], m['est'], m['held']) for m in months], 'dropped', dropped, lang_ch)

# ------------------------------------------------------------------ profile
versions = collections.Counter()
for c in OLDEST:
    if c['Kind'] in ('correction', ''):
        continue
    for a in {f.split('/')[0] for st, f in c['f'] if PROV(f) and (f.split('/')[0] in CODESET or f.split('/')[0] in NL_TEXTS)}:
        versions[(a, c['In-force'] or c['date'])] += 1
PROFILE.update({
    'commits': len(C), 'head': os.environ.get('HEAD_SHA', ''), 'built': date.today().isoformat(),
    'versions': len(versions), 'acts29': len({a for a, d in versions}), 'laws_csv': len(LAWS), 'laws_csv_laws': sum(1 for r in LAWS if is_law(r)),
    'acts2025': len(A25), 'laws2026': len(L26), 'cass': len(CASS), 'cass_meta': len(cass), 'ce': len(CE),
    'cc_rulings': len(rul), 'penal2024': len(FILES['code-penal-2024']), 'nl_texts': len(NL_TEXTS),
    'other_courts': sum(1 for c in C if c['Kind'] in ('caselaw', 'court') and c['author'] not in ("Conseil d'État", 'Cour de cassation') and not c['author'].startswith(('C. const', 'Arrest', 'Arrêt'))),
    'drafts': sum(1 for c in C if c['Kind'] == 'draft'),
    'caselaw': sum(1 for o in jl('caselaw.jsonl') if o['p'].endswith('/source.json')),   # five judgments of 1994 also have an older record (nl.json, fr.json)
    'caselaw_by': dict(collections.Counter(o['p'].split('/')[1] for o in jl('caselaw.jsonl') if o['p'].endswith('source.json'))),
    'last_in_force': max((c['In-force'] for c in C if c['In-force'] and c['In-force'] <= date.today().isoformat()), default=''),
    'first_in_force': min((c['In-force'] for c in C if c['In-force']), default=''),
})
json.dump({'charts': OUT, 'profile': PROFILE}, open(os.path.join(B, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'), default=list)
print('profile', PROFILE)
print('data.json', os.path.getsize(os.path.join(B, 'data.json')))
