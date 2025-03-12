import bpy
from typing import Tuple, Union

def enum_path_items(self, context) -> tuple[tuple[str, str, str]]:
    # with your logic to fetch and return the map data.
    map_data = context.scene.vivify_map_data
    items = [(str(i), f"{i}", f"") for i in map_data["customData"]["pointDefinitions"].keys()]
    return [("[ No preview ]", "[ No preview ]", "")] + items

class PreviewMenu(bpy.types.Panel):
    bl_idname = "OBJECT_MT_preview_menu"
    bl_label = "Preview Paths"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Vivify Preview"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Position Path to preview")
        layout.prop(context.scene, "vivify_preview_path_pos", text="")
        if context.scene.vivify_preview_path_pos != "[ No preview ]":
            layout.prop(context.scene, "vivify_preview_path_start_frame_pos", text="Start Frame")
            layout.prop(context.scene, "vivify_preview_path_end_frame_pos", text="End Frame")
        layout.separator()
        layout.label(text="Rotation Path to preview")
        layout.prop(context.scene, "vivify_preview_path_rot", text="")
        if context.scene.vivify_preview_path_rot != "[ No preview ]":
            layout.prop(context.scene, "vivify_preview_path_start_frame_rot", text="Start Frame")
            layout.prop(context.scene, "vivify_preview_path_end_frame_rot", text="End Frame")
        layout.separator()
        layout.label(text="Scale Path to preview")
        layout.prop(context.scene, "vivify_preview_path_scale", text="")
        if context.scene.vivify_preview_path_scale != "[ No preview ]":
            layout.prop(context.scene, "vivify_preview_path_start_frame_scale", text="Start Frame")
            layout.prop(context.scene, "vivify_preview_path_end_frame_scale", text="End Frame")
        layout.separator()
        layout.operator("wm.vivify_preview_paths", text="Preview Paths")
