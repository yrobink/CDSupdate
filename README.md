# CDSupdate

CDSupdate is a Python package that automates the process of retrieving, processing, and managing climate data from the Climate
Data Store (CDS) API. The tool generates daily climate data summaries, performs calculations to create custom variables such as
relative humidity and heat index which serve as risk assessments, and organizes the data into a user-friendly format. 


## Installation

CDSupdate requires the following packages:

- `numpy`
- `pandas`
- `xarray`
- `netCDF4`
- `cftime`
- `cdsapi` 
- `windows-curses` (only for Microsoft Windows users)

From pip:

~~~shell
pip3 install CDSupdate
~~~

Or from source:

~~~shell
git clone https://github.com/yrobink/CDSupdate.git
cd CDSupdaye
pip3 install .
~~~

This adds the `CDSupdate` package in your python installation, and the command
`cdsupdate`.

## How to use ?

Start by read the documentation with:

~~~shell
cdsupdate --help
~~~

As example, to download the daily mean temperature over the North Atlantic
(80W-50E,5N,72N) between 2019-11-09 and 2022-01-17 in the directory `odir`, just run:

~~~shell
cdsupdate --log info test.log --period 2019-11-09/2022-01-17 --cvar tas --area NorthAtlantic --odir odir
~~~

## How to cite it ?

You can use this [DOI:10.5281/zenodo.7991331](https://doi.org/10.5281/zenodo.7991331)

## License

Copyright(c) 2022 / 2025 Yoann Robin, Andreia Hisi

This file is part of CDSupdate.

CDSupdate is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CDSupdate is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CDSupdate.  If not, see <https://www.gnu.org/licenses/>.

