
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

from .__download import build_CDSAPIParams
from .__download import load_data_cdsapi

from .__convert import transform_data_format


###############
## Functions ##
###############

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
	
	## And now merge with current data
	##================================
	
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

