
## Copyright(c) 2022 Andreia Hisi, Yoann Robin
## 
## This file is part of CDSupdate.
## 
## CDSupdate is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## CDSupdate is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with CDSupdate.  If not, see <https://www.gnu.org/licenses/>.

##############
## Packages ##
##############

import sys,os
import datetime as dt
import time as systime

import cdsapi

import numpy  as np
import xarray as xr

#############
## Imports ##
#############

from .__release    import version
from .__curses_doc import print_doc
from .__input      import read_input

from .__download import build_CDSAPIParams
from .__download import load_data_cdsapi

from .__convert import transform_data_format
from .__convert import build_encoding_daily


###############
## Functions ##
###############

def merge_with_current_daily( logs , **kwargs ):##{{{
	## Build list of var
	## If tas, tasmin or tasmax in var, add the three
	l_var = kwargs["var"]
	if "tas" in l_var or "tasmin" in l_var or "tasmax" in l_var:
		l_var = l_var + ["tas","tasmin","tasmax"]
	l_var = list(set(l_var))
	
	for var in l_var:
		logs.write( f"Merge daily {var}" )
		
		## Path in
		pin = os.path.join( kwargs["tmp"] , var , "day" )
		
		## Path out
		pout = os.path.join( kwargs["odir"] , var , "day" )
		if not os.path.isdir(pout): os.makedirs(pout)
		
		## List of input files
		l_ifiles = [ os.path.join( pin , f ) for f in os.listdir(pin) ]
		l_ifiles.sort()
		
		## Split input in years
		d_ifiles = {}
		for f in l_ifiles:
			y = f.split("_")[-1][:4]
			d_ifiles[y] = f
		
		## List of current files
		l_cfiles = [ os.path.join( pout , f ) for f in os.listdir(pout) ]
		l_cfiles.sort()
		
		## Split current in years
		d_cfiles = {}
		for f in l_cfiles:
			y = f.split("_")[-1][:4]
			d_cfiles[y] = f
		
		
		## Now loop on years
		for y in d_ifiles:
			logs.write( f"   * '{y}'" )
			
			## Case 1: no values for the year y
			if y not in d_cfiles:
				logs.write( f"     Case 1: no values for the year {y}" )
				os.system( f"cp {d_ifiles[y]} {pout}" )
				continue
			
			## Load data
			idata = xr.open_dataset(d_ifiles[y])
			cdata = xr.open_dataset(d_cfiles[y])
			
			## Time axis
			itime = [ str(x)[:10] for x in idata.time.values ]
			ctime = [ str(x)[:10] for x in cdata.time.values ]
			
			## Time in ctime not in itime
			ntime = [ s for s in ctime if s not in itime ]
			
			## Case 2: all values must be updated
			if len(ntime) == 0:
				logs.write( f"     Case 2: all values must be updated" )
				os.remove(d_cfiles[y])
				os.system( f"cp {d_ifiles[y]} {pout}" )
				continue
			
			## Case 3: a sub part must be updated
			logs.write( f"     Case 3: a sub part must be updated" )
			odata = xr.concat( (idata,cdata.sel( time = ntime)) , dim = "time" , data_vars = "minimal" ).sortby("time")
			os.remove(d_cfiles[y])
			encoding = build_encoding_daily( var , odata.lat.size , odata.lon.size )
			t0   = str(odata.time.values[ 0])[:10].replace("-","")
			t1   = str(odata.time.values[-1])[:10].replace("-","")
			fout = f"ERA5_{var}_day_{kwargs['area_name']}_{t0}-{t1}.nc"
			odata.to_netcdf( os.path.join( pout , fout ) , encoding = encoding )
			
	logs.writeline()

##}}}

def merge_with_current( logs , **kwargs ):##{{{
	merge_with_current_daily( logs , **kwargs )
##}}}


def run_cdsupdate( logs , **kwargs ):##{{{
	"""
	CDSupdate.run_cdsupdate
	=======================
	
	Main execution, after the control of user input.
	
	"""
	
	## Start by extract years from period, to split in yearly task
	## Note: the last 30 days will be downloaded day by day
	##============================================================
	l_CDSAPIParams = build_CDSAPIParams( kwargs["period"] , logs )
	
	## Download data
	##==============
#	load_data_cdsapi( l_CDSAPIParams , logs , **kwargs )
	
	## Change data format
	##===================
#	transform_data_format( logs , **kwargs )
	
	## And now merge with current data
	##================================
	merge_with_current( logs , **kwargs )
	
##}}}

def start_cdsupdate( argv ):##{{{
	"""
	CDSupdate.start_cdsupdate
	=========================
	
	Starting point of 'cdsupdate'.
	
	"""
	## Time counter
	cputime0  = systime.process_time()
	walltime0 = dt.datetime.utcnow()
	
	## Future logs
	future_logs = []
	future_logs.append("LINE")
	future_logs.append( "Start: {}".format(str(walltime0)[:19] + " (UTC)") )
	future_logs.append("LINE")
	future_logs.append( f"CDSupdate version {version}" )
	future_logs.append("LINE")
	
	## Read input
	kwargs,logs,abort = read_input( argv , future_logs )
	
	## List of all input
	logs.write("Input parameters")
	keys = [key for key in kwargs]
	keys.sort()
	for key in keys:
		logs.write( "   * {:{fill}{align}{n}}".format( key , fill = " ",align = "<" , n = 10 ) + ": {}".format(kwargs[key]) )
	logs.writeline()
	
	## User asks help
	if kwargs["help"]:
		print_doc()
	
	## Go!
	if not abort:
		run_cdsupdate( logs , **kwargs )
	
	## End
	cputime1  = systime.process_time()
	walltime1 = dt.datetime.utcnow()
	logs.write( "End: {}".format(str(walltime1)[:19] + " (UTC)") )
	logs.write( "Wall time: {}".format(walltime1 - walltime0) )
	logs.write( "CPU time : {}".format(dt.timedelta(seconds = cputime1 - cputime0)) )
	logs.writeline()
##}}}

