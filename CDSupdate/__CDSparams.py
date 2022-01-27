
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

## All fixed parameters
##=====================

class CDSParams(object):
	pass

CDSparams = CDSParams()

CDSparams.available_area = {
	"world"  : [-180,180,-90,90],
	"europe" : [-25,40,34,72],
	"northatlantic" : [-80,50,5,70],
	"northamerica"  : [-150,-60,30,80]
	}

CDSparams.available_vars = ["tas","tasmin","tasmax"]

