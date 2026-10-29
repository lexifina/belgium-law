# Belgium: law history in git

The law of Belgium as a git history: one file per article, one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to an article; checking out a date gives the text in force that day. The text is French (Dutch and German are equally official and are not built yet).

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `be/`.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | La Constitution coordonnée (17 février 1994) | 37 | From the coordinated text (in force 27 February 1994) through every revision to L 2026-07-15/04 (24 July 2026) |
| `code-penal/` | Code pénal (8 juin 1867) | 178 | From 5 April 1990 (the oldest text Justel keeps, not the 1867 text) to Justel's update of 18 February 2026, read on 3 May 2026 |
| `ancien-code-civil/` | Code civil (21 mars 1804), the "ancien Code civil" | 115 | From 16 December 2009 (the oldest archived Justel page) to the newest archived page of each part (2021-2026) |
| `code-civil/` | Code civil (2019-): livres 1, 2 (titre 3), 3, 4, 5, 6, 8 and 9 (titre 1) | 9 | Each book from its entry into force (livre 8: 1 November 2020 ... livre 9, titre 1: 1 January 2026) |
| `titre-preliminaire-code-procedure-penale/` | Loi contenant le titre préliminaire du Code de procédure pénale (17 avril 1878) | 60 | From 31 December 1993 (the oldest text Justel keeps) to Justel's page of 9 May 2024 |
| `code-nationalite/` | Code de la nationalité belge (28 juin 1984) | 28 | From 6 July 1991 (the oldest text Justel keeps) to Justel's page of 3 July 2025 |
| `code-electoral/` | Code électoral (12 avril 1894) | 37 | From 10 January 2003 (the oldest text Justel keeps) to Justel's page of 5 May 2024 |
| `code-droit-international-prive/` | Loi portant le Code de droit international privé (16 juillet 2004) | 25 | From its entry into force (1 October 2004) to legalize-be's last version (Justel update of 29 March 2024) |
| `loi-protection-donnees/` | Loi relative à la protection des personnes physiques à l'égard des traitements de données à caractère personnel (30 juillet 2018) | 8 | From its entry into force (5 September 2018) to Justel's page of 7 May 2026 |

The per-act `README.md` in each folder lists every article, how often it changed and when.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did art. 151 of the Constitution say on 30 January 2014? | `python tools/en_vigueur_au.py 2014-01-30 constitution 151` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2014-01-30T23:59:59Z" main -- constitution/art-151.md):constitution/art-151.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2014-01-30T23:59:59Z" main -- constitution/art-151.md; git show "$($r):constitution/art-151.md"` |
| Which law wrote each paragraph of art. 41? | `git blame constitution/art-041.md` |
| Every change to art. 458 of the Code pénal, word by word | `git log -p --word-diff code-penal/art-458.md` |
| Every law in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one law changed | `git log --author="L 2014-01-06/42" main` |
| The whole Constitution on a date | `python tools/en_vigueur_au.py 2000-01-01 constitution` |

File names: `art-007-bis.md` is art. 7bis, `art-112-01.md` art. 112/1, `art-344-001.md` art. 344-1 of the old Code civil, `art-5-201.md` art. 5.201 of the new Code civil, `disp-trans-04.md` the transitional provision IV of the Constitution. After a rebuild, refresh tags with `git fetch --force --tags`.

## Dates

- Each commit is dated at **noon, Europe/Brussels, on the day the change took effect**, and that day is in the `In-force:` trailer, which the tools read.
- **Where the day comes from.** Justel, the consolidated legislation of the SPF Justice (Moniteur belge), notes every change in the text: `<L 1997-02-28/31, art. 1, 004; En vigueur : 01-03-1997>` names the amending act (its date and Justel serial number), the article that made the change, Justel's archived-version number and the in-force day. Every date here is such a note's in-force day. Justel's day applies the default rule (loi du 31 mai 1961, art. 4: a law binds from the tenth day after its publication in the Moniteur belge) or the act's own clause.
- **legalize-be's dates are not used.** legalize-be (below) dates each commit by publication of the amending act, often plus ten days, falling back on that when Justel's in-force day is "indéterminée"; here only Justel's notes date a change.
- Where a wording gained notes with two in-force days at once, it reads `[La source ne donne pas le texte en vigueur à cette date.]` between the two. Where Justel shows a change with no new dated note (mostly its own typo corrections), the change is a separate commit authored by Justel and labelled unexplained, dated by the Justel version or page that first shows it.
- Use `T23:59:59Z` with `--before`, or the tool: a bare date uses your clock's time of day.

## How the history was rebuilt

**Constitution, Code pénal and the other codes.** Justel keeps every archived version of an act ("versions archivées"). [legalize-be](https://github.com/legalize-dev/legalize-be) (pinned at `da37dfb18b17`) reconstructs those archived versions as Markdown, one commit per version. Its history is not usable as it stands, and was not used as it stands:

- its first file for each act mixes the oldest archived text (for articles changed later) with today's text (for the rest, including articles inserted later: 7bis, 22ter and 135bis of the Constitution appear in its "1994" file);
- its later files hold only the articles touched so far, and an article's new wording often appears several archived versions after the version that made it;
- its commit dates are publication dates (often plus ten days), not in-force days; some Code pénal articles are mislabelled or run together.

So each article's successive wordings are read in legalize-be's file order and each wording is dated by the Justel notes it gained. An article inserted later is left out until the in-force day of its "Inséré par" note. The newest text comes from an archived Justel page (Internet Archive) that is newer than legalize-be's last file: for the Constitution, the page of 24 August 2026, which adds the revisions of 12 June 2025 and 15 July 2026 that legalize-be lacks.

**Old and new Code civil.** legalize-be has no file for the 1804 Code civil, nor the consolidated books of the new one. A change made and replaced between two captures is not seen.

**Typesetting.** Justel's notes and change markers (`[¹ ... ]¹`, older bare brackets) are removed. Older Justel versions mark changed words with parentheses where newer ones use brackets, and Justel later tidied case, accents and final stops; where only that differs, the paragraph takes Justel's latest rendering, so such tidying is not shown as a change. Words annulled by the Constitutional Court (Justel prints them in italics with a note) are removed on the day the ruling was published in the Moniteur belge, credited to the ruling.

## How it is checked

- **Against Justel's own pages.** Every archived Justel page used (Constitution 2009-2026, Code pénal 2009-2026, every part of the old Code civil, every new book, and 9 to 26 pages for each of the other codes, including the newest) is compared, article by article, with this history on the page's own day, ignoring typesetting; the counts are among the decisions in `REPRODUCE.md`, and Lexifina's code writes the page-by-page result (`verification/*.json`) when run. The newest page of each act matches exactly. Remaining differences are Justel's own: text it showed before its in-force day, changes it recorded late (it added the 2002 euro conversion to the Code pénal only in 2010), and typos it later fixed.
- Every version of each act is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. No merge commits, no dates going backwards, nothing dated in the future, every trailer parses.
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the act that made the change, labelled with Justel's citation (`L 2014-01-06/42`: loi of 6 January 2014, Justel serial 42; `C. const. 148/2017` for a Constitutional Court ruling), with an e-mail address that cannot exist (`l-2014-01-06-42@ejustice.just.fgov.be.invalid`). The committer is always Lexifina. The Constitution's first commit is credited to the coordinated Constitution of 17 February 1994; the first commit of the other acts is "oldest version available", authored by Justel. Blame credits whole lines (one paragraph per line); use `git log -p --word-diff`.

## What it does not show

- **The Code pénal before 1990 and the old Code civil before 2009**: Justel's archive and the Internet Archive go no further back.
- **The new Code pénal.** The lois du 29 février 2024 (livres I and II) replace the 1867 Code. Justel's note on art. 38 of the livre I law records that L 2026-03-30/01 moved its entry into force to 1 September 2026; Justel's page of 3 May 2026 still shows the 1867 Code in force, and no source used here gives the clause for livre II. So the replacement is not committed, and the new Code is not built (legalize-be's files for the two laws mix the laws' own articles with the Code's, under the same numbers).
- **The newest changes to some old Code civil parts**: each part ends at its newest archived page (livre II: June 2021; livre III titres I-II: June 2022; titres VI-XIII: July 2023; the others 2024-2026). Livres II and III titres I-II were themselves replaced by the new livres 3 and 4.
- **The rest of the Code d'instruction criminelle.** Justel splits it into eight texts; only the first, the titre préliminaire du Code de procédure pénale, is built here.
- **The newest changes to the Code de droit international privé**: no Justel page newer than legalize-be's last version (Justel update of 29 March 2024) was available, so its history ends there.
- **Publication dates** of most amending acts: Justel's notes do not give them, so `Published:` is empty for them. Their titles are not given either, except "Révision de la Constitution" for the Constitution's revisions.
- **Headings** (titles, chapters, sections) and Justel's correspondence tables: only articles are files.
- **Dutch and German texts.**

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

No AI model wrote or changed legal text. Claude Opus 5.5 wrote the scripts and chose the sources; see `REPRODUCE.md`.

## Sources

| Source | Kind | Past versions | Names the amending act | Used for |
| --- | --- | --- | --- | --- |
| [Justel](https://www.ejustice.just.fgov.be/cgi_loi/welcome.pl?language=fr) (SPF Justice, Moniteur belge) | Official consolidated legislation | "versions archivées" per act | yes, a dated note per change | The source of every word and date, through the two copies below |
| [legalize-be](https://github.com/legalize-dev/legalize-be) (Legalize), commit `da37dfb18b17b06f8f8dc74c0d724cca22292bee` | Justel's archived versions as Markdown, one file per act (`be/<NUMAC>.md`), each naming its Justel source in its front matter | one commit per archived version | Justel's notes, kept in the text | Constitution (NUMAC 1994021048), Code pénal (1867060850), titre préliminaire du Code de procédure pénale (1878041750), Code de la nationalité (1984900065), Code électoral (1894041255), Code de droit international privé (2004009511), loi du 30 juillet 2018 (2018040581); in-force days and titles of the new Code civil's laws |
| – | Archived official pages | one per capture | yes | Newest texts, the old and new Code civil, and the checks |

## Licence

The legal texts are official acts of the Kingdom of Belgium, which are not protected by copyright (Code de droit économique, art. XI.172, § 2). They come from Justel (SPF Justice, Moniteur belge), through legalize-be, whose data licence is "Licence ouverte / open data fédéral belge (CC0 par défaut)" and whose pipeline is MIT (github.com/legalize-dev/legalize-pipeline), and through the Internet Archive. The arrangement, tables, commit messages and tools are by Lexifina, under the terms in `LICENSE`.

This repository is not legal advice and not an official publication.

## Français

L'histoire du droit belge dans git : un fichier par article et un commit par loi, daté du jour de son entrée en vigueur, avec la loi qui a fait la modification comme auteur (`git blame` nomme la loi de chaque alinéa). Il contient la Constitution coordonnée depuis le 27 février 1994, le Code pénal de 1867 depuis le 5 avril 1990, l'ancien Code civil depuis le 16 décembre 2009, les livres du nouveau Code civil depuis leur entrée en vigueur, le titre préliminaire du Code de procédure pénale depuis le 31 décembre 1993, le Code de la nationalité belge depuis le 6 juillet 1991, le Code électoral depuis le 10 janvier 2003, le Code de droit international privé et la loi du 30 juillet 2018 relative à la protection des données depuis leur entrée en vigueur.

- Le texte en vigueur à une date : `python tools/en_vigueur_au.py 2014-01-30 constitution 151`
- Les dates : chaque date est celle que Justel donne dans sa note sur la modification (« En vigueur : … »), qui applique la loi du 31 mai 1961, art. 4 (dixième jour après la publication au Moniteur belge), ou la disposition propre de la loi. Les dates de legalize-be (publication, souvent plus dix jours) ne sont pas utilisées.
- La reconstruction : le texte vient de legalize-be, qui reproduit les versions archivées de Justel, et des pages de Justel archivées par l'Internet Archive. Chaque formulation d'un article est datée par les notes de Justel qu'elle a gagnées. La dernière version de chaque acte correspond, article par article, à la page Justel archivée la plus récente.
- Ce qui manque : le Code pénal avant 1990 et l'ancien Code civil avant 2009 ; le nouveau Code pénal (lois du 29 février 2024), dont l'entrée en vigueur du livre I a été reportée au 1er septembre 2026 par la loi du 30 mars 2026 ; les textes néerlandais et allemand.
- Sources : Justel (SPF Justice, Moniteur belge), legalize-be (données CC0 par défaut, pipeline MIT) et l'Internet Archive. Aucun modèle d'intelligence artificielle n'a écrit de texte juridique.
