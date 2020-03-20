import os
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup, Tag, NavigableString

import util

input_path = Path('.', 'input')
output_path = Path('.', 'output')

abbreviations = {
    "n": "new",
    "u": "unused-unknown",
    "b": "bridging",
    "bc": "bridging-contained",
    "bd": "bridging-displaced",
    "g": "given",
    "gd": "given-displaced",
}


def all_files(path: Path) -> List[Path]:
    return sorted(path.glob('**/*.exb'))


# Updates given file with expanded abbreviations
def expand_abbreviations(file_path: Path):
    with file_path.open() as file:
        soup = BeautifulSoup(file, features="html.parser")

        r_type_tier = util.find_tier(soup, "r-type")

        for entry in r_type_tier.children:
            if isinstance(entry, Tag) and [c for c in entry.children]:
                text = entry.text
                text_child: NavigableString = [c for c in entry.children][0]
                text_child.replace_with(abbreviations[text])

        output_file_path = Path(output_path, *file_path.parts[1:])

        os.makedirs(Path(*output_file_path.parts[:-1]), exist_ok=True)
        with output_file_path.open(mode='w') as output:
            output.write(str(soup))


if __name__ == '__main__':
    input_files = util.exb_in(input_path)

    for input_file in input_files:
        expand_abbreviations(input_file)
