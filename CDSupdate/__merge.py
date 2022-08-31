
## Copyright(c) 2022 Yoann Robin
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

from .__convert import build_encoding_daily
from .__convert import build_encoding_hourly


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
		pin = os.path.join( kwargs["tmp"] , "day" , var )
		
		## Path out
		pout = os.path.join( kwargs["odir"] , "day" , var )
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

def merge_with_current_hourly( logs , **kwargs ):##{{{
	## Build list of var
	## If tas, tasmin or tasmax in var, add the three
	l_var = kwargs["var"]
	l_var = list(set(l_var))
	
	for var in l_var:
		logs.write( f"Merge hourly {var}" )
		
		## Path in
		pin = os.path.join( kwargs["tmp"] , "hour" , var )
		
		## Path out
		pout = os.path.join( kwargs["odir"] , "hour" , var )
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
			itime = [ str(x)[:13] for x in idata.time.values ]
			ctime = [ str(x)[:13] for x in cdata.time.values ]
			
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
			encoding = build_encoding_hourly( var , odata.lat.size , odata.lon.size )
			t0   = str(odata.time.values[ 0])[:13].replace("-","").replace("T","")
			t1   = str(odata.time.values[-1])[:13].replace("-","").replace("T","")
			fout = f"ERA5_{var}_hour_{kwargs['area_name']}_{t0}-{t1}.nc"
			odata.to_netcdf( os.path.join( pout , fout ) , encoding = encoding )
			
	logs.writeline()

##}}}

def merge_with_current( logs , **kwargs ):##{{{
	merge_with_current_daily( logs , **kwargs )
	if kwargs["keep_hourly"]:
		merge_with_current_hourly( logs , **kwargs )
##}}}

