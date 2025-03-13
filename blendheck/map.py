import bpy
import json

from . import menus

def get_map_file(path: str) -> dict:
    try:
        with open(path, "r") as file:
            imported = json.load(file)
            if "version" not in imported or imported["version"][0] != '3':
                return {}
            if "basicBeatmapEvents" not in imported:
                return {}
            if "colorNotes" not in imported:
                return {}
            return imported
    except FileNotFoundError:
        return {}

def setup_point_definitions(level: dict):
    if "customData" not in level:
        level["customData"] = {"pointDefinitions": {}}
        return level
    if "pointDefinitions" not in level["customData"]:
        level["customData"]["pointDefinitions"] = {}
        return level
    return level

def get_point_definitions(level: dict):
    if "customData" not in level or "pointDefinitions" not in level["customData"]:
        return []
    return [pd for pd in level["customData"]["pointDefinitions"].keys()]

class WM_OT_LoadMapFile(bpy.types.Operator):
    bl_idname = "wm.vivify_load_map_file"
    bl_label = "Load Map File"
    bl_category = "Vivify"

    def execute(self, context):
        if not context.scene.vivify_export_path:
            self.report({'ERROR'}, "No map file path set")
            return {'CANCELLED'}

        loaded = get_map_file(context.scene.vivify_export_path)

        if loaded == {}:
            self.report({'ERROR'}, "Failed to load map file")
            return {'CANCELLED'}

        context.scene.vivify_map_data.clear()
        context.scene.vivify_map_data.update(loaded)
        self.report({'INFO'}, "Map file loaded")

        # context.scene.vivify_preview_path_rot = "Default"

        return {'FINISHED'}

class WM_OT_RemoveMapPath(bpy.types.Operator):
    bl_idname = "wm.vivify_remove_map_path_data"
    bl_label = "Remove Map Path Data"

    path_key: bpy.props.StringProperty()

    def execute(self, context):
        context.scene.vivify_map_data["customData"]["pointDefinitions"].pop(self.path_key)
        return {'FINISHED'}

class WM_OT_SaveMapData(bpy.types.Operator):
    bl_idname = "wm.vivify_save_map_data"
    bl_label = "Save Map Data"

    def execute(self, context):
        if context.scene.vivify_export_path == "" or context.scene.vivify_export_path is None:
            self.report({'ERROR'}, "No export path set")
            return {'CANCELLED'}
        with open(context.scene.vivify_export_path, "w") as file:
            file.write(json.dumps(context.scene.vivify_map_data))
        self.report({'INFO'}, "Map data saved")
        return {'FINISHED'}

class MYADDON_PT_MapDataPanel(bpy.types.Panel):
    bl_label = "Map Point Definitions"
    bl_idname = "MYADDON_PT_MapDataPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Beatmap Data"

    def draw(self, context):
        layout = self.layout

        for pd in get_point_definitions(context.scene.vivify_map_data):
            box = layout.box()
            row = box.row()
            row.label(text=pd)

            remove_button = row.operator("wm.vivify_remove_map_path_data", text="", icon="X")
            remove_button.path_key = pd