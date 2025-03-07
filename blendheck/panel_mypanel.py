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

class WM_OT_ExportPaths(bpy.types.Operator):
    bl_idname = "wm.vivify_export_paths"
    bl_label = "Export All Paths"
    bl_category = "Vivify"

    def execute(self, context):
        if not context.scene.vivify_export_path:
            self.report({'ERROR'}, "No export path set")
            return {'CANCELLED'}

        if context.scene.vivify_map_data == {}:
            self.report({'ERROR'}, "No map data found")
            return {'CANCELLED'}

        exported_positions = []
        exported_rotations = []
        exported_scales = []

        for obj in bpy.data.objects:
            self.report({'INFO'}, f"Object {obj.name} has {len(obj.my_data.my_data_array)} data items")
            if len(obj.my_data.my_data_array) > 0:
                for i, data in enumerate(obj.my_data.my_data_array):
                    if data.export:
                        if data.path_type == 'Curve/Custom':
                            try:
                                if data.export_position:
                                    pospath = paths.export_object_path_curve_pos(obj, data, self)
                                    exported_positions.append(pospath)
                            except Exception as e:
                                self.report({'ERROR'}, f"Could not export position data for object {obj.name}: {e}")
                            try:
                                if data.export_rotation:
                                    rotpath = paths.export_object_path_curve_rot(obj, data, self)
                                    exported_rotations.append(rotpath)
                            except Exception as e:
                                self.report({'ERROR'}, f"Could not export rotation data for object {obj.name}: {e}")
                            try:
                                if data.export_scale:
                                    scalepath = paths.export_object_path_curve_scale(obj, data, self)
                                    exported_scales.append(scalepath)
                            except Exception as e:
                                self.report({'ERROR'}, f"Could not export scale data for object {obj.name}: {e}")
                        elif data.path_type == 'Keyframes':
                            if data.keyframe_type == 'Position':
                                pospath = paths.export_object_keyframes_pos(obj, data, self)
                                exported_positions.append(pospath)
                            elif data.keyframe_type == 'Rotation':
                                rotpath = paths.export_object_keyframes_rot(obj, data, self)
                                exported_rotations.append(rotpath)
                            elif data.keyframe_type == 'Scale':
                                scalepath = paths.export_object_keyframes_scale(obj, data, self)
                                exported_scales.append(scalepath)
                            pospath = paths.export_object_keyframes_pos(obj, data, self)
                            exported_positions.append(pospath)
                        else:
                            self.report({'INFO'}, f"Skipping export of data {data.point_definition_name} for object {obj.name}, what the heck did you try?")
                    else:
                        self.report({'INFO'}, f"Skipped {data.point_definition_name} for {obj.name}")

        dict_to_export = map.setup_point_definitions(context.scene.vivify_map_data)

        for pos in exported_positions:
            if pos is None:
                continue
            dict_to_export["customData"]["pointDefinitions"].update(pos.get_json_dict())
        for rot in exported_rotations:
            if rot is None:
                continue
            dict_to_export["customData"]["pointDefinitions"].update(rot.get_json_dict())
        for scale in exported_scales:
            if scale is None:
                continue
            dict_to_export["customData"]["pointDefinitions"].update(scale.get_json_dict())

        self.report({'INFO'}, f"Exported all paths! Don't forget to save the map file.")

        return {'FINISHED'}

class WM_OT_ExportSelectedPaths(bpy.types.Operator):
    bl_idname = "wm.vivify_export_paths_selected"
    bl_label = "Export Selected Paths"
    bl_category = "Vivify"

    def execute(self, context):
        if not context.scene.vivify_export_path:
            self.report({'ERROR'}, "No export path set")
            return {'CANCELLED'}

        exported_positions = []
        exported_rotations = []
        exported_scales = []

        for obj in bpy.context.selected_objects:
            self.report({'INFO'}, f"Object {obj.name} has {len(obj.my_data.my_data_array)} data items")
            if len(obj.my_data.my_data_array) > 0:
                for i, data in enumerate(obj.my_data.my_data_array):
                    if data.export:
                        if data.path_type == 'Curve/Custom':
                            try:
                                if data.export_position:
                                    pospath = paths.export_object_path_curve_pos(obj, data, self)
                                    exported_positions.append(pospath)
                            except Exception as e:
                                self.report({'ERROR'}, f"Could not export position data for object {obj.name}: {e}")
                            try:
                                if data.export_rotation:
                                    rotpath = paths.export_object_path_curve_rot(obj, data, self)
                                    exported_rotations.append(rotpath)
                            except Exception as e:
                                self.report({'ERROR'}, f"Could not export rotation data for object {obj.name}: {e}")
                            try:
                                if data.export_scale:
                                    scalepath = paths.export_object_path_curve_scale(obj, data, self)
                                    exported_scales.append(scalepath)
                            except Exception as e:
                                self.report({'ERROR'}, f"Could not export scale data for object {obj.name}: {e}")
                        elif data.path_type == 'Keyframes':
                            if data.keyframe_type == 'Position':
                                pospath = paths.export_object_keyframes_pos(obj, data, self)
                                exported_positions.append(pospath)
                            elif data.keyframe_type == 'Rotation':
                                rotpath = paths.export_object_keyframes_rot(obj, data, self)
                                exported_rotations.append(rotpath)
                            elif data.keyframe_type == 'Scale':
                                scalepath = paths.export_object_keyframes_scale(obj, data, self)
                                exported_scales.append(scalepath)
                            pospath = paths.export_object_keyframes_pos(obj, data, self)
                            exported_positions.append(pospath)
                        else:
                            self.report({'INFO'}, f"Skipping export of data {data.point_definition_name} for object {obj.name}, what the heck did you try?")
                    else:
                        self.report({'INFO'}, f"Skipped {data.point_definition_name} for {obj.name}")

        dict_to_export = map.setup_point_definitions(context.scene.vivify_map_data)

        for pos in exported_positions:
            if pos is None:
                continue
            dict_to_export["customData"]["pointDefinitions"].update(pos.get_json_dict())
        for rot in exported_rotations:
            if rot is None:
                continue
            dict_to_export["customData"]["pointDefinitions"].update(rot.get_json_dict())
        for scale in exported_scales:
            if scale is None:
                continue
            dict_to_export["customData"]["pointDefinitions"].update(scale.get_json_dict())

        self.report({'INFO'}, f"Exported all paths! Don't forget to save the map file.")

        return {'FINISHED'}

class WM_OT_AddPathData(bpy.types.Operator):
    bl_idname = "wm.vivify_add_path_data"
    bl_label = "Add Path Data"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        if len(selected_objects) == 0:
            self.report({'ERROR'}, "No objects selected")
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

    index: bpy.props.IntProperty()  # Only keep the index property
    selection_index: bpy.props.IntProperty()  # Add a selection index property

    def execute(self, context):
        obj = context.selected_objects[self.selection_index]  # Get the object from the context
        if obj and hasattr(obj, "my_data"):
            if 0 <= self.index < len(obj.my_data.my_data_array):
                obj.my_data.my_data_array.remove(self.index)  # Remove the item at the specified index
                self.report({'INFO'}, f"Removed data at index {self.index}")
            else:
                self.report({'ERROR'}, f"Invalid index {self.index}")
                return {'CANCELLED'}
        else:
            self.report({'ERROR'}, "No valid object selected or object doesn't have my_data attribute")
            return {'CANCELLED'}
        return {'FINISHED'}

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
        layout.label(text=f"{map.get_point_definitions(context.scene.vivify_map_data)}")

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
