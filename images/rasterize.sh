#!/usr/bin/env bash

fff=(
plot_elev27_5_32_5deg_4_70TeV_wobbleall_Epochall_profa_skymap.pdf
plot_elev27_5_32_5deg_4_70TeV_wobbleall_Epochall_profb_skymap.pdf
plot_elev27_5_32_5deg_4_70TeV_wobbleall_Epochall_profe_skymap.pdf
plot_elev27_5_32_5deg_4_70TeV_wobbleall_Epochall_profl_skymap.pdf
)

for f in "${fff[@]}" ; do
  echo "$f"
  s1=$( echo "$f" | cut -f1 -d '.' )
  s1="${s1}_rasterized"
  s2="${s1}.pdf"
  s1="${s1}.png"
  convert "$f" "$s1"
  convert "$s1" "$s2"
done

