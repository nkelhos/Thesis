#!/usr/bin/env python
from datetime import timedelta
import veripy
runlist = veripy.read_runlist( 'disabledpixel.crab.runlist' )
db = veripy.VeritasDB()

obstime = timedelta(seconds=0)
for run in runlist :
  iqual = db.runqual.run2ind(run)
  obstime += db.runqual.run_usable_dur[iqual]
  
print('runlist has %.1f usable hours of data' % ( obstime.seconds / 3600.0 ) )
