#!/usr/bin/env bash

localpath=$(pwd)
echo "Local path: $localpath"

downloadpath="$localpath/download"
echo "Download path: $downloadpath"

temppath="$localpath/temp"
mkdir -p $temppath
echo "Temporal path: $temppath"

rawpath="$localpath/raw"
mkdir -p $rawpath
echo "Raw path: $rawpath"
cd $downloadpath
find . -type d > $temppath/dirs.txt
find . -type f -name '*.ent.gz' | cut -c 2- | sed "s/.ent.gz//" | sort > $temppath/files.txt
cd $rawpath
xargs mkdir -p < $temppath/dirs.txt
cd $rawpath

brickpath="$localpath/brick"
mkdir -p $brickpath
echo "Data path: $brickpath"
cd $brickpath
xargs mkdir -p < $temppath/dirs.txt
cd $localpath

cat $temppath/files.txt | xargs -P14 -n1 bash -c '
if test -f '$rawpath'$1.ent; then
  echo "unzip_build: file '$brickpath'$1.parquet already created."
else
  gunzip -c -v '$downloadpath'$1.ent.gz > '$rawpath'$1.ent;
  python stages/pdb2parquet.py '$rawpath'$1.ent '$brickpath'$1.parquet
  rm '$rawpath'$1.ent
fi' {}

rm -r $rawpath
