from pathlib import Path

from bs4 import BeautifulSoup

import util

input_dir = Path('.', 'non_aligned')


def find_non_aligned(input_path: Path):
    with input_path.open() as file:
        soup = BeautifulSoup(file, features="html.parser")

        cells = util.find_cells(soup)

        output_messages = list()

        for cell in cells:
            if not cell.referent:
                message = 'No referent for cell ({}, {})'.format(cell.start, cell.end)
                output_messages.append(message)
            if not cell.r_type:
                message = 'No r_type for cell ({}, {})'.format(cell.start, cell.end)
                output_messages.append(message)
            if cell.referent and cell.referent in util.conjoined_referents and not cell.conj_referent:
                message = 'No conj_referent for conjoined_referent cell ({}, {})'.format(cell.start, cell.end)
                output_messages.append(message)

        if output_messages:
            print('==== {} ===='.format(input_path))
            print('\n'.join(output_messages))


if __name__ == '__main__':

    exb_paths = util.exb_in(input_dir)

    for path in exb_paths:
        find_non_aligned(path)
