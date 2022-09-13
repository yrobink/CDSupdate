

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

import cdsapi

import numpy  as np
import xarray as xr

#############
## Imports ##
#############

from .__CDSparams import CDSparams

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
	dbreak  = 14
	t_break = t_now - dt.timedelta( days = dbreak )
	logs.write( f"Break found: {t_break} (now - {dbreak} days)" )
	
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

def load_data_cdsapi( l_CDSAPIParams , logs , **kwargs ):##{{{
	
	## TODO add key url to optional user input
	
	## Build area
	lon_min,lon_max,lat_min,lat_max = kwargs["area"]
	area = [lat_max,lon_min,lat_min,lon_max]
	
	## cdsapi base params
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
			
			level = CDSparams.level(var)
			if cap[1].year < 1959:
				name = f"reanalysis-era5-{level}-levels-preliminary-back-extension"
			else:
				name = f"reanalysis-era5-{level}-levels"
			
			## Merge base params and time params
			params = { **bparams , **cap[0] }
			
			if level == "pressure":
				params = { **params , **{"pressure_level" : str(CDSparams.level_value(var))} }
			
			## Add variable
			params["variable"] = CDSparams.AMIP_CDS[var]
			
			## Path out
			pout = os.path.join( kwargs["tmp"] , "hourERA5" , var )
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


