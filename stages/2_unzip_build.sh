#!/usr/bin/env bash

localpath=$(pwd)
echo "Local path: $localpath"

downloadpath="$localpath/download"
echo "Download path: $downloadpath"

temppath="$localpath/temp"
mkdir -p $temppath
echo "Temporal path: $temppath"

# Execute conversion in parquet
cd $localpath
python ./stages/bindingDB2parquet.py $downloadpath/$tsv_file ./bindingDB.parquet


