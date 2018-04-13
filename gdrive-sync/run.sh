#!/bin/bash

CONFIG_PATH=/data/options.json

CLIENT_ID=$(jq --raw-output ".oauth_client_id" $CONFIG_PATH)
CLIENT_SECRET=$(jq --raw-output ".oauth_client_secret" $CONFIG_PATH)
FOLDER=$(jq --raw-output ".folder" $CONFIG_PATH)

if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="/"
fi

echo "[Info] Files will be uploaded to: ${OUTPUT_DIR}"

python3 save_settings.py "$CLIENT_ID" "$CLIENT_SECRET"

echo "[Info] Running authentication flow..."
python3 /gdrive_sync.py --auth

echo "[Info] Listening for messages via stdin service call..."

# listen for input
while read -r msg; do
    # parse JSON
    echo "$msg"
    cmd="$(echo "$msg" | jq --raw-output '.command')"
    echo "[Info] Received message with command ${cmd}"
    if [[ $cmd = "upload" ]]; then
        echo "[Info] Uploading all .tar files in /backup"
        python3 /gdrive_sync.py "$OUTPUT_DIR"
    else
        # received undefined command
        echo "[Error] Command not found: ${cmd}"
    fi
done
