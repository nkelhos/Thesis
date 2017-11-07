#!/usr/bin/env bash

TAG=$(cat tagtarget.txt)
FPNG='profile_gal_b.png'
FEPS='profile_gal_b.eps'

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/logs/plot.${TAG}.b.sprof.png $FPNG

convert $FPNG $FEPS

