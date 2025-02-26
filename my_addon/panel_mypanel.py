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

import bpy

class WM_OT_ExportPaths(bpy.types.Operator):
    bl_idname = "wm.vivify_export_paths"
    bl_label = "Export Paths"

    def execute(self, context):
        self.report({'INFO'}, "Hello World")
        return {'FINISHED'}

class WM_OT_AddPathData(bpy.types.Operator):
    bl_idname = "wm.vivify_add_path_data"
    bl_label = "Add Path Data"

    def execute(self, context):
        authorized_obj_types = ['MESH', 'EMPTY']
        selected_objects = bpy.context.selected_objects

        if len(selected_objects) == 0:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}

        # Check object types
        for obj in selected_objects:
            if obj.type not in authorized_obj_types:
                self.report({'ERROR'}, f"Object {obj.name} is of type {obj.type}. Please select only mesh objects.")
                return {'CANCELLED'}

        self.report({'INFO'}, "Hello World (yeah)")
        return {'FINISHED'}

class MYADDON_PT_VivifyPanel(bpy.types.Panel):
    bl_label = "Vivify"
    bl_idname = "MYADDON_PT_VivifyPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vivify"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Hey :D")
        layout.operator("wm.vivify_add_path_data", text="Add Path Data")
        layout.operator("wm.vivify_export_paths", text="Export Paths")
