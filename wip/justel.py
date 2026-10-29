"""Turn an archived Justel consolidated-text page (HTML, ISO-8859-1) into the Markdown layout legalize-be uses,
so lmd.units() reads both sources the same way.

Justel's page body: `<A NAME='Art.59' ...>Art.</A> <A ...> 59</A>.text<BR>&nbsp;&nbsp;next paragraph`,
headings as `<A NAME='LNK0004' ...>TITRE II.</A> - title`, change markers `[<sup>..1..</sup> words]<sup>..1..</sup>`
and footnotes `(<font color=red>1</font>)&lt;L ...&gt;`.
"""
from __future__ import annotations

import html as htmlmod
import re

SUPD = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')


def to_md(raw: bytes) -> str:
    t = raw.decode('latin-1')
    a = [i for i in (t.find("<A NAME='LNK"), t.find("<A NAME='Art.")) if i >= 0]
    if not a:
        return ''
    t = t[min(a):]
    for end in ('<div id="list-title-sw_t"', '<div id="list-title-sw_', '</div>'):
        j = t.find(end)
        if j > 0:
            t = t[:j]
            break
    t = re.sub(r'<sup>(?:(?!</sup>).)*?(\d+)(?:(?!</sup>).)*?</sup>', lambda m: m.group(1).translate(SUPD), t,
               flags=re.S | re.I)
    t = re.sub(r'\(<font[^>]*>(\d+)</font>\)', r'(\1)', t, flags=re.I)
    t = re.sub(r"<A NAME='Art\.([^']+)'[^>]*>\s*Art\.?\s*</A>\s*(?:<A [^>]*>)?\s*[^<]*?(?:</A>)?\s*\.",
               lambda m: f'\n\n##### Article {m.group(1)}. ', t, flags=re.I)
    t = re.sub(r"<A NAME='LNK\d+'[^>]*>([^<]*)</A>", lambda m: f'\n\n### {m.group(1)}', t, flags=re.I)
    t = re.sub(r'<BR\s*/?>', '\n\n', t, flags=re.I)
    t = re.sub(r'<[^<>]+>', '', t)
    t = htmlmod.unescape(t).replace(' ', ' ')
    lines = [ln.strip() for ln in t.split('\n')]
    return '\n'.join(lines)
