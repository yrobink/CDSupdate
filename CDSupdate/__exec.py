
## Copyright(c) 2022, 2023 Yoann Robin
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

import cdsapi

import numpy  as np
import pandas as pd
import xarray as xr
import netCDF4


#############
## Imports ##
#############

from .__CDSUParams import cdsuParams
from .__release    import version

from .__exceptions import AbortForHelpException

from .__io import load_data_CDS
from .__io import BRUT_to_AMIP_format
from .__io import merge_AMIP_CF_format
from .__extracvars import build_EXTRA_cvars

from .__curses_doc import print_doc


##################
## Init logging ##
##################

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


###############
## Functions ##
###############


def run_cdsupdate():##{{{
	"""
	CDSupdate.run_cdsupdate
	=======================
	
	Main execution, after the control of user input.
	
	"""
	
	## Start by split in yearly / monthly tasks
	cdsuParams.build_CDSAPIParams()
	logger.info( "Periods found to download:" )
	for key in cdsuParams.cdsApiParams:
		logger.info( " * {} / {}".format(*key) )
	
	## Download data
	load_data_CDS()
	
	## Change data format
	BRUT_to_AMIP_format()
	
	## Extra variables
	build_EXTRA_cvars()
	
	## And now merge with current data
	merge_AMIP_CF_format()
	
##}}}

def start_cdsupdate( argv ):##{{{
	"""
	CDSupdate.start_cdsupdate
	=========================
	
	Starting point of 'cdsupdate'.
	
	"""
	
	
	## Time counter
	walltime0 = dt.datetime.utcnow()
	
	## Read input
	cdsuParams.init_from_user_input(*argv)
	
	## Init logs
	cdsuParams.init_logging()
	
	## Logging
	logger.info(cdsuParams.LINE)
	logger.info( r"   ____ ____  ____                  _       _        " ) 
	logger.info( r"  / ___|  _ \/ ___| _   _ _ __   __| | __ _| |_ ___  " )
	logger.info( r" | |   | | | \___ \| | | | '_ \ / _` |/ _` | __/ _ \ " )
	logger.info( r" | |___| |_| |___) | |_| | |_) | (_| | (_| | ||  __/ " )
	logger.info( r"  \____|____/|____/ \__,_| .__/ \__,_|\__,_|\__\___| " )
	logger.info( r"                         |_|                         " )
	logger.info(cdsuParams.LINE)
	logger.info( "Start: {}".format( str(walltime0)[:19] + " (UTC)") )
	logger.info(cdsuParams.LINE)
	
	## Package version
	pkgs = [("numpy"      , np ),
	        ("pandas"     , pd ),
	        ("xarray"     , xr ),
	        ("netCDF4"    , netCDF4 )
	       ]
	
	logger.info( "Packages version:" )
	logger.info( " * {:{fill}{align}{n}}".format( "CDSupdate" , fill = " " , align = "<" , n = 12 ) + f"version {version}" )
	for name_pkg,pkg in pkgs:
		logger.info( " * {:{fill}{align}{n}}".format( name_pkg , fill = " " , align = "<" , n = 12 ) +  f"version {pkg.__version__}" )
	logger.info(cdsuParams.LINE)
	
	## Serious functions start here
	try:
		## Check inputs
		cdsuParams.check()
		
		## Init temporary
		cdsuParams.init_tmp()
		
		## List of all input
		logger.info("Input parameters:")
		for key in cdsuParams.keys():
			if key in ["LINE"]: continue
			logger.info( " * {:{fill}{align}{n}}".format( key , fill = " ",align = "<" , n = 10 ) + ": {}".format(cdsuParams[key]) )
		logger.info(cdsuParams.LINE)
		
		## If abort, stop execution
		if cdsuParams.abort:
			raise cdsuParams.error
		
		## Go
		run_cdsupdate()
		
	except AbortForHelpException:
		print_doc()
	except Exception as e:
		logger.error( f"Error: {e}" )
	
	## End
	walltime1 = dt.datetime.utcnow()
	logger.info(cdsuParams.LINE)
	logger.info( "End: {}".format(str(walltime1)[:19] + " (UTC)") )
	logger.info( "Wall time: {}".format(walltime1 - walltime0) )
	logger.info(cdsuParams.LINE)
##}}}

