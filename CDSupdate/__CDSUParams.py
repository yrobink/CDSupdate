
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


#############
## Imports ##
#############

from __future__ import annotations

import sys
import os
import argparse
import tempfile
import logging
import datetime as dt
import dataclasses

import numpy  as np
import xarray as xr
import pandas as pd

from .__exceptions  import AbortForHelpException

from .__CVarsParams import CVarsParams
from .__CVarsParams import cvarsParams


###############
## Variables ##
###############


@dataclasses.dataclass
class CDSUParams:
	
	abort : bool                = False
	error : Exception | None    = None
	help  : bool                = False
	log   : tuple[str,str|None] = ("WARNING",None)
	LINE  : str                 = "=" * 80
	
	tmp_base : str | None                         = None
	tmp_gen  : tempfile.TemporaryDirectory | None = None
	tmp      : str | None                         = None
	
	cvars       : str | list[str] | None = None
	cvars_dwl   : str | list[str] | None = None
	cvars_cmp   : str | list[str] | None = None
	cvars_lev   : str | list[str] | None = None
	area        : str             | None = None
	area_name   : str             | None = None
	period      : str             | None = None
	output_dir  : str             | None = None
	keep_hourly : bool                   = False
	
	cvarsParams  : CVarsParams   = cvarsParams
	cdsApiParams : dict | None = None
	
	def init_from_user_input( self , *argv ):##{{{
		
		argv = list(argv)
		## Special case of area
		if "--area" in argv:
			idx = argv.index("--area") + 1
			if len(argv) > idx and argv[idx][0] == "-":
				argv[idx] = " " + argv[idx]
		
		## Parser for user input
		parser = argparse.ArgumentParser( add_help = False )
		
		parser.add_argument( "-h" , "--help" , action = "store_const" , const = True , default = False )
		parser.add_argument( "--log" , nargs = '*' , default = ("WARNING",None) )
		parser.add_argument( "--tmp" , default = None )
		
		parser.add_argument( "--cvars"  , default = None )
		parser.add_argument( "--area"   , default = None )
		parser.add_argument( "--period" , default = None )
		parser.add_argument( "--output-dir"  , default = None )
		parser.add_argument( "--keep-hourly" , action = "store_const" , const = True , default = False )
		
		## Transform in dict
		kwargs = vars(parser.parse_args(argv))
		
		## And store in the class
		for key in kwargs:
			if key not in self.__dict__:
				raise Exception("Parameter not present in the class")
			self.__dict__[key] = kwargs[key]
			
		
	##}}}
	
	def init_tmp(self):##{{{
		
		if self.tmp is None:
			self.tmp_base = tempfile.gettempdir()
		else:
			self.tmp_base = self.tmp
		
		now               = str(dt.datetime.utcnow())[:19].replace("-","").replace(":","").replace(" ","-")
		prefix            = f"CDSUPDATE_{now}_"
		self.tmp_gen      = tempfile.TemporaryDirectory( dir = self.tmp_base , prefix = prefix )
		self.tmp          = self.tmp_gen.name
	##}}}
	
	def init_logging(self):##{{{
		
		if len(self.log) == 0:
			self.log = ("INFO",None)
		elif len(self.log) == 1:
			
			try:
				level = int(self.log[0])
				lfile = None
			except:
				try:
					level = getattr( logging , self.log[0].upper() , None )
					lfile = None
				except:
					level = "INFO"
					lfile = self.log[0]
			self.log = (level,lfile)
		
		level,lfile = self.log
		
		## loglevel can be an integet
		try:
			level = int(level)
		except:
			level = getattr( logging , level.upper() , None )
		
		## If it is not an integer, raise an error
		if not isinstance( level , int ): 
			raise UserDefinedLoggingLevelError( f"Invalid log level: {level}; nothing, an integer, 'debug', 'info', 'warning', 'error' or 'critical' expected" )
		
		##
		log_kwargs = {
			"format" : '%(message)s',
#			"format" : '%(levelname)s:%(name)s:%(funcName)s: %(message)s',
			"level"  : level
			}
		
		if lfile is not None:
			log_kwargs["filename"] = lfile
		
		logging.basicConfig(**log_kwargs)
		logging.captureWarnings(True)
		
	##}}}
	
	def check( self ): ##{{{
		
		try:
			## If help, stop
			if self.help:
				raise AbortForHelpException
			
			## Test of the output dir exist
			if self.output_dir is None:
				raise Exception("Output directory must be given!")
			self.output_dir = os.path.split(self.output_dir)[0]
			if not os.path.isdir(self.output_dir):
				raise Exception( f"Output directory {self.output_dir} is not a path!" )
			if self.output_dir.split(os.path.sep)[-1] == "ERA5":
				self.output_dir = os.path.sep.join( self.output_dir.split(os.path.sep)[:-1] )
			
			## Test if the tmp directory exists
			if self.tmp is not None:
				if not os.path.isdir(self.tmp):
					raise Exception( f"The temporary directory {self.tmp} is given, but doesn't exists!" )
			
			## Now cvars
			if self.cvars is None:
				raise Exception( f"List of climate variables is empty" )
			self.cvars = self.cvars.split(",")
			for cvar in self.cvars:
				if not self.cvarsParams.is_available(cvar):
					raise Exception( f"The cvar {cvar} is not supported" )
			dwl,cmp,lev = self.cvarsParams.cvars_from_request(self.cvars)
			self.cvars_dwl = dwl
			self.cvars_cmp = cmp
			self.cvars_lev = lev
			
			## The area
			if self.area is None:
				raise Exception( f"Area not given!" )
			self.area = self.area.split(",")
			if len(self.area) == 5:
				self.area_name = self.area[0]
				self.area      = self.area[1:]
			elif len(self.area) == 1:
				self.area_name = self.area[0]
				if not self.area_name in self.cvarsParams.available_area:
					raise Exception( f"Area {self.area_name} is not available" )
				self.area = self.cvarsParams.available_area[self.area_name]
			elif not len(self.area) == 4:
				raise Exception( f"Invalid format for area!")
			
			try:
				self.area = [float(s) for s in self.area]
			except:
				raise Exception( f"Bound of area not castable to float {self.area}" )
			
			if self.area_name is None:
				lon0,lon1,lat0,lat1 = self.area
				self.area_name = "area-{:,g}-{:,g}-{:,g}-{:,g}".format(lon0+180,lon1+180,lat0+90,lat1+90)
			
			## And finally the period
			if self.period is None:
				raise Exception( f"Period not given!" )
			self.period = self.period.split("/")
			if len(self.period) == 1:
				self.period.append( str(dt.datetime.utcnow())[:10] )
			try:
				self.period = [dt.datetime.fromisoformat(t) for t in self.period]
			except:
				raise Exception( f"Invalid format for period, use isoformat! (YYYY-MM-DD)" )
			if not self.period[0] < self.period[1]:
				raise Exception( f"Start period greater than the end!" )
			
			
		except Exception as e:
			self.abort = True
			self.error = e
		
		
	##}}}
	
	def keys(self):##{{{
		keys = [key for key in self.__dict__]
		keys.sort()
		return keys
	##}}}
	
	def __getitem__( self , key ):##{{{
		return self.__dict__.get(key)
	##}}}
	
	def _period_to_CDSAPI( self , tl , tr , all_year = False ):##{{{
		
		## Global parameters
		months = ["{:{fill}{align}{n}}".format(i+1,fill="0",align=">",n=2) for i in range(12)]
		days   = ["{:{fill}{align}{n}}".format(i+1,fill="0",align=">",n=2) for i in range(31)]
		hours  = ["{:{fill}{align}{n}}:00".format(i,fill="0",align=">",n=2) for i in range(24)]
		
		##
		year = tl[:4]
		if all_year:
			p = { "year"  : year,
			      "month" : months,
			      "day"   : days,
			      "time"  : hours
			    }
			return p
		
		##
		month = tl[5:7]
		dtl   = dt.datetime.fromisoformat(tl)
		dtr   = dt.datetime.fromisoformat(tr)
		if dtl.day == 1 and not (dtr.month == (dtr + dt.timedelta( days = 1 )).month):
			p = { "year"  : year,
			      "month" : month,
			      "day"   : days,
			      "time"  : hours
			    }
		else:
			p = { "year"  : year,
			      "month" : month,
			      "day"   : ["{:{fill}{align}{n}}".format(d,fill="0",align=">",n=2) for d in range(dtl.day,dtr.day+1,1)],
			      "time"  : hours
			    }
		return p
	##}}}
	
	def build_CDSAPIParams(self):##{{{
		
		t0,t1 = self.period
		time  = pd.date_range(t0,t1)
		time  = xr.DataArray( time.values , dims = ["time"] , coords = [time.values] )
		
		## Loop on year
		cdsApiParams = {}
		for year in np.unique(time.dt.year):
			
			## Select only the year
			timeY = time.groupby("time.year")[year]
			
			## Check if year is complete
			if timeY.dt.month[0] == 1 and timeY.dt.day[0] == 1 and timeY.dt.month[-1] == 12 and timeY.dt.day[-1] == 31:
				tl = str(timeY[ 0].values)[:10]
				tr = str(timeY[-1].values)[:10]
				cdsApiParams[(tl,tr)] = self._period_to_CDSAPI( tl , tr , True )
				continue
			
			## Not complete, so loop on month
			for month in np.unique(timeY.dt.month):
				timeM = timeY.groupby("time.month")[month]
				tl    = str(timeM[ 0].values)[:10]
				tr    = str(timeM[-1].values)[:10]
				cdsApiParams[(tl,tr)] = self._period_to_CDSAPI( tl , tr )
		
		self.cdsApiParams = cdsApiParams
	##}}}

cdsuParams = CDSUParams()



