
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

import os
import datetime as dt
import random
import string


#############
## Imports ##
#############

from .__logs       import LogFile
from .__CDSparams  import CDSparams

from .__exceptions import CDSInputPeriodSizeError
from .__exceptions import CDSInputPeriodOrderError


###############
## Functions ##
###############

def read_input( argv , future_logs ):
	"""
	CDSupdate.read_input
	====================
	
	Function which transforms user input to a dict of parameters.
	
	Arguments
	---------
	argv [tuple]
		Tuple of input: sys.argv
	future_logs [list]
		Future logs to write
	
	Return
	------
	kwargs [dict]
		Dict of parameters
	logs [CDSupdate.LogFile]
		Log system
	abort [bool]
		False if all inputs are valid, True otherwise.
	"""
	abort  = False
	kwargs = { "clog" : False , "keep_hourly" : False , "help" : False , "keep_tmp" : False }
	
	## Start by read input parameters
	##===============================
	
	## Control if required parameters are given
	##=========================================
	l_req = ["period","var","area","odir"]
	l_giv = list( set(l_req) & set(kwargs) )
	l_mis = [req for req in l_req if not req in l_giv]
	n_mis = len(l_mis)
	if n_mis > 0:
		logs.write( "Required input '{}' not given, abort.".format(", ".join(l_mis)) )
		return kwargs,logs,abort
	
	## Control if required parameters are CORRECTLY given
	##===================================================
	
	## Area
	if kwargs["area"] in CDSparams.available_area:
		kwargs["area_name"] = kwargs["area"]
		kwargs["area"]      = CDSparams.available_area[kwargs["area"]]
	else:
		try:
			area_name = kwargs["area"].split(",")[0]
			area = [float(x) for x in kwargs["area"].split(",")[1:]]
			if not len(area) == 4:
				raise ValueError
			lon_min,lon_max,lat_min,lat_max = area
			kwargs["area"]      = area
			kwargs["area_name"] = area_name
		except:
			logs.write( "Error: 'area={}' not in the format lon_min,lon_max,lat_min,lat_max. Abort.".format(kwargs["area"]) )
			abort = True
	
	## Variable
	l_vars = kwargs["var"].split(",")
	
	for var in l_vars:
		if var not in CDSparams.available_vars:
			logs.write( f"Error: variable '{var}' not available. Abort." )
			abort = True
	kwargs["var"] = l_vars
	
	## Period
	try:
		l_dates = [ dt.datetime.fromisoformat(date) for date in kwargs["period"].split("/") if len(date) > 0]
		if len(l_dates) == 1:
			l_dates.append( dt.datetime.utcnow() )
		if len(l_dates) > 2:
			raise CDSInputPeriodSizeError
		if not l_dates[0] <= l_dates[1]:
			raise CDSInputPeriodOrderError
		kwargs["period"] = [ date.isoformat()[:10] for date in l_dates ] ## Keep only the day, all days will be downloaded
	except ValueError:
		logs.write( f"Error: dates of the period are not in the iso format. Abort." )
		abort = True
	except CDSInputPeriodSizeError:
		logs.write( "Error: too many periods in the period input. Abort." )
		abort = True
	except CDSInputPeriodOrderError:
		logs.write( "Error: in the period, the first date is greater than the second. Abort." )
		abort = True
	
	## odir
	try:
		if not os.path.isdir(kwargs["odir"]):
			raise NotADirectoryError
	except NotADirectoryError:
		logs.write( "Error: the output directory {} is not valid. Abort.".format(kwargs["odir"]) )
		abort = True
	
	
	try:
		if kwargs.get("tmp") is not None and not os.path.isdir(kwargs["tmp"]):
			raise NotADirectoryError
		if kwargs.get("tmp") is None:
			tmp = os.path.join( os.environ["WORKDIR"] , "JOB_CDSupdate_" + "".join( random.choices( string.ascii_uppercase + string.digits , k = 30 ) ) )
			os.makedirs(tmp)
			kwargs["tmp"] = tmp
			
	except NotADirectoryError:
		logs.write( "Error: the temporary directory {} is not valid. Abort.".format(kwargs["tmp"]) )
		abort = True
	except KeyError:
		logs.write( f"Error: the input '--tmpdir' and the environment variable 'WORKDIR' are not set simultaneously. Abort." )
		abort = True
	
	
	##
	logs.writeline()
	
	return kwargs,logs,abort


