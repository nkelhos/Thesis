#!/usr/bin/env python
import veripy, os

fname = 'VR78128.ReconMethodDisp.Cut-NTel2-ExtendedSource-Hard.chunk1.fits'

obs = veripy.load_obs_proper([fname])
pname = 'effarea_space.pdf'
veripy.plot_effarea( obs[0], pname, title='Effective Area for Sgr A* Run 78128', show_events=True )



