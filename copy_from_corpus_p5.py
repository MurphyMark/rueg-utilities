from pathlib import Path

from copy_from_corpus import copy_from_corpus

corpus_directory = Path('..', '..', 'work', 'rueg-corpus', 'exb', 'RUEG', 'P5')

if __name__ == '__main__':
    mark_config = Path('.', 'config', 'mark')
    tatiana_config = Path('.', 'config', 'tatiana')

    copy_from_corpus(corpus_directory, [mark_config, tatiana_config])

    print(len([i for i in Path('.', 'input').glob('**/*.exb')]))
