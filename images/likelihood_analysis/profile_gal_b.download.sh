#!/usr/bin/env bash

FPNG='profile_gal_b.png'
FEPS='profile_gal_b.eps'

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/logs/plot.brbbbar.10.0TeV.nfits1000.withpntsrc.b.sprof.png $FPNG

convert $FPNG $FEPS

