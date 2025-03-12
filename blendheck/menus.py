import bpy

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
        layout.prop(context.scene, "vivify_preview_path_start_frame_pos", text="Start Frame")
        layout.prop(context.scene, "vivify_preview_path_end_frame_pos", text="End Frame")
        layout.separator()
        layout.label(text="Rotation Path to preview")
        layout.prop(context.scene, "vivify_preview_path_rot", text="")
        layout.prop(context.scene, "vivify_preview_path_start_frame_rot", text="Start Frame")
        layout.prop(context.scene, "vivify_preview_path_end_frame_rot", text="End Frame")
        layout.separator()
        layout.label(text="Scale Path to preview")
        layout.prop(context.scene, "vivify_preview_path_scale", text="")
        layout.prop(context.scene, "vivify_preview_path_start_frame_scale", text="Start Frame")
        layout.prop(context.scene, "vivify_preview_path_end_frame_scale", text="End Frame")
        layout.separator()
        layout.operator("wm.vivify_preview_paths", text="Preview Paths")
