#!/usr/bin/env bash
rm *.png *.cbk *.json *.eps *.pdf *.fits

scp nkelleyh3@cygnus-6.pace.gatech.edu:/nv/hp11/nkelleyh3/data/software/veripy/cluster/backgrounds/background.ReconMethodDisp.Cut-NTel2-ExtendedSource-Hard.V5.cbk .

tar xvzf background.ReconMethodDisp.Cut-NTel2-ExtendedSource-Hard.V5.cbk 

montage radial_profile_0.png radial_profile_1.png -tile 1x2 -geometry +2+2 radial_profiles.png
convert radial_profiles.png radial_profiles.eps

montage fine_energy_histogram.png background_profile.png -tile 1x2 -geometry +2+2 background_construction.png
convert background_construction.png background_construction.eps


