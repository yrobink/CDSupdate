
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
import pathlib
from setuptools import setup

## Start by import release details
cpath = pathlib.Path(__file__).absolute().parent ## current-path
with open( cpath / "CDSupdate" / "__release.py" , "r" ) as f:
	lines = f.readlines()
exec("".join(lines))

##

## Required elements
author           = ", ".join(authors)
author_email     = ", ".join(authors_email)
long_description = (cpath / "README.md").read_text()
package_dir      = { "CDSupdate" : "CDSupdate" }
requires         = [ "numpy" , "pandas" , "xarray" , "netCDF4" , "cftime" , "cdsapi" ]
scripts          = ["scripts/cdsupdate"]
keywords         = ["Climate Data Store","Auto update"]
platforms        = ["linux","macosx"]
packages         = [
	"CDSupdate",
	"CDSupdate.data",
	]
classifiers      = [
	"Development Status :: 5 - Production/Stable",
	"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
	"Natural Language :: English",
	"Operating System :: MacOS :: MacOS X",
	"Operating System :: POSIX :: Linux",
	"Programming Language :: Python :: 3",
	"Topic :: Scientific/Engineering :: Mathematics"
	]

## Now the setup
setup(  name             = name,
		version          = version,
		description      = description,
		long_description = long_description,
		long_description_content_type = 'text/markdown',
		author           = author,
		author_email     = author_email,
		url              = src_url,
		packages         = packages,
		package_dir      = package_dir,
		install_requires = requires,
		scripts          = scripts,
		license          = license,
		keywords         = keywords,
		platforms        = platforms,
		classifiers      = classifiers,
		include_package_data = True
     )

