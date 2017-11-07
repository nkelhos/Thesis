#!/usr/bin/env bash
TAG=$(cat tagtarget.txt)
FPNG='counts_skymap.png'
FEPS='counts_skymap.eps'
scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/logs/plot.${TAG}.counts.png $FPNG
convert $FPNG $FEPS
