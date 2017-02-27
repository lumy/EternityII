#!/bin/bash

SYM_LINKS_FORMAT="%010d"
OUTPUT_NAME="puzzle_life.mpeg"
FFMPEG=$(which ffmpeg)
LN=$(which ln)
if [[ "" == "$LN" ]]; then
  LN=$(which cp)
else
  LN="$LN -s"
fi
if [[ "" == "$FFMPEG" ]]; then
  echo "You need ffmpeg installed"
  exit -1
fi

function create_symbolic_links()
{
    local -i index=0
    local IFS_SAVE=$IFS

    for line in `ls`; do
    local -x symbolic_link=`printf "$SYM_LINKS_FORMAT%s" $index ".jpeg"`

	$LN -f "$line" "$symbolic_link"
#    cp -f "$line" "$symbolic_link"

	index=$((index + 1))
    done
    IFS=$IFS_SAVE
}

function delete_symbolic_links()
{
    local -i index=0
    local IFS_SAVE=$IFS

    for line in `ls`; do
	local -x symbolic_link=`printf "$SYM_LINKS_FORMAT%s" $index ".jpeg"`

	rm -f "$symbolic_link"
	index=$((index + 1))
    done
    IFS=$IFS_SAVE
}

if ! [ $1 ]; then
    echo "Usage: $0 <./log_directory>"
    exit 1
fi

cd "$1"
cd "images"

# create_symbolic_links

$FFMPEG -framerate 0.80  -i  "$SYM_LINKS_FORMAT.jpeg" -r 30 "$OUTPUT_NAME"

#delete_symbolic_links
