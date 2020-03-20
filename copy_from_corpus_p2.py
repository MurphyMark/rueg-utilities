from pathlib import Path

from copy_from_corpus import copy_from_corpus

corpus_directory = Path('..', '..', 'work', 'rueg-corpus', 'exb', 'RUEG', 'P2')

if __name__ == '__main__':
    abigail_config = Path('.', 'config', 'abigail')
    chris_config = Path('.', 'config', 'chris')
    janie_config = Path('.', 'config', 'janie')

    copy_from_corpus(corpus_directory, [abigail_config, chris_config, janie_config])

    print(len([i for i in Path('.', 'input').glob('**/*.exb')]))
