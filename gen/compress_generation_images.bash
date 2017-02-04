#!/bin/bash

ARCHIVE_DIR="generations_images"
OUTPUT_FILE="$ARCHIVE_DIR.tar.gz"

if ! [ $1 ]; then
    echo "Usage: $0 <./log_directory>"
    exit 1
fi

cd "$1"

first_image=`ls -tr gen_* | head -n1`
last_image=`ls -tr gen_* | tail -n1`

mkdir "$ARCHIVE_DIR"

mv gen_* "$ARCHIVE_DIR"

cp "$ARCHIVE_DIR/$first_image" .
cp "$ARCHIVE_DIR/$last_image" .

export GZIP=-9
tar cvzf "$OUTPUT_FILE" "$ARCHIVE_DIR"

rm -r "$ARCHIVE_DIR"

echo "Output file: '$OUTPUT_FILE'"
