#!/usr/bin/env bash

rm *.{png,eps,pdf}

#scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/crab_test/plots/*png .
#scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/crab_test/plots/*pdf .
#scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/crab_test/replot/*pdf .
scp nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/crab_test/refined_analysis/output/*nfits165*pdf .


for f in `ls -1 *pdf` ; do
  echo $f
  EPS=${f%.*}
  EPS=$(echo $EPS | tr '.-' '_')
  EPS="${EPS}.pdf"
  echo "-> $EPS"
  #convert $f $EPS
  mv "$f" "$EPS"
done

fff=(
plot_elev27_5_32_5deg_4_70TeV_nfits165_profa_skymap.pdf
plot_elev27_5_32_5deg_4_70TeV_nfits165_profl_skymap.pdf
plot_elev27_5_32_5deg_4_70TeV_nfits165_profb_skymap.pdf
plot_elev27_5_32_5deg_4_70TeV_nfits165_profe_skymap.pdf
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

#montage -mode concatenate -density 110 -border 10x10 -bordercolor White -tile x1 plot_elev27_5_32_5deg_4_70TeV_mapresiduals_coarse.pdf plot_elev27_5_32_5deg_4_70TeV_mapresiduals_fine.pdf crab_signif_joined.pdf

