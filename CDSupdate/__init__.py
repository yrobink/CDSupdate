
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

from .__exec      import start_cdsupdate
from .__input     import read_input
from .__logs      import LogFile
from .__doc       import doc
from .__release   import version
from .__CDSparams import CDSparams
from .__sys       import rmdirs

from .__exceptions import CDSInputPeriodSizeError
from .__exceptions import CDSInputPeriodOrderError

from .__download import build_yearly_CDSAPIParams
from .__download import build_CDSAPIParams
from .__download import build_name_AMIP_ERA5
from .__download import build_name_AMIP_CDSAPI
from .__download import load_data_cdsapi

from .__convert import build_attrs_daily
from .__convert import build_attrs_hourly
from .__convert import build_encoding_daily
from .__convert import build_encoding_hourly
from .__convert import transform_to_daily
from .__convert import transform_to_hourly
from .__convert import transform_data_format

from .__merge import merge_with_current_daily
from .__merge import merge_with_current_hourly
from .__merge import merge_with_current


###################
## Set variables ##
###################

__version__ = version
__doc__     = doc
