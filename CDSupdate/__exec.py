
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


#############
## Imports ##
#############

from .__release import version
from .__doc     import doc
from .__input   import read_input

###############
## Functions ##
###############

class YearlyTask:##{{{
	def __init__( self , year , t0 , t1 , t_break ):
		
		self.t_break = t_break
		ty0 = dt.datetime( year ,  1 ,  1 )
		ty1 = dt.datetime( year , 12 , 31 )
		
		if ty0 >= t0 and ty1 <= t1:
			self.t0 = ty0
			self.t1 = ty1
		elif ty0 < t0 and ty1 <= t1:
			self.t0 = t0
			self.t1 = ty1
		elif ty0 >= t0 and ty1 > t1:
			self.t0 = ty0
			self.t1 = t1
		else:
			self.t0 = t0
			self.t1 = t1
	
	def start( self ):
		if self.t1 < self.t_break:
			print(f"Run between {self.t0} / {self.t1}")
		elif self.t0 < self.t_break and self.t_break < self.t1:
			print(f"Run between {self.t0} / {self.t_break}")
			t = self.t_break + dt.timedelta(days=1)
			while t <= self.t1:
				print(f"Run {t}")
				t += dt.timedelta(days=1)
		else:
			t = self.t0
			while t <= self.t1:
				print(f"Run {t}")
				t += dt.timedelta(days=1)
			
	def __str__( self ):
		return f"YearlyTask:: t0: {self.t0}, t1: {self.t1}, t_break: {self.t_break}"
	
	def __repr__( self ):
		return self.__str__()
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
	
	## Split in yearly time, and find the break
	t0 = dt.datetime.fromisoformat(kwargs["period"][0])
	t1 = dt.datetime.fromisoformat(kwargs["period"][1])
	year0 = t0.year
	year1 = t1.year
	
	t_now   = dt.datetime.utcnow()
	t_now   = dt.datetime( t_now.year , t_now.month , t_now.day )
	t_break = t_now - dt.timedelta( days = 30 )
	
	## Build list of tasks
	l_ytasks = [ YearlyTask( year , t0 , t1 , t_break ) for year in range(year0,year1+1,1) ]
	
	for ytask in l_ytasks:
		print(ytask)
		ytask.start()
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
		print(doc)
	
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

