from pathlib import Path

from bs4 import BeautifulSoup

import util


input_dir = Path('.', 'explained_conj_referents')


def find_given_before_introduction(input_path: Path):
    with input_path.open() as file:
        soup = BeautifulSoup(file, features="html.parser")

        cells = util.find_cells(soup)

        output_messages = list()

        for cell in cells:
            if cell.conj_referent and str(cell.conj_referent) == '1':
                message = 'Explained conj_referent at cell ({}, {})'.format(cell.start, cell.end)
                output_messages.append(message)

        if output_messages:
            print('==== {} ===='.format(input_path))
            print('\n'.join(output_messages))


if __name__ == '__main__':

    exb_paths = util.exb_in(input_dir)

    for path in exb_paths:
        find_given_before_introduction(path)
