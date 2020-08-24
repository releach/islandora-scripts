#!/bin/bash

# This script takes a folder of tiffs and places them in the directory structure necessary for islandora_book_batch_preprocess.
# To run this: sh flatDir2book.sh input-directory/

IPATH=$1 #Path to input directory of tiffs. Filename prefixes must be uniform (eg ms0500-) and suffixes must be in three-digit number format (eg 001.tiff)

c=1
for f in $IPATH*.tiff
  do
    filename="${f%%.*}"
    echo Processing $filename ...
    mkdir $IPATH$c
    mv "$f" $IPATH$c/OBJ.tif
    let c=c+1
  done
