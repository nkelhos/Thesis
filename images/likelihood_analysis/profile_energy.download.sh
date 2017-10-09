#!/usr/bin/env bash

FPNG='profile_energy.png'
FEPS='profile_energy.eps'

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/logs/plot.brbbbar.45.0TeV.nfits1000.withpntsrc.enprofile.png $FPNG

convert $FPNG $FEPS

