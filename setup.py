
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

import os

## Start by import release details
from CDSupdate.__release import name
from CDSupdate.__release import version
from CDSupdate.__release import description
from CDSupdate.__release import long_description
from CDSupdate.__release import authors
from CDSupdate.__release import authors_email
from CDSupdate.__release import src_url
from CDSupdate.__release import license

## Required elements
author           = ", ".join(authors)
author_email     = ", ".join(authors_email)
package_dir      = { "Explore2" : "Explore2" }
requires         = [ "numpy" , "scipy" , "xarray" , "netCDF4" , "cftime" , "cdsapi" ]
scripts          = ["scripts/cdsupdate"]
keywords         = ["Climate Data Store","Auto update"]
platforms        = ["linux","macosx"]
packages         = [
	"CDSupdate",
	]

## Now the setup
from distutils.core import setup

setup(  name             = name,
		version          = version,
		description      = description,
		long_description = long_description,
		author           = author,
		author_email     = author_email,
		url              = src_url,
		packages         = packages,
		package_dir      = package_dir,
		requires         = requires,
		scripts          = scripts,
		license          = license,
		keywords         = keywords,
		platforms        = platforms
     )

