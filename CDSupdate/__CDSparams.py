
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

import os
import pandas as pd


## All fixed parameters
##=====================

class CDSParams:##{{{
	
	def __init__(self):##{{{
		
		cpath = os.path.dirname(os.path.abspath(__file__))
		
		## First, read the table of variables
		self.cvar_tab = pd.read_csv( os.path.join( cpath , "data" , "ERA5-name.csv" ) , keep_default_na = False )
		
		## List of available variables
		self.available_vars = self.cvar_tab["AMIP"].values.tolist()
		if "tas" in self.available_vars:
			self.available_vars.append("tasmax")
			self.available_vars.append("tasmin")
		self.available_vars.sort()
		
		## Conversion
		self.AMIP_ERA5 = { str(self.cvar_tab.loc[i,"AMIP"]) : str(self.cvar_tab.loc[i,"ERA5"]) for i in range(self.cvar_tab.shape[0]) }
		self.ERA5_AMIP = { str(self.cvar_tab.loc[i,"ERA5"]) : str(self.cvar_tab.loc[i,"AMIP"]) for i in range(self.cvar_tab.shape[0]) }
		self.AMIP_CDS  = { str(self.cvar_tab.loc[i,"AMIP"]) : str(self.cvar_tab.loc[i,"CDS"])  for i in range(self.cvar_tab.shape[0]) }
		self.CDS_AMIP  = { str(self.cvar_tab.loc[i,"CDS"])  : str(self.cvar_tab.loc[i,"AMIP"]) for i in range(self.cvar_tab.shape[0]) }
		
		## Now read description
		self.description = {}
		for cvar in self.available_vars:
			try:
				with open( os.path.join( cpath , "data" , f"ERA5-{cvar}-description.txt" ) , "r" ) as f:
					self.description[cvar] = "".join(f.readlines()).replace("\n","")
			except:
				self.description[cvar] = ""
		
		## Now read areas
		self.areas_tab = pd.read_csv( os.path.join( cpath , "data" , "areas.csv" ) )
		
		self.available_area = {}
		for i in range(self.areas_tab.shape[0]):
			self.available_area[str(self.areas_tab.iloc[i,0])] = [float(x) for x in self.areas_tab.iloc[i,1:].values.tolist()]
	##}}}
	
	def level( self , cvar ):##{{{
		tab   = self.cvar_tab.copy()
		tab.index = tab["AMIP"]
		return tab.loc[cvar,"level"]
	##}}}
	
	def level_value( self , cvar ):
		tab   = self.cvar_tab.copy()
		tab.index = tab["AMIP"]
		return tab.loc[cvar,"level_value"]
	
	def attrs( self , cvar , freq = "hourly" ):##{{{
		
		attrs = {}
		tab   = self.cvar_tab.copy()
		tab.index = tab["AMIP"]
		
		attrs["standard_name"] = tab.loc[cvar]["standard_name"]
		attrs["long_name"]     = tab.loc[cvar][f"{freq}_long_name"]
		attrs["units"]         = tab.loc[cvar]["units"]
		attrs["comment"]       = tab.loc[cvar][f"{freq}_comment"]
		attrs["CDS_name"]      = tab.loc[cvar]["CDS"]
		attrs["ERA5_name"]     = tab.loc[cvar]["ERA5"]
		attrs["description"]   = self.description[cvar]
		
		return attrs
	##}}}
	
##}}}

CDSparams = CDSParams()

