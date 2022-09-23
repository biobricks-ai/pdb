#!/usr/bin/env bash

# Download files

localpath=$(pwd)
echo "Local path: $localpath"

downloadpath="$localpath/download"
echo "Download path: $downloadpath"
mkdir -p "$downloadpath"
cd $downloadpath;
ftpbase="ftp://rsync.wwpdb.org/pub/pdb/data/structures/divided/pdb/"
wget -r -A ent.gz -nH --cut-dirs=6 -nc $ftpbase
echo "Download done."
