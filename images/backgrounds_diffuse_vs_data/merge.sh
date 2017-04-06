#!/usr/bin/env bash

montage lowelev_bck_fits_1.888TeV.raw.png lowelev_bck_fits_2.494TeV.raw.png lowelev_bck_fits_3.070TeV.raw.png lowelev_bck_fits_4.194TeV.raw.png -tile 2x2 -geometry +2+2 diffuse_sims.png

convert diffuse_sims.png diffuse_sims.eps
