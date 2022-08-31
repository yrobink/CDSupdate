
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
import rich
import itertools as itt
import datetime as dt
import datetime as dt
import time as systime

import numpy as np
import xarray as xr

import cdsapi


## Functions / classes / objects
## not in the toolchain currently
#################################

def load_data():##{{{
	key = None
	url = None
	verify = None
	
	## Parameters
	lat_min = 5
	lat_max = 70
	lon_min = -80
	lon_max = 50
	name   = "reanalysis-era5-single-levels"
	params = { "product_type" : "reanalysis",
	           "format"       : "netcdf",
	           "variable"     : "2m_temperature",
	           "year"         : "2022",
	           "month"        : "01",
	           "day"          : ["01","02"],
	           "time"         : ["{:{fill}{align}{n}}:00".format(i,fill="0",align=">",n=2) for i in range(24)],
	           "area"         : [lat_max,lon_min,lat_min,lon_max]
	           }
	ofile  = os.path.join( os.environ["DATADIR"] , "tmp" , "auERA5" , "ERA5.nc" )
	
	client = cdsapi.Client( key = key , url = url , verify = verify )
	client.retrieve( name , params , ofile )

##}}}

def build_attrs(var): ##{{{
	
	## Start with variables attributes
	varattrs = {}
	varattrs["coordinates"]   = "lat lon"
	
	if var == "tas":
		varattrs["standard_name"] = "air_temperature" ;
		varattrs["long_name"]     = "Daily Mean Near-Surface Air Temperature" ;
		varattrs["units"]         = "Kelvin"
		varattrs["comment"]       = "Computed as hourly average"
	if var == "tasmin":
		varattrs["standard_name"] = "air_temperature" ;
		varattrs["long_name"]     = "Daily Min Near-Surface Air Temperature" ;
		varattrs["units"]         = "Kelvin"
	if var == "tasmax":
		varattrs["standard_name"] = "air_temperature" ;
		varattrs["long_name"]     = "Daily Max Near-Surface Air Temperature" ;
		varattrs["units"]         = "Kelvin"
	if var == "huss":
		varattrs["standard_name"] = "specific_humidity" ;
		varattrs["long_name"]     = "Near Surface Specific Humidity" ;
		varattrs["units"]         = "kg.kg-1"
	if var == "rlds":
		varattrs["standard_name"] = "surface_downwelling_longwave_flux_in_air" ;
		varattrs["long_name"]     = "Surface Downwelling Longwave Radiation" ;
		varattrs["units"]         = "W.m-2"
	if var == "rsds":
		varattrs["standard_name"] = "surface_downwelling_shortwave_flux_in_air" ;
		varattrs["long_name"]     = "Surface Downwelling Shortwave Radiation" ;
		varattrs["units"]         = "W.m-2"
	if var == "sfcWind":
		varattrs["standard_name"] = "wind_speed" ;
		varattrs["long_name"]     = "Near-Surface Wind Speed" ;
		varattrs["units"]         = "m.s-1"
	if var == "pr":
		varattrs["standard_name"] = "precipitation_flux" ;
		varattrs["long_name"]     = "Liquid Precipitation Flux" ;
		varattrs["units"]         = "kg.m-2.s-1"
	if var == "prsn":
		varattrs["standard_name"] = "snowfall_flux" ;
		varattrs["long_name"]     = "Snowfall Flux" ;
		varattrs["units"]         = "kg.m-2.s-1"
	if var == "prtot":
		varattrs["standard_name"] = "precipitation_flux" ;
		varattrs["long_name"]     = "Total Precipitation Flux" ;
		varattrs["units"]         = "kg.m-2.s-1"
	if var == "ps":
		varattrs["standard_name"] = "surface_air_pressure" ;
		varattrs["long_name"]     = "Surface Air Pressure" ;
		varattrs["units"]         = "Pa"
	if var == "hurs":
		varattrs["standard_name"] = "relative_humidity" ;
		varattrs["long_name"]     = "Relative Humidity" ;
		varattrs["units"]         = "%"
	if var == "co2s":
		varattrs["standard_name"] = "mass_concentration_of_carbon_dioxide_in_air" ;
		varattrs["long_name"]     = "Near-Surface Mass Concentration of CO2" ;
		varattrs["units"]         = "kg.m-3"
	
	## Coordinates attributes
	timeattrs = {}
	timeattrs["axis"]          = "T"
	timeattrs["standard_name"] = "time"
	timeattrs["long_name"]     = "time axis"
	
	latattrs = {}
	latattrs["axis"]           = "y"
	latattrs["long_name"]      = "latitude coordinate"
	latattrs["standard_name"]  = "latitude"
	latattrs["units"]          = "degrees_north"
	
	lonattrs = {}
	lonattrs["axis"]           = "x"
	lonattrs["long_name"]      = "longitude coordinate"
	lonattrs["standard_name"]  = "longitude"
	lonattrs["units"]          = "degrees_east"
	
	## Global attributes
	attrs = {}
	attrs["title"]         = "reanalysis-era5-single-levels"
	attrs["Conventions"]   = "CF-1.6"
	attrs["source"]        = "https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview"
	attrs["contact"]       = "andreia.hisi@lsce.ipsl.fr, yoann.robin@lsce.ipsl.fr"
	attrs["creation_date"] = str(dt.datetime.utcnow())[:19] + " (UTC)"
	attrs["comment"]       = "The area in the file name is in the form 'lon_min+180'-'lon_max+180'-'lat_min'-'lat_max', i.e. the longitude lives in the range 0/360 to have only positive values. But the longitude coordinate lives in the range -180/180."
	attrs["reference"]     = "Hersbach, H., Bell, B., Berrisford, P., Biavati, G., Horányi, A., Muñoz Sabater, J., Nicolas, J., Peubey, C., Radu, R., Rozum, I., Schepers, D., Simmons, A., Soci, C., Dee, D., Thépaut, J-N. (2018): ERA5 hourly data on single levels from 1979 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). (Accessed on {}), 10.24381/cds.adbb2d47".format(str(dt.datetime.utcnow())[:10])
	return varattrs,timeattrs,latattrs,lonattrs,attrs
##}}}

def build_encoding( var , nlat , nlon ):##{{{
	encoding = { "time" : { "dtype" : "float32" , "zlib" : True , "complevel": 5 , "chunksizes" : (1,) , "units" : "days since 1850-01-01" } ,
				 "lon"  : { "dtype" : "float32" , "zlib" : True , "complevel": 5 , "chunksizes" : (nlon,) } ,
				 "lat"  : { "dtype" : "float32" , "zlib" : True , "complevel": 5 , "chunksizes" : (nlat,) } ,
				 var    : { "dtype" : "float32" , "zlib" : True , "complevel": 5 , "chunksizes" : (1,nlat,nlon) } ,
				}
	
	return encoding
##}}}

def nccds2ncstd():##{{{
	## Build area name
	lat_min = 5
	lat_max = 70
	lon_min = -80
	lon_max = 50
	area = f"{lon_min+180}-{lon_max+180}-{lat_min}-{lat_max}"
	
	## Read data
	ifile = os.path.join( os.environ["DATADIR"] , "tmp" , "auERA5" , "ERA5.nc" )
	idata = xr.open_dataset(ifile)
	
	## Start by read coordinates
	time = [dt.datetime(2022,1,1) + dt.timedelta( days = int(i) - 1 ) for i in np.unique(idata.time["time.day"])]
	lat  = idata.latitude.values
	lon  = idata.longitude.values
	
	## Daily values, and in array to remove all attributes
	tas    = idata.groupby("time.day").mean().t2m.values
	tasmin = idata.groupby("time.day").min().t2m.values
	tasmax = idata.groupby("time.day").max().t2m.values
	
	## Reverse axis
	argslat = np.argsort(lat)
	argslon = np.argsort(lon)
	tas     = tas[:,argslat,:][:,:,argslon].copy()
	tasmin  = tasmin[:,argslat,:][:,:,argslon].copy()
	tasmax  = tasmax[:,argslat,:][:,:,argslon].copy()
	lat     = lat[argslat].copy()
	lon     = lon[argslon].copy()
	
	## Back to xarray with good coordinates
	tas    = xr.DataArray( tas    , dims = ["time","lat","lon"] , coords = [time,lat,lon] )
	tasmin = xr.DataArray( tasmin , dims = ["time","lat","lon"] , coords = [time,lat,lon] )
	tasmax = xr.DataArray( tasmax , dims = ["time","lat","lon"] , coords = [time,lat,lon] )
	
	## Now in dataset
	dtas    = xr.Dataset( { "tas"    : tas } )
	dtasmin = xr.Dataset( { "tasmin" : tasmin } )
	dtasmax = xr.Dataset( { "tasmax" : tasmax } )
	
	## Attributes
	for dX,var in zip([dtas,dtasmin,dtasmax],["tas","tasmin","tasmax"]):
		varattrs,timeattrs,latattrs,lonattrs,attrs = build_attrs("tas")
		dX[var].attrs = varattrs
		dX.time.attrs = timeattrs
		dX.lat.attrs  = latattrs
		dX.lon.attrs  = lonattrs
		dX.attrs      = attrs
	
	## And in netcdf
	t0 = str(time[0])[:10].replace("-","")
	t1 = str(time[-1])[:10].replace("-","")
	for dX,var in zip([dtas,dtasmin,dtasmax],["tas","tasmin","tasmax"]):
		dX.to_netcdf( os.path.join( os.environ["DATADIR"] , "tmp" , "auERA5" , f"ERA5_day_{var}_{area}_{t0}-{t1}.nc" ) , encoding = build_encoding(var,lat.size,lon.size) )
##}}}

