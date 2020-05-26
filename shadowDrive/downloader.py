
import io
from googleapiclient.http import MediaIoBaseDownload

INVALID_TYPES = [
    'application/vnd.google-apps.folder',
    'application/vnd.google-apps.spreadsheet',
    'application/vnd.google-apps.document',
    'application/vnd.google-apps.presentation',
]

def downloadFileFromId(service, fileId, filename):
    request = service.files().get_media(fileId=fileId)
    fh = io.FileIO(filename, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    print(f'Download {filename}: 0%', end='')
    while done is False:
        status, done = downloader.next_chunk()
        print(f"\rDownload {filename}: {int(status.progress() * 100)}%", end='')
    print('')

def canBeDownloaded(file):
    return not file['mimeType'] in INVALID_TYPES