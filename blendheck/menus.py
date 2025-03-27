import bpy
from typing import Tuple, Union

def enum_path_items(self, context) -> tuple[tuple[str, str, str]]:
    # with your logic to fetch and return the map data.
    map_data = context.scene.vivify_map_data
    items = [(str(i), f"{i}", f"") for i in map_data["customData"]["pointDefinitions"].keys()]
    return [("[ No path ]", "[ No path ]", "")] + items

class PreviewMenu(bpy.types.Panel):
    bl_idname = "OBJECT_MT_preview_menu"
    bl_label = "Apply paths"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Beatmap Data"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Position Path to apply")
        layout.prop(context.scene, "vivify_preview_path_pos", text="")
        if context.scene.vivify_preview_path_pos != "[ No path ]":
            layout.prop(context.scene, "vivify_preview_path_start_frame_pos", text="Start Frame")
            layout.prop(context.scene, "vivify_preview_path_end_frame_pos", text="End Frame")
        else:
            layout.label(text="Static Position")
            col = layout.column(align=True)
            col.prop(context.scene, "vivify_preview_static_pos_x", text="X")
            col.prop(context.scene, "vivify_preview_static_pos_y", text="Y")
            col.prop(context.scene, "vivify_preview_static_pos_z", text="Z")
        layout.separator()
        layout.label(text="Rotation Path to apply")
        layout.prop(context.scene, "vivify_preview_path_rot", text="")
        if context.scene.vivify_preview_path_rot != "[ No path ]":
            layout.prop(context.scene, "vivify_preview_path_start_frame_rot", text="Start Frame")
            layout.prop(context.scene, "vivify_preview_path_end_frame_rot", text="End Frame")
        else:
            layout.label(text="Static Rotation")
            col = layout.column(align=True)
            col.prop(context.scene, "vivify_preview_static_rot_x", text="X")
            col.prop(context.scene, "vivify_preview_static_rot_y", text="Y")
            col.prop(context.scene, "vivify_preview_static_rot_z", text="Z")
        layout.separator()
        layout.label(text="Scale Path to apply")
        layout.prop(context.scene, "vivify_preview_path_scale", text="")
        if context.scene.vivify_preview_path_scale != "[ No path ]":
            layout.prop(context.scene, "vivify_preview_path_start_frame_scale", text="Start Frame")
            layout.prop(context.scene, "vivify_preview_path_end_frame_scale", text="End Frame")
        else:
            layout.label(text="Static Scale")
            col = layout.column(align=True)
            col.prop(context.scene, "vivify_preview_static_scale_x", text="X")
            col.prop(context.scene, "vivify_preview_static_scale_y", text="Y")
            col.prop(context.scene, "vivify_preview_static_scale_z", text="Z")
        layout.separator()
        layout.prop(context.scene, "vivify_convert_preview_coordinates")
        layout.operator("wm.vivify_preview_paths", text="Apply Paths")
