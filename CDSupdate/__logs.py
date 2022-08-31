
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


#############
## Classes ##
#############

class LogFile:
	"""
	CDSupdate.LogFile
	=================
	
	Class to write logs in a file / console.
	
	"""
	def __init__( self , logf = None ):
		"""
		Constructor
		-----------
		
		logf [None,file,"console"]
			Where to write the logs. Can be a file, the keyword 'console' means
			the console is used, and if None no logs are written.
		
		"""
		self._logf    = None
		self._console = False
		self._last_is_line = False
		if logf is None:
			return
		
		if logf == "console":
			self._console = True
			return
		else:
			self._logf = logf
			if os.path.isfile(self._logf):
				os.remove(self._logf)
	
	def write( self , log , end = "\n" ):
		"""
		LogFile.write
		-------------
		
		Method to write a log.
		
		log [str]
			The log to write
		end [str]
			End character to write after 'log', default is '\\n'.
		"""
		if self._console:
			print( log , end = end )
		elif self._logf is not None:
			with open( self._logf , "a" ) as f:
				f.write( log + end )
		self._last_is_line = False
	
	def writeline( self , ch = "-" , size = 80 ):
		"""
		LogFile.writeline
		-----------------
		
		Method to write a line.
		
		ch [str]
			The character for a line, default is '-'.
		size [int]
			The size of the line, default is 80.
		"""
		if not self._last_is_line:
			self.write( ch * size )
			self._last_is_line = True

