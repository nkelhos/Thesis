#!/usr/bin/env bash

#rm *eps *png *pdf
rm *pdf

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/plots/background_vs_elevation/*pdf .

#scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/plots/background_vs_elevation.srccrab.png .
#scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/plots/background_vs_elevation.srcsgra.png .

#for f in `ls -1 *png` ; do
  #EPS="${f%.*}"
  #EPS=$(echo $EPS | tr '.' '_')
  #EPS="${EPS}.eps"
  #convert $f $EPS
#done

for f in `ls -1 *pdf` ; do
  CLEAN="${f%.*}"
  CLEAN=$(echo $CLEAN | tr '.' '_')
  mv "$f" "${CLEAN}.pdf"
done
