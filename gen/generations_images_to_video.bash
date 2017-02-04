#!/bin/bash

SYM_LINKS_FORMAT="%010d"
OUTPUT_NAME="puzzle_life.mpeg"

function create_symbolic_links()
{
    local -i index=0
    local IFS_SAVE=$IFS

    while IFS= read -r line; do
	local -x symbolic_link=`printf "$SYM_LINKS_FORMAT%s" $index ".jpeg"`

	ln -sf "$line" "$symbolic_link"
	index=$((index + 1))
    done <<< `ls -tr gen_*`
    IFS=$IFS_SAVE
}

function delete_symbolic_links()
{
    local -i index=0
    local IFS_SAVE=$IFS

    while IFS= read -r line; do
	local -x symbolic_link=`printf "$SYM_LINKS_FORMAT%s" $index ".jpeg"`

	rm "$symbolic_link"
	index=$((index + 1))
    done <<< `ls -tr gen_*`
    IFS=$IFS_SAVE
}

if ! [ $1 ]; then
    echo "Usage: $0 <./log_directory>"
    exit 1
fi

cd "$1"

create_symbolic_links

ffmpeg -i "$SYM_LINKS_FORMAT.jpeg" "$OUTPUT_NAME"

delete_symbolic_links
