import bpy
from . import paths
from . import map

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
