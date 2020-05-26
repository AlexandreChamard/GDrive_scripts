#!/usr/bin/python3

import sys
import json
import pickle
import os.path
from pathlib import Path

import functools 
import operator 

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from scanGDrive import requestTree, dumpTree
from arborescence import generateTree

DEFAULT_PATH = Path('../store')

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def loadConfig(path):
    with open(path) as f:
        config = json.loads(f.read())
        if 'shadow_folders' in config is False:
            raise Exception('Config Error: need "shadow_folders" key')
        for f in config['shadow_folders']:
            if not 'folder_name' in f or not isinstance(f['folder_name'], str):
                raise Exception('Config Error: need "folder_name" key on shadow folders and must be a string')
            if not 'folder_id' in f or not isinstance(f['folder_id'], str):
                raise Exception('Config Error: need "folder_id" key on shadow folders and must be a string')
            if not 'storage_loc' in f:
                f['storage_loc'] = DEFAULT_PATH
            elif not isinstance(f['storage_loc'], str):
                raise Exception('Config Error: "storage_loc" must be a string')
            if 'downloads' in f:
                if not isinstance(f['downloads'], list) or not functools.reduce(operator.__and__, map(lambda s: isinstance(s, str), f['downloads']), True):
                    raise Exception('Config Error: "downloads" must be a list of string')
                if functools.reduce(operator.__or__, map(lambda s: s.find('..') != -1, f['downloads']), False):
                    raise Exception("Config Error: downloads' strings cannot contain '..'")
        return config

def main():
    if len(sys.argv) == 1:
        print('missing config argument')
        return
    config = loadConfig(sys.argv[1])
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

    for folder in config['shadow_folders']:
        print('\n=======================')
        print(folder)
        try:
            tree = requestTree(service, folder['folder_id'])
            dumpTree(tree, DEFAULT_PATH / f'{folder["folder_name"]}_result.json')
            generateTree(service, tree, folder)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(f'{type(e)}: an error has occur in {folder["folder_name"]}')
                raise e

    '''
    1. requeter tous les metadatas
    récuperer:
    - tout les dossiers
    - tout les fichiers
    - les id des fichiers
    - les sizes (réelles)
    - les noms de fichiers
    - le type de fichier
    regarder si optimisable (prendre seulement les updates)
    regarder si optimisable (requeter tout les fichiers qui ont pour super-parent la racine)

    TODO 2. verifier les diferences avec le local
    lister les modifications positives (ajout)
    lister les modifications positives (deletion)
    merge les dossiers bougés (retrouver dans ajout et deletion)

    3.
    recréer l'arborescence dans l'ordi avec des fichiers vides
    nommer les fichiers name.metadata
    si le fichier dans le drive est type google:
    gdoc -> .gdoc.metadata
    gsheet -> .gsheet.metadata
    '''


if __name__ == '__main__':
    main()

