#!/usr/bin/python3

import platform
from pathlib import Path

def generateTree(tree, rootPath):
    paths = [[Path(rootPath) / tree['name'], tree]]
    print('begin tree generation')
    while len(paths) > 0:
        [path, node] = paths.pop()

        if path.exists() is False and path.is_dir() is False:
            print(f'path {path} is dir: {path.is_dir()}')
            path.mkdir()
        if path.is_dir() is False:
            print(f'Error: fail to generate directory {path}')
            return
        for file in node['files']:
            filename = path / file['name']
            # TODO changer l'extension
            if filename.exists() is False:
                filename.touch()

        paths = paths + list(map(lambda f: [path / f['name'], f], node['folders']))

    print('tree generation successful')