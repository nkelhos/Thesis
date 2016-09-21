#!/usr/local/bin/bash

input='backgrounds.pdf'
cropped=`echo $input | sed -e 's/\.pdf$/-crop.pdf/'`
if [ ! -e $cropped ] ; then 
  pdfcrop $input
fi

echo "cropped:$cropped"

tmpeps=`echo $cropped | sed -e 's/\.pdf$/.eps/'`

pdftops -f 1 -l 1 -eps $cropped
s1='backgrounds.highelev.eps'
mv $tmpeps ${s1}

pdftops -f 2 -l 2 -eps $cropped
s2='backgrounds.lowelev29.eps'
mv $tmpeps ${s2}

pdftops -f 3 -l 3 -eps $cropped
s3='backgrounds.lowelev26.eps'
mv $tmpeps ${s3}

