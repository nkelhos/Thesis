#!/usr/bin/env bash

rm *.{png,eps,pdf}

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/crab_test/plots/*png .

for f in `ls -1 *png` ; do
  echo $f
  EPS=${f%.*}
  EPS=$(echo $EPS | tr '.-' '_')
  EPS="${EPS}.pdf"
  echo "-> $EPS"
  convert $f $EPS
done

