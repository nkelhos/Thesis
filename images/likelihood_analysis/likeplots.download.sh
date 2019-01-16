#!/usr/bin/env bash

rm *png *pdf

#scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/logs/*45.0TeV.nfits1000.*pdf .
scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/refined_platinum_analysis/output/nfits1000/*45.00TeV.*pdf .
scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/refined_platinum_analysis/output/nfits1000/subplots/*45.00TeV.*pdf .

for f in $( ls -1 *pdf) ; do
  TARG=$(echo ${f%%.pdf} | tr '.' '_' ).pdf
  echo "renaming $f into:"
  echo "  $TARG"
  mv $f $TARG
done
  

fff=(
plot_brbbbar_45_00TeV_profile_baxis_json_minimap.pdf
plot_brbbbar_45_00TeV_profile_laxis_json_minimap.pdf
plot_brbbbar_45_00TeV_profile_energy_json_minimap.pdf
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

#scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/paramhists/plot*pdf .
#mv plot.pref.pdf plot_pref.pdf
#mv plot.indx.pdf plot_indx.pdf

