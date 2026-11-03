# SpecMine research — CS 599 Checkpoint 2

This repository contains a **pilot analysis** of the SpecMine v1.1 sample (July 2026 snapshot) examining whether specification-related pull requests also change code. It is a work in progress, not a completed implementation-timing study.

## Research questions

1. Are specifications and code changed together in PRs, and can their relative timing be established?
2. Do referenced files exist at a specified repository revision, and is reference match rate associated with specification length? **RQ2 not yet implemented.**

## Data

Original dataset and loader: https://github.com/shyamagarwal13/specmine-official

Data archive: https://doi.org/10.5281/zenodo.22102779

Data are **not redistributed** here. Download/clone the official repository and run its loader to obtain the `data/` directory. The scripts expect `../specmine-official/data` by default; use `--data-dir /path/to/data` to override.

## Reproduce

From this repository's root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python analysis/checkpoint2_cochange.py
python analysis/checkpoint2_timing.py
```

## Preliminary findings

The SpecMine sample contains 5,335 PR rows and 5,322 distinct `(repo_name, pr_number)` keys. Eight PRs are associated with more than one tool; 13 extra rows occur across these repeated keys. There are no fully identical PR rows. Counting each unique PR once and marking it as a co-change if **any** tool-specific record reports both specification and code changes gives 4,300 / 5,322 = **80.8%**.

The official example loader separately reported 4,294 / 5,335 = 80.5%, reflecting a different counting basis. Neither rate demonstrates that a specification preceded code.

A preliminary repository/time-window join found 4,270 PRs with candidate specification commits during their PR windows. **This does not verify those commits belong to those PRs.** It is not evidence of implementation order.

## Limitations and next steps

- Verify file classifications with manual inspection of PRs; this validation has **not** yet been performed.
- Check duplicate tool-associated rows and whether timestamps agree across tool records.
- Establish actual commit-to-PR membership and obtain code commit timestamps before classifying before/same/after timing.
- For RQ2, select a repository revision (preferably the specification's commit SHA) and inspect the corresponding tree; not yet implemented.
- Sample is intentionally selected and not representative of all GitHub repositories.

## Supporting files

- `analysis/checkpoint2_cochange.py` — unique PR aggregation
- `analysis/checkpoint2_timing.py` — exploratory repository-level time overlap
- `results/checkpoint2_results.csv` — output previously generated in local analysis
- `results/cochange_summary.csv` — independently confirmed terminal counts; regenerate using the script

