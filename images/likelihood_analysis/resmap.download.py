#!/usr/bin/env python
import os
from subprocess import call

with open('tagtarget.txt','r') as f :
  tag = f.readlines()
tag = tag[0].rstrip()

for f in ['ALGOSIGNIFICANCE','ALGOSUBDIV','ALGOSUBDIVSQRT','ALGOSUB','phist.ALGOSIGNIFICANCE'] :
    if f.startswith('ALGO') : f = f + '.withobradius'
    targ = 'plot.%s.%s.resmap.png' % (tag, f)
    fpng = 'plot_resmap_%s.png' % f.lower()
    feps = os.path.splitext(fpng)[0].replace('.','_') + '.eps'
    call( ['scp','nkelhos@warp-zeuthen.desy.de:/afs/ifh.de/group/cta/scratch/nkelhos/dm_halo_testing/veripy/thesis/analysis/dm_plus_pnt/logs/%s'%targ, fpng ] )
    call( [ 'convert', fpng, feps ] )
    
