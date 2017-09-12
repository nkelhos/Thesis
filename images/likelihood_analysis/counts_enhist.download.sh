#!/usr/bin/env bash

FPNG='counts_enhist.png'
FEPS='counts_enhist.eps'

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/logs/plot.brbbbar.10.0TeV.nfits1000.withpntsrc.enhist.png $FPNG

convert $FPNG $FEPS

