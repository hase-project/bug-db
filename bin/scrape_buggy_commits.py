#!/usr/bin/env python
import glob
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterator, Tuple

import pandas as pd


def normalize_string(s: str) -> str:
    if isinstance(s, str):
        return s.strip()
    return s


INTERNAL_ID = re.compile(".*internal\s+id.*", re.IGNORECASE)


def scrape_ids(df: pd.DataFrame) -> Dict[int, int]:
    found_internal_ids = False
    row_to_id = {}  # type: Dict[int, int]
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


UNFIXED_COMMIT = re.compile(".*unfixed\s+commit.*", re.IGNORECASE)


def scrape_commits(df: pd.DataFrame) -> Dict[int, str]:
    found_commits = False
    row_to_commits = {}  # type: Dict[int, str]
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


BUG_TYPE = re.compile(".*bug\s+(type|details).*", re.IGNORECASE)


def scrape_bug_type(df: pd.DataFrame, col: int) -> Dict[int, str]:
    found_bug_type = False
    row_to_commits = {}  # type: Dict[int, str]
    for (row, value) in enumerate(df[df.columns[col]].values):
        value = normalize_string(value)
        if isinstance(value, str) and BUG_TYPE.match(value):
            found_bug_type = True
        elif found_bug_type:
            row_to_commits[row] = value
    return row_to_commits


def scrape_bugs(df: pd.DataFrame, bug_col: int = 9) -> Iterator[Tuple[int, str, str]]:
    row_to_id = scrape_ids(df)
    row_to_commits = scrape_commits(df)
    row_to_bug_type = scrape_bug_type(df, bug_col)
    assert len(row_to_bug_type) > 0
    assert len(row_to_commits.keys() - row_to_id.keys()) == 0
    bugs_with_commits = row_to_id.keys() & row_to_commits.keys()
    for id in bugs_with_commits:
        yield (row_to_id[id], row_to_commits[id], row_to_bug_type[id])


def main() -> None:
    if len(sys.argv) < 2:
        print("USAGE: {} sheet_directory".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    sheet_path = Path(sys.argv[1])
    sheets = glob.glob(str(sheet_path.joinpath("*.csv")))
    reproducible_bugs = defaultdict(list)  # type: defaultdict
    for sheet in sheets:
        with open(sheet) as f:
            df = pd.read_csv(f)
        bug_col = 9
        name, _ = os.path.splitext(os.path.basename(sheet))
        if name.lower() in "coreutils":
            bug_col = 8
        elif name.lower() == "jasper":
            bug_col = 10
        for (bug_id, commit, bug_type) in scrape_bugs(df, bug_col):
            reproducible_bugs["project"].append(name.lower())
            reproducible_bugs["bug_id"].append(bug_id)
            reproducible_bugs["commit"].append(commit)
            reproducible_bugs["bug_type"].append(bug_type)
    new_df = pd.DataFrame(reproducible_bugs)
    new_df.to_csv(sys.stdout, sep="\t")


if __name__ == "__main__":
    main()
