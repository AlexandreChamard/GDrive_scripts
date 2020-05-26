#!/usr/bin/python3

import platform
from pathlib import Path

from downloader import downloadFileFromId, canBeDownloaded

def generateTree(service, tree, folder):
    rootPath, rootName = Path(folder['storage_loc']), folder['folder_name']
    if not rootPath.is_dir():
        print(f'path {rootPath} does not exists')
        return
    paths = [[rootPath / rootName, tree]]
    downloadPaths = folder['downloads'] if 'downloads' in folder else []
    downloadPaths = list(map(lambda p: str(paths[0][0] / p), downloadPaths))
    print(f'begin tree generation on {paths[0][0]}')
    while len(paths) > 0:
        [path, node] = paths.pop()

        if not path.exists():
            path.mkdir()
        if not path.is_dir():
            print(f'Error: fail to generate directory {path}')
            return
        for file in node['files']:
            filename = path / file['name']
            # TODO changer l'extension
            if not file['trashed'] and not filename.exists():
                touch = True
                try:
                    # TODO mettre ça ailleur
                    # TODO télécharger aussi si la date de mise à jour ne correspond pas
                    if canBeDownloaded(file):
                        for p in downloadPaths:
                            print(f'{filename} in {p}')
                            if filename.match(p):
                                print(f'TRUE {filename} in {p}')
                                downloadFileFromId(service, file['id'], filename)
                                touch = False
                                break
                finally:
                    if touch is True:
                        filename.touch()

        paths = paths + list(map(lambda f: [path / f['name'], f], node['folders']))

    print('tree generated successfuly')