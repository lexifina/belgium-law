# België: de geschiedenis van het recht in git

**Nederlands** · **[Or read it in English](README.en.md)**

<picture>
<source media="(prefers-color-scheme: dark)" srcset="data/nl/effort-dark.svg">
<img alt="De wetgeving van België in deze repository: wat erin staat, wijzigingen per jaar van inwerkingtreding, volledigheid ten opzichte van de officiële bronnen en juistheid van wat is opgenomen" src="data/nl/effort-light.svg" width="880">
</picture>

Het recht van België als git-geschiedenis: één bestand per artikel, één commit per versie op de dag van inwerkingtreding, en de akte die elke wijziging aanbracht als auteur van de commit. `git blame` noemt de akte achter elke alinea; `git log` toont elke wijziging van een artikel; een datum kiezen geeft de tekst die op die dag van kracht was.

Onderdeel van [lexifina/global-law](https://github.com/lexifina/global-law), één git-geschiedenis voor het recht van elk land: dit is het nationale recht van België, dat global-law leest in `belgium/national/acts/`.

**Wat er nu in staat:** de Grondwet en 29 wetboeken en wetten, met 2.103 versies uit Justel: daaronder de Code pénal, de nieuwe Code pénal van 2024 (alleen de huidige tekst), de oude en de nieuwe Code civil, de Code judiciaire, de Code d'instruction criminelle (als de acht teksten van Justel), de Code de droit économique, de Code des sociétés et des associations, vier arbeidswetten en de loi sur les étrangers. Vijf ervan staan ook in het Nederlands. De map van elke akte heeft een `README.md` met elk artikel en wanneer het werd gewijzigd; [`data/laws.csv`](data/laws.csv) noemt elke wijzigende akte.

Eén map per soort akte, in de taal van de tekst: `constitution/` en `grondwet/` (de Grondwet in het Frans en in het Nederlands), `code/` (de wetboeken in het Frans: `code/civil/`, `code/judiciaire/`, `code/penal/`, `code/instruction-criminelle/livre-1/` …) en `wetboek/` (in het Nederlands: `wetboek/strafwetboek/`, `wetboek/strafvordering/…`), `loi/`, `arrete/`, `decret/`, `ordonnance/`, `reglement/`, `circulaire/`, `convention/`, `accord/`, `revision/` (herzieningen van de Grondwet) en `autre/` (andere teksten), met `caselaw/` (rechtspraak), `local/` en `drafts/` (ontwerpen, geen recht). Een akte met haar versies is een map met één bestand per artikel (`loi/contrats-travail/art-037.md` is art. 37 van de Loi relative aux contrats de travail van 3 juli 1978; `art-007-bis.md` is art. 7bis, `art-112-01.md` art. 112/1); een wetboek van meer dan 1.000 artikelen is verdeeld in submappen per 500 artikelen (`code/judiciaire/art-0500-0999/`) of per boek (`code/droit-economique/livre-xi/`, `code/societes-associations/livre-07/`). De andere teksten uit Justel staan per soort, uitvaardiger en jaar onder hun NUMAC (`loi/justice/2026/2026000329/`). [`data/paths.json`](data/paths.json) geeft de map van elke akte en waar de mappen vóór 15 november 2026 stonden.

De tekst is Frans, zoals Justel hem afdrukt; de Grondwet (`grondwet/`), de Code pénal (`wetboek/strafwetboek/`) en drie teksten van de Code d'instruction criminelle (`wetboek/strafvordering/`) staan ook in het Nederlands. De Duitse tekst, die evenzeer officieel is, staat er niet in, en een Engelse vertaling maakt geen deel uit van dit archief.

## Vragen als git-commando's

| Vraag | Commando |
| --- | --- |
| Elke wijziging van art. 37 van de Loi relative aux contrats de travail | `git log --follow -p --word-diff -- loi/contrats-travail/art-037.md` |
| Welke akte schreef elke alinea van art. 37? | `git blame loi/contrats-travail/art-037.md` |
| Elke versie van de Loi relative aux contrats de travail, met de dag van inwerkingtreding | `git log --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- loi/contrats-travail loi-contrats-travail` |
| Art. 37 zoals van kracht op 1 januari 2000 | `python tools/en_vigueur_au.py 2000-01-01 loi/contrats-travail 37` |

De mappen staan sinds 15 november 2026 op hun huidige plaats; `--follow`, het oude pad naast het nieuwe en `tools/on.py` lezen een akte ook van vóór die dag.

**Buiten git** stellen we dit archief ook openbaar en gratis beschikbaar:

- **[Vraag Claude naar het Belgische recht](https://global-law.lexifina.com/v1/try_claude?country=belgium)**: opent Claude met een eerste vraag klaar.
- **[Vraag het ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=belgium)**: dezelfde vraag in ChatGPT.
- **[Zoek in het Belgische recht op onze site](https://lexifina.com/law?country=belgium&q=vacances+annuelles)**: een zoekopdracht naar "vacances annuelles" (jaarlijkse vakantie), met de tekst van elke bepaling en de versies ervan, zonder account.
- **[REST-API voor ontwikkelaars](https://global-law.lexifina.com/v1/search_law?query=vacances+annuelles&jurisdiction=belgium)**: dezelfde zoekopdracht als JSON, zonder sleutel. De documentatie staat [hier](https://lexifina.com/api/global-law).

Beide assistenten lezen het archief via de gratis connector Global law (MCP, `https://global-law.lexifina.com/mcp`); de eerste keer geeft de chat je de link om hem toe te voegen. Vraag in het Frans, in het Nederlands of in het Engels.

**Draai het eenvoudig zelf.** Je hebt alleen git en Python nodig, en de tools draaien op je eigen computer:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add belgium/national/acts
python3 tools/law.py show 2026-01-01 belgium/national/acts/loi-contrats-travail/art-037.md
```

Geopend in Claude Code, Cursor, VS Code of Codex start de kloon ook een lokale MCP-server met dezelfde tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Datums

Elke commit is gedateerd om 12 uur 's middags, Europe/Brussels, op de dag dat de wijziging in werking trad, en draagt die dag in zijn trailer `In-force:`:

- de dag is die welke Justel vermeldt in zijn nota bij de wijziging (`<L 1997-02-28/31, art. 1, 004; En vigueur : 01-03-1997>`), volgens de eigen bepaling van de akte of de standaardregel (wet van 31 mei 1961, art. 4: de tiende dag na de bekendmaking in het Belgisch Staatsblad);
- in de Code pénal, de Code judiciaire, de Code d'instruction criminelle, de Code de droit économique, de Code des sociétés et des associations, de arbeidswetten en de loi sur les étrangers wordt een wijziging die Justel dateert vóór haar bekendmaking gecommit op de dag van bekendmaking; `REPRODUCE.md` noemt elk geval met beide dagen;
- een formulering die Justel noteert als "En vigueur : indéterminée", of vooraf afdrukt als "Droit futur", wordt niet gelezen als geldende tekst; de ene wijziging die later ingaat (1 mei 2027) staat op de branch `futur`.

Elke wijziging wordt toegeschreven aan de akte die haar aanbracht, met de citatie van Justel (`L 2014-01-06/42`, `AR 1991-05-21/31`, `C. const. 148/2017` voor een arrest van het Grondwettelijk Hof). De eerste commit van de Grondwet (de gecoördineerde tekst van 17 februari 1994), de nieuwe Code civil, de Code de droit économique en de Code des sociétés et des associations is de akte zoals aangenomen; de eerste commit van elke andere akte is de "oldest version available", toegeschreven aan Justel, net als de wijzigingen die Justel zonder gedateerde nota toont (meestal zijn eigen correcties).

## Hoe het wordt gecontroleerd

- Elke gebruikte gearchiveerde pagina van Justel wordt artikel per artikel vergeleken met deze geschiedenis op de dag van die pagina, zonder rekening te houden met de opmaak; de nieuwste pagina van elke akte komt overeen, op de tijdsverschillen na die `REPRODUCE.md` noemt.
- `tools/check_repo.py` leest elke versie uit git terug op de dag van inwerkingtreding en op de dag ervoor, en beide moeten overeenkomen met het corpus: 2.095 versies, geen enkele afwijking.
- Een tweede build uit hetzelfde corpus gaf identieke hashes.
- De geschiedenis wordt alleen aangevuld: geen merge-commits, geen datums die teruglopen, niets gedateerd in de toekomst, en de trailers van elke commit zijn leesbaar.
- [vulnerabilities/](vulnerabilities/): mogelijke redactionele fouten in het Belgische recht, gevonden door de detectoren van global-law en met de hand gecontroleerd.

## Wat het niet toont

- **Teksten van vóór het archief van Justel.** De meeste akten beginnen bij de oudste tekst die Justel bewaart of de oudste gearchiveerde pagina van Justel (de Code pénal in 1990, de Code judiciaire in 1985, de oude Code civil en de Code d'instruction criminelle in 2009), niet zoals ze werden aangenomen.
- **De nieuwste wijzigingen van sommige akten.** Waar geen nieuwere pagina van Justel beschikbaar was, eindigt de geschiedenis vroeger (de Code de droit international privé en de loi sur les accidents du travail in 2024; de delen van de oude Code civil tussen 2021 en 2026).
- **De nieuwe Code pénal** (wetten van 29 februari 2024): niet gebouwd, en de vervanging van de Code van 1867 is niet gecommit.
- **Ander recht.** Alleen deze 24 akten staan erin: geen andere wetten of besluiten, geen rechtspraak, en geen Duitse tekst of Nederlandse tekst van de andere 19 akten.
- **Opschriften** (titels, hoofdstukken, afdelingen) en de bijlagen van de Code de droit économique: alleen artikelen zijn bestanden.

## Bronnen

| Bron | Soort | Vroegere versies | Opmerkingen |
| --- | --- | --- | --- |
| [Justel](https://www.ejustice.just.fgov.be/cgi_loi/welcome.pl?language=fr) (FOD Justitie, Belgisch Staatsblad) | Officiële geconsolideerde wetgeving | "versions archivées" per akte | Een gedateerde nota per wijziging noemt de wijzigende akte en de dag van inwerkingtreding; gelezen via de twee kopieën hieronder |
| [legalize-be](https://github.com/legalize-dev/legalize-be) (Legalize), commit `da37dfb18b17` | De gearchiveerde versies van Justel als Markdown | één commit per gearchiveerde versie | De oudere versies van de meeste akten, hier opnieuw gedateerd volgens de nota's van Justel (de eigen datums van legalize-be worden niet gebruikt) |
| [Internet Archive](https://web.archive.org/) | Gearchiveerde pagina's van Justel | één per opname | De nieuwste teksten, de akten die legalize-be niet heeft, de Nederlandse teksten en de controles |

## Licentie

Zie [`LICENSE`](LICENSE). Officiële akten zijn in België niet auteursrechtelijk beschermd (Code de droit économique, art. XI.172, § 2); de gegevens van legalize-be vallen onder de "Licence ouverte / open data fédéral belge (CC0 par défaut)". De eigen bijdragen van Lexifina (de geschiedenis, commitberichten, tabellen en tools) vallen onder CC0 1.0.

Geen AI-model heeft juridische tekst geschreven, vertaald of verbeterd; de scripts zijn geschreven door een AI-model (zie [`REPRODUCE.md`](REPRODUCE.md)).

Dit is een vertaling van de Engelse versie ([README.en.md](README.en.md)); bij verschillen geldt de Engelse versie.

## Visualisaties

[visualisations/](visualisations/): nog leeg, een plaats voor grafieken over het Belgische recht, getekend uit deze repository.

## Meer

Uit de repository [lexifina/global-law](https://github.com/lexifina/global-law) (in het Engels):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): alle functies en wat elk corpus moet ondersteunen (`git blame`, `law.py`, MCP-tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): vragen en antwoorden · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): wijzigingen voorstellen · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): MCP-server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): hoe het is gemaakt · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): hoe actueel elk corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): of de updates werken · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): hoe elke officiële bron op wijzigingen wordt gevolgd
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): hoe snel de tools zijn, gemeten
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): grafieken en verbanden in het recht van de hele wereld
- [Kwetsbaarheden](https://github.com/lexifina/global-law/tree/main/vulnerabilities): fouten in regelingen zoals ze zijn gepubliceerd
