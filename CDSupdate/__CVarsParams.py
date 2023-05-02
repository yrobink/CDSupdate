
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

import os
import re
import pandas as pd


###########
## Class ##
###########

class CVarsParams:##{{{
	
	def __init__( self ):##{{{
		
		## Levels
		self._avail_levels =  ['1', '2', '3','5', '7', '10','20', '30', '50',
		                       '70', '100', '125','150', '175', '200','225',
		                       '250', '300','350', '400', '450','500', '550',
		                       '600','650', '700', '750','775', '800', '825',
		                       '850', '875', '900','925', '950', '975','1000']
		
		
		## Read table of cvars
		cpath = os.path.dirname(os.path.abspath(__file__))
		self._cvar_tab = pd.read_csv( os.path.join( cpath , "data" , "ERA5-name.csv" ) , keep_default_na = False )
		
		## All cvars
		self.all_cvars = self._cvar_tab["AMIP"].values.tolist()
		self.dwl_cvars = []
		self.cmp_cvars = []
		self.dep_cvars = {}
		
		## Build the dependecy graph
		deps = self._cvar_tab["dep"].values.tolist()
		for cvar,dep in zip(self.all_cvars,deps):
			if len(dep) == 0:
				self.dwl_cvars.append(cvar)
				self.dep_cvars[cvar] = []
			else:
				self.cmp_cvars.append(cvar)
				self.dep_cvars[cvar] = dep.split(";")
		
		## Conversion
		self.AMIP_ERA5 = { str(self._cvar_tab.loc[i,"AMIP"]) : str(self._cvar_tab.loc[i,"ERA5"]) for i in range(self._cvar_tab.shape[0]) }
		self.ERA5_AMIP = { str(self._cvar_tab.loc[i,"ERA5"]) : str(self._cvar_tab.loc[i,"AMIP"]) for i in range(self._cvar_tab.shape[0]) }
		self.AMIP_CDS  = { str(self._cvar_tab.loc[i,"AMIP"]) : str(self._cvar_tab.loc[i,"CDS"])  for i in range(self._cvar_tab.shape[0]) }
		self.CDS_AMIP  = { str(self._cvar_tab.loc[i,"CDS"])  : str(self._cvar_tab.loc[i,"AMIP"]) for i in range(self._cvar_tab.shape[0]) }
		
		## Now read description
		self.description = {}
		for cvar in self.all_cvars:
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
	
	def removeLevel( self , cvar ):##{{{
		c,l = self.split_level(cvar)
		return c
	##}}}
	
	def split_level( self , cvar ):##{{{
		
		level = re.findall( r'\d+' , cvar )
		if len(level) == 0:
			return cvar,"single"
		
		return cvar.replace(level[0],""),level[0]
	##}}}
	
	def is_available( self , cvar ):##{{{
		c,l = self.split_level(cvar)
		
		if not c in self.all_cvars:
			return False
		
		if (l == "single") or (l in self._avail_levels):
			return True
		
		return False
	##}}}
	
	def is_downloadable( self , cvar ):##{{{
		return self.removeLevel(cvar) in self.dwl_cvars
	##}}}
	
	def is_computable( self , cvar ):##{{{
		return cvar in self.cmp_cvars
	##}}}
	
	def _increase_request( self , cvars ):##{{{
		
		out = list(cvars)
		for cvar in cvars:
			for c in self.dep_cvars[self.removeLevel(cvar)]:
				if c in out:
					del out[out.index(c)]
				out.append(c)
		
		if len(out) == len(cvars):
			return out
		else:
			return self._increase_request(out)
	##}}}
	
	def cvars_from_request( self , request ):##{{{
		
		to_dwl = []
		to_cmp = []
		levs   = []
		
		all_needed = self._increase_request(request)[::-1]
		
		for cvar in all_needed:
			c,l = self.split_level(cvar)
			if c in self.dwl_cvars:
				to_dwl.append(c)
				levs.append(l)
			else:
				to_cmp.append(cvar)
		
		return to_dwl,to_cmp,levs
	##}}}
	
	def level( self , cvar ):##{{{
		tab   = self._cvar_tab.copy()
		tab.index = tab["AMIP"]
		return tab.loc[cvar,"level"]
	##}}}
	
	def height( self , cvar ):##{{{
		tab   = self._cvar_tab.copy()
		tab.index = tab["AMIP"]
		return tab.loc[cvar,"height"]
	##}}}
	
	def attrs( self , cvar ):##{{{
		
		attrs = {}
		tab   = self._cvar_tab.copy()
		tab.index = tab["AMIP"]
		
		attrs["standard_name"] = tab.loc[cvar]["standard_name"]
		attrs["long_name"]     = tab.loc[cvar][f"long_name"]
		attrs["units"]         = tab.loc[cvar]["units"]
		attrs["comment"]       = tab.loc[cvar][f"comment"]
		attrs["CDS_name"]      = tab.loc[cvar]["CDS"]
		attrs["ERA5_name"]     = tab.loc[cvar]["ERA5"]
		attrs["description"]   = self.description[cvar]
		
		return attrs
	##}}}
	
##}}}

cvarsParams = CVarsParams()



