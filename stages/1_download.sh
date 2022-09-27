#!/usr/bin/env bash

# Download files

localpath=$(pwd)
echo "Local path: $localpath"

temppath="$localpath/temp"
echo "Temporal path: $temppath"
mkdir -p $temppath
cd $temppath;

ftpbase="ftp://rsync.wwpdb.org/pub/pdb/data/structures/divided/pdb/"
wget --no-remove-listing $ftpbase
cat index.html | grep -Po '(?<=href=")[^"]*' | sort | cut -d "/" -f 10 > dirs.txt
rm .listing
rm index.html

downloadpath="$localpath/download"
echo "Download path: $downloadpath"
mkdir -p "$downloadpath"
cd $downloadpath;
xargs mkdir -p < $temppath/dirs.txt

cat $temppath/dirs.txt | xargs -P14 -n1 bash -c '
echo $1
wget -r -A ent.gz -nH -q --cut-dirs=7 -nc -P '$downloadpath'/$1 '$ftpbase'$1' {}

echo "Download done."
