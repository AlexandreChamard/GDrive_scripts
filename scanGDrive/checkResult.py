#!/usr/bin/python3

import shlex
import math
import sys

FILENAME = 'result.txt'

'''
folder:
    isFolder = True
    parent
    name
    size
    ssize
    id
    children

file:
    isFolder = False
    name
    size
    ssize
'''

def getDataFromFile():
    currentFolder = None
    indent = 0
    with open(FILENAME) as f:
        for line in f:
            if line == '':
                break
            n = getIndent(line)
            while n < indent:
                sortChildren(currentFolder)
                currentFolder = currentFolder['parent']
                indent -= 1
            words = shlex.split(line)
            if words[0] == 'folder':
                [_, name, size, id] = words
                currentFolder = {
                    'isFolder': True,
                    'parent': currentFolder,
                    'name': name,
                    'size': int(size),
                    'ssize': genStrSize(size),
                    'id': id,
                    'children': []
                }
                if currentFolder['parent'] is not None:
                    currentFolder['parent']['children'].append(currentFolder)
                indent += 1
            else:
                [_, name, size] = words
                currentFolder['children'].append({
                    'isFolder': False,
                    'name': name,
                    'size': int(size),
                    'ssize': genStrSize(size)
                })
    if currentFolder is None:
        return None
    while currentFolder['parent'] is not None:
        sortChildren(currentFolder)
        currentFolder = currentFolder['parent']
    sortChildren(currentFolder)
    return currentFolder

def sortChildren(folder):
    folder['children'] = sorted(folder['children'], key=lambda child: int(child['size']), reverse=True)

def genStrSize(s):
    s = s[::-1]
    return (','.join([s[i:i+3] for i in range(0, len(s), 3)]))[::-1]

def getIndent(line):
    i = 0
    while line[i] == '\t':
        i += 1
    return i

INDENT_STR = '  '
def dumpFolder(folder, maxIndent, indent=1, powerSize=0):
    if powerSize == 0:
        powerSize = len(folder['ssize']) + 1
    print(f"{INDENT_STR * indent}-{folder['ssize'].rjust(powerSize)} F {folder['name']!r}\t\t{folder['id']}")
    if indent > maxIndent:
        return
    indent += 1
    if len(folder["children"]) > 0:
        powerSize = len(folder["children"][0]["ssize"]) + 1
    for child in folder['children']:
        if child['isFolder'] is True:
            dumpFolder(child, maxIndent, indent, powerSize)
        else:
            print(f"{INDENT_STR * indent}-{child['ssize'].rjust(powerSize)} {child['name']!r}")

def printHelp():
    print('ls [n]:\t\tliste les fichiers à partir de dossier jusqu\'à de la profondeur n (1 par default)')
    print('cd:\t\tretourne à la racine (dossier le plus haut)')
    print('cd ..:\t\tretourne un dossier au dessus')
    print('cd name:\tva dans le dossier name')
    print('exit:\t\texit')
    print('help:\t\thelp')

def main():
    folder = getDataFromFile()
    printHelp()
    while True:
        line = input('> ')
        try:
            words = shlex.split(line)
            if len(words) == 0:
                continue
            if words[0] == 'exit':
                break

            elif words[0] == 'help':
                printHelp()

            elif words[0] == 'ls':
                if len(words) > 1:
                    dumpFolder(folder, int(words[1]))
                else:
                    dumpFolder(folder, 1)

            elif words[0] == 'cd':
                if len(words) == 1: # goto Base
                    while folder['parent'] is not None:
                        folder = folder['parent']
                elif words[1] == '..':
                    if folder['parent'] is None:
                        print('already on base')
                    else:
                        folder = folder['parent']
                else:
                    folderName = ' '.join(words[1:])
                    for child in folder['children']:
                        if child['name'] == folderName:
                            if child['isFolder'] is True:
                                folder = child
                            else:
                                print(f'{folderName!r} is not a folder')
                            break
                    else:
                        print(f'folder {folderName!r} not found')

            else:
                print(f"bad command {words[0]}. print 'help' for show the help.")

        except ValueError:
            print("Could not convert data to an integer.")

if __name__ == '__main__':
    main()