# CDSupdate

*Currently, CDSupdate doesn't work, in development (pre-pre-alpha version)!*

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

This adds the `CDSupdate` package in your python installation, and the command
`cdsupdate`. You can read the documentation with:

~~~shell
cdsupdate --help
~~~


## License

Copyright(c) 2022 Andreia Hisi, Yoann Robin

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

