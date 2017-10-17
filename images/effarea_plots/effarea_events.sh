#!/usr/bin/env bash

scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/plots/effarea_events*png .

montage effarea_events_crab.png effarea_events_sgra.png -tile 1x2 -geometry +2+2 effarea_events.png
convert effarea_events.png effarea_events.eps
