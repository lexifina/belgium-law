# Tools

The scripts behind this Belgium-only run of global-law's vulnerability detectors. They run inside a copy of
[global-law/vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) (Python 3.11+,
`pip install duckdb pyarrow`), with a bare clone of this repository at `sources/corpus/belgium-law.git`, a blobless bare
clone of global-law at `sources/global-law.git`, and a `pins.json` that names only belgium-law and its commit.
`build_vulns.py`, `flags_chart.py`, `late_ext_select.py`, `late_ext_rebut.py` and `config.json` sit in the folder that
holds the global-law checkout as `gl/`, three folders above the scripts.

| Script | What it does |
| --- | --- |
| `run.sh` | Indexes the history and texts, adds Belgium's history rows, and runs the detectors |
| `rerun.sh` | The same from `add_root.py` onward, after a change to the kinds counted as law |
| `add_root.py` | Builds Belgium's history rows from this repository's own commits (global-law's list did not include Belgium), so the history detectors read every change |
| `run_triage.sh` | The model review: the 40 strongest flags per category, the 40 strongest lapsed time limits in law texts, and the empty periods |
| `late_ext_select.py` | Chooses the empty periods for global-law's review of that category (there were none here) |
| `late_ext_rebut.py` | Adds the second, arguing-against pass to the empty-period review, as `triage.py` does for the other categories |
| `build_vulns.py` | Builds `data/flags.csv`, `data/reviewed.csv` and `data/by_category.csv` from the findings and the model review |
| `flags_chart.py` | Draws the chart at the top of the READMEs, in Dutch and English, light and dark |
| `config.json` | The repository, the Dutch category names, the folders that are not law (`caselaw/`, `circulaire/`, `data/`, `tools/`) and the chart labels |

The model review needs `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` and `LLM_AUTH` set for an OpenAI-compatible Responses API.
It was run as `bash run_triage.sh '^(caselaw|circulaire|data|tools)/'`.

Two changes to the shared scripts were made for this run:

- `add_root.py` counts the `Kind:` values `decree` (royal decrees amending a code), `court` (words annulled by the
  Constitutional Court) and `local-regulation` as changes to the law, besides `law`; `publisher` (changes Justel shows
  without an amendment note), `correction`, `caselaw` and commits without an `In-force` trailer are left out of the history
  detectors.
- `run.sh` takes `LE_WORKERS` and `LE_GREP_THREADS` from the environment (default 6); the run used
  `LE_WORKERS=2 LE_GREP_THREADS=2 bash run.sh 2` on a machine shared with other runs.
