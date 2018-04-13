from pathlib import Path

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def main(output_dir):

    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    # at this point, user will need to navigate
    # to given URL in web browser to authenticate

    drive = GoogleDrive(gauth)

    if output_dir is None:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run the Gdrive Sync file uploader.')
    parser.add_argument(
        'client_id', type=str, help='Client ID from the Google API Console')
    parser.add_argument(
        'client_secret',
        type=str,
        help='Client Secret from the Google API Console')
    parser.add_argument(
        '--auth',
        dest='auth',
        action='store_true',
        help='If true, will run the auth flow and exit')
    parser.set_defaults(auth=False)
    args = parser.parse_args()
    if args.auth:
        gauth = GoogleAuth()
        gauth.CommandLineAuth()
    else:
        main(args.number)
