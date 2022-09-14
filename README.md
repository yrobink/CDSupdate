# CDSupdate


CDSupdate is a tools to automatically download and update data from the Climate
Data Store. Currently, only ERA5 is supported.

## Installation

CDSupdate requires the following packages:

- `numpy`
- `scipy`
- `xarray`
- `netCDF4`
- `cftime`
- `cdsapi` 
- `windows-curses` (only for Microsoft Windows users)

Just run with python:

~~~shell
python3 setup.py install
~~~

Or (for user only installation):

~~~shell
python3 setup.py install --user
~~~

Or 

~~~shell
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
(80W-50E,5N,72N) between 2019-11-09 and 2022-01-17 in the directory `odir` (and
`tmp` is used as temporary dir), just run:

~~~shell
cdsupdate --log test.log --period 2019-11-09/2022-01-17 --var tas --area NorthAtlantic --odir odir --tmpdir tmp
~~~


## License

Copyright(c) 2022 Yoann Robin

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

