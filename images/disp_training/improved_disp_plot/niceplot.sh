#!/usr/bin/env bash

if [ ! -e somefile.txt ] ; then
  scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/thesis_disp_plots/disp.Zen62deg.V6.Noise450.ntree2000.maxdepth6.disp/somefile.txt .
fi

./niceplot.py

