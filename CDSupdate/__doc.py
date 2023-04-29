
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

#############
## Imports ##
#############

from .__release import version
from .__release import long_description
from .__release import license
from .__release import license_txt
from .__release import src_url
from .__release import authors_doc

from .__CDSParams import cdsParams


###############
## Variables ##
###############

area_description = "\n".join(
["- {:{fill}{align}{n}}: ".format(f"'{area_name}'",fill="",align="<",n=16) + "{}".format(",".join([str(x) for x in cdsParams.available_area[area_name]])) for area_name in cdsParams.available_area]
)

doc = """\

CDSupdate ({})
{}

{}

Input parameters
----------------
--log flog
    Write logs in the file 'flog'.
--clog
    Print logs in the console, override --log.
--period t0/t1
    Period to download/update, t* must be in the iso format YYYY-MM-DD. If t1
    is not given, t1 = today.
--var var0,var1,...
    List of variables to download/update.
--area name,xmin,xmax,ymin,ymax OR keyword
    Area, can be a grid, or a keyword, see area section.
--keephourly
    Keep also hourly data
--odir output_directory
    Output directory.
--tmpdir temporary_directory
    Temporary directory used to download data before formatting. If not given, a
    random folder is built in the directory given by the environement variable
    '$WORKDIR'. Raise an error if not given and '$WORKDIR' is not set.
--keeptmp
    Not remove the temporary directory at the end
--help
    Print the documentation.
--origin
    Data to download, currently not used (only ERA5 reanalysis).
--cdskey [currently not used]
    CDS key, if not given use '$HOME/.cdsapirc'.
--cdsurl [currently not used]
    CDS url, if not given use '$HOME/.cdsapirc'.

About the variables
-------------------
- Original data being at hourly scale, use 'tas', 'tasmin' or 'tasmax'  as var
  updates the three.
- Current variables supported: {}.

About the area
--------------
You can pass a box, or the following keywords:
{}

Examples
--------
cdsupdate --clog --period 2022-01-01/2022-01-14 --var prtot --keephourly --area NorthAtlantic --odir $wdir/data/ --tmpdir $wdir/tmp --keeptmp ## Change wdir for a directory
cdsupdate --clog --period 2022-01-01/2022-01-14 --var prtot --keephourly --area France,-5,10,41,52 --odir $wdir/data/ --tmpdir $wdir/tmp --keeptmp ## Change wdir for a directory

License {}
{}
{}

Sources and author(s)
---------------------
Sources   : {}
Author(s) : {}
""".format( version , "=" * (12+len(version)) ,
            long_description,
            ", ".join([f"'{s}'" for s in cdsParams.available_cvars]),
            area_description,
            license , "-" * ( 8 + len(license) ) , license_txt ,
            src_url , authors_doc )

