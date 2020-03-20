import os
import re
import shutil
from pathlib import Path
from typing import Tuple, List

output_directory = Path('.', 'input')


class Exb:
    path: Path
    file_name: str
    speaker: str

    def __init__(self, path: Path):
        self.path = path
        self.file_name = path.parts[-1]
        self.speaker = self.file_name.split('_')[0]


# Returns a list of (file_name, group)
def read_configs(config_paths: List[Path]) -> List[Tuple[str, str]]:
    config_list = list()

    for config_path in config_paths:
        with config_path.open() as config:
            lines = [s.rstrip() for s in config.readlines()]

            if len(lines) % 2 != 0:
                raise Exception('Invalid config file')

            midpoint = len(lines) // 2
            file_names = lines[:midpoint]
            paths = lines[midpoint:]

            config_list += (list(zip(file_names, paths)))

    return config_list


# list of (speaker, group) -> list of (corpus_path, output_path)
def generate_paths(corpus_directory: Path, speakers: List[Tuple[str, str]]) -> List[Tuple[Path, Path]]:
    paths = list()
    all_exb_files = [Exb(p) for p in corpus_directory.glob('**/*.exb')]
    for (speaker, group) in speakers:

        speaker_paths = list()
        for exb in all_exb_files:
            if speaker.lower() == exb.speaker.lower() \
                    and re.findall('_..e\\.exb', exb.file_name.lower()):
                corpus_path = exb.path
                output_path = Path(output_directory, group, exb.file_name)
                speaker_paths.append((corpus_path, output_path))
                paths += speaker_paths

        if len(speaker_paths) != 4:
            raise Exception('Wrong number of speaker files')

    return paths


# Takes a list of (corpus_path, output_path)
def copy_files(files: List[Tuple[Path, Path]]):
    for (corpus_path, output_path) in files:
        os.makedirs(Path(*output_path.parts[:-1]), exist_ok=True)
        shutil.copy(str(corpus_path), str(output_path))


def copy_from_corpus(corpus_directory: Path, config_paths: List[Path]):
    configs = read_configs(config_paths)
    copy_paths = generate_paths(corpus_directory, configs)
    copy_files(copy_paths)
