
## Copyright(c) 2022, 2023 Yoann Robin, Andreia Hisi
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

from .__exec      import start_cdsupdate
from .__doc       import doc
from .__release   import version


###################
## Set variables ##
###################

__version__ = version
__doc__     = doc

