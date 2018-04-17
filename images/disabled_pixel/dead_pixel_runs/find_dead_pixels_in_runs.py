#!/usr/bin/env python
import veripy, json, os
import pymysql.cursors

db = veripy.VeritasDB()

srcs = ['Crab', 'Sgr A*', 'Sgr A* Off']
pdfile = 'pixeldict.json'

with open( 'database.txt', 'a' ) as f :

  pixeldict = {}
  if os.path.exists( pdfile ) :
    with open( pdfile, 'r') as g :
      pixeldict = json.load(g)
  
  for src in srcs :
    csrc    = veripy.clean_source_name( src )
    runlist = veripy.get_veripy_dir() + '/thesis/runlists/thesis.%s.runlist'%csrc
    runs    = veripy.read_runlist( runlist )[:3]
    veripy.mkdir( csrc )
    
    for run in runs :
      runfile = csrc + '/%d.dat'%run
      #if run not in pixeldict.keys() :
      if not os.path.exists( runfile ) :
        pixeldict[run] = []
        
        rind    = db.runinfo.run2ind( run )
        dbalpha = db.runinfo.run_time_alpha[rind]
        dbomega = db.runinfo.run_time_omega[rind]
        print('%d %d %s %s' % ( rind, run, dbalpha, dbomega ) )
        
      
        runfilerows = []
        dburl = veripy.get_db_url()
        conn  = pymysql.connect( host=dburl.hostname, user='readonly', db='VERITAS')
        for tel in [0,1,2,3] :
          cur   = conn.cursor()
          cmd   = 'SELECT db_start_time, channel, voltage_meas, current_meas FROM tblHV_Telescope%d_Status WHERE db_start_time BETWEEN \'%s\' AND \'%s\'' % ( tel, dbalpha, dbomega )
          #print('  cmd:', cmd )
          cur.execute( (cmd) )
          nrows = 0
          for row in cur.fetchall() :
            #print('    row:',row)
            nrows += 1
            s = '%d %d %s %d %s %s' % ( run, tel+1, row[0], row[1], row[2], row[3] )
            #f.write( s + '\n' )
            runfilerows += [ s ]
            pixeldict[run] += [ tel+1, str(row[0]), row[1], row[2], row[3] ]
          print('  run %d tel %d has %d rows...' % ( run, tel+1, nrows ) )
        
        with open( runfile, 'w' ) as g :
          for r in runfilerows :
            g.write( r + '\n' )
  
  with open( pdfile , 'w' ) as g :
    json.dump( pixeldict, g )

