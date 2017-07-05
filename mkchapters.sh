#!/bin/sh

SOURCE_DIR="../mes.wiki/doku"
TARGET_DIR="Kapitel"

brew install pandoc &> /dev/null || \
sudo apt-get install -y pandoc

if [ ! -d $SOURCE_DIR ]; then
    repo="$(dirname $SOURCE_DIR)"
    echo "The repo \"$repo\" does not exist in parent directory."
    echo "git clone https://gitlab.com/kaikuehne/mes.wiki $repo"
    exit 1
fi

if [ ! -d Kapitel ]; then
    mkdir Kapitel
fi

for md in "$SOURCE_DIR"/*-*.md; do
    echo "Converting $(basename $md)..."
    pandoc --normalize --smart --top-level-division=chapter $md -f markdown -t latex -o "Kapitel/$(basename $md).tex"
done

