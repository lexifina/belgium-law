# Belgian law in 20 charts

[Nederlands](README.md) · [Français](README.fr.md)

Charts on the law of every country, drawn from all of global-law: [global-law visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations). Only the charts on Belgium are here.

Twenty charts on Belgian law, drawn only from the data in this repository: the Constitution and 23 codes and laws with every version from Justel and the acts that changed them, 753 acts of 2025 from Belgium's eight lawmakers, the federal laws of 2026, the new Criminal Code, and decisions of the Court of Cassation, the Council of State and the Constitutional Court. Codes and laws go by English names here; the charts are drawn from their French texts, the only ones the repository has of all of them.

Open [`belgisch-recht-in-20-grafieken.html`](belgisch-recht-in-20-grafieken.html) in a browser. The page is one file with all its data inside; it loads only the d3 and topojson libraries, the world map of chart 5 and its fonts from the web. The buttons at the top right choose the language (Dutch, French or English) and the view (light or dark). Each chart names its source in the repository, the number of records and its limits, and has a table of every figure below it. Hover over a mark for the exact values.

The charts are descriptive: they show what the sources record, not why.

## The charts

### I. Eight lawmakers, one Moniteur

#### 1. Eight lawmakers, one Moniteur

The 753 acts of 2025 in this repository by authority and by kind of act: 38% federal, 24% from the Walloon Region; 19% are laws, decrees or ordinances.

![Eight lawmakers, one Moniteur](stills/en/01.png)

#### 2. From signature to the Moniteur

Days from signature to publication in the Moniteur belge, by authority: a median of 13 for federal acts, 64 for those of the German-speaking Community.

![From signature to the Moniteur](stills/en/02.png)

#### 3. Entry into force

When the acts of 2025 take effect, counted from publication: 61% of the Walloon acts on the tenth day, 41% of those of the French Community retroactively.

![Entry into force](stills/en/03.png)

#### 4. The Moniteur in pages

The continuous page numbering of the Moniteur: up to page 100,364 in 2025, and by 17 September 2026, 29% fewer pages than a year earlier.

![The Moniteur in pages](stills/en/04.png)

#### 5. Assent to treaties

Acts of assent to treaties, by treaty and partner country: a median of 6.9 years after signature; the Walloon Parliament assented to 20 air services agreements.

![Assent to treaties](stills/en/05.png)

#### 6. EU directives

Acts that say themselves that they transpose an EU directive: 45 acts and 36 directives, 6 of them by two or three authorities.

![EU directives](stills/en/06.png)

### II. The federal Parliament

#### 7. Chamber and Senate

The procedure (article 74, 77 or 78 of the Constitution) and the kind of the 117 federal laws from October 2025 to October 2026: 89% deal with a matter the Chamber handles without the Senate.

![Chamber and Senate](stills/en/07.png)

#### 8. The legislative calendar

Amending laws per month since 1995, with the months of the federal elections: 7 of the 8 elections were followed by 5 to 9 months without a single amending law.

![The legislative calendar](stills/en/08.png)

#### 9. From enactment to the Moniteur

Days from the date of a law to its publication, by year (a median of 55 in 1997, 8 in 2021), and the day it takes effect: 45% on the tenth day.

![From enactment to the Moniteur](stills/en/09.png)

#### 10. Retroactive effect

Changes to the codes that took effect before they were published, by year and code: 416, a median of 95 days earlier.

![Retroactive effect](stills/en/10.png)

### III. The codes

#### 11. The codes changed most often

New versions per year of each code and law: the Judicial Code 613 since 1985.

![The codes changed most often](stills/en/11.png)

#### 12. The articles changed most often

The 20 articles that most often received a new text: art. 569 of the Judicial Code 30 times.

![The articles changed most often](stills/en/12.png)

#### 13. Inserted articles

The article numbers of eight codes and laws over the years, plain, with bis or ter, or with a slash: the Aliens Act has 452, 310 of them with a slash.

![Inserted articles](stills/en/13.png)

#### 14. When changes take effect

The calendar day on which changes to the codes take effect: 218 on 1 January, 86 on 1 September.

![When changes take effect](stills/en/14.png)

#### 15. Four new codes

The books of the Code of Economic Law, the Companies and Associations Code, the new Civil Code and the new Criminal Code, from law to entry into force: 29 books and parts, 5,387 articles.

![Four new codes](stills/en/15.png)

#### 16. The new Criminal Code

The 481 offence provisions of the new Criminal Code by penalty level: 48% at level 2 or 3.

![The new Criminal Code](stills/en/16.png)

### IV. The Constitution and the courts

#### 17. The Constitution since 1994

The revisions of the Constitution since 1994, by part and by year: 82, 42 of them of 6 January 2014.

![The Constitution since 1994](stills/en/17.png)

#### 18. The Constitutional Court in the codes

The 18 rulings of the Constitutional Court that struck words from the codes, with the days to the Moniteur: a median of 26.

![The Constitutional Court in the codes](stills/en/18.png)

#### 19. The Court of Cassation on Juportal

Days from judgment to publication on Juportal: a median of 6 for criminal judgments, 25 for civil ones, 54 for opinions.

![The Court of Cassation on Juportal](stills/en/19.png)

#### 20. The Council of State in 1994–1996

Judgments of the Council of State per month by their numbering, and the chambers by language: an average of 522 a month, 131 in August 1995.

![The Council of State in 1994–1996](stills/en/20.png)

## Data

At commit `74e1bf145f`, built on 16 November 2026.

| Data | Where in the repository | Records | Coverage |
| --- | --- | ---: | --- |
| Git history | branch `main` | 4,742 commits | each version on the day it took effect (`In-force:`) |
| Constitution, codes and laws | `constitution/`, `code-judiciaire/`, `code-penal/` … (24 French and 5 Dutch texts) | 2,097 versions | 1981–2026, from the oldest text in Justel's archive |
| Amending acts | `data/laws.csv` | 1,327 acts (1,226 laws) | 1982–2026 |
| Retroactive changes | `REPRODUCE.md` | 416 | published 1987–2026 |
| Acts of 2025 | `arrete/`, `decret/`, `loi/`, `ordonnance/`, `reglement/`, `norm/`, `convention/`, `circulaire/`, `accord/` | 753 acts | signed in 2025, 62% in October–December |
| Federal laws of 2026 | `loi-2026…/` | 82 laws | January–October 2026 |
| New Criminal Code | `code-penal-2024/` | 699 articles | in force since 1 September 2026 |
| Court of Cassation | `caselaw/cour-cassation/` | 366 decisions (280 with Juportal's data) | mostly 2021–2026 |
| Council of State | `caselaw/conseil-etat/` | 1,164 judgments (252 with text) | July 1994 – June 1996 |

## Limits

- **The acts of 2025 are a selection.** The repository holds the acts from the first pages of Justel's lists, most of them signed in October–December 2025; the shares in charts 1 to 6 are those of this selection, not of a full year.
- **The codes start in Justel's archive.** Most codes and laws start at the oldest text Justel keeps (the Judicial Code in 1985, the Criminal Code in 1990, the old Civil Code and the Code of Criminal Procedure in 2009), not as they were adopted; early years therefore count fewer codes (charts 8 to 14).
- **Categories come from titles and texts.** The kind of act (charts 1 and 7), assent to treaties (5), the transposition of directives (6), the procedure of the federal laws (7) and the penalty levels (16) are read from titles and texts, by the rules in `src/prep.py`.
- **Retroactive effect** is recorded in the repository on the day of publication (chart 10); charts 9 and 14 count that day.
- **One fact comes from outside the repository:** the months of the federal elections in chart 8, for orientation.
- **The case law is a selection** (charts 19 and 20): mostly metadata and the official link, with the text for some of the decisions.
- **Incomplete periods** (2025 and 2026 in the codes, June 1996 at the Council of State) are drawn lighter.

## Rebuild

```sh
python visualisations/src/make.py            # git history + tables + texts -> src/.build/ -> belgisch-recht-in-20-grafieken.html
node visualisations/src/stills.cjs           # images for these READMEs (needs Playwright; PLAYWRIGHT=<path> if it is not global)
```

`make.py` reads everything from git objects, so it also works in a blobless clone or a `--no-checkout` clone (it fetches the blobs it needs in one request per step). It reads `origin/main` (or `HEAD`) by default; `--ref` picks another branch or commit. It writes nothing into the repository except the page and the `src/.build/` folder (which git ignores).

| File | What it does |
| --- | --- |
| `src/make.py` | extracts the history, the tables and the texts into `src/.build/`, then runs `prep.py` and `build.py` |
| `src/prep.py` | computes every figure of the 20 charts and the data profile into `src/.build/data.json` |
| `src/page.tpl.html` | the page: the text in three languages, the charts (d3), the tables |
| `src/build.py` | puts `data.json` into the template and writes the page |
| `src/stills.cjs` | draws each chart as a png in `stills/nl/`, `stills/fr/` and `stills/en/` |
