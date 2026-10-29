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
    t = re.sub(r'\s+', ' ', raw.decode('latin-1'))   # older pages break lines inside tags
    t = re.sub(r'<a\s+name\s*=\s*', "<A NAME=", t, flags=re.I)
    a = [i for i in (t.find("<A NAME='LNK"), t.find("<A NAME='Art.")) if i >= 0]
    if not a:
        return ''
    t = t[min(a):]
    # the text ends where the page's next box (new layout) or the table cell (old layout) ends
    ends = [j for j in (t.find('<div id="list-title-sw_'), t.find('</div>'), t.lower().find('</th>'),
                        t.lower().find('<a name="modification"')) if j > 0]
    if ends:
        t = t[:min(ends)]
    t = re.sub(r'<sup>(?:(?!</sup>).)*?<span[^>]*>\s*(\d+)\s*</span>(?:(?!</sup>).)*?</sup>',
               lambda m: m.group(1).translate(SUPD), t, flags=re.S | re.I)
    t = re.sub(r'<sup>\s*(?:<[^>]*>\s*)*(\d+)\s*(?:<[^>]*>\s*)*</sup>', lambda m: m.group(1).translate(SUPD), t,
               flags=re.S | re.I)
    t = re.sub(r'\(<font[^>]*>(\d+)</font>\)', r'(\1)', t, flags=re.I)
    t = re.sub(r"<A NAME='Art\.([^']+)'[^>]*>(?:\s*Art(?:icle)?\.?\s*)?</A>\s*(?:Art(?:icle)?\.?\s*)?"
               r"(?:<A [^>]*>)?\s*[^<]*?(?:</A>)?\s*\.",
               lambda m: f'\n\n##### Article {m.group(1)}. ', t, flags=re.I)
    t = re.sub(r"<A NAME='LNK\d+'[^>]*>([^<]*)</A>", lambda m: f'\n\n### {m.group(1)}', t, flags=re.I)
    t = re.sub(r'<BR\s*/?>', '\n\n', t, flags=re.I)
    t = re.sub(r'<[^<>]+>', '', t)
    t = htmlmod.unescape(t).replace(' ', ' ')
    lines = [ln.strip() for ln in t.split('\n')]
    return '\n'.join(lines)
