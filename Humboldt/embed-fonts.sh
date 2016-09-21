#!/bin/bash

# usage 
if [ ! -n "$1" ] 
then
  echo "embed-fonts.sh <list> "
  echo
  echo "list contains a list of files with <filename.pdf> "
  exit
fi

LIST=$1
#echo $LIST

for FILE in $( cat $LIST ); do
    
    echo "trying to convert $FILE "
    b=`basename $FILE .pdf`
    
    # copy file over (just safety)
    cp -v $FILE $b.not-embedded.pdf

    # convert pdf to pdf to embed fonts
    gs -dBATCH -dNOPAUSE -dNOOUTERSAVE -sDEVICE=pdfwrite -dEmbedAllFonts=true -dPDFSETTINGS=/prepress -sOutputFile=$FILE $b.not-embedded.pdf

done

