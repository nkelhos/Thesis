#!/usr/bin/env bash

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/plots/eventpsf_*png .

montage eventpsf_sgra.png eventpsf_crab.png -tile 1x2 -geometry +2+2 eventpsf.png
convert eventpsf.png eventpsf.eps