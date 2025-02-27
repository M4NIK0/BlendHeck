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

class Simple3DPoint:
    x: float = 0
    y: float = 0
    z: float = 0
    precision: int = 4
    easing: str = None

    def __init__(self, x: float = 0, y: float = 0, z: float = 0, precision: int = 4, easing: str = None):
        self.x = x
        self.y = y
        self.z = z
        self.precision = precision
        self.easing = easing

    def __str__(self):
        return f"[{self.x:.{self.precision}f} {self.y:.{self.precision}f} {self.z:.{self.precision}f}" + (f",\"{self.easing}\"" if self.easing else "") + "]"

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

def export_object_path_curve_pos(obj, path: VivifyProp, operator=None):
    if operator:
        operator.report({'INFO'}, f"Exporting path for object {obj.name} with data {path.point_definition_name}")

    points = []
    min = path.start_frame
    max = path.end_frame

    if min > max:
        if operator:
            operator.report({'ERROR'}, "Start frame must be less than end frame")
        return None

    if int((max - min) / path.steps) == 0:
        if operator:
            operator.report({'ERROR'}, "Steps must be less than the range of frames")
        return None

    for i in range(min, max + int((max - min) / path.steps), int((max - min) / path.steps)):
        bpy.context.scene.frame_set(i)
        ol = obj.matrix_world.to_translation()
        points.append(Simple3DPoint(x=ol.x, y=ol.y, z=ol.z))

    if operator:
        operator.report({'INFO'}, f"Exported {len(points)} points for object {obj.name} with data {path.point_definition_name}")

    return points

bpy.utils.register_class(VivifyProp)
bpy.utils.register_class(VivifyPropArray)
bpy.types.Object.my_data = bpy.props.PointerProperty(type=VivifyPropArray)

class WM_OT_ExportPaths(bpy.types.Operator):
    bl_idname = "wm.vivify_export_paths"
    bl_label = "Export All Paths"
    bl_category = "Vivify"

    def execute(self, context):
        exported = []
        for obj in bpy.data.objects:
            self.report({'INFO'}, f"Object {obj.name} has {len(obj.my_data.my_data_array)} data items")
            if len(obj.my_data.my_data_array) > 0:
                for i, data in enumerate(obj.my_data.my_data_array):
                    res = export_object_path_curve_pos(obj, data, self)
                    if res:
                        exported.append(res)
                    else:
                        self.report({'ERROR'}, f"Could not export path for object {obj.name} with data {data.point_definition_name}")

        self.report({'INFO'}, f"Exported {len(exported)} paths")
        self.report({'INFO'}, f"Exported {exported[0][0]} paths")

        return {'FINISHED'}

class WM_OT_ExportSelectedPaths(bpy.types.Operator):
    bl_idname = "wm.vivify_export_paths_selected"
    bl_label = "Export Selected Paths"
    bl_category = "Vivify"

    def execute(self, context):
        for obj in bpy.data.objects:
            self.report({'INFO'}, f"Object {obj.name} has {len(obj.my_data.my_data_array)} data items")
            if len(obj.my_data.my_data_array) > 0:
                for i, data in enumerate(obj.my_data.my_data_array):
                    export_object_path_curve_pos(obj, data, self)

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
    bl_label = "Vivify Menu"
    bl_idname = "VIEW3D_MT_vivify_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.vivify_export_paths", text="Export Paths")

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

        if context.selected_objects:
            layout.label(text="Selected objects:")
            for obj in context.selected_objects:
                layout.label(text=obj.name)

        if len(context.selected_objects) > 0:
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
                        box.prop(current_selected_object.my_data.my_data_array[i], "export")
                        box.prop(current_selected_object.my_data.my_data_array[i], "export_position")
                        box.prop(current_selected_object.my_data.my_data_array[i], "export_rotation")
                        box.prop(current_selected_object.my_data.my_data_array[i], "export_scale")
                        box.prop(current_selected_object.my_data.my_data_array[i], "steps")
                        box.prop(current_selected_object.my_data.my_data_array[i], "start_frame")
                        box.prop(current_selected_object.my_data.my_data_array[i], "end_frame")

                    # Add a "Remove" button next to each item
                    remove_button = box.operator("wm.vivify_remove_path_data", text="Remove Path Data")
                    remove_button.index = i  # Pass the index of the current data
                    remove_button.selection_index = sel_index  # Pass the index of the current object
                sel_index += 1
        else:
            layout.label(text="No object selected")
