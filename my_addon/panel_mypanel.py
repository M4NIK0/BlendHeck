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

class VivifyProp(bpy.types.PropertyGroup):
    point_definition_name: bpy.props.StringProperty(name="Name", default="Animation")
    export: bpy.props.BoolProperty(name="Export", default=True)
    export_position: bpy.props.BoolProperty(name="Export Position", default=True)
    export_rotation: bpy.props.BoolProperty(name="Export Rotation", default=True)
    export_scale: bpy.props.BoolProperty(name="Export Scale", default=True)
    steps: bpy.props.IntProperty(name="Steps", default=10)
    start_frame: bpy.props.IntProperty(name="Start Frame", default=1)
    end_frame: bpy.props.IntProperty(name="End Frame", default=100)

    # Add a collapsed property to control visibility
    collapsed: bpy.props.BoolProperty(name="Collapsed", default=False)

class VivifyPropArray(bpy.types.PropertyGroup):
    my_data_array: bpy.props.CollectionProperty(type=VivifyProp)

bpy.utils.register_class(VivifyProp)
bpy.utils.register_class(VivifyPropArray)
bpy.types.Object.my_data = bpy.props.PointerProperty(type=VivifyPropArray)

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

        # Add data to selected objects
        for obj in selected_objects:
            if obj.my_data.my_data_array.add() is not None:
                self.report({'INFO'}, f"Added data to object {obj.name}")
            else:
                self.report({'ERROR'}, f"Could not add data to object {obj.name}")

        self.report({'INFO'}, "Hello World (yeah)")
        return {'FINISHED'}

class WM_OT_RemovePathData(bpy.types.Operator):
    bl_idname = "wm.vivify_remove_path_data"
    bl_label = "Remove Path Data"

    index: bpy.props.IntProperty()

    def execute(self, context):
        obj = context.object
        if obj and hasattr(obj, "my_data"):
            if 0 <= self.index < len(obj.my_data.my_data_array):
                obj.my_data.my_data_array.remove(self.index)  # Remove the item at the specified index
                self.report({'INFO'}, f"Removed data at index {self.index}")
            else:
                self.report({'ERROR'}, "Invalid index")
                return {'CANCELLED'}
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

        if context.object:
            for i, data in enumerate(context.object.my_data.my_data_array):
                box = layout.box()
                box.label(text="Object path")

                # Use a Boolean property to control the visibility of the box contents (collapsible)
                is_collapsed = context.object.my_data.my_data_array[i].collapsed
                row = box.row()
                row.prop(context.object.my_data.my_data_array[i], "point_definition_name")

                # Toggle collapse button
                row = box.row()
                row.prop(context.object.my_data.my_data_array[i], "collapsed", text="Collapse", icon="TRIA_DOWN" if not is_collapsed else "TRIA_RIGHT")

                # Show content conditionally based on the collapse state
                if not is_collapsed:
                    box.prop(context.object.my_data.my_data_array[i], "export")
                    box.prop(context.object.my_data.my_data_array[i], "export_position")
                    box.prop(context.object.my_data.my_data_array[i], "export_rotation")
                    box.prop(context.object.my_data.my_data_array[i], "export_scale")
                    box.prop(context.object.my_data.my_data_array[i], "steps")
                    box.prop(context.object.my_data.my_data_array[i], "start_frame")
                    box.prop(context.object.my_data.my_data_array[i], "end_frame")

                # Add a "Remove" button next to each item
                remove_button = box.operator("wm.vivify_remove_path_data", text="Remove Path Data")
                remove_button.index = i  # Pass the index of the current data