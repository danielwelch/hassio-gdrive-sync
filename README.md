# Hass.io Add-on: Google Drive Sync
Back up your Hass.io snapshots to Google Drive.

### About
This add-on allows you to upload your Hass.io snapshots to your Google Drive, keeping your snapshots safe and available in case of hardware failure. Uploads are triggered via a service call, making it easy to automate periodic backups or trigger uploads to Google Drive via script as you would with any other Home Assistant service.

This add-on uses the [pydrive](https://pythonhosted.org/PyDrive/) Python library to upload files to Google Drive.

It requires that you generate a Client Secret and Client ID via the Google API Console, which must be added to this add-on's configuration via the Hass.io UI (see below for further details).

### Installation
1. Add the add-ons repository to your Hass.io instance: `https://github.com/danielwelch/hassio-addons`
2. Install the Google Drive Sync add-on
3. Configure the add-on with your Client ID, Client Secret, and desired output directory (see configuration below)

### Usage #TODO

Gdrive Sync uploads all snapshot files (specifically, all `.tar` files) in the Hass.io `/backup` directory to a specified path in your Google Drive. This target path is specified via the `folder` option. Once the add-on is started, it will initiate the authentication flow (see below) and,after that is completed, will listen for service calls.

After the add-on is configured and started, trigger an upload by calling the `hassio.addon_stdin` service with the following service data:

```json
{"addon":"7be23ff5_gdrive_sync","input":{"command":"upload"}}
```

This triggers the `dropbox_uploader.sh` script with the provided access token. You can use Home Assistant automations or scripts to run uploads at certain time intervals, under certain conditions, etc.

Gdrive Sync will only upload new snapshots to the specified path, and will skip snapshots already in the target folder.

*Note*: The hash `7be23ff5` that is prepended to the `gdrive_sync` add-on slug above is required.

### Configuration

To access your personal Dropobox, this add-on (and the `pydrive` library more generally) requires a client ID and secret, as well as some manual authentication. Follow these steps to get authenticated during add-on installation:
1. Go to `https://console.developers.google.com/apis/` and create a new project
2. Open the `Credentials` page from the side bar, click the `Create credentials` button, and select `Oauth Client ID` from the dropdown menu
3. Select `Other` as the type and name it whatever you want
4. Once the credentials are created, copy the displayed Client ID into the `client_id` option in this add-on's configuration, and the secret into `client_secret` (you can also download these as a JSON if you'd like)
5. Upon starting the add-on, you should see a message asking you to visit a link in your browser and to enter in a verification code before continuing. Go to the link, copy the verification code, and use a `hassio.addon_stdin` service call to pass the verification code into the add-ons `STDIN` with the following service data: `{"addon":"7be23ff5_gdrive_sync","input":{"<YOUR_VERIFICATION_CODE_HERE"}}`


|Parameter|Required|Description|
|---------|--------|-----------|
|`client_id`|Yes|The client id you generated above via the Google API Console.|
|`client_secret`|Yes|The client secret you generated above via the Google API Console.|
|`folder`|No|The target directory in your Dropbox to which you want to upload. If left empty, defaults to  the top level of directory of your Google Drive.|

Example Configuration:
```json
{
  "client_id": "<YOUR_TOKEN>",
  "client_secret": "<YOUR_SECRET>",
  "folder": "/hasssio-backups/"
}
```

### Suggestions and Issues
If you have suggestions or use-cases not covered by this add-on, please leave a comment on [the forum topic](). Otherwise, you may file an issue here. The flexibility of the service call and JSON service data means that this add-on could be expanded to include new features or options relatively easily.

