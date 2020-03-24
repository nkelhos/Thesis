#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
from math import log10


fig = plt.figure( figsize=(10,5) )
ax  = fig.add_subplot(111)

def func(beta, gamma) :
  # returns probability P
  return pow( 10, (gamma+1) * log10( beta ) )
    
bmin = 1
bmax = 1.25
nbetas = 100
betaw = (bmax-bmin) / nbetas
betas = [ bmin + i * betaw for i in range(nbetas) ]

ProbGam15s = [ func(b,-1.5) for b in betas ]
ProbGam20s = [ func(b,-2.0) for b in betas ]
ProbGam25s = [ func(b,-2.5) for b in betas ]

fs = 20

plt.plot( betas, ProbGam15s, 'r-', label= r'$\gamma = -1.5$', linewidth=3 )
plt.plot( betas, ProbGam20s, 'g-', label= r'$\gamma = -2.0$', linewidth=3 )
plt.plot( betas, ProbGam25s, 'b-', label= r'$\gamma = -2.5$', linewidth=3 )
plt.plot( [1.1], [0.9], marker='^', color='orange' )
plt.text( 1.165, 0.965, r'$P=10^{ \left (\gamma + 1 \right ) \log_{10}{\beta}}$', fontsize=fs+5 )

plt.title( 'Spectral Index Contours', fontsize=fs )
plt.xlabel( r'$\beta$ : Fractional Energy Increase per Crossing Cycle', fontsize=fs-2 )
plt.ylabel(r'Return Probability $P$', fontsize=fs-2)
plt.tick_params(axis='both', which='major', labelsize=fs-5 )
legend = ax.legend( loc='lower left', shadow=True, prop={'size':fs-5})
f1 = 'spectral_index_contours.pdf'
fig.savefig( f1, bbox_inches='tight', dpi=300 )
plt.close(fig)


emin = 0.5 # TeV
emax = 10  # TeV
nenergies = 100
ewidth    = ( log10(emax) - log10(emin) ) / (nenergies-1)
energies  = [ pow( 10, log10(emin) + i*ewidth ) for i in range(nenergies) ]

def func( energy, gamma ) :
  return pow( energy, gamma )
dNdEGam15s = [ func( e, -1.5 ) for e in energies ]
dNdEGam20s = [ func( e, -2.0 ) for e in energies ]
dNdEGam25s = [ func( e, -2.5 ) for e in energies ]

fig = plt.figure( figsize=(10,5) )
ax  = fig.add_subplot(111)

plt.plot( energies, dNdEGam15s, 'r-', label= r'$\gamma = -1.5$', linewidth=3 )
plt.plot( energies, dNdEGam20s, 'g-', label= r'$\gamma = -2.0$', linewidth=3 )
plt.plot( energies, dNdEGam25s, 'b-', label= r'$\gamma = -2.5$', linewidth=3 )
plt.text( 3, 1, r'$\frac{dN}{dE} = \left ( \frac{E}{1\,\textrm{\LARGE TeV}} \right )^{\gamma} $', fontsize=fs+7 )

plt.title( 'Differential Spectra of Power Laws with Spectral Indicies', fontsize=fs )
plt.xlabel( r'Energy [TeV]', fontsize=fs-2 )
plt.ylabel(r'$\frac{dN}{dE}$', fontsize=fs-2)
plt.tick_params(axis='both', which='major', labelsize=fs-5 )
legend = ax.legend( loc='lower left', shadow=True, prop={'size':fs-5})
plt.xscale('log')
plt.yscale('log')
w = 0.025
ax.set_xlim([pow(10,log10(emin)-w), pow(10,log10(emax)+w) ] )
xt = [0.5, 0.7, 1,2,3,5,7,10]
ax.set_xticks( xt )
ax.set_xticklabels( [ str(x) for x in xt ] )
yt = [ 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3 ]
ax.set_yticks( yt )
ax.set_yticklabels( [ str(y) for y in yt ] )
f2 = 'differential_spectra.pdf'
fig.savefig( f2, bbox_inches='tight', dpi=300 )
plt.close(fig)


outf = 'merged_spectra.pdf'
cmd = 'montage -mode concatenate -gravity center -tile 1x2 %s %s %s' % (f1,f2,outf)
os.system(cmd)
#cmd = 'pdfcrop %s merged_spectra.pdf' % outf
#os.system(cmd)
