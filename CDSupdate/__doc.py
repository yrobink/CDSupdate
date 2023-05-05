
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
from .__release import license
from .__release import license_txt
from .__release import src_url
from .__release import authors_doc

from .__CVarsParams import cvarsParams


###############
## Variables ##
###############

area_description = "\n".join(
["- {:{fill}{align}{n}}: ".format(f"'{area_name}'",fill="",align="<",n=16) + "{}".format(",".join([str(x) for x in cvarsParams.available_area[area_name]])) for area_name in cvarsParams.available_area]
)

doc = """\

CDSupdate ({})
{}

CDSupdate is a tools to automatically download and update data from the Climate
Data Store. Currently, only ERA5 is supported.

Input parameters
----------------
--log [LOGLEVEL FILE]
    Enable log, first optional is argument is the level (default is WARNING),
    the second is a file.
--period t0/t1
    Period to download/update, t* must be in the iso format YYYY-MM-DD. If t1
    is not given, t1 = today.
--cvar cvar0,cvar1,...
    List of variables to download/update.
--area name,xmin,xmax,ymin,ymax OR keyword
    Area, can be a grid, or a keyword, see area section.
--keep-hourly
    Keep also hourly data
--output-dir output_directory
    Output directory.
--tmp temporary_directory
    Temporary directory used to download data before formatting.
--help
    Print the documentation.

About the variables
-------------------
- Current single level variable supported:
  {}
- Current pressure level variable supported:
  {}
- Pressure level supported:
  {}

About the area
--------------
You can pass a box, or the following keywords:
{}

Examples
--------
cdsupdate --log info --period 2022-01-01/2023-04-14 --cvar tas,pr,zg500 --keep-hourly --area NorthAtlantic      --output-dir <ERA5_dir> ## Change <ERA5_dir> for a directory
cdsupdate --log info --period 2022-01-01/2023-04-14 --cvar tas,pr,zg500 --keep-hourly --area France,-5,10,41,52 --output-dir <ERA5_dir> ## Change <ERA5_dir> for a directory

License {}
{}
{}

Sources and author(s)
---------------------
Sources   : {}
Author(s) : {}
""".format( version , "=" * (12+len(version)) ,
            ", ".join([f"'{s}'" for s in cvarsParams.all_cvars if cvarsParams.level(s) == "single"]),
            ", ".join([f"'{s}'" for s in cvarsParams.all_cvars if not cvarsParams.level(s) == "single"]),
            ", ".join([f"'{s}'" for s in cvarsParams._avail_levels]),
            area_description,
            license , "-" * ( 8 + len(license) ) , license_txt ,
            src_url , authors_doc )

line_length = 80
line_cut    = 30
lines = []
for line in doc.split("\n"):
	if len(line) < line_length:
		lines.append(line)
	else:
		b = line_length
		while not line[b] == " ":
		 b = b - 1
		lines.append(line[:b])
		res = line[b:]
		while len(res) > line_cut:
			b = line_cut
			while not res[b] == " ":
				b = b - 1
			ex = res[:b]
			lines.append( " " * (line_length - 1 - len(ex)) + ex )
			res = res[b:]
		lines.append( " " * (line_length - 1 - len(res)) + res )

doc = "\n".join(lines)

