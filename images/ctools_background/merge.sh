#!/usr/bin/env bash

montage radial_profile_0.png radial_profile_1.png -tile x1 -geometry +2+2 radial_profiles.png
convert radial_profiles.png radial_profiles.eps

montage fine_energy_histogram.png background_profile.png -tile x1 -geometry +2+2 background_construction.png
convert background_construction.png background_construction.eps
