#!/usr/bin/env python
import glob
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterator, Tuple

import pandas as pd

INTERNAL_ID = re.compile(".*internal\s+id.*", re.IGNORECASE)
UNFIXED_COMMIT = re.compile(".*unfixed\s+commit.*", re.IGNORECASE)


def normalize_string(s):
    if isinstance(s, str):
        return s.strip()
    return s


def scrape_ids(df) -> Dict[int, int]:
    found_internal_ids = False
    row_to_id: Dict[int, int] = {}
    for (row, value) in enumerate(df[df.columns[0]].values):
        value = normalize_string(value)
        if isinstance(value, str) and INTERNAL_ID.match(value):
            found_internal_ids = True
        elif found_internal_ids:
            try:
                row_to_id[row] = int(value)
            except ValueError:
                found_internal_ids = False
    return row_to_id


def scrape_commits(df) -> Dict[int, str]:
    found_commits = False
    row_to_commits: Dict[int, str] = {}
    for (row, value) in enumerate(df[df.columns[4]].values):
        value = normalize_string(value)
        if isinstance(value, str) and UNFIXED_COMMIT.match(value):
            found_commits = True
        elif (
            found_commits
            and isinstance(value, str)
            and re.match("^[a-fA-F0-9]+$", value)
        ):
            row_to_commits[row] = value
    return row_to_commits


def scrape_bugs(df) -> Iterator[Tuple[int, str]]:
    row_to_id = scrape_ids(df)
    row_to_commits = scrape_commits(df)
    assert len(row_to_commits.keys() - row_to_id.keys()) == 0
    bugs_with_commits = row_to_id.keys() & row_to_commits.keys()
    for id in bugs_with_commits:
        yield (row_to_id[id], row_to_commits[id])


def main():
    if len(sys.argv) < 2:
        print(f"USAGE: {sys.argv[0]} sheet_directory", file=sys.stderr)
        sys.exit(1)
    sheet_path = Path(sys.argv[1])
    sheets = glob.glob(str(sheet_path.joinpath("*.csv")))
    reproducible_bugs = defaultdict(list)
    for sheet in sheets:
        with open(sheet) as f:
            df = pd.read_csv(f)
        for (bug_id, commit) in scrape_bugs(df):
            name, _ = os.path.splitext(os.path.basename(sheet))
            reproducible_bugs["project"].append(name.lower())
            reproducible_bugs["bug_id"].append(bug_id)
            reproducible_bugs["commit"].append(commit)
    new_df = pd.DataFrame(reproducible_bugs)
    new_df.to_csv(sys.stdout, sep="\t")


if __name__ == "__main__":
    main()
