# Add-on description
# Copyright (C) YEAR AUTHOR
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

bl_info = {
    "name": "blendheck",
    "author": "Nyaniko~",
    "description": "A Vivify preview/editor for Blender",
    "blender": (4, 3, 0),
    "version": (0, 1, 0),
    "location": "Sidebar",
    "category": "Object",
    "warning": "",
}

# Wrap in try-except here so that we can use hatch's dynamic version detection
# without this failing. See the `[tool.hatch.version]` section in `pyproject.toml`.

try:
    from . import auto_load

    auto_load.init()

    def register():
        auto_load.register()

    def unregister():
        auto_load.unregister()
except ImportError:
    pass
