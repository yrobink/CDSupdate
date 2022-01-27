
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

import os
import datetime as dt


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
	kwargs = { "clog": False , "help" : False }
	
	## Start by read input parameters
	##===============================
	for i,arg in enumerate(argv):
		
		if arg in ["--log"]:
			try:
				kwargs["log"] = argv[i+1]
			except:
				future_logs.append("Parameter '--log' is used without output file, abort.")
				abort = True
		if arg in ["--clog"]:
			kwargs["clog"] = True
		if arg in ["--period"]:
			try:
				kwargs["period"] = argv[i+1]
			except:
				future_logs.append("Parameter '--period' is used without the period, abort.")
				abort = True
		if arg in ["--var"]:
			try:
				kwargs["var"] = argv[i+1]
			except:
				future_logs.append("Parameter '--var' is used without the list of variables, abort.")
				abort = True
		if arg in ["--area"]:
			try:
				kwargs["area"] = argv[i+1]
			except:
				future_logs.append("Parameter '--area' is used without the area, abort.")
				abort = True
		if arg in ["--odir"]:
			try:
				kwargs["odir"] = argv[i+1]
			except:
				future_logs.append("Parameter '--odir' is used without output directory, abort.")
				abort = True
		if arg in ["--help"]:
			kwargs["help"] = True
			abort = True
	
	## Define the log
	##===============
	if kwargs["clog"]:
		kwargs["log"] = "console"
	if kwargs.get("log") is not None and not kwargs["log"] == "console":
		logpath = os.path.dirname(os.path.abspath(kwargs["log"]))
		if not os.path.isdir(logpath):
			future_logs.append("The log path '{}' is not a path, back to the console and abort.".format(logpath))
			kwargs["log"] = "console"
			abort = True
	logs = LogFile(kwargs.get("log"))
	
	for log in future_logs:
		if log == "LINE":
			logs.writeline()
		else:
			logs.write(log)
	
	## First abort
	##============
	if abort:
		return kwargs,logs,abort
	
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
			area = [float(x) for x in kwargs["area"].split(",")]
			if not len(area) == 4:
				raise ValueError
			lon_min,lon_max,lat_min,lat_max = area
			area_name = "box-{:,g}-{:,g}-{:,g}-{:,g}".format(lon_min+180,lon_max+180,lat_min,lat_max)
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
	
	##
	logs.writeline()
	
	return kwargs,logs,abort


