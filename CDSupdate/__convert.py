
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

import numpy  as np
import xarray as xr

#############
## Imports ##
#############

from .__CDSparams import CDSparams


###############
## Functions ##
###############

def build_attrs_daily(var): ##{{{
	
	## Start with variables attributes
	varattrs = CDSparams.attrs( var , "daily" )
	
#	if var == "tas":
#		varattrs["standard_name"] = "air_temperature" ;
#		varattrs["long_name"]     = "Daily Mean Near-Surface Air Temperature" ;
#		varattrs["units"]         = "Kelvin"
#		varattrs["comment"]       = "Computed as hourly average"
#	if var == "tasmin":
#		varattrs["standard_name"] = "air_temperature" ;
#		varattrs["long_name"]     = "Daily Min Near-Surface Air Temperature" ;
#		varattrs["units"]         = "Kelvin"
#	if var == "tasmax":
#		varattrs["standard_name"] = "air_temperature" ;
#		varattrs["long_name"]     = "Daily Max Near-Surface Air Temperature" ;
#		varattrs["units"]         = "Kelvin"
#	if var == "huss":
#		varattrs["standard_name"] = "specific_humidity" ;
#		varattrs["long_name"]     = "Near Surface Specific Humidity" ;
#		varattrs["units"]         = "kg.kg-1"
#	if var == "rlds":
#		varattrs["standard_name"] = "surface_downwelling_longwave_flux_in_air" ;
#		varattrs["long_name"]     = "Surface Downwelling Longwave Radiation" ;
#		varattrs["units"]         = "W.m-2"
#	if var == "rsds":
#		varattrs["standard_name"] = "surface_downwelling_shortwave_flux_in_air" ;
#		varattrs["long_name"]     = "Surface Downwelling Shortwave Radiation" ;
#		varattrs["units"]         = "W.m-2"
#	if var == "sfcWind":
#		varattrs["standard_name"] = "wind_speed" ;
#		varattrs["long_name"]     = "Near-Surface Wind Speed" ;
#		varattrs["units"]         = "m.s-1"
#	if var == "pr":
#		varattrs["standard_name"] = "precipitation_flux" ;
#		varattrs["long_name"]     = "Liquid Precipitation Flux" ;
#		varattrs["units"]         = "kg.m-2.s-1"
#	if var == "prsn":
#		varattrs["standard_name"] = "snowfall_flux" ;
#		varattrs["long_name"]     = "Snowfall Flux" ;
#		varattrs["units"]         = "kg.m-2.s-1"
#	if var == "prtot":
#		varattrs["standard_name"] = "precipitation_flux" ;
#		varattrs["long_name"]     = "Total Precipitation Flux" ;
#		varattrs["units"]         = "kg.m-2.s-1"
#	if var == "ps":
#		varattrs["standard_name"] = "surface_air_pressure" ;
#		varattrs["long_name"]     = "Surface Air Pressure" ;
#		varattrs["units"]         = "Pa"
#	if var == "psl":
#		varattrs["standard_name"] = "air_pressure_at_sea_level" ;
#		varattrs["long_name"]     = "Sea Level Pressure" ;
#		varattrs["units"]         = "Pa"
#	if var == "hurs":
#		varattrs["standard_name"] = "relative_humidity" ;
#		varattrs["long_name"]     = "Relative Humidity" ;
#		varattrs["units"]         = "%"
#	if var == "co2s":
#		varattrs["standard_name"] = "mass_concentration_of_carbon_dioxide_in_air" ;
#		varattrs["long_name"]     = "Near-Surface Mass Concentration of CO2" ;
#		varattrs["units"]         = "kg.m-3"
	
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
	attrs["title"]         = "reanalysis-era5"
	attrs["Conventions"]   = "CF-1.6"
	attrs["source"]        = "https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview"
	attrs["contact"]       = "andreia.hisi@lsce.ipsl.fr, yoann.robin@lsce.ipsl.fr"
	attrs["creation_date"] = str(dt.datetime.utcnow())[:19] + " (UTC)"
	attrs["comment_area"]       = "The area in the file name is in the form 'lon_min+180'-'lon_max+180'-'lat_min'-'lat_max', i.e. the longitude lives in the range 0/360 to have only positive values. But the longitude coordinate lives in the range -180/180."
	attrs["reference"]     = "Hersbach, H., Bell, B., Berrisford, P., Biavati, G., Horányi, A., Muñoz Sabater, J., Nicolas, J., Peubey, C., Radu, R., Rozum, I., Schepers, D., Simmons, A., Soci, C., Dee, D., Thépaut, J-N. (2018): ERA5 hourly data on single levels from 1979 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). (Accessed on {}), 10.24381/cds.adbb2d47".format(str(dt.datetime.utcnow())[:10])
	return varattrs,timeattrs,latattrs,lonattrs,attrs
##}}}

def build_attrs_hourly(var): ##{{{
	
	## Start with variables attributes
	varattrs = CDSparams.attrs( var , "hourly" )
	
#	if var == "tas":
#		varattrs["standard_name"] = "air_temperature" ;
#		varattrs["long_name"]     = "Hourly Mean Near-Surface Air Temperature" ;
#		varattrs["units"]         = "Kelvin"
#	if var == "huss":
#		varattrs["standard_name"] = "specific_humidity" ;
#		varattrs["long_name"]     = "Near Surface Specific Humidity" ;
#		varattrs["units"]         = "kg.kg-1"
#	if var == "rlds":
#		varattrs["standard_name"] = "surface_downwelling_longwave_flux_in_air" ;
#		varattrs["long_name"]     = "Surface Downwelling Longwave Radiation" ;
#		varattrs["units"]         = "W.m-2"
#	if var == "rsds":
#		varattrs["standard_name"] = "surface_downwelling_shortwave_flux_in_air" ;
#		varattrs["long_name"]     = "Surface Downwelling Shortwave Radiation" ;
#		varattrs["units"]         = "W.m-2"
#	if var == "sfcWind":
#		varattrs["standard_name"] = "wind_speed" ;
#		varattrs["long_name"]     = "Near-Surface Wind Speed" ;
#		varattrs["units"]         = "m.s-1"
#	if var == "pr":
#		varattrs["standard_name"] = "precipitation_flux" ;
#		varattrs["long_name"]     = "Liquid Precipitation Flux" ;
#		varattrs["units"]         = "kg.m-2.s-1"
#	if var == "prsn":
#		varattrs["standard_name"] = "snowfall_flux" ;
#		varattrs["long_name"]     = "Snowfall Flux" ;
#		varattrs["units"]         = "kg.m-2.s-1"
#	if var == "prtot":
#		varattrs["standard_name"] = "precipitation_flux" ;
#		varattrs["long_name"]     = "Total Precipitation Flux" ;
#		varattrs["units"]         = "kg.m-2.s-1"
#	if var == "ps":
#		varattrs["standard_name"] = "surface_air_pressure" ;
#		varattrs["long_name"]     = "Surface Air Pressure" ;
#		varattrs["units"]         = "Pa"
#	if var == "psl":
#		varattrs["standard_name"] = "air_pressure_at_sea_level" ;
#		varattrs["long_name"]     = "Sea Level Pressure" ;
#		varattrs["units"]         = "Pa"
#	if var == "hurs":
#		varattrs["standard_name"] = "relative_humidity" ;
#		varattrs["long_name"]     = "Relative Humidity" ;
#		varattrs["units"]         = "%"
#	if var == "co2s":
#		varattrs["standard_name"] = "mass_concentration_of_carbon_dioxide_in_air" ;
#		varattrs["long_name"]     = "Near-Surface Mass Concentration of CO2" ;
#		varattrs["units"]         = "kg.m-3"
	
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
	attrs["title"]         = "reanalysis-era5"
	attrs["Conventions"]   = "CF-1.6"
	attrs["source"]        = "https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview"
	attrs["contact"]       = "andreia.hisi@lsce.ipsl.fr, yoann.robin@lsce.ipsl.fr"
	attrs["creation_date"] = str(dt.datetime.utcnow())[:19] + " (UTC)"
	attrs["comment_area"]       = "The area in the file name is in the form 'lon_min+180'-'lon_max+180'-'lat_min'-'lat_max', i.e. the longitude lives in the range 0/360 to have only positive values. But the longitude coordinate lives in the range -180/180."
	attrs["reference"]     = "Hersbach, H., Bell, B., Berrisford, P., Biavati, G., Horányi, A., Muñoz Sabater, J., Nicolas, J., Peubey, C., Radu, R., Rozum, I., Schepers, D., Simmons, A., Soci, C., Dee, D., Thépaut, J-N. (2018): ERA5 hourly data on single levels from 1979 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). (Accessed on {}), 10.24381/cds.adbb2d47".format(str(dt.datetime.utcnow())[:10])
	return varattrs,timeattrs,latattrs,lonattrs,attrs
##}}}


def build_encoding_daily( var , nlat , nlon ):##{{{
	encoding = { "time" : { "dtype" : "double"  , "zlib" : True , "complevel": 5 , "chunksizes" : (1,) , "units" : "days since 1850-01-01" } ,
				 "lon"  : { "dtype" : "double"  , "zlib" : True , "complevel": 5 , "chunksizes" : (nlon,) } ,
				 "lat"  : { "dtype" : "double"  , "zlib" : True , "complevel": 5 , "chunksizes" : (nlat,) } ,
				 var    : { "dtype" : "float32" , "zlib" : True , "complevel": 5 , "chunksizes" : (1,nlat,nlon) } ,
				}
	
	return encoding
##}}}

def build_encoding_hourly( var , nlat , nlon ):##{{{
	encoding = { "time" : { "dtype" : "double"  , "zlib" : True , "complevel": 5 , "chunksizes" : (1,) , "units" : "hours since 1850-01-01 00:00:00" } ,
				 "lon"  : { "dtype" : "double"  , "zlib" : True , "complevel": 5 , "chunksizes" : (nlon,) } ,
				 "lat"  : { "dtype" : "double"  , "zlib" : True , "complevel": 5 , "chunksizes" : (nlat,) } ,
				 var    : { "dtype" : "float32" , "zlib" : True , "complevel": 5 , "chunksizes" : (1,nlat,nlon) } ,
				}
	
	return encoding
##}}}


def transform_to_daily( avar , l_files , year , logs , **kwargs ):##{{{
	
	## dict to convert ERA5 / AMIP
	evar = CDSparams.AMIP_ERA5[avar]
	
	## Load data
	ldata = []
	for f in l_files:
		dx = xr.open_dataset(f)
		if "expver" in dx:
			dx = dx.sel( expver = 1 ).combine_first( dx.sel( expver = 5 ) )
		ldata.append(dx)
	
	datai = xr.concat( ldata , dim = "time" ).compute()
	
	## First the time axis, check that the last day has the 24 hours
	t_beg = str(datai.time[ 0].values)[:10]
	t_end = str(datai.time[-1].values)[:10]
	data_end = datai.sel( time = t_end )
	t_beg = dt.datetime.fromisoformat(t_beg)
	t_end = dt.datetime.fromisoformat(t_end)
	if data_end.time.size < 24:
		t_end = t_end - dt.timedelta( hours = 1 )
	if t_end < t_beg:
		return
	datai = datai.sel( time = slice(t_beg,t_end) )
	
	## Transform in daily data
	if avar in []:
		data = datai.groupby("time.dayofyear").sum()
	else:
		data = datai.groupby("time.dayofyear").mean()
	
	## Build the time axis
	time = [dt.datetime(year,1,1) + dt.timedelta( days = int(i) - 1 ) for i in data["dayofyear"].values]
	
	## Build latitude / longitude
	lat     = datai.latitude.values
	lon     = datai.longitude.values
	argslat = np.argsort(lat)
	argslon = np.argsort(lon)
	lat     = lat[argslat].copy()
	lon     = lon[argslon].copy()
	
	## Extract array, and change axis order
	arr = data[evar].values[:,argslat,:][:,:,argslon].copy()
	
	if avar in ["zg500"]:
		g = 9.80665
		arr = arr / g
	
	## Back to xarray
	xarr = xr.DataArray( arr , dims = ["time","lat","lon"] , coords = [time,lat,lon] )
	
	## To dataset
	dxarr = xr.Dataset( { avar : xarr } )
	
	## Attributes
	varattrs,timeattrs,latattrs,lonattrs,attrs = build_attrs_daily(avar)
	dxarr[avar].attrs = varattrs
	dxarr.time.attrs = timeattrs
	dxarr.lat.attrs  = latattrs
	dxarr.lon.attrs  = lonattrs
	dxarr.attrs      = attrs
	if not kwargs["area_name"][:3] == "box": del dxarr.attrs["comment_area"]
	
	## Save
	pout = os.path.join( kwargs["tmp"] , "day" , avar )
	if not os.path.isdir(pout):
		os.makedirs(pout)
	t0   = str(time[ 0])[:10].replace("-","")
	t1   = str(time[-1])[:10].replace("-","")
	fout = f"ERA5_{avar}_day_{kwargs['area_name']}_{t0}-{t1}.nc"
	encoding = build_encoding_daily( avar , lat.size , lon.size )
	dxarr.to_netcdf( os.path.join( pout , fout ) , encoding = encoding )
	
	if not avar == "tas":
		return
	
	## Specific case: tasmin / tasmax
	datan = datai.groupby("time.dayofyear").min()
	datax = datai.groupby("time.dayofyear").max()
	
	arrn = datan[evar].values[:,argslat,:][:,:,argslon].copy()
	arrx = datax[evar].values[:,argslat,:][:,:,argslon].copy()
	
	xarrn = xr.DataArray( arrn , dims = ["time","lat","lon"] , coords = [time,lat,lon] )
	xarrx = xr.DataArray( arrx , dims = ["time","lat","lon"] , coords = [time,lat,lon] )
	
	dxarrn = xr.Dataset( { avar + "min" : xarrn } )
	dxarrx = xr.Dataset( { avar + "max" : xarrx } )
	
	varattrs,timeattrs,latattrs,lonattrs,attrs = build_attrs_daily(avar + "min")
	dxarrn[avar + "min"].attrs = varattrs
	dxarrn.time.attrs = timeattrs
	dxarrn.lat.attrs  = latattrs
	dxarrn.lon.attrs  = lonattrs
	dxarrn.attrs      = attrs
	if not kwargs["area_name"][:3] == "box": del dxarrn.attrs["comment_area"]
	
	varattrs,timeattrs,latattrs,lonattrs,attrs = build_attrs_daily(avar + "max")
	dxarrx[avar + "max"].attrs = varattrs
	dxarrx.time.attrs = timeattrs
	dxarrx.lat.attrs  = latattrs
	dxarrx.lon.attrs  = lonattrs
	dxarrx.attrs      = attrs
	if not kwargs["area_name"][:3] == "box": del dxarrx.attrs["comment_area"]
	
	pout = os.path.join( kwargs["tmp"] , "day" , avar + "min" )
	if not os.path.isdir(pout): os.makedirs(pout)
	fout = f"ERA5_{avar}min_day_{kwargs['area_name']}_{t0}-{t1}.nc"
	encoding = build_encoding_daily( avar + "min" , lat.size , lon.size )
	dxarrn.to_netcdf( os.path.join( pout , fout ) , encoding = encoding )
	
	pout = os.path.join( kwargs["tmp"] , "day" , avar + "max" )
	if not os.path.isdir(pout): os.makedirs(pout)
	fout = f"ERA5_{avar}max_day_{kwargs['area_name']}_{t0}-{t1}.nc"
	encoding = build_encoding_daily( avar + "max" , lat.size , lon.size )
	dxarrx.to_netcdf( os.path.join( pout , fout ) , encoding = encoding )
	
##}}}

def transform_to_hourly( avar , l_files , year , logs , **kwargs ):##{{{
	
	## dict to convert ERA5 / AMIP
	evar = CDSparams.AMIP_ERA5[avar]
	
	## Load data
	ldata = []
	for f in l_files:
		dx = xr.open_dataset(f)
		if "expver" in dx:
			dx = dx.sel( expver = 1 ).combine_first( dx.sel( expver = 5 ) )
		ldata.append(dx)
	
	datai = xr.concat( ldata , dim = "time" ).compute()
	
	## First the time axis, check that the last day has the 24 hours
	t_beg = str(datai.time[ 0].values)[:10]
	t_end = str(datai.time[-1].values)[:10]
	data_end = datai.sel( time = t_end )
	t_beg = dt.datetime.fromisoformat(t_beg)
	t_end = dt.datetime.fromisoformat(t_end)
	if data_end.time.size < 24:
		t_end = t_end - dt.timedelta( hours = 1 )
	else:
		t_end = t_end + dt.timedelta( hours = 23 )
	if t_end < t_beg:
		return
	datai = datai.sel( time = slice(t_beg,t_end) )
	
	## Build the time axis
	time = datai.time
	
	## Build latitude / longitude
	lat     = datai.latitude.values
	lon     = datai.longitude.values
	argslat = np.argsort(lat)
	argslon = np.argsort(lon)
	lat     = lat[argslat].copy()
	lon     = lon[argslon].copy()
	
	## Extract array, and change axis order
	arr = datai[evar].values[:,argslat,:][:,:,argslon].copy()
	
	## Back to xarray
	xarr = xr.DataArray( arr , dims = ["time","lat","lon"] , coords = [time,lat,lon] )
	
	## To dataset
	dxarr = xr.Dataset( { avar : xarr } )
	
	## Attributes
	varattrs,timeattrs,latattrs,lonattrs,attrs = build_attrs_hourly(avar)
	dxarr[avar].attrs = varattrs
	dxarr.time.attrs = timeattrs
	dxarr.lat.attrs  = latattrs
	dxarr.lon.attrs  = lonattrs
	dxarr.attrs      = attrs
	if not kwargs["area_name"][:3] == "box": del dxarr.attrs["comment_area"]
	
	## Save
	pout = os.path.join( kwargs["tmp"] , "hour" , avar )
	if not os.path.isdir(pout):
		os.makedirs(pout)
	t0   = str(time[ 0].values)[:10].replace("-","") + "00"
	t1   = str(time[-1].values)[:10].replace("-","") + "23"
	fout = f"ERA5_{avar}_hour_{kwargs['area_name']}_{t0}-{t1}.nc"
	encoding = build_encoding_hourly( avar , lat.size , lon.size )
	dxarr.to_netcdf( os.path.join( pout , fout ) , encoding = encoding )
	
##}}}

def transform_data_format( logs , **kwargs ):##{{{
	
	## Build list of var
	## => remove duplicated var (tas, tasmin and tasmax have the same effect)
	l_var = kwargs["var"]
	for v in ["tasmin","tasmax"]:
		if v in l_var:
			l_var[l_var.index(v)] = "tas"
	l_var = list(set(l_var))
	
	lhourly = "" if not kwargs["keep_hourly"] else " / hourly"
	
	for var in l_var:
		logs.write( f"Build daily{lhourly} {var}" )
		## Path in
		pin = os.path.join( kwargs["tmp"] , "hourERA5" , var )
		
		## List of files
		l_files = [ os.path.join( pin , f ) for f in os.listdir(pin) ]
		l_files.sort()
		
		## Split in years
		d_files = {}
		for f in l_files:
			y = f.split("_")[-1][:4]
			if y not in d_files:
				d_files[y] = []
			d_files[y].append(f)
		
		## Now loop on years
		for y in d_files:
			logs.write( f"   * '{y}'" )
			transform_to_daily( var , d_files[y] , int(y) , logs , **kwargs )
			if kwargs["keep_hourly"]:
				transform_to_hourly( var , d_files[y] , int(y) , logs , **kwargs )
			
	logs.writeline()
##}}}


