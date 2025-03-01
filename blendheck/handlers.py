import bpy
import bpy.app.handlers as hdlrs
from . import map

@hdlrs.persistent
def load_map_handler(scene) -> None:
    if scene.vivify_export_path:
        map_data = map.get_map_file(scene.vivify_export_path)
        bpy.context.scene.vivify_map_data.update(map_data)
    else:
        bpy.context.scene.vivify_map_data.clear()
