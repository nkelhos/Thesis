#!/usr/bin/env bash

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/plots/effarea_events*pdf .

#montage effarea_events_crab.pdf effarea_events_sgra.pdf -tile 1x2 -geometry +2+2 effarea_events.pdf
pdfjam effarea_events_crab.pdf effarea_events_sgra.pdf --outfile effarea_events_tmp.pdf --nup 1x2

pdfcrop effarea_events_tmp.pdf effarea_events.pdf

#convert effarea_events.png effarea_events.eps
