#!/usr/bin/env python
import matplotlib.pyplot as plt
plt.rc( 'text', usetex=True )

plots = {}
plots['100 TeV' ] = 'dnde_CIRELLI11_EW_GAMMA_m100000_bbbar.txt'
plots['10 TeV'  ] = 'dnde_CIRELLI11_EW_GAMMA_m10000_bbbar.txt'
plots['1 TeV'   ] = 'dnde_CIRELLI11_EW_GAMMA_m1000_bbbar.txt'
plots['100 GeV' ] = 'dnde_CIRELLI11_EW_GAMMA_m100_bbbar.txt'
plots['10 GeV'  ] = 'dnde_CIRELLI11_EW_GAMMA_m10_bbbar.txt'

order = [ '100 TeV', '10 TeV', '1 TeV', '100 GeV', '10 GeV' ]

leg = []
for mass in order :
  fname = plots[mass]
  print('file: %s' % fname )
  leg += [ r'$\chi_{m}=%s$' % mass ]

  x, y = [], []
  with open( fname, 'r' ) as f :
    for line in f.readlines() :
      l = line.split('#')[0]
      l = l.rstrip()
      if len(l) > 0 :
        #print('line: %s' % repr(l) )
        vec = l.split()
        #print('vec: %s' % repr(vec) )
        xstr = vec[0]
        ystr = vec[1]
        #print('xstr, ystr: %s %s' % ( repr(xstr) , repr(ystr) ) )
        yval = float(ystr)
        xval = float(xstr) / 1e3 # switch from GeV to TeV
        if yval > 0.0 :
          x += [ xval ]
          y += [ yval ]

  plt.plot(x,y)
      
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'Photon Energy $Log_{10}(TeV)$')
plt.ylabel(r'$\frac{dN}{dE}$')
plt.legend( leg, loc='upper right' )
plt.title( r'$\chi\chi \rightarrow b\bar{b} \rightarrow \gamma\gamma$ Spectrum from Different Mass $\chi$' )
plt.savefig('bbbar_spectrum.png')

plt.clf()

plots = {}
plots['gamma'] = 'dnde_CIRELLI11_EW_GAMMA_m1000_gammagamma.txt'
plots['Z'    ] = 'dnde_CIRELLI11_EW_GAMMA_m1000_ZZ.txt'
plots['W'    ] = 'dnde_CIRELLI11_EW_GAMMA_m1000_W+W-.txt'
plots['h'    ] = 'dnde_CIRELLI11_EW_GAMMA_m1000_hh.txt'
plots['tau'  ] = 'dnde_CIRELLI11_EW_GAMMA_m1000_tautau.txt'
plots['b'    ] = 'dnde_CIRELLI11_EW_GAMMA_m1000_bbbar.txt'

channelnames = {}
channelnames['gamma'] = r'\gamma\gamma'
channelnames['Z'    ] = r'ZZ \rightarrow \gamma\gamma'
channelnames['W'    ] = r'W^{+}W^{-} \rightarrow \gamma\gamma'
channelnames['h'    ] = r'hh \rightarrow \gamma\gamma'
channelnames['tau'  ] = r'\tau\bar{\tau} \rightarrow \gamma\gamma'
channelnames['b'    ] = r'b\bar{b} \rightarrow \gamma\gamma'

order = [ 'gamma', 'Z', 'W', 'h', 'tau', 'b' ]
leg = []
for channel in order :
  fname = plots[channel]
  channelname = channelnames[channel]
  print('file: %s' % fname )

  x, y = [], []
  with open( fname, 'r' ) as f :
    for line in f.readlines() :
      l = line.split('#')[0]
      l = l.rstrip()
      if len(l) > 0 :
        #print('line: %s' % repr(l) )
        vec = l.split()
        #print('vec: %s' % repr(vec) )
        xstr = vec[0]
        ystr = vec[1]
        #print('xstr, ystr: %s %s' % ( repr(xstr) , repr(ystr) ) )
        yval = float(ystr)
        xval = float(xstr) / 1e3 # switch from GeV to TeV
        if yval > 0.0 :
          x += [ xval ]
          y += [ yval ]

  plt.plot(x,y)
  leg += [ r'$\chi\chi \rightarrow %s $' % channelname ]

plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'Photon Energy $Log_{10}(TeV)$')
plt.ylabel(r'$\frac{dN}{dE}$ (\# photons per interaction)')
plt.legend( leg, loc='upper right' )
plt.title( r'$\chi\chi \rightarrow ?? \rightarrow \gamma\gamma$ Photon Spectrum from Different Annihilation Channels ($\chi_{m} = 1 TeV$)' )
plt.savefig('channel_spectrum.png')
