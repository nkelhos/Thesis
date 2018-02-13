#!/usr/bin/env bash

rm plot.brbbbar.45.0TeV.nfits1000.withpntsrc.regionprof*.counts.png
rm *regionprof*_counts.pdf

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/logs/plot.brbbbar.45.0TeV.nfits1000.withpntsrc.regionprof*.counts.png .

for f in $( ls -1 plot.brbbbar.45.0TeV.nfits1000.withpntsrc.regionprof*.counts.png) ; do
  TARG=$(echo ${f%%.png} | tr '.' '_' ).pdf
  echo "converting $f into:"
  echo "  $TARG"
  convert $f $TARG
done
