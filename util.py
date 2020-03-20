from pathlib import Path
from typing import List

from bs4 import BeautifulSoup, Tag


class Cell:
    start: int
    end: int
    referent: str = None
    r_type: str = None
    conj_referent: str = None


acceptable_referents = ['man', 'woman1', 'couple', 'people', 'family', 'ball', 'stroller', 'baby', 'woman2', 'dog',
                        'leash', 'groceries', 'trunk', 'car1', 'car2', 'car3', 'cars', 'driver1', 'driver2', 'drivers']
acceptable_r_types = ['n', 'u', 'b', 'bc', 'bd', 'g', 'gd']
acceptable_conj_referents = ['0', '1']
conjoined_referents = {'couple', 'people', 'family', 'cars', 'drivers'}

# The referent and any conjoined referents directly containing it (no bridging)
referent_parents = {
    'man': {'people'},
    'woman': {'people'},
    'baby': {'people'},
    'woman2': {'people'},
    'car1': {'cars'},
    'car2': {'cars'},
    'driver1': {'drivers'},
    'driver2': 'drivers'
}

referent_members = {
    'couple': {'man', 'woman'},
    'cars': {'car1', 'car2'},
    'drivers': {'driver1', 'driver2'}
}


def exb_in(directory: Path) -> [Path]:
    return [p for p in directory.glob('**/*.exb')]


# Merge lists of cells with referent, r_type, and conj_referent
def merge_cells(referent_cells: List[Cell], r_type_cells: List[Cell], conj_referent_cells: List[Cell]) -> List[Cell]:
    cells = list()

    while referent_cells or r_type_cells or conj_referent_cells:

        def nth_or_none(lst, n: int):
            if n < len(lst):
                return lst[n]
            else:
                return None

        referent_cell = nth_or_none(referent_cells, 0)
        r_type_cell = nth_or_none(r_type_cells, 0)
        conj_referent_cell = nth_or_none(conj_referent_cells, 0)

        min_list = [referent_cell, r_type_cell, conj_referent_cell]
        min_list = [x.start for x in min_list if x is not None]
        min_start = min(min_list)

        if referent_cell and referent_cell.start == min_start:
            start = referent_cell.start
            end = referent_cell.end
        elif r_type_cell and r_type_cell.start == min_start:
            start = r_type_cell.start
            end = r_type_cell.end
        elif conj_referent_cell and conj_referent_cell.start == min_start:
            start = conj_referent_cell.start
            end = conj_referent_cell.end
        else:
            raise Exception('panic')

        cell = Cell()
        cell.start = start
        cell.end = end

        if referent_cell and (referent_cell.start, referent_cell.end) == (start, end):
            cell.referent = referent_cell.referent
            del referent_cells[0]
        if r_type_cell and (r_type_cell.start, r_type_cell.end) == (start, end):
            cell.r_type = r_type_cell.r_type
            del r_type_cells[0]
        if conj_referent_cell and (conj_referent_cell.start, conj_referent_cell.end) == (start, end):
            cell.conj_referent = conj_referent_cell.conj_referent
            del conj_referent_cells[0]

        cells.append(cell)

    return cells


def find_cells(soup: BeautifulSoup) -> List[Cell]:
    referent_tier = list(find_tier(soup, 'referent').children)
    r_type_tier = list(find_tier(soup, 'r-type').children)
    conj_referent_tier = list(find_tier(soup, 'conj_referent').children)

    def tier_to_cells(tier: List[Tag], tier_name: str) -> List[Cell]:
        cells = list()
        for cell_tag in tier:
            if isinstance(cell_tag, Tag):
                cell = Cell()

                # T20 -> 20
                def cell_position_int(position: str) -> int:
                    return int(position[1:])

                cell.start = cell_position_int(cell_tag.attrs['start'])
                cell.end = cell_position_int(cell_tag.attrs['end'])

                if tier_name == 'referent':
                    cell.referent = cell_tag.text
                elif tier_name == 'r-type':
                    cell.r_type = cell_tag.text
                elif tier_name == 'conj_referent':
                    cell.conj_referent = cell_tag.text
                else:
                    raise Exception('panic')

                cells.append(cell)

        return cells

    referent_cells = tier_to_cells(referent_tier, 'referent')
    r_type_cells = tier_to_cells(r_type_tier, 'r-type')
    conj_referent_cells = tier_to_cells(conj_referent_tier, 'conj_referent')

    return merge_cells(referent_cells, r_type_cells, conj_referent_cells)


def find_tier(soup: BeautifulSoup, tier_name: str) -> Tag:
    tier = soup.find('tier', category=tier_name)

    if isinstance(tier, Tag):
        return tier
    else:
        raise Exception('Invalid tier found.')
