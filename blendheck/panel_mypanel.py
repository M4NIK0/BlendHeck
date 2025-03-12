# Add-on description
# Copyright (C) YEAR AUTHOR
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (a                                    t your option) any later version.
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
import json
from . import props
from . import paths
from . import map

bpy.utils.register_class(props.VivifyProp)
bpy.utils.register_class(props.VivifyPropArray)
bpy.types.Object.my_data = bpy.props.PointerProperty(type=props.VivifyPropArray)

class VIEW3D_MT_vivify_menu(bpy.types.Menu):
    bl_label = "Vivify"
    bl_idname = "VIEW3D_MT_vivify_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.vivify_save_map_data", text="Save Map Data")
        layout.operator("wm.vivify_load_map_file", text="Load Map File")
        layout.operator("wm.vivify_export_paths", text="Export All Paths")
        layout.operator("wm.vivify_export_paths_selected", text="Export Selected Paths")

# Add the Vivify menu to the 3D View header (next to Object, View, etc.)
def draw_vivify_menu(self, context):
    layout = self.layout
    layout.menu("VIEW3D_MT_vivify_menu")

class MYADDON_PT_VivifyPanel(bpy.types.Panel):
    bl_label = "Vivify"
    bl_idname = "MYADDON_PT_VivifyPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vivify"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.vivify_add_path_data", text="Add Path Data")
        layout.operator("wm.vivify_export_paths", text="Export All Paths")
        layout.operator("wm.vivify_export_paths_selected", text="Export Selected Paths")
        layout.prop(context.scene, "vivify_export_path", text="Map File")
        layout.operator("wm.select_export_path", text="Choose File")
        layout.operator("wm.vivify_load_map_file", text="Load Map File")
        layout.operator("wm.vivify_save_map_data", text="Save Map Data")
        layout.prop(context.scene, "vivify_save_map_data_with_blend", text="Save Map Data With Blend File")
        layout.prop(context.scene, "vivify_convert_coordinates", text="Convert to Unity Coordinates")
        layout.label(text=f"{map.get_point_definitions(context.scene.vivify_map_data)}")
        layout.operator("wm.display_preview_menu", text="Preview paths")

class MYADDON_PT_VivifyPathsPanel(bpy.types.Panel):
    bl_label = "Paths"
    bl_idname = "MYADDON_PT_VivifyPathsPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vivify"

    def draw(self, context):
        layout = self.layout
        if len(context.selected_objects) > 0:
            # Check if there is any data to display
            has_display = False
            for current_selected_object in context.selected_objects:
                if len(current_selected_object.my_data.my_data_array) > 0:
                    has_display = True
                    break
            if not has_display:
                layout.label(text="No data to display")
                return

            sel_index = 0
            for current_selected_object in context.selected_objects:
                for i, data in enumerate(current_selected_object.my_data.my_data_array):
                    box = layout.box()
                    box.label(text="Object path " + ("(" + current_selected_object.name + ")" if len(context.selected_objects) > 1 else ""))

                    # Use a Boolean property to control the visibility of the box contents (collapsible)
                    is_collapsed = current_selected_object.my_data.my_data_array[i].collapsed
                    row = box.row()
                    row.prop(current_selected_object.my_data.my_data_array[i], "point_definition_name")

                    # Toggle collapse button
                    row = box.row()
                    row.prop(current_selected_object.my_data.my_data_array[i], "collapsed", text="Collapse", icon="TRIA_DOWN" if not is_collapsed else "TRIA_RIGHT")

                    # Show content conditionally based on the collapse state
                    if not is_collapsed:
                        box.prop(current_selected_object.my_data.my_data_array[i], "path_type")
                        box.prop(current_selected_object.my_data.my_data_array[i], "export")
                        if current_selected_object.my_data.my_data_array[i].path_type == 'Curve/Custom':
                            box.prop(current_selected_object.my_data.my_data_array[i], "export_position")
                            box.prop(current_selected_object.my_data.my_data_array[i], "export_rotation")
                            box.prop(current_selected_object.my_data.my_data_array[i], "export_scale")
                            box.prop(current_selected_object.my_data.my_data_array[i], "steps")
                        else:
                            box.prop(current_selected_object.my_data.my_data_array[i], "keyframe_type")
                        box.prop(current_selected_object.my_data.my_data_array[i], "start_frame")
                        box.prop(current_selected_object.my_data.my_data_array[i], "end_frame")

                    # Add a "Remove" button next to each item
                    remove_button = box.operator("wm.vivify_remove_path_data", text="Remove Path Data")
                    remove_button.index = i  # Pass the index of the current data
                    remove_button.selection_index = sel_index  # Pass the index of the current object
                sel_index += 1
        else:
            layout.label(text="No object selected")
