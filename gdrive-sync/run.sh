#!/bin/bash

CONFIG_PATH=/data/options.json

# CLIENT_ID=$(jq --raw-output ".client_id" $CONFIG_PATH)
# CLIENT_SECRET=$(jq --raw-output ".client_secret" $CONFIG_PATH)
KEYFILE=$(jq --raw-output ".keyfile" $CONFIG_PATH)
FOLDER=$(jq --raw-output ".folder" $CONFIG_PATH)

KEYFILE_PATH="/share/${KEYFILE}"

if [ -z "$FOLDER" ]; then
    FOLDER="/"
fi

echo "[Info] Files will be uploaded to: ${FOLDER}"

# python3 /save_settings.py --clientid "$CLIENT_ID" --secret "$CLIENT_SECRET"

# echo "[Info] Running authentication flow..."
# python3 /gdrive_sync.py --auth

echo "[Info] Listening for messages via stdin service call..."

# listen for input
while read -r msg; do
    # parse JSON
    echo "$msg"
    cmd="$(echo "$msg" | jq --raw-output '.command')"
    echo "[Info] Received message with command ${cmd}"
    if [[ $cmd = "upload" ]]; then
        echo "[Info] Uploading all .tar files in /backup"
        python3 /gdrive_sync.py --output "$OUTPUT_DIR" --keyfile "$KEYFILE_PATH"
    else
        # received undefined command
        echo "[Error] Command not found: ${cmd}"
    fi
done
