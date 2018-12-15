#!/usr/bin/env bash

rm *pdf

rsync -a -v --files-from=flist.txt nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/crescent/even_simpler_search/plots/ .
for f in `ls -1 *pdf` ; do
  echo $f
  CL=${f%.*}
  CL=$(echo $CL | tr '.-' '_')
  CL="${CL}.pdf"
  echo "-> $CL"
  mv "$f" "$CL"
done
