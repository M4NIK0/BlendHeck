import bpy

class VivifyProp(bpy.types.PropertyGroup):
    point_definition_name: bpy.props.StringProperty(name="Name", default="Animation")
    export: bpy.props.BoolProperty(name="Export", default=True)
    export_position: bpy.props.BoolProperty(name="Export Position", default=True)
    export_rotation: bpy.props.BoolProperty(name="Export Rotation", default=True)
    export_scale: bpy.props.BoolProperty(name="Export Scale", default=True)
    steps: bpy.props.IntProperty(name="Steps", default=10)
    start_frame: bpy.props.IntProperty(name="Start Frame", default=1)
    end_frame: bpy.props.IntProperty(name="End Frame", default=100)

    # Add a collapsed property to control visibility
    collapsed: bpy.props.BoolProperty(name="Collapsed", default=False)

class VivifyPropArray(bpy.types.PropertyGroup):
    my_data_array: bpy.props.CollectionProperty(type=VivifyProp)
