
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
	
##}}}

def build_hurs():##{{{
	
	cvar = "hurs"
	area_name = cdsuParams.area_name
	
	## files
	ipathD  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , "dptas" )
	ipathT  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" ,   "tas" )
	ifilesD = os.listdir(ipathD)
	ifilesT = os.listdir(ipathT)
	ifilesD.sort()
	ifilesT.sort()
	
	for ifileD,ifileT in zip(ifilesD,ifilesT):
		
		idataD = xr.open_dataset( os.path.join( ipathD , ifileD ) )
		idataT = xr.open_dataset( os.path.join( ipathT , ifileT ) )
		
		year  = idataT.time.dt.year[0].values
		dtime = [dt.datetime(int(year),1,1) + dt.timedelta( days = int(i) - 1 ) for i in np.unique(idataD.time.dt.dayofyear.values)]
		
		## Build hourly hurs
		odatah = idataD.copy( deep = True ).rename( dptas = cvar )
		eD     = 6.1078 * np.exp( 17.1 * ( idataD["dptas"] - 273.15 ) / ( 235 + idataD["dptas"] - 273.15 ) )
		eT     = 6.1078 * np.exp( 17.1 * ( idataT[  "tas"] - 273.15 ) / ( 235 + idataT[  "tas"] - 273.15 ) )
		odatah[cvar] = eD / eT * 100
		
		## Build daily
		odatad = odatah.groupby("time.dayofyear").mean().rename( dayofyear = "time" ).assign_coords( time = dtime )
		
		## Save hourly
		opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , cvar )
		t0    = str(odatah.time[ 0].values)[:13].replace("-","").replace(" ","").replace("T","")
		t1    = str(odatah.time[-1].values)[:13].replace("-","").replace(" ","").replace("T","")
		ofile = f"ERA5-AMIP_{cvar}_hr_{area_name}_{t0}-{t1}.nc"
		target = os.path.join( opath , ofile )
		if not os.path.isdir(opath):
			os.makedirs(opath)
		logger.info( f" * Save 'TMP/ERA5-AMIP/hr/{cvar}/{ofile}'" )
		odatah.to_netcdf( os.path.join( opath , ofile ) )
		
		## Save daily
		opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "day" , cvar )
		t0    = str(odatad.time[ 0].values)[:10].replace("-","").replace(" ","").replace("T","")
		t1    = str(odatad.time[-1].values)[:10].replace("-","").replace(" ","").replace("T","")
		ofile = f"ERA5-AMIP_{cvar}_day_{area_name}_{t0}-{t1}.nc"
		target = os.path.join( opath , ofile )
		if not os.path.isdir(opath):
			os.makedirs(opath)
		logger.info( f" * Save 'TMP/ERA5-AMIP/day/{cvar}/{ofile}'" )
		odatad.to_netcdf( os.path.join( opath , ofile ) )
##}}}

def build_huss():##{{{
	
	cvar = "huss"
	area_name = cdsuParams.area_name
	
	## files
	ipathD  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , "dptas" )
	ipathP  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" ,    "ps" )
	ifilesD = os.listdir(ipathD)
	ifilesP = os.listdir(ipathP)
	ifilesD.sort()
	ifilesP.sort()
	
	for ifileD,ifileP in zip(ifilesD,ifilesP):
		
		idataD = xr.open_dataset( os.path.join( ipathD , ifileD ) )
		idataP = xr.open_dataset( os.path.join( ipathP , ifileP ) )
		
		year  = idataP.time.dt.year[0].values
		dtime = [dt.datetime(int(year),1,1) + dt.timedelta( days = int(i) - 1 ) for i in np.unique(idataP.time.dt.dayofyear.values)]
		
		## Build hourly huss
		odatah = idataD.copy( deep = True ).rename( dptas = cvar )
		rdry   = 287.0597
		rvap   = 461.5250
		a1     = 611.21
		a3     = 17.502
		a4     = 32.19
		T0     = 273.16
		
		E            = a1 * np.exp( a3 * ( idataD["dptas"] - T0 ) / ( idataD["dptas"] - a4 ) )
		odatah[cvar] = E * ( rdry / rvap ) / ( idataP["ps"] - ( E * ( 1 - rdry / rvap ) ) )
		
		## Build daily
		odatad = odatah.groupby("time.dayofyear").mean().rename( dayofyear = "time" ).assign_coords( time = dtime )
		
		## Save hourly
		opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , cvar )
		t0    = str(odatah.time[ 0].values)[:13].replace("-","").replace(" ","").replace("T","")
		t1    = str(odatah.time[-1].values)[:13].replace("-","").replace(" ","").replace("T","")
		ofile = f"ERA5-AMIP_{cvar}_hr_{area_name}_{t0}-{t1}.nc"
		target = os.path.join( opath , ofile )
		if not os.path.isdir(opath):
			os.makedirs(opath)
		logger.info( f" * Save 'TMP/ERA5-AMIP/hr/{cvar}/{ofile}'" )
		odatah.to_netcdf( os.path.join( opath , ofile ) )
		
		## Save daily
		opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "day" , cvar )
		t0    = str(odatad.time[ 0].values)[:10].replace("-","").replace(" ","").replace("T","")
		t1    = str(odatad.time[-1].values)[:10].replace("-","").replace(" ","").replace("T","")
		ofile = f"ERA5-AMIP_{cvar}_day_{area_name}_{t0}-{t1}.nc"
		target = os.path.join( opath , ofile )
		if not os.path.isdir(opath):
			os.makedirs(opath)
		logger.info( f" * Save 'TMP/ERA5-AMIP/day/{cvar}/{ofile}'" )
		odatad.to_netcdf( os.path.join( opath , ofile ) )
##}}}

def build_heatIndex():##{{{
	
	cvar = "heatIndex"
	area_name = cdsuParams.area_name
	
	## files
	cvar0   = "tas"
	ipath0  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , cvar0 )
	ifiles0 = os.listdir(ipath0)
	ifiles0.sort()
	cvar1   = "hurs"
	ipath1  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , cvar1 )
	ifiles1 = os.listdir(ipath1)
	ifiles1.sort()
	
	
	for ifile0,ifile1 in zip(ifiles0,ifiles1):
		
		idata0 = xr.open_dataset( os.path.join( ipath0 , ifile0 ) )
		idata1 = xr.open_dataset( os.path.join( ipath1 , ifile1 ) )
		
		year  = idata0.time.dt.year[0].values
		dtime = [dt.datetime(int(year),1,1) + dt.timedelta( days = int(i) - 1 ) for i in np.unique(idata0.time.dt.dayofyear.values)]
		
		## Build hourly heatIndex
		odatah = idata0.copy( deep = True ).rename( { cvar0 : cvar } )
		c0     = -8.784695
		c1     = 1.61139411
		c2     = 2.338549
		c3     = -0.14611605
		c4     = -1.2308094e-2
		c5     = -1.6424828e-2
		c6     = 2.211732e-3
		c7     = 7.2546e-4
		c8     = -3.582e-6
		T      = idata0[cvar0] - 273.15
		H      = idata1[cvar1].round(0)
		
		odatah[cvar] = 273.15 + c0 + c1 * T + c2 * H + c3 * T * H + c4 * T**2 + c5 * H**2 + c6 * T**2 * H + c7 * T * H**2 + c8 * T**2 * H**2
		odatah[cvar] = odatah[cvar].where( T > 20 , np.nan )
		
		## Build daily
		odatad = odatah.groupby("time.dayofyear").mean().rename( dayofyear = "time" ).assign_coords( time = dtime )
		
		## Save hourly
		opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , cvar )
		t0    = str(odatah.time[ 0].values)[:13].replace("-","").replace(" ","").replace("T","")
		t1    = str(odatah.time[-1].values)[:13].replace("-","").replace(" ","").replace("T","")
		ofile = f"ERA5-AMIP_{cvar}_hr_{area_name}_{t0}-{t1}.nc"
		target = os.path.join( opath , ofile )
		if not os.path.isdir(opath):
			os.makedirs(opath)
		logger.info( f" * Save 'TMP/ERA5-AMIP/hr/{cvar}/{ofile}'" )
		odatah.to_netcdf( os.path.join( opath , ofile ) )
		
		## Save daily
		opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "day" , cvar )
		t0    = str(odatad.time[ 0].values)[:10].replace("-","").replace(" ","").replace("T","")
		t1    = str(odatad.time[-1].values)[:10].replace("-","").replace(" ","").replace("T","")
		ofile = f"ERA5-AMIP_{cvar}_day_{area_name}_{t0}-{t1}.nc"
		target = os.path.join( opath , ofile )
		if not os.path.isdir(opath):
			os.makedirs(opath)
		logger.info( f" * Save 'TMP/ERA5-AMIP/day/{cvar}/{ofile}'" )
		odatad.to_netcdf( os.path.join( opath , ofile ) )
##}}}

def build_cvarmin( cvar ):##{{{
	
	cvarN = f"{cvar}min"
	area_name = cdsuParams.area_name
	
	## files
	ipath  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , cvar )
	ifiles = os.listdir(ipath)
	ifiles.sort()
	
	
	for ifile in ifiles:
		
		idata = xr.open_dataset( os.path.join( ipath , ifile ) )
		
		year  = idata.time.dt.year[0].values
		dtime = [dt.datetime(int(year),1,1) + dt.timedelta( days = int(i) - 1 ) for i in np.unique(idata.time.dt.dayofyear.values)]
		
		## Build daily
		odatad = idata.groupby("time.dayofyear").min().rename( dayofyear = "time" ).assign_coords( time = dtime ).rename( { cvar : cvarN } )
		
		## Save daily
		opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "day" , cvarN )
		t0    = str(odatad.time[ 0].values)[:10].replace("-","").replace(" ","").replace("T","")
		t1    = str(odatad.time[-1].values)[:10].replace("-","").replace(" ","").replace("T","")
		ofile = f"ERA5-AMIP_{cvarN}_day_{area_name}_{t0}-{t1}.nc"
		target = os.path.join( opath , ofile )
		if not os.path.isdir(opath):
			os.makedirs(opath)
		logger.info( f" * Save 'TMP/ERA5-AMIP/day/{cvarN}/{ofile}'" )
		odatad.to_netcdf( os.path.join( opath , ofile ) )
##}}}

def build_cvarmax( cvar ):##{{{
	
	cvarX = f"{cvar}max"
	area_name = cdsuParams.area_name
	
	## files
	ipath  = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , cvar )
	ifiles = os.listdir(ipath)
	ifiles.sort()
	
	
	for ifile in ifiles:
		
		idata = xr.open_dataset( os.path.join( ipath , ifile ) )
		
		year  = idata.time.dt.year[0].values
		dtime = [dt.datetime(int(year),1,1) + dt.timedelta( days = int(i) - 1 ) for i in np.unique(idata.time.dt.dayofyear.values)]
		
		## Build daily
		odatad = idata.groupby("time.dayofyear").max().rename( dayofyear = "time" ).assign_coords( time = dtime ).rename( { cvar : cvarX } )
		
		## Save daily
		opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "day" , cvarX )
		t0    = str(odatad.time[ 0].values)[:10].replace("-","").replace(" ","").replace("T","")
		t1    = str(odatad.time[-1].values)[:10].replace("-","").replace(" ","").replace("T","")
		ofile = f"ERA5-AMIP_{cvarX}_day_{area_name}_{t0}-{t1}.nc"
		target = os.path.join( opath , ofile )
		if not os.path.isdir(opath):
			os.makedirs(opath)
		logger.info( f" * Save 'TMP/ERA5-AMIP/day/{cvarX}/{ofile}'" )
		odatad.to_netcdf( os.path.join( opath , ofile ) )
##}}}

def build_EXTRA_cvars():##{{{
	
	cvars_cmp = cdsuParams.cvars_cmp
	for cvar in cvars_cmp:
		logger.info( f"Build EXTRA cvar '{cvar}'" )
		
		if cvar[-3:] == "min":
			build_cvarmin( cvar[:-3] )
		if cvar[-3:] == "max":
			build_cvarmax( cvar[:-3] )
		if cvar == "sfcWind":
			build_sfcWind()
		if cvar == "hurs":
			build_hurs()
		if cvar == "huss":
			build_huss()
		if cvar == "heatIndex":
			build_heatIndex()
	
##}}}


