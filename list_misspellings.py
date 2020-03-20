from pathlib import Path
from typing import List

from bs4 import BeautifulSoup, Tag

import util
from util import acceptable_referents, acceptable_r_types, acceptable_conj_referents

input_dir = Path('.', 'corrected_misspellings')


def correct_misspellings_tier(file_name: str, acceptable_values: List[str], tier: Tag):
    for entry in tier.children:
        if isinstance(entry, Tag) and list(entry.children):
            text = entry.text
            if text not in acceptable_values:
                print(file_name)
                print(text + '\t' + entry.attrs['start'])


def correct_misspellings(input_dir: Path, input_paths: [Path]):
    for input_path in input_paths:
        with input_path.open() as file:
            soup = BeautifulSoup(file, features="html.parser")

            referent_tier = util.find_tier(soup, "referent")
            r_type_tier = util.find_tier(soup, "r-type")
            conj_referent_tier = util.find_tier(soup, "conj_referent")

            correct_misspellings_tier(file.name, acceptable_referents, referent_tier)
            correct_misspellings_tier(file.name, acceptable_r_types, r_type_tier)
            correct_misspellings_tier(file.name, acceptable_conj_referents, conj_referent_tier)


if __name__ == '__main__':
    input_paths = util.exb_in(input_dir)
    correct_misspellings(input_dir, input_paths)
