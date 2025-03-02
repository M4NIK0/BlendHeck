import bpy
import json

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

        return {'FINISHED'}
