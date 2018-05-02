import argparse
from pathlib import Path

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials


def main(keyfile, output_dir, user):

    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive']
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        keyfile, scope)

    drive = GoogleDrive(gauth)

    if not output_dir:
        parent_dir_id = 'root'
    else:
        try:
            parent_dir = drive.ListFile({
                'q':
                "title = {} and trashed=false".format(output_dir)
            }).GetList()[0]
        except IndexError:
            # create parent directory under root
            parent_dir = drive.CreateFile({
                'title':
                output_dir,
                'mimeType':
                'application/vnd.google-apps.folder'
            })
            parent_dir.Upload()
            # set permissions for this folder
            parent_dir.InsertPermission({
                'type': 'user',
                'value': user,
                'role': 'owner'
            })
            parent_dir_id = parent_dir.metadata["id"]
        parent_dir_id = parent_dir.metadata["id"]

    # List the files in the given folder
    file_list = drive.ListFile({
        'q':
        "'{}' in parents and trashed=false".format(parent_dir_id)
    }).GetList()
    file_names = (file.metadata["title"] for file in file_list)
    # Upload backups that are not already in our file list
    for path in Path('/backup').glob('**/*.tar'):
        if path.name not in file_names:
            file = drive.CreateFile({
                'title': path.name,
                'parents': [parent_dir_id]
            })
            file.Upload()
            file.InsertPermission({
                'type': 'user',
                'value': user,
                'role': 'owner'
            })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run the Gdrive Sync file uploader.')
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='output directory for uploaded files'),
    parser.add_argument(
        '--keyfile',
        dest='keyfile',
        type=str,
        required=True,
        help='If true, will run the auth flow and exit')
    parser.add_argument(
        '--user',
        dest='user',
        type=str,
        required=True,
        help='User email for google drive')
    parser.set_defaults(auth=False)
    args = parser.parse_args()
    main(args.keyfile, args.output, args.user)
