import bpy
import json

def get_map_file(path: str) -> dict:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def update_export_path(self: bpy.types.bpy_struct, context: bpy.types.Context) -> None:
    path = context.scene.vivify_export_path

    map_data = get_map_file(path)
    if map_data == {}:
        bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Invalid map file"), title="Error", icon='ERROR')
        return

    try:
        context.scene.vivify_map_data.update(map_data)
    except Exception as e:
        bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=e), title="Error", icon='ERROR')

    bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Map file loaded" + f"{context.scene.vivify_map_data}"), title="Info", icon='INFO')
