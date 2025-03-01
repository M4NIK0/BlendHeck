import bpy
import bpy.app.handlers as hdlrs
from . import map

@hdlrs.persistent
def load_map_handler(scene) -> None:
    scene.vivify_map_data.clear()
