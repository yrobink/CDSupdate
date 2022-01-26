
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

#############
## Imports ##
#############

from .__release import version
from .__release import long_description
from .__release import license
from .__release import license_txt
from .__release import src_url
from .__release import authors_doc


###############
## Variables ##
###############

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
--area xmin,xmax,ymin,ymax
    Area, can be a grid, or a keyword, see area section.
--odir output_directory
    Output directory.
--help
    Print the documentation.
--origin
    Data to download, currently not used (only ERA5 reanalysis).
--cdskey
    CDS key, if not given use '$HOME/.cdsapirc'.
--cdsurl
    CDS url, if not given use '$HOME/.cdsapirc'.

About the variables
-------------------
- Original data being at hourly scale, use 'tas', 'tasmin' or 'tasmax'  as var
  updates the three.
- Current variables supported: 'tas', 'tasmin' and 'tasmax'.

About the area
--------------
You can pass a box, or the following keywords:
- 'world'  : all the world, equivalent to -180,180,-90,90
- 'europe' : Europe with Copernicus defitinion, i.e. ...

License {}
{}
{}

Sources and author(s)
---------------------
Sources   : {}
Author(s) : {}
""".format( version , "=" * (12+len(version)) ,
            long_description,
            license , "-" * ( 8 + len(license) ) , license_txt ,
            src_url , authors_doc )

