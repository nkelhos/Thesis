#!/usr/bin/env bash

#scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/plots/eventpsf_* .
scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/plots/eventpsf_*pdf .

#montage eventpsf_sgra.png eventpsf_crab.png -tile 1x2 -geometry +2+2 eventpsf.png
#convert eventpsf.png eventpsf.eps
#montage eventpsf_sgra.pdf eventpsf_crab.pdf -tile 1x2 -geometry +2+2 eventpsf.pdf
