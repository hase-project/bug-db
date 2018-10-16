import csv
from collections import defaultdict
from typing import Dict, List

from .utils import ROOT

HEMIPTERA_COMMITS_PATH = ROOT.joinpath("hemiptera_commits.tsv")


def read_bug_ids_per_project() -> Dict[str, Dict[int, str]]:
    bug_ids: Dict[str, Dict[int, str]] = defaultdict(dict)
    with open(HEMIPTERA_COMMITS_PATH) as tsvfile:
        tsvreader = csv.DictReader(tsvfile, delimiter="\t")
        for line in tsvreader:
            bug_id = int(line["bug_id"])
            name = line["project"]
            bug_ids[name][bug_id] = line["commit"]
    return bug_ids
