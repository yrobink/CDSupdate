
## Copyright(c) 2023 Yoann Robin
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
import logging

import numpy  as np
import xarray as xr


#############
## Imports ##
#############

from .__CDSUParams import cdsuParams


##################
## Init logging ##
##################

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


###############
## Functions ##
###############

def build_tasmin():##{{{
	
	area_name = cdsuParams.area_name
	ipath  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , "tas" )
	ifiles = os.listdir(ipath)
	ifiles.sort()
	cvar = "tasmin"
	
	for ifile in ifiles:
		
		idata = xr.open_dataset( os.path.join( ipath , ifile ) )
		year  = idata.time.dt.year[0].values
		dtime = [dt.datetime(int(year),1,1) + dt.timedelta( days = int(i) - 1 ) for i in np.unique(idata.time.dt.dayofyear.values)]
		
		## Build daily variable
		ddata = idata.groupby("time.dayofyear").min().rename( dayofyear = "time" ).assign_coords( time = dtime ).rename( { "tas" : cvar } )
		
		## Save daily variable
		opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "day" , cvar )
		t0    = str(ddata.time[ 0].values)[:10].replace("-","").replace(" ","").replace("T","")
		t1    = str(ddata.time[-1].values)[:10].replace("-","").replace(" ","").replace("T","")
		ofile = f"ERA5-AMIP_{cvar}_day_{area_name}_{t0}-{t1}.nc"
		target = os.path.join( opath , ofile )
		if not os.path.isdir(opath):
			os.makedirs(opath)
		logger.info( f" * Save 'TMP/ERA5-AMIP/day/{cvar}/{ofile}'" )
		ddata.to_netcdf( os.path.join( opath , ofile ) )
##}}}

def build_tasmax():##{{{
	
	area_name = cdsuParams.area_name
	ipath  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , "tas" )
	ifiles = os.listdir(ipath)
	ifiles.sort()
	cvar = "tasmax"
	
	for ifile in ifiles:
		
		idata = xr.open_dataset( os.path.join( ipath , ifile ) )
		year  = idata.time.dt.year[0].values
		dtime = [dt.datetime(int(year),1,1) + dt.timedelta( days = int(i) - 1 ) for i in np.unique(idata.time.dt.dayofyear.values)]
		
		## Build daily variable
		ddata = idata.groupby("time.dayofyear").max().rename( dayofyear = "time" ).assign_coords( time = dtime ).rename( { "tas" : cvar } )
		
		## Save daily variable
		opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "day" , cvar )
		t0    = str(ddata.time[ 0].values)[:10].replace("-","").replace(" ","").replace("T","")
		t1    = str(ddata.time[-1].values)[:10].replace("-","").replace(" ","").replace("T","")
		ofile = f"ERA5-AMIP_{cvar}_day_{area_name}_{t0}-{t1}.nc"
		target = os.path.join( opath , ofile )
		if not os.path.isdir(opath):
			os.makedirs(opath)
		logger.info( f" * Save 'TMP/ERA5-AMIP/day/{cvar}/{ofile}'" )
		ddata.to_netcdf( os.path.join( opath , ofile ) )
##}}}

def build_sfcWind():##{{{
	area_name = cdsuParams.area_name
	
	## files
	ipathu  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , "uas" )
	ipathv  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , "vas" )
	ifilesu = os.listdir(ipathu)
	ifilesv = os.listdir(ipathv)
	ifilesu.sort()
	ifilesv.sort()
	
	for ifileu,ifilev in zip(ifilesu,ifilesv):
		
		idatau = xr.open_dataset( os.path.join( ipathu , ifileu ) )
		idatav = xr.open_dataset( os.path.join( ipathv , ifilev ) )
		
		year  = idatau.time.dt.year[0].values
		dtime = [dt.datetime(int(year),1,1) + dt.timedelta( days = int(i) - 1 ) for i in np.unique(idatau.time.dt.dayofyear.values)]
		
		## Build hourly sfcWind
		odatah = idatau.copy( deep = True ).rename( uas = "sfcWind" )
		odatah["sfcWind"] = np.sqrt( idatau["uas"]**2 + idatav["vas"]**2 )
		
		## Build daily
		odatad = odatah.groupby("time.dayofyear").mean().rename( dayofyear = "time" ).assign_coords( time = dtime )
		
		## Save hourly
		if cdsuParams.keep_hourly:
			opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , "sfcWind" )
			t0    = str(odatah.time[ 0].values)[:13].replace("-","").replace(" ","").replace("T","")
			t1    = str(odatah.time[-1].values)[:13].replace("-","").replace(" ","").replace("T","")
			ofile = f"ERA5-AMIP_sfcWind_hr_{area_name}_{t0}-{t1}.nc"
			target = os.path.join( opath , ofile )
			if not os.path.isdir(opath):
				os.makedirs(opath)
			logger.info( f" * Save 'TMP/ERA5-AMIP/hr/sfcWind/{ofile}'" )
			odatah.to_netcdf( os.path.join( opath , ofile ) )
		
		## Save daily
		opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "day" , "sfcWind" )
		t0    = str(odatad.time[ 0].values)[:10].replace("-","").replace(" ","").replace("T","")
		t1    = str(odatad.time[-1].values)[:10].replace("-","").replace(" ","").replace("T","")
		ofile = f"ERA5-AMIP_sfcWind_day_{area_name}_{t0}-{t1}.nc"
		target = os.path.join( opath , ofile )
		if not os.path.isdir(opath):
			os.makedirs(opath)
		logger.info( f" * Save 'TMP/ERA5-AMIP/day/sfcWind/{ofile}'" )
		odatad.to_netcdf( os.path.join( opath , ofile ) )
	
	cdsuParams.cvars.append("sfcWind")
##}}}

def build_EXTRA_cvars():##{{{
	
	cvars_cmp = cdsuParams.cvars_cmp
	for cvar in cvars_cmp:
		logger.info( f"Build EXTRA cvar '{cvar}'" )
		
		if cvar == "tasmin":
			build_tasmin()
		if cvar == "tasmax":
			build_tasmax()
		if cvar == "sfcWind":
			build_sfcWind()
	
##}}}


