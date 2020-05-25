#!/usr/bin/python3

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from scanGDriveFolder import requestTree, pprintTree
from arborescence import generateTree

FILENAME = 'result.txt'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

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

    print('ok')
    folderId = input('Folder id: ')
    tree = requestTree(service, folderId.strip())
    pprintTree(tree, FILENAME)
    generateTree(tree, '.')
    input('press enter to close...')


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

