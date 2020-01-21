import math, numpy, scipy, sys
from gammalib import GEnergy, GSkyDir, deg2rad, rad2deg, twopi
from gammalib import GCTAObservation, GCTAResponseIrf
from veripy import obs2ontime, background_profile, plot_fits_background_grid
from astropy.io import fits
import matplotlib.pyplot as plt

def background2fits_prototype( data, fname ) :
  """Prototype function for writing a 3D background to a fits file.
    
    **Args:**
      data : dict, containing columns and detx/dety/energy background cube
      fname : str, output filename to write fits file to
  """
  print()
  print('Warning, this is a prototype function!')
  print()
    
  # figure out basics of the fits table
  ndetx   = len( data['DETX_LO'] )
  ndety   = len( data['DETY_LO'] )
  nenez   = len( data['BGD'    ] )
  formx   = '%dE' % ndetx
  formz   = '%dE' % nenez
  formxyz = '%dE' % ( ndetx * ndety * nenez )
  bgddim  = '(%d,%d,%d)' % ( ndetx, ndety, nenez ) 
  
  # setup table columns
  cols = []
  for key in [ 'DETX_LO', 'DETX_HI', 'DETY_LO', 'DETY_HI' ] :
    cols.append( fits.Column( name=key , format=formx  , unit='deg'       , array=[ data[key] ]             ) )
  for key in [ 'ENERG_LO', 'ENERG_HI' ] :
    encol = [ en.TeV() for en in data[key] ] # convert from list of GEnergy's to list of TeV floats
    cols.append( fits.Column( name=key , format=formz  , unit='TeV'       , array=[ encol     ]             ) )
  for key in [ 'BGD' ] :
    cols.append( fits.Column( name=key , format=formxyz, unit='1/s/MeV/sr', array=[ data[key] ], dim=bgddim ) )

  # setup fits table
  tablehdu      = fits.BinTableHDU.from_columns( cols )
  
  # name the table and make sure the dimensionality of the BGD column is set correctly
  tablehdu.name = 'BACKGROUND'
  tablehdu.header.set( 'TDIM7', bgddim )
  tablehdu.header.set( 'TDIM8', bgddim )
  
  # write table to file
  print('writing fits table to %s' % fname)
  tablehdu.writeto( fname, clobber=True)

def write_archive_radial_smart2( obs, fname, enbins=[0.085,300], fine_energy_hist='', profile_plot_format='', bkg_profile_plot='', bkg_grid_plot='', tmp_dir='', perturb=False, seed=12 ) :
    """Create a ctools background from the input obs, and save it as a fits file to fname.
    
    **Args:**
      obs   : GObservations object containing event list to use
      fname : str, output fits filename
    
    **Opts:**
      enbins              : [float,float], min and max energy, TeV
      fine_energy_hist    : str, output file path for energy histogram used in 
                            scaling radial profiles
      profile_plot_format : str, output filename format, must have '%d' 
                            somewhere in it
      bkg_profile_plot    : str, background vs energy plot filename
      bkg_grid_plot       : str, grid of detx/y background plots
      perturb             : bool, if true, randomly vary bins via poissonian errors
      seed                : int, random seed to use if perturb is True
    """

    # number of radial bins for building the initial radial background histogram
    nradbins = 47

    # outer radius for building initial radial background histogram
    maxrad = 3.0

    # number of bins in each camera axis of the fits 2D background
    nbkgbins = 80

    # number of extra 'empty' maps to add above and below the existing backgrounds
    nenergybordermaps = 3

    # width in energy space of border maps, in log10(TeV) space
    energyborderwidth = 0.2

    # counts/s/sr/MeV value to use at the edge of the camera and energy range
    bordervalue = 1e-13

    # aim for at least this many events per deg2 for each energy bin
    min_population = 150

    # number of bins near the camera center to combine, since their low solid angle tends to
    # cause larger fluctuations in the number of events
    nradbincombine = 2

    # divide up energy range into this many fine energy bins, for use with templates
    nenfine = 65

    # extra factor (so the likelihood doesn't have to travel so far)
    xfactor = 6.51e-3

    # calculate binning and number of events required per spatial template energy bin
    raddelta = maxrad / nradbins
    def offset2radbin( offset ) :
      return int( offset / raddelta )
    enmin, enmax = sorted(enbins)
    camera_area = math.pi * pow(maxrad,2)
    pop_thresh  = int( min_population * camera_area ) # minimum number of events needed 
    print('population threshold:',pop_thresh)
    
    # find median energy among all events
    enlist = []
    for run in obs :
      for ev in run.events() :
        en = ev.energy().TeV()
        if en > enmin and en < enmax :
          enlist += [ en ]
    enlist = sorted(enlist)
    median_pos    = len(enlist)//2
    median_energy = enlist[ median_pos ]
    print('median is %.2f TeV at %d' % ( median_energy, median_pos ) )
    if len(enlist) < pop_thresh :
      raise RuntimeError('only %d total events available, need at least %d to reach required population threshold of %d events/deg2...' % (len(enlist), pop_thresh, min_population) ) 
    
    # expand energy binning upwards from the median energy
    enspec = []
    current_pos = median_pos
    while True :
      next_pos = current_pos + pop_thresh
      # gobble the next one too if we're over the edge of the list
      # if we didn't do this, we'd have a low energy bin without enough events to pass pop_thresh
      if next_pos + pop_thresh > len(enlist) :
        next_pos = len(enlist)-1
      tmp_emin = enlist[current_pos]
      tmp_emax = enlist[next_pos] if enlist[next_pos] < enmax else enmax
      enspec = enspec + [ [ GEnergy( tmp_emin, 'TeV') , GEnergy( tmp_emax, 'TeV' ) ] ]
      if next_pos == len(enlist)-1 : break
      current_pos = next_pos
    
    # expand energy binning downwards from the median energy
    current_pos = median_pos
    while True :
      next_pos = current_pos - pop_thresh
      # gobble the next one too if we're over the edge of the list
      # if we didn't do this, we'd have a low energy bin without enough events to pass pop_thresh
      if next_pos - pop_thresh < 0 :
        next_pos = 0
      tmp_emax = enlist[current_pos]
      tmp_emin = enlist[next_pos] if enlist[next_pos] > enmin else enmin
      enspec = [ [ GEnergy( tmp_emin, 'TeV' ), GEnergy( tmp_emax, 'TeV' ) ] ] + enspec
      if next_pos == 0 : break
      current_pos = next_pos
    
    # add indexes to the energy specifications
    for i in range(len(enspec)) :
      enspec[i] = [i] + enspec[i]
    print('enspec:')
    for es in enspec :
      print(es[0], '%.2f'%es[1].TeV(), '%.2f'%es[2].TeV() )
    print()
    
    center = GSkyDir()
    center.radec(0.0,0.0)
    bkgmaps = []
    delta   = 2*maxrad / nbkgbins # bin width in deg
    binarea = delta*delta * deg2rad * deg2rad # sr
    bintime = obs2ontime( obs )
    
    energ_lo, energ_hi = [], []
    detx_lo , detx_hi  = [], []
    dety_lo , dety_hi  = [], []
    for ix in range(nbkgbins) :
      lo = -maxrad + (  ix   *delta )
      hi = -maxrad + ( (ix+1)*delta )
      detx_lo += [ lo ]
      detx_hi += [ hi ]
      dety_lo += [ lo ]
      dety_hi += [ hi ]
    
    # radial interpolation functions and the energies over which they should be used
    rad_interp_funcs = []
    
    for ien, en_min, en_max in enspec :
      radbins    = [ 0 for i in range(nradbins) ]
      binenergy  = en_max.MeV() - en_min.MeV()
      bin_volume = binenergy * binarea * bintime
      
      if perturb :
        # 2d histogram with fine binning
        numpy.random.seed(seed)
        nfine    = 137 # number of bins in each dimension
        finelim  = 3.0 # deg span
        twodhist = [ [ 0 ] * nfine for i in range(nfine) ]
        minlim   = -1 * finelim
        limwid   = 2 * finelim
        binwid   = limwid / nfine
        def val2index(  val   ) : return int( ( val - minlim ) / binwid )
        def index2cent( index ) : return ( ( index + 0.5 ) * binwid ) + minlim
        for run in obs :
          for ev in run.events() :
            en = ev.energy()
            if en > en_min and en <= en_max :
              dx = ev.dir().detx() * rad2deg
              dy = ev.dir().dety() * rad2deg
              ix = val2index( dx )
              iy = val2index( dy )
              twodhist[ix][iy] += 1
              print('twodhistfill : ix iy %3d %3d : dx dy %6.3f %6.3f'%(ix,iy,dx,dy))
        
        # show
        for ix in range(nfine) :
          dx = index2cent( ix )
          for iy in range(nfine) :
            dy     = index2cent( iy )
            if twodhist[ix][iy] > 0 :
              print('twodhistprint : ix iy %3d %3d : dx dy %6.3f %6.3f : twodhist %2d'%(ix,iy,dx,dy,twodhist[ix][iy]))
        
        # randomly perturb via poissonian statistics
        for ix in range(nfine) :
          dx = index2cent( ix )
          for iy in range(nfine) :
            dy     = index2cent( iy )
            twodhist[ix][iy] = numpy.random.poisson( lam=twodhist[ix][iy] )
            if twodhist[ix][iy] > 0 :
              print('twodhistperturb : ix iy %3d %3d : dx dy %6.3f %6.3f : twodhist %.3f'%(ix,iy,dx,dy,twodhist[ix][iy]))
        
        # rebin radially
        for ix in range( nfine ) :
          dx = index2cent( ix )
          for iy in range( nfine ) :
            dy     = index2cent( iy )
            detdir = GSkyDir()
            detdir.radec( dx*deg2rad, dy*deg2rad )
            offset = center.dist( detdir ) * rad2deg
            print('ix iy %d %d : dx dy %.3f %.3f : offset %.3f' % ( ix, iy, dx, dy, offset ) )
            if offset > finelim : continue
            rbin   = offset2radbin( offset )
            print('twodhist rebin ix iy %3d %3d : dx dy %.2f %.2f : offset %.3f : rbin %d'%(ix,iy,dx,dy,offset,rbin))
            radbins[rbin] += twodhist[ix][iy]
      
      else :
        # else radially bin events like normal
        for run in obs :
          for ev in run.events() :
            en = ev.energy()
            if en > en_min and en <= en_max :
              detx   = ev.dir().detx()
              dety   = ev.dir().dety()
              detdir = GSkyDir()
              detdir.radec( detx, dety )
              offset = center.dist( detdir ) * rad2deg
              rbin   = offset2radbin( offset )
              radbins[rbin] += 1
      
      #for i in range(
      #print(
    
      # calculate the average # events per bin area
      radbinavgs = [0 for i in range(len(radbins)) ]
      yerr       = [0 for i in range(len(radbins)) ]
      time, signal = [], []
      for i, r in enumerate(radbins) :
        
        # if requested, merge the first nradbincombine bins to help them stabilize
        # (the bins close to the camera center tend to fluctuate due to low statistics)
        if i < nradbincombine :
          rcombine      = sum( radbins[:nradbincombine] )
          rcombine_area = math.pi * pow( nradbincombine*raddelta ,2)
          radbinavgs[i] = rcombine / rcombine_area
          yerr[i]       = math.sqrt( rcombine )
        else :
          # otherwise just take the bin's counts / area
          area          = math.pi * ( pow((i+1)*raddelta,2) - pow(i*raddelta,2) )
          if radbins[i] == 0 :
            radbinavgs[i] = bordervalue
          else :
            radbinavgs[i] = radbins[i] / area
          yerr[i]       = math.sqrt( radbins[i] )
          if radbins[i] > 0 :
            time.append(   (i+0.5)*raddelta )
            signal.append( radbinavgs[i] )
      
      # find center of first bin with zero events
      zerorad = maxrad
      for i, r in enumerate(radbins) :
        rcenter = (i+0.5) * raddelta
        # if this bin and all later bins have zero events,
        # this is the radius at which we start zeroing-out background values
        # otherwise the interpolation function bounces around a bit, causing weird values
        if sum(radbins[i:]) == 0 :
          zerorad = rcenter
          break
      print()
      print('zero radius : %.2f deg' % zerorad )
      print('ien:%d : %d events : %d events/deg2' % (ien, sum(radbins), sum(radbins)/(math.pi*pow(maxrad,2)) ) )
      for i, r in enumerate( radbinavgs ) :
        print('  r%2d: %4.2f : %4d : %6.1e : %4.1e' % ( i, i*raddelta, radbins[i], r, yerr[i] ) )
      print()
      
      # fit a polynomial to this curve
      x  = numpy.array( [ (i+0.5)*raddelta for i in range(len(radbins)) ] )
      y  = numpy.array( radbinavgs )
      ye = numpy.array( yerr )
      # since the bins are radial, the radius=0 bin edge should have a derivative of zero
      # so we repeate the radius=0 bin counts for a few more points to force the interpolation
      # to weight that effect more
      for i in range(4) :
        x  = numpy.insert( x , 0, x[0] - raddelta, axis=0 )
        y  = numpy.insert( y , 0, y[0]           , axis=0 )
        ye = numpy.insert( ye, 0, ye[0]          , axis=0 )
      for i in range(6) :
        x  = numpy.append( x , x[ -1] + raddelta )
        y  = numpy.append( y , y[ -1]            )
        ye = numpy.append( ye, ye[-1]            )
      
      # interpolate from our points
      # the 'kind' kwarg indicates the interpolation mode
      # kind=3 :  uses an interpolating spline with a minimum sum-of-squares discontinuity in the 3rd derivative
      interpf6 = scipy.interpolate.interp1d( x, y, kind=3, axis=-1, copy=True, bounds_error=False )
      
      x2 = numpy.linspace( -0.75, maxrad*1.2, 200 )
      y6 = numpy.array( [ interpf6( i )  for i in x2 ] )
      
      # interpolate the radial bins
      coefs = numpy.polynomial.polynomial.polyfit( x, y,4)
      ffit  = numpy.polynomial.polynomial.polyval( x2, coefs )
      if len(profile_plot_format) > 0 :
        fig   = plt.figure()
        ax1   = fig.add_subplot(111)
        ax1.errorbar( x, y, yerr=ye, fmt='o', linewidth=3, capsize=4, elinewidth=3, markeredgewidth=3, label='Observed Events' )
        lines = ax1.plot( x2, y6, color='purple', linewidth=3, label='Interpolated Curve' )
        plt.title( 'Events/degrees${}^{2}$ in Radial Bins (%.2f - %.2f TeV)' % ( en_min.TeV(), en_max.TeV() ), fontsize=15 )
        plt.xlabel(r'Angular Distance from Camera Center (${}^{\circ}$)', fontsize=15)
        plt.ylabel('Events/degree${}^{2}$', fontsize=15)
        #plt.setp( lines, color='purple', linewidth=3 )
        plt.legend( loc='upper right', prop={'size':15}, numpoints=1 )
        plt.tick_params(axis='both', which='major', labelsize=15)
        plt.savefig( profile_plot_format % ien, dpi=150)
        plt.close( fig )
      
      # add our interpolation function to the list of radial profiles
      rad_interp_funcs += [ [en_min, en_max, interpf6, zerorad] ]
    
    
    # log10 mean of a list of GEnergy objects
    def en_lmean( enlist ) :
      entotal = sum( [ en.log10TeV() for en in enlist ] )
      return GEnergy( pow( 10, entotal/len(enlist) ), 'TeV' )
    
    # fine energy bin specifications
    e_log_min   = math.log10(enmin)
    e_log_max   = math.log10(enmax)
    e_log_delta = ( math.log10( enmax ) - e_log_min ) / nenfine

    # figure out how many events are in each fine energy bin
    n_events_fine = [ 0 for i in range(nenfine) ]
    for run in obs :
      for ev in run.events() :
        enlog = ev.energy().log10TeV()
        ibin  = int( ( enlog - e_log_min ) / e_log_delta )
        if ibin >= 0 and ibin < nenfine :
          n_events_fine[ibin] += 1
    
    print()
    print('energy histogram')
    for i in range(nenfine) :
      en = pow(10, e_log_min + i*e_log_delta )
      print('  %.2f TeV - %d' % ( en, n_events_fine[i] ) )
    print()
    
    if len(fine_energy_hist) > 0 :
      
      # figure out x limits
      xmin_i, xmax_i = -1, -1
      for i in range(nenfine) :
        xmin_i = i
        if n_events_fine[i] > 0 : break
      print()
      print('calculating xmax_i:')
      for i in reversed(range(nenfine)) :
        xmax_i = i
        print('  i:%2d  xmax:%.3f'%(i, e_log_min + ((xmax_i+1)*e_log_delta) ) )
        if n_events_fine[i] > 0 : 
          print('  break!')
          break
      xmin = e_log_min + ((xmin_i-1)*e_log_delta) # with buffer of 1 bin width
      xmax = e_log_min + ((xmax_i+2)*e_log_delta) # with buffer of 1 bin width
      print()
      print('Fine Energy Histogram')
      print('xmin', xmin)
      print('xmin_i',xmin_i)
      print('xmax', xmax)
      print('xmax_i',xmax_i)
      print()
      
      # construct the plot
      fig = plt.figure( figsize=[11,9] )
      lowedges = [ e_log_min + i*e_log_delta for i in range(nenfine) ]
      plt.bar( lowedges, n_events_fine, width=e_log_delta )
      plt.title('Events in Fine Energy Bins', fontsize=20)
      #plt.xscale('log')
      plt.yscale('log')
      plt.xlabel('Energy log10(TeV)', fontsize=15 )
      plt.ylabel('# Events', fontsize=15)
      plt.tick_params(axis='both', which='major', labelsize=15)
      plt.xlim([xmin,xmax])
      fig.tight_layout()
      plt.savefig( fine_energy_hist, dpi=100 )
      plt.close(fig)
    
    bin_solid_angle = pow( delta * deg2rad , 2 )
    bin_time = obs2ontime( obs )
    
    print('r= 0.0,  0.5,  1.0')
    bkgmaps  = []
    energ_hi = []
    energ_lo = []
    # loop over fine energy bins
    for ifine in range(nenfine) :
      ef_min   = GEnergy( pow( 10, e_log_min +  ifine   *e_log_delta) , 'TeV' )
      ef_max   = GEnergy( pow( 10, e_log_min + (ifine+1)*e_log_delta) , 'TeV' )
      ef_lmean = en_lmean( [ ef_min, ef_max ] )
      
      # figure out which unnormalized radial profile to use for this fine energy bin
      rad_interp_mean_en = [ en_lmean( [ b[0], b[1] ] ) for b in rad_interp_funcs ]
      if ef_lmean < min(rad_interp_mean_en) :
        # if we're below the lowest radial profile's mean energy, just use it (no interpolation)
        igross       = 0
        igross_lmean = en_lmean( [ rad_interp_funcs[igross][0], rad_interp_funcs[igross][1] ]  )
        zerorad      = rad_interp_funcs[igross][3]
        def prof_unnorm(rad) :
          return rad_interp_funcs[igross][2](rad) if rad < zerorad else 0.0 
        #print('for fine bin %2d %6.2f TeV : using %6.2f TeV Radial Profile (#%d)' % ( ifine, ef_lmean.TeV(), igross_lmean.TeV(), igross ) )
        
      elif ef_lmean > max(rad_interp_mean_en) :
        # if we're above the highest radial profile's mean energy, just use it (no interpolation)
        igross       = len(rad_interp_funcs)-1
        igross_lmean = en_lmean( [ rad_interp_funcs[igross][0], rad_interp_funcs[igross][1] ]  )
        zerorad      = rad_interp_funcs[igross][3]
        def prof_unnorm(rad) :
          return rad_interp_funcs[igross][2](rad) if rad < zerorad else 0.0
        #print('for fine bin %2d %6.2f TeV : using %6.2f TeV Radial Profile (#%d)' % ( ifine, ef_lmean.TeV(), igross_lmean.TeV(), igross ) )
        
      else :
        # pick the two closest (in energy) radial profiles and do a linear interpolation in log space
        rad_interp_indexes = []
        for i in range( len(rad_interp_mean_en)-1 ) :
          if ef_lmean > rad_interp_mean_en[i] and ef_lmean < rad_interp_mean_en[i+1] :
            rad_interp_indexes = [ i, i+1 ]
        if len(rad_interp_indexes) == 0 :
          raise RuntimeError( 'could not find two gross-energy-bins to interpolate radial profiles between, for fine energy bin at %.2f TeV...' % ef_lmean.TeV() )
        
        # setup the interpolation
        def prof_unnorm( rad ) :
          i1, i2 = rad_interp_indexes
          xx1 = en_lmean( rad_interp_funcs[i1][:2] ).log10TeV()
          xx2 = en_lmean( rad_interp_funcs[i2][:2] ).log10TeV()
          p1 = rad_interp_funcs[i1][2](rad) if rad < rad_interp_funcs[i1][3] else 0.0
          p2 = rad_interp_funcs[i2][2](rad) if rad < rad_interp_funcs[i2][3] else 0.0
          ptargetfunc = scipy.interpolate.interp1d( [xx1,xx2], [p1,p2], kind='linear', axis=-1, copy=True, bounds_error=False )
          return ptargetfunc( ef_lmean.log10TeV() )
        #i1, i2 = rad_interp_indexes
        #x1 = en_lmean( rad_interp_funcs[i1][:2] )
        #x2 = en_lmean( rad_interp_funcs[i2][:2] )
        #print('for fine bin %2d %6.2f TeV : interpolating between gross bins at %6.2f (#%d) and %6.2f TeV (#%d)' % ( ifine, ef_lmean.TeV(), x1.TeV(), i1, x2.TeV(), i2 ) )
          
      # normalize profile to one by integrating it in polar coordinates around the entire camera
      integ = scipy.integrate.quad( lambda x : x*prof_unnorm(x), 0, maxrad )
      #print('integral: ', integ )
      radnorm = twopi * integ[0]
      def prof(rad) : 
        p = prof_unnorm(rad)
        return p/radnorm if p > 0 else 0.0
      #total = twopi * scipy.integrate.quad( lambda r : r*prof(r), 0, maxrad )[0]
      print( '%6.2f TeV =  %5.3f  :  %5.3f  :  %5.3f  :  %5.3f  :  %9.7f' % ( ef_lmean.TeV(), prof(0.0), prof(0.5), prof(1.0), prof(1.5), prof(2.25) ) )
      
      # prepare to print radial profile to a 2D array
      bin_ewidth = ef_max.MeV() - ef_min.MeV()
      nfine      = n_events_fine[ifine]
      bin_volume = bin_solid_angle * bin_time * bin_ewidth
      enmap      = numpy.zeros((nbkgbins, nbkgbins)) 
      
      # loop over x and y bins in the 2D array
      for ix in range(nbkgbins) :
        xpos = -maxrad + (ix+0.5)*delta
        for iy in range(nbkgbins) :
          ypos   = -maxrad + (iy+0.5)*delta
          offset = math.sqrt( xpos*xpos + ypos*ypos )
          
          # scale profile by background counts and the bin's detx/dety/energy volume
          val = nfine * prof( offset ) * xfactor / bin_volume
          
          # add this background value to the counts map
          enmap[ix][iy] = val if val > 0.0 else bordervalue

      bkgmaps  += [ enmap  ]
      energ_lo += [ ef_min.TeV() ]
      energ_hi += [ ef_max.TeV() ]
      
    print()
      
    # figure out which maps are already border maps (they only have one unique element - the bordervalue)
    isborder = [ len(numpy.unique(m)) == 1 for m in bkgmaps ]
    
    # count how many border maps we already have (due to 0 events in some fine energy bins)
    nlowborder, nhighborder = 0, 0
    for i in range( len(bkgmaps) ) :
      if isborder[i] : nlowborder += 1
      else : break
    for i in reversed( range( len(bkgmaps) ) ) :
      if isborder[i] : nhighborder += 1
      else : break
    
    # if we need to add lower energy border maps, add them
    print('found %d lower energy border maps already in place...'  % nlowborder  )
    print('found %d higher energy border maps already in place...' % nhighborder )
    bordermap       = numpy.full( ( nbkgbins, nbkgbins ), bordervalue )
    if nlowborder < nenergybordermaps :
      print('so we\'re adding %d extra energy border maps to the low energy end' % (nenergybordermaps-nlowborder) )
      for i in range( nenergybordermaps - nlowborder ) :
        bkgmaps         = [bordermap] + bkgmaps
        down_energy_max = GEnergy( energ_lo[0], 'TeV' )
        down_energy_min = GEnergy( pow( 10, down_energy_max.log10TeV() - energyborderwidth ), 'TeV' )
        print('adding upper border map from %.2f-%.2f TeV...' % ( down_energy_min.TeV(), down_energy_max.TeV() ) )
        energ_lo = [ down_energy_min.TeV() ] + energ_lo
        energ_hi = [ down_energy_max.TeV() ] + energ_hi

    # or if we have have too many border maps, remove a few until we have nenergybordermaps
    elif nlowborder > nenergybordermaps :
      print('pruning %d excess energy border maps from the low energy end' % (nlowborder-nenergybordermaps) )
      for i in range( nlowborder - nenergybordermaps ) :
        del bkgmaps[ 0]
        del energ_lo[0]
        del energ_hi[0]
    
    # if we need to add more upper energy border maps, add them
    if nhighborder < nenergybordermaps :
      print('adding %d extra energy border maps to the high energy end' % (nenergybordermaps-nhighborder) )
      for i in range( nenergybordermaps - nhighborder ) :
        # add upper-energy border background
        bkgmaps += [ bordermap ]
        uppp_energy_min = GEnergy( energ_hi[-1], 'TeV' )
        uppp_energy_max = GEnergy( pow( 10, uppp_energy_min.log10TeV() + energyborderwidth ), 'TeV' )
        print('adding lower border map from %.2f-%.2f TeV...' % ( uppp_energy_min.TeV(), uppp_energy_max.TeV() ) )
        energ_lo += [ uppp_energy_min.TeV() ]
        energ_hi += [ uppp_energy_max.TeV() ]
      
    # or if we have have too many border maps, remove a few until we have nenergybordermaps
    elif nhighborder > nenergybordermaps :
      print('pruning %d excess energy border maps from the high energy end' % (nhighborder-nenergybordermaps) )
      for i in range( nhighborder - nenergybordermaps ) :
        del bkgmaps[ -1]
        del energ_lo[-1]
        del energ_hi[-1]
    
    
    # add our empty energy-border maps, so ctools interpolation behaves 
    # properly at the edges of the energy range
    while False :
      for i in range(nenergybordermaps) :
        
        # add lower-energy border background
        bordermap       = numpy.full( ( nbkgbins, nbkgbins ), bordervalue )
        bkgmaps         = [bordermap] + bkgmaps
        down_energy_max = GEnergy( energ_lo[0], 'TeV' )
        print('down_energy_max:', repr(down_energy_max) )
        down_energy_min = GEnergy( pow( 10, down_energy_max.log10TeV() - energyborderwidth ), 'TeV' )
        print('adding upper border map from %.2f-%.2f TeV...' % ( down_energy_min.TeV(), down_energy_max.TeV() ) )
        energ_lo = [ down_energy_min.TeV() ] + energ_lo
        energ_hi = [ down_energy_max.TeV() ] + energ_hi

        # add upper-energy border background
        bkgmaps += [ bordermap ]
        uppp_energy_min = GEnergy( energ_hi[-1], 'TeV' )
        uppp_energy_max = GEnergy( pow( 10, uppp_energy_min.log10TeV() + energyborderwidth ), 'TeV' )
        print('adding lower border map from %.2f-%.2f TeV...' % ( uppp_energy_min.TeV(), uppp_energy_max.TeV() ) )
        energ_lo += [ uppp_energy_min.TeV() ]
        energ_hi += [ uppp_energy_max.TeV() ]
    
    # write our background cube
    bkgdata = {}
    bkgdata['BGD'     ] = bkgmaps
    bkgdata['DETX_LO' ] = detx_lo
    bkgdata['DETX_HI' ] = detx_hi
    bkgdata['DETY_LO' ] = dety_lo
    bkgdata['DETY_HI' ] = dety_hi
    bkgdata['ENERG_LO'] = [ GEnergy( en, 'TeV' ) for en in energ_lo ]
    bkgdata['ENERG_HI'] = [ GEnergy( en, 'TeV' ) for en in energ_hi ]
    background2fits_prototype( bkgdata, fname )
    
    if len(bkg_profile_plot) > 0 or len(bkg_grid_plot) > 0 :
      run = GCTAObservation()
      rsp = GCTAResponseIrf()
      rsp.load_background( fname )
      run.response( rsp )
      if len(bkg_profile_plot) > 0 :
        background_profile( run, bkg_profile_plot )
      if len(bkg_grid_plot) > 0 :
        plot_fits_background_grid( run, bkg_grid_plot, temp_dir=tmp_dir )
    
    return

