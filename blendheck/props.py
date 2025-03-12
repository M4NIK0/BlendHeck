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
    path_type: bpy.props.EnumProperty(name = "Path Type", description = "Choose curve type",
                                      items = (
                                          ('Curve/Custom', "Curve/Custom", "Used to manage custom animations such as baked physics or bézier curves"),
                                          ('Keyframes', "Keyframes", "Used to manage keyframes animations for precise control"),
                                      ))
    keyframe_type: bpy.props.EnumProperty(name = "Property", description = "Choose which property to animate",
                                      items = (
                                          ('Position', "Position", "Position of the object"),
                                          ('Rotation', "Rotation", "Rotation of the object"),
                                          ('Scale', "Scale", "Scale of the object"),
                                      ))

    # Add a collapsed property to control visibility
    collapsed: bpy.props.BoolProperty(name="Collapsed", default=False)

class VivifyPropArray(bpy.types.PropertyGroup):
    my_data_array: bpy.props.CollectionProperty(type=VivifyProp)

class VivifyPreviewPointPropertyGroup(bpy.types.PropertyGroup):
    x: bpy.props.FloatProperty(name="X", description="X coordinate", default=0.0)
    y: bpy.props.FloatProperty(name="Y", description="Y coordinate", default=0.0)
    z: bpy.props.FloatProperty(name="Z", description="Z coordinate", default=0.0)
