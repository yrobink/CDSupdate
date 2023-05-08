
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


version_major = "1"
version_minor = "2"
version_patch = "1"
version_extra = ""
version       = f"{version_major}.{version_minor}.{version_patch}{version_extra}"

name = "CDSupdate"

description = "Auto-updater of data from the Climate Data Store"

authors       = ["Yoann Robin"]
authors_email = ["yoann.robin.k@gmail.com"]
authors_doc   = ", ".join( [ f"{ath} ({athm})" for ath,athm in zip(authors,authors_email) ] )

src_url = "https://github.com/yrobink/CDSupdate"

license = "GNU-GPL3"
license_txt = """\
Copyright(c) 2022, 2023 Yoann Robin

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
"""
