from pathlib import Path
from typing import Set

from bs4 import BeautifulSoup

import util


input_dir = Path('.', 'given_before_introduction')


def is_given_acceptable(seen_referents: Set[str], referent: str):
    return referent in seen_referents \
           or (referent in util.referent_parents
               and any([parent in seen_referents for parent in util.referent_parents[referent]])) \
           or (referent in util.referent_members
               and all([member in seen_referents for member in util.referent_members[referent]]))


def find_given_before_introduction(input_path: Path):
    with input_path.open() as file:
        soup = BeautifulSoup(file, features="html.parser")

        cells = util.find_cells(soup)

        seen_referents = set()
        output_messages = list()

        for cell in cells:
            if cell.referent and cell.r_type and cell.r_type == 'g':
                if not is_given_acceptable(seen_referents, cell.referent):
                    message = 'Given before introduction for cell ({}, {})'.format(cell.start, cell.end)
                    output_messages.append(message)
            if cell.referent:
                seen_referents.add(cell.referent)

        if output_messages:
            print('==== {} ===='.format(input_path))
            print('\n'.join(output_messages))


if __name__ == '__main__':

    exb_paths = util.exb_in(input_dir)

    for path in exb_paths:
        find_given_before_introduction(path)
