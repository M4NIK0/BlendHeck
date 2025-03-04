import bpy
import bpy.app.handlers as hdlrs
from . import map
import json

@hdlrs.persistent
def load_map_handler(scene) -> None:
    scene.vivify_map_data.clear()

@hdlrs.persistent
def save_map_handler(dummy) -> None:
    if bpy.context.scene.vivify_map_data:
        if bpy.context.scene.vivify_export_path == "" or bpy.context.scene.vivify_export_path is None:
            return
        with open(bpy.context.scene.vivify_export_path, "w") as file:
            file.write(json.dumps(bpy.context.scene.vivify_map_data))
