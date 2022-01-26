
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

#############
## Imports ##
#############

from .__logs import LogFile


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
	if abort:
		return kwargs,logs,abort
	
	## Control if required parameters are given
	l_req = ["period","var","area","odir"]
	l_giv = list( set(l_req) & set(kwargs) )
	l_mis = [req for req in l_req if not req in l_giv]
	n_mis = len(l_mis)
	if n_mis > 0:
		logs.write( "Required input '{}' not given, abort.".format(", ".join(l_mis)) )
		return kwargs,logs,abort
	
	## Control if required parameters are CORRECTLY given
	
	
	
	return kwargs,logs,abort


