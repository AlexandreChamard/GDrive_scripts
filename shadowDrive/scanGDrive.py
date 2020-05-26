#!/usr/bin/python3

import json
from copy import deepcopy

FIELD_INFO = 'id, name, mimeType, size, modifiedTime, trashed'

def serializeTree(tree):
    n_tree = deepcopy(tree)
    nodes = [n_tree]
    while len(nodes) > 0:
        node = nodes.pop()
        del node['parent']
        nodes = nodes + node['folders']
    return n_tree

def dumpTree(tree, filename=None):
    serializedTree = json.dumps(serializeTree(tree), indent=2)
    if filename is None:
        print(serializedTree)
    else:
        try:
            with open(filename, 'w') as f:
                f.write(serializedTree)
        except:
            print(f'error in file "{filename}"')
            pass

def requestTree(service, baseId):
    print('start request tree')

    base = service.files().get(
        supportsAllDrives=True,
        fileId=baseId,
        fields=FIELD_INFO).execute()
    base['folders'] = []
    base['files'] = []
    base['parent'] = None
    base['size'] = 0
    folders = [base]
    while len(folders) > 0:
        f = folders.pop()
        listChildren(service, f)
        folders += f['folders']
    return base

def listChildren(service, folder):
    print(f'listChildren: {folder["name"]}')
    token = None
    while True:
        results = service.files().list(
                q=f"'{folder['id']}' in parents",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageToken=token,
                fields=f'nextPageToken, files({FIELD_INFO})').execute()
        files = results.get('files', [])
        token = results.get('nextPageToken', [])

        if files:
            for file in files:
                # replace all '/' and '\\' occurences because they break paths
                if file['name'].find('/') != -1:
                    file['name'] = file['name'].replace('/', '-')
                if file['name'].find('\\') != -1:
                    file['name'] = file['name'].replace('\\', '-')

                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    # folder
                    folder['folders'].append(file)
                    file['folders'] = []
                    file['files'] = []
                    file['size'] = 0
                    file['parent'] = folder
                else:
                    # file
                    folder['files'].append(file)
                    file['size'] = int(file['size']) if 'size' in file else 0
                    if file['mimeType'] == 'application/vnd.google-apps.document':
                        file['name'] = file['name'] + '.gdoc'
                    elif file['mimeType'] == 'application/vnd.google-apps.spreadsheet':
                        file['name'] = file['name'] + '.gsheet'
                    elif file['mimeType'] == 'application/vnd.google-apps.presentation':
                        file['name'] = file['name'] + '.gpres'
                    f = folder
                    while f is not None:
                        f['size'] += file['size']
                        f = f['parent']
        if not token:
            break

'''
mimeType = type de fichier
folder:      application/vnd.google-apps.folder
spreadsheet: application/vnd.google-apps.spreadsheet
docx:        application/vnd.openxmlformats-officedocument.wordprocessingml.document
pptx:        application/vnd.openxmlformats-officedocument.presentationml.presentation
'''