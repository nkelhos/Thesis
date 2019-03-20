#!/usr/bin/env bash

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/paramhists/plot*pdf .

mv plot.pref.pdf plot_pref.pdf
mv plot.indx.pdf plot_indx.pdf

