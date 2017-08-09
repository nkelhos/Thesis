#!/usr/bin/env python
import veripy, sys, os, gammalib, shutil, re, glob, ctools, time
import datetime, gc
from io import StringIO
from os.path import join
from math import log10
from gammalib import GModelSpatialPointSource, GModelSpectralPlaw, GModelSpatialDiffuseMap, GModelSpectralFunc, GModelSky, GFilename, GEnergy, GModelSpectralExpPlaw
import matplotlib.pyplot  as plt
import matplotlib.patches as patches

emin , emax  =  4, 70   # TeV
elmin, elmax = 26, 30.5 # deg
dm_mass = GEnergy(10,'TeV')
span = 4 # deg

t1 = time.time()
clumpy = join( os.environ['CLUMPY'], 'bin', 'clumpy' )
db   = veripy.VeritasDB()
sgra = db.source2dir('Sgr A*')
fitsfiles = sorted( veripy.scan_for_fits_files( join( veripy.get_veripy_dir(), 'fits/sgra' ) ) )

def get_time() :
  return datetime.datetime.now()

statistics = []
statfile = 'logs/statistics.txt'
with open(statfile,'w') as f : f.write('')
def printstat(s) :
  t = get_time()
  print(t,s)
  statistics.append( s )
  with open(statfile,'a') as f :
    f.write('%-28s %s\n' % ( t, s ) )

printstat( 'found %d fits files' % len(fitsfiles) )
fitsfiles = fitsfiles[140:160]

t3 = time.time()
obs_allelev = veripy.load_obs_proper( fitsfiles, bkg='powerlaw' )
print('%-26s done loading files' % ( get_time() ) )
printstat( 'loaded %d fits files' % len(fitsfiles) )
t4 = time.time()
printstat( '%.1f seconds to load fits files' % ( t4-t3 ) )
printstat( '(%.1f seconds per fits file)' % ( (t4-t3)/len(fitsfiles) ) )
nevents = sum( [ len(ob.events()) for ob in obs_allelev ] )
printstat('%d events before cuts' % nevents )
printstat( 'Ontime before pelev cuts: %.2f min' % ( sum([ ob.ontime() for ob in obs_allelev])/60.0) )
obs_elev  = db.select_pointing_elevation( obs_allelev, minelev=elmin, maxelev=elmax )
ontimemin = sum([ob.ontime() for ob in obs_elev]) / 60.0
printstat('Ontime after pelev cuts: %.2f min' % ontimemin )

obs, cutobs = veripy.obs_split( obs_elev, lambda ob: ob.ontime() > 60 )

printstat( 'Pruned Observations: %d' % len( cutobs ) )
printstat( 'Ontime after pruning obs < 60sec: %.2f min' % ( sum([ob.ontime() for ob in obs])/60.0 ) )
printstat( 'Livetime: %.2f min' % ( sum([ob.livetime() for ob in obs ])/60.0 ) )
printstat( 'Energies: %.0f - %.0f TeV' % ( emin, emax ) )

cutoff = GEnergy( 12, 'TeV' )
pivot  = GEnergy( pow(10, ( log10( min([emax,cutoff.TeV()]) ) + log10(emin) ) / 2.0 ), 'TeV' )
printstat( 'Pivot energy at %.2f TeV' % pivot.TeV() )
for m in obs.models() :
  m.spectral()['Index'].free()
  m.spectral()['Index'].value( 0.0 )
  m.spectral()['Prefactor'].value(1.0)
  m.spectral()['Prefactor'].free()
  m.spectral()['Prefactor'].min( 1e-2 )
  m.spectral()['PivotEnergy'].value(pivot.MeV())
  m.spectral()['PivotEnergy'].fix()

###################
# GC POINT SOURCE #
###################
srcname = 'sgra'
sgra_model = srcname
add_gc_pointsource = True
if add_gc_pointsource :
  spatial = GModelSpatialPointSource(sgra)
  spatial['RA' ].fix()
  spatial['DEC'].fix()
  #spectral = GModelSpectralPlaw()
  #spectral['Prefactor'  ].value( 3.0e-22 ) # 10^2 smaller than crab
  #spectral['Prefactor'  ].scale( 1.0e-22 )
  #spectral['Prefactor'  ].free()
  #spectral['Prefactor'  ].min( 1e-30 )
  #spectral['PivotEnergy'].value( pivot.MeV() )
  #spectral['PivotEnergy'].fix()
  #spectral['Index'      ].value( -2.0 )
  #spectral['Index'      ].free()
  spectral = GModelSpectralExpPlaw()
  spectral['Prefactor'   ].value( 3e-22 )
  spectral['Prefactor'   ].scale( 1e-22 )
  spectral['Prefactor'   ].free()
  spectral['Prefactor'   ].min( 1e-30 )
  spectral['Index'       ].value( -2 )
  spectral['Index'       ].free()
  spectral['PivotEnergy' ].value( pivot.MeV() )
  spectral['PivotEnergy' ].fix()
  spectral['CutoffEnergy'].value( cutoff.MeV() )
  spectral['CutoffEnergy'].free()
  source = GModelSky( spatial, spectral )
  source.name( srcname )
  source.tscalc( True )
  print(source)
  obs.models().append( source )

tmp   = join( os.path.dirname(os.path.realpath(__file__)), 'logs', 'tmp' )
tmp_halo = join( tmp, 'halo_output' )
tmp_spec = join( tmp, 'spectrum_output' )
veripy.mkdir( tmp )
  
add_dm_halo = True
dmhalo = 'dmhalo'
dm_model = dmhalo
if add_dm_halo : 

  ###########
  # DM HALO #
  ###########
  shape = 'einasto'
  core  = 0.5   # kpc, from hess2015
  fov   = 10    # deg, square span of spatial map
  res   = 0.01 # deg, jfactor integration angle
  bran  = 'bbbar'

  cent  = gammalib.GSkyDir( sgra )
  halo_fits = 'logs/halo.fits'

  pcodes = {'bbbar':11}
  
  if not os.path.exists( halo_fits ) :

    try : 
      shutil.rmtree( tmp_halo )
    except FileNotFoundError :
      pass
    veripy.mkdir( tmp_halo )
      
    cmds  = [ clumpy ]
    cmds += [ '-g5'  ]
    cmds += [ '-D'   ]
    veripy.cmd_line( cmds, cwd=tmp, prefix='halo -D' )
      
    pfile_d = join( tmp, 'clumpy_params_g5.txt'  )
    pfile   = join( tmp, 'clumpy.halo.pfile.txt' )
    settings = {}
    settings['gPP_DM_IS_ANNIHIL_OR_DECAY'] = [ '[-]'  , '1'          ] # annihlating dm (not decaying)
    settings['gSIM_ALPHAINT_DEG'         ] = [ '[deg]', '%f'   % res ] # min halo integration angle
    settings['gSIM_THETA_ORTH_SIZE_DEG'  ] = [ '[deg]', '%.3f' % fov ] # 
    settings['gSIM_THETA_SIZE_DEG'       ] = [ '[deg]', '%.3f' % fov ]
    settings['gSIM_PSI_OBS_DEG'          ] = [ '[deg]', '0.0' ] # '%.4f' % cent.l_deg() ]
    settings['gSIM_THETA_OBS_DEG'        ] = [ '[deg]', '0.0' ] # '%.4f' % cent.b_deg() ]
    settings['gSIM_IS_WRITE_ROOTFILES'   ] = [ '[-]'  , '0' ]  # don't write root files
    settings['gMW_SUBS_N_INM1M2'         ] = [ '[-]'  , '0' ]  # don't add in subclumps
    settings['gSIM_OUTPUT_DIR'           ] = [ '[-]'  , tmp_halo ]

    if shape == 'einasto' :
      settings['gMW_TOT_FLAG_PROFILE'] = [ '[-]', 'kEINASTO' ]
    elif shape == 'nfw' :
      settings['gMW_TOT_FLAG_PROFILE'   ] = ['[-]', 'kZHAO' ]
      settings['gMW_TOT_SHAPE_PARAMS[0]'] = ['[-]', '1'     ] # alpha
      settings['gMW_TOT_SHAPE_PARAMS[1]'] = ['[-]', '3'     ] # beta
      settings['gMW_TOT_SHAPE_PARAMS[2]'] = ['[-]', '1'     ] # gamma

    veripy.clumpy_param_replacer( pfile_d, pfile, settings )

    cmds  = [ clumpy ]
    cmds += [ '-g5'  ]      # clumpy run mode
    cmds += [ '-i', pfile ] # use this parameter file
    cmds += [ '-p'   ]      # don't show root plot windows
    veripy.cmd_line( cmds, cwd='tmp', prefix='halo -i' )

    halo_fits_healpix = veripy.scan_for_fits_files( tmp_halo )[0]

    cmds  = [ 'python' ]
    cmds += [ join( os.environ['CLUMPY'], 'python_helperscripts', 'makeFitsImage.py' ) ]
    cmds += [ '-i', halo_fits_healpix ]
    veripy.cmd_line( cmds, cwd=tmp_halo, prefix='healpix2fits' )

    halo_fits_tmp = glob.glob( tmp_halo + '/annihil*JFACTOR*.fits' )[0]

    halo_fits_tmp2 = join( tmp_halo, 'halo2.fits' )
    veripy.recenter_halo_fits( halo_fits_tmp, sgra, halo_fits_tmp2 )

    shutil.copyfile( halo_fits_tmp2, halo_fits )
    
  
  printstat('halo_fits: ' + os.path.basename(halo_fits) )
  spatial = GModelSpatialDiffuseMap( halo_fits )
  spatial['Normalization'].fix()
  jfactor = veripy.read_halo_jfactor_fits( halo_fits )
  printstat(os.path.basename(halo_fits) + ' loaded into GModelSpatialDiffuseMap()' )

  amin,amax,anpts = 1e-2, 8, 80
  adelta_log = ( log10(amax) - log10(amin) ) / ( anpts - 1 )
  angs = [ pow( 10, log10(amin) + i*adelta_log ) for i in range(anpts) ]
  
  photon = gammalib.GPhoton()
  photon.energy( GEnergy(1,'TeV') )
  photon.time( gammalib.GTime(0,'sec') )
  svals = [[] for j in range(4) ]
  for j in range(4) :
    for i in range(anpts) :
      skydir = gammalib.GSkyDir()
      if   j == 0 : skydir.lb_deg( sgra.l_deg() + angs[i], sgra.b_deg() )
      elif j == 1 : skydir.lb_deg( sgra.l_deg() - angs[i], sgra.b_deg() )
      elif j == 2 : skydir.lb_deg( sgra.l_deg()          , sgra.b_deg() + angs[i] )
      elif j == 3 : skydir.lb_deg( sgra.l_deg()          , sgra.b_deg() - angs[i] )
      photon.dir( skydir )
      val = spatial.eval( photon )
      svals[j] += [ val ]
  
  fig = plt.figure()
  fax = fig.add_subplot(111)
  #for j in range(4) :
    #plt.plot( angs, svals[j], zorder=2 )
  
  avgsvals = [ ]
  for i in range(anpts) :
    avgsvals += [ sum( svals[j][i] for j in range(4) ) / 4 ]
  plt.plot( angs, avgsvals, label='Halo J Factor' )
  
  boxleft  = min( angs )
  boxright = span/2.0
  ymin = 10 / 2
  ymax = max(svals[0]) * 2
  c = 'lightblue'
  fax.add_patch( patches.Rectangle( (boxleft,ymin), boxright-boxleft, ymax-ymin, linewidth=0, facecolor=c, zorder=1, label='VERITAS observations radius' ) )
  
  plt.title('WIMP Halo: J-Factor' )
  plt.xlabel(r'Angle from Galactic Center $\left \{ {}^{\circ} \right \}$')
  plt.ylabel(r'??')
  plt.xscale('log')
  plt.yscale('log')
  plt.xlim([ amin, amax ])
  plt.ylim([ ymin, ymax ])
  legend = fax.legend( loc='lower left', shadow=True )
  
  plt.savefig('logs/halo.png', dpi=100 )
  plt.clf()
  
  

  # if any of the spectrum settings change, this file must be deleted
  spec_file = 'logs/spec.txt'
  if not os.path.exists( spec_file ) :
    
    try : 
      shutil.rmtree( tmp_spec )
    except FileNotFoundError :
      pass
    veripy.mkdir( tmp_spec )
    
    cmds  = [ clumpy ]
    cmds += [ '-z'   ]
    cmds += [ '-D'   ]
    veripy.cmd_line( cmds, cwd=tmp, prefix='spec -D' )

    pfile_s = join( tmp, 'clumpy_params_z.txt'   )
    pfile   = join( tmp, 'clumpy.spec.pfile.txt' )

    settings = {}
    # convert branching channel to the '0,0,0,0,1,0,0,0,0,0' code
    brcode = code = ','.join([ '1' if pcodes[bran] == i else '0' for i in range(28) ])
    settings['gPP_BR'                       ] = [ '[-]'     , brcode          ]
    settings['gPP_DM_ANNIHIL_DELTA'         ] = [ '[-]'     , '2'             ]
    settings['gPP_DM_ANNIHIL_SIGMAV_CM3PERS'] = [ '[cm^3/s]', '3e-26'         ]
    settings['gPP_DM_IS_ANNIHIL_OR_DECAY'   ] = [ '[-]'     , '1'             ]
    settings['gPP_DM_MASS_GEV'              ] = [ '[GeV]'   , '%.1f' % dm_mass.GeV() ] 
    settings['gPP_FLAG_SPECTRUMMODEL'       ] = [ '[-]'     , 'kCIRELLI11_EW' ]
    settings['gSIM_XPOWER'                  ] = [ '[-]'     , '0'             ]
    
    # go higher than the dm mass so ctools energy integration doesn't freak out
    settings['gSIM_FLUX_EMAX_GEV'           ] = [ '[GeV]'   , '%.1f' % (dm_mass.GeV()*4) ]
    
    settings['gSIM_OUTPUT_DIR'              ] = [ '[-]'     , tmp_spec        ]
    veripy.clumpy_param_replacer( pfile_s, pfile, settings )

    cmds  = [ clumpy ]
    cmds += [ '-z'   ]
    cmds += [ '-i', pfile ]
    cmds += [ '-p'   ]
    veripy.cmd_line( cmds, cwd=tmp_spec, prefix='spec -i' )

    spec_file_tmp = glob.glob(tmp_spec+'/spectra_*.txt')[0]

    # copy our spectrum file, removing any comment lines
    spec_file_clean = join( tmp, 'spec.txt' )
    with open( spec_file_tmp, 'r' ) as fin :
      with open( spec_file_clean, 'w' )  as fout :
        for l in fin.readlines() :
          l = l.rstrip()
          cl = veripy.remove_comment( l )
          if len(cl.split()) == 2 :
            fout.write( cl + '\n' )

    shutil.copyfile( spec_file_clean, spec_file )
  
  printstat( 'spectrum file: ' + os.path.basename( spec_file ) )
  spectral = GModelSpectralFunc( spec_file, 1.0 )
  spectral['Normalization'].fix()
  
  dm = GModelSky( spatial, spectral )
  dm.name( dmhalo )
  dm.tscalc( True )
  print(dm)
  obs.models().append( dm )
  
  ens, fluxes = [], []
  with open( spec_file, 'r' ) as f :
    h = [ l.rstrip().split() for l in f.readlines() ]
    j = [ l for l in h if len(l) > 0 ]
    ens, fluxes = zip( *j )
    ens    = [ float(en)   * 1e-6 for en   in ens    ] # convert MeV to TeV
    fluxes = [ float(flux) * 1e6  for flux in fluxes ] # convert MeV^-1 to TeV^1

  
  fig = plt.figure()
  fax = fig.add_subplot(111)
  ys   = [ fluxes[i] for i in range(len(fluxes)) if ens[i] < dm_mass.TeV() ]
  ymin = min( ys ) / 10
  ymax = max( ys ) * 10
  fax.plot( ens, fluxes, zorder=2 )
  plt.title(r'Gamma-Ray Annihilation Spectrum: $m_{\chi}$ = %s' % str(dm_mass) )
  plt.xlabel(r'Energy $\left \{ log_{10} \mathrm{TeV} \right \}$')
  plt.ylabel(r'$\frac{dN}{dE} \left \{ \frac{1}{s*cm^{2}*\mathrm{TeV}} \right \}$')
  plt.xscale('log')
  plt.yscale('log')
  plt.ylim([ymin, ymax])
  plt.savefig('logs/spec.png', dpi=100 )
  plt.clf()
    

halo_fits_tot_jfactor = veripy.read_halo_jfactor_fits( halo_fits )


print( get_time(), 'starting ctselect' )
t3 = time.time()
sel = ctools.ctselect( obs )
sel['usepnt' ] = True
sel['ra'     ] = sgra.ra_deg()  # 'NONE'
sel['dec'    ] = sgra.dec_deg() # 'NONE'
sel['rad'    ] = span/2 # 'NONE'
sel['tmin'   ] = 0.0
sel['tmax'   ] = 0.0
sel['emin'   ] = emin
sel['emax'   ] = emax
sel['logfile'] = 'logs/ctselect.log'
sel.logFileOpen()
sel.run()
sel.logFileClose()
t4 = time.time()
printstat( '%.1f seconds to run ctselect' % ( t4-t3 ) )

del obs
gc.collect()
obs = sel.obs()
printstat( '%d events after cuts' % ( sum( [ len(ob.events()) for ob in sel.obs() ] ) ) )

printstat( 'starting ctlike' )
t3 = time.time()
like = ctools.ctlike( obs )
like['chatter' ] = 4
like['debug'   ] = False
like['edisp'   ] = True
like['outmodel'] = 'logs/out.xml'
like['logfile' ] = 'logs/ctlike.log'
like.logFileOpen()
like.run()
like.logFileClose()
t4 = time.time()
printstat( '%.1f seconds to run ctlike' % ( t4-t3 ) )
del obs
gc.collect()
obs = like.obs()

for model in [ sgra_model, dm_model ] :
  
  if model in [ m.name() for m in obs.models() ] :
    
    m = obs.models()[model]
    params = [ m.spectral()[i].name() for i in range(m.spectral().size()) ]
    if 'Prefactor'     in params : printstat( '%s Prefactor: %.4g +/- %.4g ph/cm2/s/MeV'     % ( model, m['Prefactor'].value()    , m['Prefactor'].error()     ) )
    if 'Normalization' in params : printstat( '%s Normalization: %.4g +/- %.4g ph/cm2/s/MeV' % ( model, m['Normalization'].value(), m['Normalization'].error() ) )
    if 'Index'         in params : printstat( '%s Index: %.4f +/- %.4f'                      % ( model, m['Index'].value()        , m['Index'].error()         ) )
    if 'CutoffEnergy'  in params : printstat( '%s Cutoff Energy: %.4f TeV +/- %.4f'          % ( model, m['CutoffEnergy'].value() , m['CutoffEnergy'].error()  ) )
    if 'PivotEnergy'   in params : printstat( '%s Pivot Energy: %.4f TeV'                    % ( model, m['PivotEnergy'].value() * 1e-6 ) )
    printstat( '%s TS: %.2f' % (model, m.ts() ) )
  

xml = 'logs/models.xml'
obs.models().save( xml )

printstat( 'plotting counts skymap'  )
veripy.obs_skymap(       obs, sgra, 'logs/counts.png'   , show='', radius=span/2, pradius=40, title='GC Counts', extra_art=['Sgr A*'] )
printstat( 'plotting energy profile' )
veripy.energy_profile(   obs, sgra, 'logs/enprofile.png', show='', ebins_c=29, cspan=0.2, cbins=21, title='GC Energy Profile', observed='errorbar' )
printstat( 'spatial profile along l' )
veripy.spatial_profile(  obs, sgra, 'logs/sprof.l.png'  , show='', span=span, cbins=27, mscale=5, axis='l', title='GC Profile in L', observed='errorbar' )
printstat( 'spatial profile along b' )
veripy.spatial_profile(  obs, sgra, 'logs/sprof.b.png'  , show='', span=span, cbins=27, mscale=5, axis='b', title='GC Profile in B', observed='errorbar' )
printstat( 'events energy histogram' )
nevents = sum( [ len(ob.events()) for ob in obs ] )
veripy.energy_histogram( obs, sgra, 'logs/enhist.png'   , ebins=60, title='Energy Histogram - %d Events' % nevents )

printstat( 'pointing elevation minutes' )
runs = veripy.obs2runs( obs )
db.plot_elev_bins( runs, 'logs/pelev.png', elmin=elmin-0.5, elmax=elmax+0.5, nelbins=80 )

printstat('starting ctulimit')
eref = gammalib.GEnergy( 10, 'TeV' )
t3 = time.time()
ul = ctools.ctulimit( obs )
ul['srcname'   ] = dmhalo
ul['edisp'     ] = True
ul['confidence'] = 0.68
ul['eref'      ] = eref.TeV()  # reference energy for differential limit
ul['emin'      ] = emin
ul['emax'      ] = emax
ul['tol'       ] = 1e-5
ul['max_iter'  ] = 50
ul['sigma_min' ] = 0.0
ul['sigma_max' ] = 10.0
ul['debug'     ] = True
ul['chatter'   ] = 4
ul['logfile'   ] = 'logs/ctulimit.log'
ul.logFileOpen()
ul.run()
ul.logFileClose()
t4 = time.time()
printstat('%.1f seconds to run ctulimit' % ( t4-t3 ) )
printstat('%s ctulimit Differential flux limit %.2g ph/cm2/s/MeV at %g TeV'     % ( dmhalo, ul.diff_ulimit() , eref.TeV() ) )
printstat('%s ctulimit Integral flux limit     %.2g ph/cm2/s within %g-%g TeV'  % ( dmhalo, ul.flux_ulimit() , emin, emax ) )
printstat('%s ctulimit Energy flux limit       %.2g erg/cm2/s within %g-%g TeV' % ( dmhalo, ul.eflux_ulimit(), emin, emax ) )

t2 = time.time()
printstat( 'total runtime %.1f seconds' % (t2-t1) )

print()
print('statistics:')
for s in statistics :
  print('  ',s)
print()

shutil.copyfile( __file__, join( tmp, os.path.basename( __file__ ) ) )
shutil.copyfile( __file__, __file__+'.bak' )

