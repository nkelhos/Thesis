#!/usr/bin/env bash

TAG=$(cat tagtarget.txt)
FPNG='profile_energy.png'
FEPS='profile_energy.eps'

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/logs/plot.${TAG}.enprofile.png $FPNG

convert $FPNG $FEPS

