#!/usr/bin/env bash

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/logs/*45.0TeV.nfits1000.*pdf .

for f in $( ls -1 *pdf) ; do
  TARG=$(echo ${f%%.pdf} | tr '.' '_' ).pdf
  echo "renaming $f into:"
  echo "  $TARG"
  mv $f $TARG
done
  


