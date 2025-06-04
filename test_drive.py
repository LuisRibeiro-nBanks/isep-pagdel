import os
import pickle
import mimetypes
import io
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import argparse


SCOPES = ['https://www.googleapis.com/auth/drive.file']
FIXED_FILE_ID = '1wyouGaezj9A3gKb6ynytuQJikBNf-_8R' 


def authenticate():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def upload_file(service, filepath, file_id):
    mime_type = mimetypes.guess_type(filepath)[0]
    media = MediaFileUpload(filepath, mimetype=mime_type)
    updated_file = service.files().update(
        fileId=file_id,
        media_body=media
    ).execute()
    print(f"✅ File updated on Drive. File ID: {updated_file.get('id')}")
    return updated_file.get('id')

def download_file(service, file_id, dest_path):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(dest_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"⬇ Download progress: {int(status.progress() * 100)}%")
    print(f"✅ File downloaded to: {dest_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Upload or Download CSV from Google Drive")
    parser.add_argument('--mode', choices=['upload', 'download'], required=True, help="Choose 'upload' or 'download'")
    parser.add_argument('--file', required=True, help="Path to local file (for upload) or destination (for download)")
    
    args = parser.parse_args()
    drive_service = authenticate()
    
    if args.mode == 'upload':
        upload_file(drive_service, args.file, FIXED_FILE_ID)
        print(f"Uploaded File Successfully")
    elif args.mode == 'download':
        download_file(drive_service, FIXED_FILE_ID, args.file)
        print(f"Downloaded File Successfully")