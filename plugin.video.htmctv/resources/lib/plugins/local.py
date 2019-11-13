"""
    local.py --- Jen Plugin for accessing local xml files
    Copyright (C) 2017, Midraal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os

import xbmc
import xbmcaddon
import xbmcvfs

from ..plugin import Plugin


PATH = xbmcaddon.Addon().getAddonInfo("path")


class Local(Plugin):
    name = "local"

    def get_xml(self, url):
        if not url:
            return False
        if url.startswith("file://"):
            url = url.replace("file://", "")
            xml_file = xbmcvfs.File(os.path.join(PATH, "xml", url))
            xml = xml_file.read()
            xml_file.close()
            return xml
        else:
            return False

    def get_xml_uncached(self, url):
        return self.get_xml(url)

    def replace_url(self, url):
        if url.startswith("file://"):
            url = url.replace("file://", os.path.join(PATH, "xml") + "/")
            return url
