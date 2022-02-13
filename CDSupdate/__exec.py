
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

###############
## Functions ##
###############

def build_yearly_CDSAPIParams( t0 , t1 = None , logs = None ):##{{{
	"""
	CDSupdate.build_yearly_CDSAPIParams
	===================================
	
	Same as CDSupdate.build_yearly_CDSAPIParams, but assume that t0 and t1
	are in the same year.
	
	"""
	months = ["{:{fill}{align}{n}}".format(i+1,fill="0",align=">",n=2) for i in range(12)]
	days   = ["{:{fill}{align}{n}}".format(i+1,fill="0",align=">",n=2) for i in range(31)]
	hours  = ["{:{fill}{align}{n}}:00".format(i,fill="0",align=">",n=2) for i in range(24)]
	
	## Case 1: only one day
	if t1 is None:
		logs.write( f"   * {t0}" )
		p = { "year"  : f"{t0.year}" ,
		      "month" :  "{}".format(months[t0.month-1]),
		      "day"   :  "{}".format(days[t0.day-1]),
		      "time"  : hours
		    }
		return [(p,t0,None)]
	
	## Case 2: all the year
	if t0.month == 1 and t0.day == 1 and t1.month == 12 and t1.day == 31:
		logs.write( f"   * {t0} / {t1}" )
		p = { "year"  : f"{t0.year}" ,
		      "month" : months,
		      "day"   : days,
		      "time"  : hours
		    }
		return [(p,t0,t1)]
	
	## Case 3: all f*****g others cases
	is_end_of_month = lambda t: ( t + dt.timedelta(days=1) ).day == 1
	if t0.month == t1.month:
		logs.write( f"   * {t0} / {t1}" )
		p = { "year"  : f"{t0.year}" ,
		      "month" : "{}".format(months[t0.month-1]),
		      "day"   : days[(t0.day-1):t1.day], ##days[(t0.day-1):(t1.day-1+1)]
		      "time"  : hours
		    }
		return [(p,t0,t1)]
	if t0.day == 1 and is_end_of_month(t1):
		logs.write( f"   * {t0} / {t1}" )
		p = { "year"  : f"{t0.year}" ,
		      "month" : months[(t0.month-1):t1.month], ##months[(t0.month-1):(t1.month-1+1)]
		      "day"   : days,
		      "time"  : hours
		    }
		return [(p,t0,t1)]
	elif t0.day == 1 and not is_end_of_month(t1): ## From here, t0.month < t1.month
		t1mr = dt.datetime( t1.year , t1.month , 1 )
		t1ml = t1mr - dt.timedelta(days=1)
		lp_l = build_yearly_CDSAPIParams( t0   , t1ml , logs )
		lp_r = build_yearly_CDSAPIParams( t1mr , t1   , logs )
		return lp_l + lp_r
	elif t0.day > 1 and is_end_of_month(t1):
		t1mr = dt.datetime( t0.year , t0.month + 1 , 1 )
		t1ml = t1mr - dt.timedelta(days=1)
		lp_l = build_yearly_CDSAPIParams( t0   , t1ml , logs )
		lp_r = build_yearly_CDSAPIParams( t1mr , t1   , logs )
		return lp_l + lp_r
	else:
		t1mr = dt.datetime( t0.year , t0.month + 1 , 1 )
		t1ml = t1mr - dt.timedelta(days=1)
		lp_l = build_yearly_CDSAPIParams( t0   , t1ml , logs )
		lp_r = build_yearly_CDSAPIParams( t1mr , t1   , logs )
		return lp_l + lp_r
##}}}

def build_CDSAPIParams( period , logs ):##{{{
	"""
	CDSupdate.build_CDSAPIParams
	============================
	
	This function is used to transform the period (date_start,date_end) in
	cdsapi time params, i.e. a dict of the form:
	
	>>> {
	>>> "year"  : ["2015",...],
	>>> "month" : ["01","02",...],
	>>> "day"   : ["01","02",...]
	>>> "time"  : ["00:00","01:00",...]
	>>> }
	
	The problem is to cut the period to download only required data. For example,
	the period ("2015-01-07","2015-03-17") is splitted in a list of three
	dict:
	- One for the period ("2015-01-07","2015-01-31"), because the first days are
	  not required,
	- One for the period ("2015-02-01","2015-02-28"), all days of the month,
	- One for the period ("2015-03-01","2015-03-17"), because the last days are
	  not required,
	
	Furthermore, a "break" is introduced 30 days before "now", and all values
	after this date are downloaded only day by day. This is due to a problem
	of the format of the netcdf file from ERA5 for values too close from now.
	This problem can be solved by downloading daily values.
	
	"""
	
	logs.writeline()
	logs.write( "Build yearly period" )
	
	## Split in yearly time, and find the break
	t0 = dt.datetime.fromisoformat(period[0])
	t1 = dt.datetime.fromisoformat(period[1])
	year0 = t0.year
	year1 = t1.year
	
	t_now   = dt.datetime.utcnow()
	t_now   = dt.datetime( t_now.year , t_now.month , t_now.day )
	t_break = t_now - dt.timedelta( days = 30 )
	logs.write( f"Break found: {t_break} (now - 30 days)" )
	
	## Loop on year
	logs.write( "Periods to download:" )
	l_CDSAPIParams = []
	for year in range(year0,year1+1,1):
		
		## Find the bound [ty0;ty1] into the current year
		tby0 = dt.datetime( year ,  1 ,  1 )
		tby1 = dt.datetime( year , 12 , 31 )
		
		if tby0 >= t0 and tby1 <= t1:
			ty0 = tby0
			ty1 = tby1
		elif tby0 < t0 and tby1 <= t1:
			ty0 = t0
			ty1 = tby1
		elif tby0 >= t0 and tby1 > t1:
			ty0 = tby0
			ty1 = t1
		else:
			ty0 = t0
			ty1 = t1
		
		## Now we build yearly params
		if ty1 < t_break:
			l_CDSAPIParams += build_yearly_CDSAPIParams( ty0 , ty1 , logs )
		elif ty0 < t_break and t_break <= ty1:
			l_CDSAPIParams += build_yearly_CDSAPIParams( ty0 , t_break , logs )
			t = t_break + dt.timedelta(days=1)
			while t <= ty1:
				l_CDSAPIParams += build_yearly_CDSAPIParams( t , logs = logs )
				t += dt.timedelta(days=1)
		else:
			t = ty0
			while t <= t1:
				l_CDSAPIParams += build_yearly_CDSAPIParams( t , logs = logs )
				t += dt.timedelta(days=1)
	
	logs.writeline()
	return l_CDSAPIParams
##}}}


def build_name_AMIP_ERA5():##{{{
	name_AMPI2ERA5 = { "tas" : "t2m" }
	name_ERA52AMIP = {}
	for avar in name_AMPI2ERA5:
		name_ERA52AMIP[name_AMPI2ERA5[avar]] = avar
	
	return name_AMPI2ERA5,name_ERA52AMIP
##}}}

def build_name_AMIP_CDSAPI():##{{{
	name_AMPI2ERA5 = { "tas" : "2m_temperature" }
	name_ERA52AMIP = {}
	for avar in name_AMPI2ERA5:
		name_ERA52AMIP[name_AMPI2ERA5[avar]] = avar
	
	return name_AMPI2ERA5,name_ERA52AMIP
##}}}

def load_data_cdsapi( l_CDSAPIParams , logs , **kwargs ):##{{{
	
	## TODO replace tmp var by a user defined path
	## TODO add key url to optional user input
	## TODO name_AMIP2ERA5 in independent function
	## TODO ERA5 before after 1978
	
	name_AMPI2ERA5,name_ERA52AMIP = build_name_AMIP_CDSAPI()
	
	## Build area
	lon_min,lon_max,lat_min,lat_max = kwargs["area"]
	area = [lat_max,lon_min,lat_min,lon_max]
	
	## cdsapi base params
	name    = "reanalysis-era5-single-levels"
	bparams = { "product_type" : "reanalysis",
	           "format"        : "netcdf",
	           "area"          : area
	           }
	
	## Build list of var
	## => remove duplicated var (tas, tasmin and tasmax have the same effect)
	l_var = kwargs["var"]
	for v in ["tasmin","tasmax"]:
		if v in l_var:
			l_var[l_var.index(v)] = "tas"
	l_var = list(set(l_var))
	
	## cdsapi client params
	key = None
	url = None
	verify = None
	
	## Loop
	for var in l_var:
		logs.write( f"Download data '{var}'" )
		for cap in l_CDSAPIParams:
			
			## Merge base params and time params
			params = { **bparams , **cap[0] }
			
			## Add variable
			params["variable"] = name_AMPI2ERA5[var]
			
			## Path out
			pout = os.path.join( kwargs["odir"] , "tmp" , var , "hour" )
			if not os.path.isdir(pout):
				os.makedirs(pout)
			
			# File out
			t0 = str(cap[1])[:10].replace("-","") + "00"
			if cap[2] is None:
				t1 = t0[:-2] + "23"
			else:
				t1 = str(cap[2])[:10].replace("-","") + "23"
			fout = f"ERA5_{var}_hour_{kwargs['area_name']}_{t0}-{t1}.nc"
			logs.write( f"   * Period {t0}/{t1}" )
			
			## Download
			try:
				client = cdsapi.Client( key = key , url = url , verify = verify , quiet = True )
				client.retrieve( name , params , os.path.join( pout , fout ) )
			except Exception as e:
				logs.write( f"      => Warning '{e}', data not used." )
				## Data almost surely not available, but if the exception is due
				## to another problems, it is prefereable to remove the file,
				## cdsapi just raises a generic Exception, not a specific
				## Exception
				if os.path.isfile( os.path.join( pout , fout ) ):
					os.remove( os.path.join( pout , fout ) )
	
	logs.writeline()
	
##}}}


def build_attrs(var): ##{{{
	
	## Start with variables attributes
	varattrs = {}
#	varattrs["coordinates"]   = "lat lon"
	
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
	encoding = { "time" : { "dtype" : "int32"   , "zlib" : True , "complevel": 5 , "chunksizes" : (1,) , "units" : "days since 1850-01-01" } ,
				 "lon"  : { "dtype" : "float32" , "zlib" : True , "complevel": 5 , "chunksizes" : (nlon,) } ,
				 "lat"  : { "dtype" : "float32" , "zlib" : True , "complevel": 5 , "chunksizes" : (nlat,) } ,
				 var    : { "dtype" : "float32" , "zlib" : True , "complevel": 5 , "chunksizes" : (1,nlat,nlon) } ,
				}
	
	return encoding
##}}}


def transform_to_daily( avar , l_files , year , logs , **kwargs ):##{{{
	
	## dict to convert ERA5 / AMIP
	name_AMPI2ERA5,name_ERA52AMIP = build_name_AMIP_ERA5()
	evar = name_AMPI2ERA5[avar]
	
	## Load data
	datai = xr.concat( [xr.load_dataset(f) for f in l_files] , dim = "time" )
	
	## First the time axis, check that the last day has the 24 hours
	t_beg = str(datai.time[ 0].values)[:10]
	t_end = str(datai.time[-1].values)[:10]
	data_end = datai.sel( time = t_end )
	t_beg = dt.datetime.fromisoformat(t_beg)
	t_end = dt.datetime.fromisoformat(t_end)
	if data_end.time.size < 24:
		t_end = t_end - dt.timedelta( days = 1 )
	if t_end < t_beg:
		return
	datai = datai.sel( time = slice(t_beg,t_end) )
	
	## Transform in daily data
	if avar in ["tas"]:
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
	
	## Back to xarray
	xarr = xr.DataArray( arr , dims = ["time","lat","lon"] , coords = [time,lat,lon] )
	
	## To dataset
	dxarr = xr.Dataset( { avar : xarr } )
	
	## Attributes
	varattrs,timeattrs,latattrs,lonattrs,attrs = build_attrs(avar)
	dxarr[avar].attrs = varattrs
	dxarr.time.attrs = timeattrs
	dxarr.lat.attrs  = latattrs
	dxarr.lon.attrs  = lonattrs
	dxarr.attrs      = attrs
	
	## Save
	pout = os.path.join( kwargs["odir"] , "tmp" , avar , "day" )
	if not os.path.isdir(pout):
		os.makedirs(pout)
	t0   = str(time[ 0])[:10].replace("-","")
	t1   = str(time[-1])[:10].replace("-","")
	fout = f"ERA5_{avar}_day_{kwargs['area_name']}_{t0}-{t1}.nc"
	encoding = build_encoding( avar , lat.size , lon.size )
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
	
	varattrs,timeattrs,latattrs,lonattrs,attrs = build_attrs(avar + "min")
	dxarrn[avar + "min"].attrs = varattrs
	dxarrn.time.attrs = timeattrs
	dxarrn.lat.attrs  = latattrs
	dxarrn.lon.attrs  = lonattrs
	dxarrn.attrs      = attrs
	
	varattrs,timeattrs,latattrs,lonattrs,attrs = build_attrs(avar + "max")
	dxarrx[avar + "max"].attrs = varattrs
	dxarrx.time.attrs = timeattrs
	dxarrx.lat.attrs  = latattrs
	dxarrx.lon.attrs  = lonattrs
	dxarrx.attrs      = attrs
	
	pout = os.path.join( kwargs["odir"] , "tmp" , avar + "min" , "day" )
	if not os.path.isdir(pout): os.makedirs(pout)
	fout = f"ERA5_{avar}min_day_{kwargs['area_name']}_{t0}-{t1}.nc"
	encoding = build_encoding( avar + "min" , lat.size , lon.size )
	dxarrn.to_netcdf( os.path.join( pout , fout ) , encoding = encoding )
	
	pout = os.path.join( kwargs["odir"] , "tmp" , avar + "max" , "day" )
	if not os.path.isdir(pout): os.makedirs(pout)
	fout = f"ERA5_{avar}max_day_{kwargs['area_name']}_{t0}-{t1}.nc"
	encoding = build_encoding( avar + "max" , lat.size , lon.size )
	dxarrx.to_netcdf( os.path.join( pout , fout ) , encoding = encoding )
	
##}}}

def transform_data_format( logs , **kwargs ):##{{{
	
	## Build list of var
	## => remove duplicated var (tas, tasmin and tasmax have the same effect)
	l_var = kwargs["var"]
	for v in ["tasmin","tasmax"]:
		if v in l_var:
			l_var[l_var.index(v)] = "tas"
	l_var = list(set(l_var))
	
	for var in l_var:
		## Path out
		pout = os.path.join( kwargs["odir"] , "tmp" , var , "hour" )
		
		## List of files
		l_files = [ os.path.join( pout , f ) for f in os.listdir(pout) ]
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
			transform_to_daily( var , d_files[y] , int(y) , logs , **kwargs )
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
	transform_data_format( logs , **kwargs )
	
	
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

