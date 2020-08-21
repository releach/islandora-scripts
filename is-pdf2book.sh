#!/bin/bash


# This script takes a folder of ISCRUD-derived PDFs and MODSXML (so named namespace_pid_DSID.ext), breaks the PDFS
# into tiffs, and places them in the directory structure necessary for islandora_book_batch_preprocess.
# To run this: sh is-pdf2book.sh input-directory/ output-directory/
IPATH=$1  # Path to input directory containing PDFs.
OPATH=$2  # Path to output directory.



if [ ! -d "$OPATH" ]; then
    mkdir -p "$OPATH"
fi

for FILE in $IPATH*.pdf; do
    PID=$(echo $FILE | cut -d'/' -f2 |cut -d'_' -f1,2 )
    BOOK=$OPATH$(basename $FILE .pdf)
    mkdir $BOOK
    mv $IPATH$PID"_MODS.xml" $BOOK
    gs -dNOPAUSE -r300x300 -sDEVICE=tiff24nc -sOutputFile=$BOOK.tiff "./$FILE" -c quit
    convert "$BOOK.tiff" "%03d.tiff"

    cp $FILE $BOOK
    rm "$BOOK.tiff"

    c=1
    for f in *.tiff
      do
        mkdir "$BOOK"/$c
        filename="${f%%.*}"
        echo Processing $filename ...
        mv "$f" "$BOOK"/$c/OBJ.tif
        # mv "$f" "$OPATH"_tmp
        let c=c+1
      done
done
