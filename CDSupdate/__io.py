
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

import os
import logging
import cdsapi

import datetime as dt
import numpy  as np
import xarray as xr

import netCDF4
import cftime


#############
## Imports ##
#############

from .__CDSUParams import cdsuParams
from .__release import version
from .__release import src_url


##################
## Init logging ##
##################

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

for mod in ["cdsapi"]:
	logging.getLogger(mod).setLevel(logging.ERROR)


###############
## Functions ##
###############

def load_data_CDS():##{{{
	
	## Build area
	lon0,lon1,lat0,lat1 = cdsuParams.area
	cdsarea   = [lat1,lon0,lat0,lon1]
	area_name = cdsuParams.area_name
	
	## cdsapi base params
	request_base = {
	           "product_type" : "reanalysis",
	           "format"        : "netcdf",
	           "area"          : cdsarea
	           }
	
	## List of climate vars
	cvars_dwl = cdsuParams.cvars_dwl
	cvars_lev = cdsuParams.cvars_lev
	
	## cdsapi client params
	cdskey = None
	cdsurl = None
	cdsverify = None
	
	## Now loop on cvar for download
	for cvar,level in zip(cvars_dwl,cvars_lev):
		
		logger.info( f"Start download {cvar} ({level})" )
		
		## Find the level (surface or pressure level)
		logger.info( f" * Level: {level}" )
		
		## Build name
		if level == "single":
			name  = f"reanalysis-era5-{level}-levels"
		else:
			name  = f"reanalysis-era5-pressure-levels"
		
		for key in cdsuParams.cdsApiParams:
			
			## Build request
			cap = cdsuParams.cdsApiParams[key]
			request = { **request_base , **cap }
			request["variable"] = cdsuParams.cvarsParams.AMIP_CDS[cvar]
			
			h = ""
			if not level == "single":
				h = level
				request["pressure_level"] = level
			
			## Build target
			opath = os.path.join( cdsuParams.tmp , "ERA5-BRUT" , "hr" , cvar + h )
			ofile = f"ERA5-BRUT_{cvar+h}_hr_{area_name}_{key[0].replace('-','')}-{key[1].replace('-','')}.nc"
			target = os.path.join( opath , ofile )
			if not os.path.isdir(opath):
				os.makedirs(opath)
			
			## Log
			logger.info( " * Load '{} / {}' in 'TMP/ERA5-BRUT/hr/".format(*key) + f"{cvar+h}/" + ofile + "'" )
			
			## And run download
			try:
				client = cdsapi.Client( key = cdskey , url = cdsurl , verify = cdsverify , quiet = True , progress = False )
				client.retrieve( name , request , target )
			except Exception as e:
				logger.info( f" * => Warning '{e}', data not used." )
				if os.path.isfile(target):
					os.remove(target)

##}}}

def BRUT_to_AMIP_format():##{{{
	
	## Parameters
	cvars = cdsuParams.cvars
	area_name = cdsuParams.area_name
	
	## List of climate vars
	cvars_dwl = cdsuParams.cvars_dwl
	cvars_lev = cdsuParams.cvars_lev
	
	## Loop on climate variables
	for cvar,level in zip(cvars_dwl,cvars_lev):
		
		h = "" if level == "single" else level
		
		evar = cdsuParams.cvarsParams.AMIP_ERA5[cvar]
		logger.info( f"BRUT to AMIP:" )
		logger.info( f" * {evar} to {cvar+h}" )
		
		## Parameters
		ipath = os.path.join( cdsuParams.tmp , "ERA5-BRUT" , "hr" , cvar + h )
		
		## List files
		ifiles = os.listdir(ipath)
		ifiles.sort()
		
		## Split in year
		difiles = {}
		for ifile in ifiles:
			
			year = ifile.split("_")[-1][:4]
			if year in difiles:
				difiles[year].append(ifile)
			else:
				difiles[year] = [ifile]
		
		## Now loop on years
		for year in difiles:
			
			## Load data
			idata  = xr.open_mfdataset( [ os.path.join( ipath , ifile ) for ifile in difiles[year] ] )
			if "expver" in idata:
				idata = idata.sel( expver = 1 ).combine_first( idata.sel( expver = 5 ) )
			idata = idata.compute()
			
			## Reorganize lon / lat axis
			idata = idata.rename( { "longitude" : "lon" , "latitude" : "lat" , evar : cvar + h } )
			idata = idata.assign_coords( lon = idata.lon.where( idata.lon < 180 , idata.lon.values - 360 ) ).sortby("lon").sortby("lat").compute()
			
			## Delete last day if all hours are not present
			t0 = str(idata.time[ 0].values)[:10] + " 00:00"
			t1 = str(idata.time[-1].values)[:10]
			tm = dt.datetime.fromisoformat(t1 + " 00:00") - dt.timedelta( hours = 1 )
			if idata.sel( time = t1 ).time.size < 24:
				idata = idata.sel( time = slice(t0,tm) ).compute()
			
			## Change scale
			if cvar in ["zg"]:
				g = 9.80665
				idata[cvar+h] = idata[cvar+h] / g
			
			## Transform hourly variable
			opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "hr" , cvar + h )
			t0    = str(idata.time[ 0].values)[:13].replace("-","").replace(" ","").replace("T","")
			t1    = str(idata.time[-1].values)[:13].replace("-","").replace(" ","").replace("T","")
			ofile = f"ERA5-AMIP_{cvar+h}_hr_{area_name}_{t0}-{t1}.nc"
			target = os.path.join( opath , ofile )
			if not os.path.isdir(opath):
				os.makedirs(opath)
			logger.info( f" * Save 'TMP/ERA5-AMIP/hr/{cvar+h}/{ofile}'" )
			idata.to_netcdf( os.path.join( opath , ofile ) )
			
			## Build daily variable
			dtime = [dt.datetime(int(year),1,1) + dt.timedelta( days = int(i) - 1 ) for i in np.unique(idata.time.dt.dayofyear.values)]
			ddata = idata.groupby("time.dayofyear").mean().rename( dayofyear = "time" ).assign_coords( time = dtime )
			
			## Save daily variable
			opath = os.path.join( cdsuParams.tmp , "ERA5-AMIP" , "day" , cvar + h )
			t0    = str(ddata.time[ 0].values)[:10].replace("-","").replace(" ","").replace("T","")
			t1    = str(ddata.time[-1].values)[:10].replace("-","").replace(" ","").replace("T","")
			ofile = f"ERA5-AMIP_{cvar+h}_day_{area_name}_{t0}-{t1}.nc"
			target = os.path.join( opath , ofile )
			if not os.path.isdir(opath):
				os.makedirs(opath)
			logger.info( f" * Save 'TMP/ERA5-AMIP/day/{cvar+h}/{ofile}'" )
			ddata.to_netcdf( os.path.join( opath , ofile ) )
##}}}

def build_gattrs( cvar , level ): ##{{{
	
	level_name = "single"
	if not level == "pressure":
		level_name = "pressure"
	
	## Global attributes
	now    = str(dt.datetime.utcnow())[:19]
	gattrs = {}
	gattrs["title"]         = f"reanalysis-era5-{level_name}-level"
	gattrs["institution"]   = "ECMWF"
	gattrs["Conventions"]   = "CF-1.10"
	gattrs["creation_date"] = now + " (UTC)"
	
	gattrs["level"] = level
	if level == "single":
		gattrs["source"] = "https://doi.org/10.24381/cds.adbb2d47"
	else:
		gattrs["source"] = "https://doi.org/10.24381/cds.bd0915c6"
	
	
	## Reference
	if level == "single":
		ref  ="Hersbach, H., Bell, B., Berrisford, P., Biavati, G., Horányi, A., Muñoz Sabater, J., Nicolas, J., Peubey, C., Radu, R., Rozum, I., Schepers, D., Simmons, A., Soci, C., Dee, D., Thépaut, J-N. (2023): ERA5 hourly data on single levels from 1940 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS), DOI: 10.24381/cds.adbb2d47 (Accessed on {})".format(now)
	else:
		ref = "Hersbach, H., Bell, B., Berrisford, P., Biavati, G., Horányi, A., Muñoz Sabater, J., Nicolas, J., Peubey, C., Radu, R., Rozum, I., Schepers, D., Simmons, A., Soci, C., Dee, D., Thépaut, J-N. (2023): ERA5 hourly data on pressure levels from 1940 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS), DOI: 10.24381/cds.bd0915c6 (Accessed on {})".format(now)
	gattrs["references"] = ref
	
	## CDSupdate
	gattrs["CDSupdate_version"] = f"{version}"
	gattrs["CDSupdate_url"] = src_url
	
	return gattrs
##}}}

def save_netcdf( idata , cvar , freq , ofile ):##{{{
	
	avar,level    = cdsuParams.cvarsParams.split_level(cvar)
	time_units    = "hours since 1900-01-01 00:00"
	time_calendar = "standard"
	
	nlat  = idata.lat.size
	nlon  = idata.lon.size
	ntime = idata.time.size
	if freq == "hr":
		time  = [ dt.datetime(y,m,d,h) for y,m,d,h in zip(idata.time.dt.year.values,idata.time.dt.month.values,idata.time.dt.day.values,idata.time.dt.hour.values) ]
	else:
		time  = [ dt.datetime(y,m,d) for y,m,d in zip(idata.time.dt.year.values,idata.time.dt.month.values,idata.time.dt.day.values) ]
	
	with netCDF4.Dataset( ofile , mode = "w" ) as ncf:
		
		## Add dimensions
		ncd_lat  = ncf.createDimension( "lat"  , idata.lat.size )
		ncd_lon  = ncf.createDimension( "lon"  , idata.lon.size )
		ncd_time = ncf.createDimension( "time" , None           )
		
		## Add variables of dimensions
		ncv_lat    = ncf.createVariable( "lat"    , "double" , ("lat",)  , fill_value = np.nan , shuffle = False , compression = "zlib" , complevel = 5 , chunksizes = (nlat,) )
		ncv_lon    = ncf.createVariable( "lon"    , "double" , ("lon",)  , fill_value = np.nan , shuffle = False , compression = "zlib" , complevel = 5 , chunksizes = (nlon,) )
		ncv_height = ncf.createVariable( "height" , "double" )
		ncv_time   = ncf.createVariable( "time"   , "double" , ("time",) , fill_value = np.nan , shuffle = False , compression = "zlib" , complevel = 5 , chunksizes = (1,)    )
		
		## Add attributes
		ncv_lat.setncattr( "axis"          , "Y"             )
		ncv_lat.setncattr( "long_name"     , "Latitude"      )
		ncv_lat.setncattr( "standard_name" , "latitude"      )
		ncv_lat.setncattr( "units"         , "degrees_north" )
		
		ncv_lon.setncattr( "axis"          , "X"            )
		ncv_lon.setncattr( "long_name"     , "Longitude"    )
		ncv_lon.setncattr( "standard_name" , "longitude"    )
		ncv_lon.setncattr( "units"         , "degrees_east" )
		
		ncv_height.setncattr( "axis"          , "Z"      )
		ncv_height.setncattr( "long_name"     , "height" )
		ncv_height.setncattr( "standard_name" , "height" )
		ncv_height.setncattr( "positive"      , "up"     )
		if level == "single":
			ncv_height.setncattr( "units"         , "m"      )
		else:
			ncv_height.setncattr( "units"         , "hPa"    )
		
		ncv_time.setncattr( "axis"          , "T"           )
		ncv_time.setncattr( "long_name"     , "Time Axis"   )
		ncv_time.setncattr( "standard_name" , "time"        )
		ncv_time.setncattr( "units"         , time_units    )
		ncv_time.setncattr( "calendar"      , time_calendar )
		
		## Fill variables of dimensions
		ncv_lat[:]    = idata.lat.values
		ncv_lon[:]    = idata.lon.values
		ncv_time[:]   = cftime.date2num( time , time_units , time_calendar )
		
		## Now the main variable
		ncv_cvar = ncf.createVariable( cvar , "float32" , ("time","lat","lon")  , fill_value = np.nan , shuffle = False , compression = "zlib" , complevel = 5 , chunksizes = (1,nlat,nlon) )
		ncv_cvar[:] = idata[cvar].values
		
		## Attributes
		cvarattrs = cdsuParams.cvarsParams.attrs(avar)
		for att in cvarattrs:
			if len(cvarattrs[att]) == 0:
				continue
			if att == "long_name" and not (level == "single"):
				ncv_cvar.setncattr( att , cvarattrs[att].replace("__CHANGE__",level) )
			else:
				ncv_cvar.setncattr( att , cvarattrs[att] )
		
		ncv_cvar.setncattr( "coordinates" , "height lat lon" )
		if level == "single":
			ncv_height[:] = float(cdsuParams.cvarsParams.height(cvar))
		else:
			ncv_height[:] = float(level)
		
		## Add global attrs
		gattrs = build_gattrs( cvar , level )
		for attr in gattrs:
			ncf.setncattr( attr , gattrs[attr] )
	
##}}}

def merge_AMIP_CF_format():##{{{
	
	## Parameters
	area_name = cdsuParams.area_name
	
	## List of cvars
	cvars = list(cdsuParams.cvars_cmp)
	for cvar,level in zip(cdsuParams.cvars_dwl,cdsuParams.cvars_lev):
		if level == "single":
			cvars.append(cvar)
		else:
			cvars.append(cvar + level)
	
	## Loop on frequences
	for freq in ["hr","day"]:
		
		if freq == "hr" and not cdsuParams.keep_hourly:
			continue
		
		## Loop on climate variables
		for cvar in cvars:
			logger.info( "AMIP to CF, final merge" )
			logger.info( f" * {cvar}" )
			
			## Path
			ipath = os.path.join( cdsuParams.tmp        , "ERA5-AMIP" ,             freq , cvar )
			if not os.path.isdir(ipath):
				continue
			opath = os.path.join( cdsuParams.output_dir , "ERA5"      , area_name , freq , cvar )
			if not os.path.isdir(opath):
				os.makedirs(opath)
			
			## List files
			ifilesN = os.listdir(ipath)
			ifilesO = os.listdir(opath)
			
			## Split files in year
			difilesN = { ifileN.split("_")[-1][:4] : ifileN for ifileN in ifilesN }
			difilesO = { ifileO.split("_")[-1][:4] : ifileO for ifileO in ifilesO }
			
			## Total available years
			years = list(set( list(difilesN) + list(difilesO) ))
			years.sort()
			for year in years:
				
				ifileN = difilesN.get(year)
				ifileO = difilesO.get(year)
				
				## Case 1, no new file for this specific year
				if ifileN is None:
					continue
				
				## Case 2, new file, but no old data
				if ifileO is None:
					logger.info( f" * No old data to merge" )
					idataN = xr.open_dataset( os.path.join( ipath , ifileN ) )
					t0    = str(idataN.time[ 0].values)[:10].replace("-","").replace(" ","").replace("T","")
					t1    = str(idataN.time[-1].values)[:10].replace("-","").replace(" ","").replace("T","")
					ofile  = f"ERA5_{cvar}_{freq}_{area_name}_{t0}-{t1}.nc"
					logger.info( f" * Save '{ofile}'" )
					save_netcdf( idataN , cvar , freq , os.path.join( opath , ofile ) )
				
				## Case 3, must merge the two files
				if ifileO is not None and ifileN is not None:
					logger.info( f" * Require merge" )
					idataN = xr.open_dataset( os.path.join( ipath , ifileN ) ).expand_dims("version").assign_coords( version = [1] )
					idataO = xr.open_dataset( os.path.join( opath , ifileO ) ).expand_dims("version").assign_coords( version = [0] )
					idata  = xr.concat( [idataN,idataO] , dim = "version" )
					idata  = idata.sel( version = 1 ).combine_first( idata.sel( version = 0 ) ).compute()
					del idataN
					del idataO
					os.remove( os.path.join( opath , ifileO ) )
					
					t0    = str(idata.time[ 0].values)[:10].replace("-","").replace(" ","").replace("T","")
					t1    = str(idata.time[-1].values)[:10].replace("-","").replace(" ","").replace("T","")
					ofile  = f"ERA5_{cvar}_{freq}_{area_name}_{t0}-{t1}.nc"
					logger.info( f" * Save '{ofile}'" )
					save_netcdf( idata , cvar , freq , os.path.join( opath , ofile ) )
##}}}


