#!/usr/bin/env bash
fname=backgrounds_sims/backgrounds_sims.001.cropped.png
convert backgrounds_sims/backgrounds_sims.001.png -trim $fname
convert $fname backgrounds_sims.eps
