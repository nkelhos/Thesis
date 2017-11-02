#!/usr/bin/env python
import veripy, glob, json, re, numpy
import matplotlib.pyplot as plt
from gammalib import GEnergy

specfiles = glob.glob('logs/spec*json')
emin, emax = [ GEnergy(e,'TeV') for e in [4,70] ]

fig = plt.figure()
fax = fig.add_subplot(111)

xranges, yranges = [], []

for f in sorted(specfiles) :
  p      = re.search( 'spec\.([A-Za-z\-\+]+)\.([0-9.]+)(\w+)\.json' , f )
  branch = p.groups()[0]
  dmmass = GEnergy( float(p.groups()[1]), p.groups()[2] )
  blatex = veripy.clumpy_branch_latex(branch)
  
  with open(f,'r') as g :
    spec = json.load(g)
  
  x = [ ix * 1e-3 for ix in spec['energy']['data'] ]
  y = [ iy * 1e3  for iy in spec['dnde'  ]['data'] ]
  
  plt.plot( x, y, label=r'%s $\rightarrow %s$'%( str(dmmass), blatex ) )
  
  xranges += x
  yranges += y
  
  v = veripy.clumpy_integrate_single_int_spectrum_json( f, emin, emax, zero_guess=emax.GeV() )
  if isinstance(v,numpy.ndarray) :
    v = v[0]
  print('%-30s : 4-70TeV = %.3g' % ( f, v ) )
  

plt.title(  r'WIMP Single Annihilation Output $\gamma$ Spectra' )
plt.xlabel( r'Energy $log_{10}[GeV]$'    )
plt.ylabel( r'$\frac{dN}{dE} [GeV^{-1}]$')
plt.xscale('log')
plt.yscale('log')
plt.xlim([ min(xranges), max(xranges) ])
plt.ylim([ min(yranges), max(yranges) ])
legend = fax.legend( loc='lower left', shadow=True )
plt.savefig( 'logs/spectra.png', dpi=100 )
plt.clf()

