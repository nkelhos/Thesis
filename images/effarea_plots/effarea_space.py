#!/usr/bin/env python
import veripy, os

fname = 'VR78128.ReconMethodDisp.Cut-NTel2-ExtendedSource-Hard.chunk1.fits'

obs = veripy.load_obs_proper([fname])
for ext in ['pdf','png'] :
  pname = 'effarea_space.%s' % ext
  veripy.plot_effarea( obs[0], pname, title='Effective Area for Galactic Center Run 78128', show_events=True )



