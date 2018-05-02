# Hass.io Add-on: Google Drive Sync
Back up your Hass.io snapshots to Google Drive.

### About
This add-on allows you to upload your Hass.io snapshots to your Google Drive, keeping your snapshots safe and available in case of hardware failure. Uploads are triggered via a service call, making it easy to automate periodic backups or trigger uploads to Google Drive via script as you would with any other Home Assistant service.

This add-on uses the [pydrive](https://pythonhosted.org/PyDrive/) Python library and Google Service Accounts to upload files to Google Drive.

It requires that you create a Google Service Account and save a corresponding keyfile in the Hassio `share` directory, which is mounted into this add-on.

### Installation
1. Add the add-ons repository to your Hass.io instance: `https://github.com/danielwelch/hassio-addons`
2. Install the Google Drive Sync add-on
3. Configure the add-on with the name of your keyfile, Google account email address, and desired output directory (see configuration below)

### Usage #TODO

Gdrive Sync uploads all snapshot files (specifically, all `.tar` files) in the Hass.io `/backup` directory to a specified path in your Google Drive. This target path is specified via the `folder` option. Once the add-on is started, it will listen for service calls.

After the add-on is configured and started, trigger an upload by calling the `hassio.addon_stdin` service with the following service data:

```json
{"addon":"7be23ff5_gdrive_sync","input":{"command":"upload"}}
```

This triggers the `gdrive_sync.py` script within the add-on, which will upload files using the service account associated with the keyfile provided. You can use Home Assistant automations or scripts to run uploads at certain time intervals, under certain conditions, etc.

Gdrive Sync will only upload new snapshots to the specified path, and will skip snapshots already in the target folder.

*Note*: The hash `7be23ff5` that is prepended to the `gdrive_sync` add-on slug above is required.

### Configuration

This add-on uses a Google Service Account to manage API calls for file information and uploads. Follow these steps to set up a service account and get authenticated:
1. Go to `https://console.developers.google.com/projectselector/iam-admin/serviceaccounts` and create a new project (you must do this from the same google account that is related to the Drive you wish to upload to)
2. Select `Create Service Account`
3. Name your account and download a JSON keyfile
4. Save your keyfile in the `/share` directory in your Hass.io instance. Rename if you want. Be sure to enter the corresponding name of the file (extension included) in the `keyfile` parameter in the add-on configuration.



|Parameter|Required|Description|
|---------|--------|-----------|
|`keyfile`|Yes|The filename (including file extension) of the keyfile created above, as it is saved in your `/share` directory|
|`user`|Yes|The email address for your google account related to the Drive you wish to upload to.|
|`folder`|No|The target directory in your Dropbox to which you want to upload. If left empty, defaults to  the top level of directory of your Google Drive.|

Example Configuration:
```json
{
  "keyfile": "my_keyfile.json",
  "user": "user@gmail.com",
  "folder": "hasssio-backups"
}
```

### Suggestions and Issues
If you have suggestions or use-cases not covered by this add-on, please leave a comment on [the forum topic](). Otherwise, you may file an issue here. The flexibility of the service call and JSON service data means that this add-on could be expanded to include new features or options relatively easily.

