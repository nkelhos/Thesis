#!/usr/bin/env python
import veripy, os

fname = 'VR78128.ReconMethodDisp.Cut-NTel2-ExtendedSource-Hard.chunk1.fits'
pname = 'effarea_space.png'
ename = os.path.splitext(pname)[0] + '.eps'
obs = veripy.load_obs_proper([fname])
veripy.plot_effarea( obs[0], pname, title='Effective Area for Galactic Center Run 78128', show_events=True )
veripy.cmd_line([ 'convert', pname, ename ])


