#!/usr/bin/python3

from __future__ import print_function
import pickle
import socket
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

socket.setdefaulttimeout(300)

FIELD_INFO = 'id, name, quotaBytesUsed, size'

FILENAME = 'result.txt'

def dumpTree(tree):
    with open(FILENAME, 'w') as f:
        identStr = '\t'
        indent = 0

        folders = [tree]

        while len(folders) > 0:
            if folders[-1] is None:
                indent -= 1
                folders.pop()
                continue

            folder = folders[-1]
            folders[-1] = None
            try:
                f.write(f'{identStr * indent}folder {folder["name"]!r} {folder["size"]} https://drive.google.com/drive/u/0/folders/{folder["id"]}\n')
            except UnicodeEncodeError:
                name = f'{folder["name"].encode("unicode_escape")!r}'
                f.write(f'{identStr * indent}folder {name[1:]} {folder["size"]} https://drive.google.com/drive/u/0/folders/{folder["id"]}\n')
            indent += 1

            for file in folder['files']:
                try:
                    f.write(f'{identStr * indent}file {file["name"]!r} {file["size"]}\n')
                except UnicodeEncodeError:
                    name = f'{file["name"].encode("unicode_escape")!r}'
                    f.write(f'{identStr * indent}file {name[1:]} {file["size"]}\n')
            folders += folder['folders']
    print(f'\nfile {FILENAME} has been created')

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
        listFiles(service, f)
        listFolders(service, f)
        folders += f['folders']
    dumpTree(base)

def listFiles(service, folder):
    print('listFiles: '+folder['name'])
    token = None
    while True:
        results = service.files().list(
                q=f"'{folder['id']}' in parents and mimeType != 'application/vnd.google-apps.folder'",
                # q="'"+folder['id']+"' in parents and mimeType != 'application/vnd.google-apps.folder'",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageToken=token,
                fields=f"nextPageToken, files({FIELD_INFO})").execute()
        files = results.get('files', [])
        token = results.get('nextPageToken', [])

        if files:
            folder['files'] += files
            for file in files:
                f = folder
                while f is not None:
                    f['size'] += int(file['size'])
                    f = f['parent']
        if not token:
            break

def listFolders(service, folder, token=None):
    print('listFolders: '+folder['name'])
    token = None
    while True:
        results = service.files().list(
                q=f"'{folder['id']}' in parents and mimeType = 'application/vnd.google-apps.folder'",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageToken=token,
                fields=f"nextPageToken, files({FIELD_INFO})").execute()
        folders = results.get('files', [])
        token = results.get('nextPageToken', [])

        if folders:
            for f in folders:
                f['folders'] = []
                f['files'] = []
                f['size'] = 0
                f['parent'] = folder
                folder['folders'].append(f)
        if not token:
            break

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    print('create service')
    service = build('drive', 'v3', credentials=creds)

    folderId = input('Folder id: ')
    requestTree(service, folderId.strip())
    input('press enter to close...')


if __name__ == '__main__':
    main()

'''
mimeType = type de fichier
folder:      application/vnd.google-apps.folder
spreadsheet: application/vnd.google-apps.spreadsheet
docx:        application/vnd.openxmlformats-officedocument.wordprocessingml.document
pptx:        application/vnd.openxmlformats-officedocument.presentationml.presentation
'''