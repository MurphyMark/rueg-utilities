from pathlib import Path
from queue import Queue

from bs4 import BeautifulSoup

import util

NUMBER_OF_REPETITIONS = 3

input_dir = Path('.', 'non_aligned')


def find_repetitions(input_path: Path):
    with input_path.open() as file:
        soup = BeautifulSoup(file, features="html.parser")

        cells = util.find_cells(soup)

        last_n_referents = list()
        max_size = NUMBER_OF_REPETITIONS - 1
        output_messages = list()

        for cell in cells:
            if cell.referent and last_n_referents and all([r == cell.referent for r in last_n_referents]):
                message = 'Duplicated referent at cell ({}, {})'.format(cell.start, cell.end)
                output_messages.append(message)
            if len(last_n_referents) == max_size:
                del last_n_referents[0]

            last_n_referents.append(cell.referent)

        if output_messages:
            print('==== {} ===='.format(input_path))
            print('\n'.join(output_messages))


if __name__ == '__main__':

    exb_paths = util.exb_in(input_dir)

    for path in exb_paths:
        find_repetitions(path)
