import bpy
from . import props

class Point:
    x: float = 0
    y: float = 0
    z: float = 0
    precision: int = 4
    easing: str = None
    time: float = None

    def __init__(self, x: float = 0, y: float = 0, z: float = 0, precision: int = 4, easing: str = None, time: float = None):
        self.x = x
        self.y = y
        self.z = z
        self.precision = precision
        self.easing = easing
        self.time = time

    def __str__(self):
        return f"[{self.x:.{self.precision}f},{self.y:.{self.precision}f},{self.z:.{self.precision}f}" + (f",{self.time}" if self.time is not None else "") + (f",\"{self.easing}\"" if self.easing else "") + "]"

    def get_json_list(self):
        return [self.x, self.y, self.z] + ([self.time] if self.time is not None else []) + ([self.easing] if self.easing else [])

class PositionPath:
    points: list[Point] = []
    name: str = "Animation"

    def __init__(self, points: list[Point], name: str):
        self.points = points
        self.name = name

    def __str__(self):
        return "[" + ",".join([str(p) for p in self.points]) + "]"

    def get_json_dict(self):
        return {self.name: [p.get_json_list() for p in self.points]}

class RotationPath:
    points: list[Point] = []
    name: str = "Animation"

    def __init__(self, points: list[Point], name: str):
        self.points = points
        self.name = name

    def __str__(self):
        return "[" + ",".join([str(p) for p in self.points]) + "]"

    def get_json_dict(self):
        return {self.name: [p.get_json_list() for p in self.points]}

class ScalePath:
    points: list[Point] = []
    name: str = "Animation"

    def __init__(self, points: list[Point], name: str):
        self.points = points
        self.name = name

    def __str__(self):
        return "[" + ",".join([str(p) for p in self.points]) + "]"

    def get_json_dict(self):
        return {self.name: [p.get_json_list() for p in self.points]}

def export_object_path_curve_pos(obj, path: props.VivifyProp, operator=None):
    localtransforms = False # TODO: add some stuff to the panel parameters
    points = []
    min = path.start_frame
    max = path.end_frame

    if min > max:
        if operator:
            operator.report({'ERROR'}, "Start frame must be less than end frame")
        return None

    if int((max - min) / path.steps) == 0:
        if operator:
            operator.report({'ERROR'}, "Steps must be less than the range of frames")
        return None

    for i in range(min, max + int((max - min) / path.steps), int((max - min) / path.steps)):
        current_animation_frame = round((i - min) / (max - min), 6)
        bpy.context.scene.frame_set(i)
        ol = None
        if localtransforms:
            ol = obj.location
        else:
            ol = obj.matrix_world.to_translation()
        points.append(Point(x=ol.x, y=ol.y, z=ol.z, time=current_animation_frame))

    if operator:
        operator.report({'INFO'}, f"Exported {len(points)} points for object {obj.name} with position curve {path.point_definition_name}")

    return PositionPath(points, path.point_definition_name + "_pos")

def export_object_path_curve_rot(obj, path: props.VivifyProp, operator=None):
    localtransforms = False # TODO: add some stuff to the panel parameters
    points = []
    min = path.start_frame
    max = path.end_frame

    if min > max:
        if operator:
            operator.report({'ERROR'}, "Start frame must be less than end frame")
        return None

    if int((max - min) / path.steps) == 0:
        if operator:
            operator.report({'ERROR'}, "Steps must be less than the range of frames")
        return None

    for i in range(min, max + int((max - min) / path.steps), int((max - min) / path.steps)):
        current_animation_frame = round((i - min) / (max - min), 6)
        bpy.context.scene.frame_set(i)
        ol = None
        if localtransforms:
            ol = obj.rotation_euler
        else:
            ol = obj.matrix_world.to_euler()
        points.append(Point(x=ol.x / 3.14159265359 * 180, y=ol.y / 3.14159265359 * 180, z=ol.z / 3.14159265359 * 180, time=current_animation_frame))

    if operator:
        operator.report({'INFO'}, f"Exported {len(points)} points for object {obj.name} with rotation curve {path.point_definition_name}")

    return RotationPath(points, path.point_definition_name + "_rot")

def export_object_path_curve_scale(obj, path: props.VivifyProp, operator=None):
    localtransforms = False # TODO: add some stuff to the panel parameters
    points = []
    min = path.start_frame
    max = path.end_frame

    if min > max:
        if operator:
            operator.report({'ERROR'}, "Start frame must be less than end frame")
        return None

    if int((max - min) / path.steps) == 0:
        if operator:
            operator.report({'ERROR'}, "Steps must be less than the range of frames")
        return None

    for i in range(min, max + int((max - min) / path.steps), int((max - min) / path.steps)):
        current_animation_frame = round((i - min) / (max - min), 6)
        bpy.context.scene.frame_set(i)
        ol = None
        if localtransforms:
            ol = obj.scale
        else:
            ol = obj.matrix_world.to_scale()
        points.append(Point(x=ol.x, y=ol.y, z=ol.z, time=current_animation_frame))

    if operator:
        operator.report({'INFO'}, f"Exported {len(points)} points for object {obj.name} with scale curve {path.point_definition_name}")

    return ScalePath(points, path.point_definition_name + "_scale")

def export_object_keyframes_pos(obj, path: props.VivifyProp, operator=None):
    localtransforms = False # TODO: add some stuff to the panel parameters
    points = []
    min = path.start_frame
    max = path.end_frame

    if min > max:
        if operator:
            operator.report({'ERROR'}, "Start frame must be less than end frame")
        return None

    if int((max - min) / path.steps) == 0:
        if operator:
            operator.report({'ERROR'}, "Steps must be less than the range of frames")
        return None

    if obj.animation_data is None or obj.animation_data.action is None:
        if operator:
            operator.report({'ERROR'}, "No animation data found for object")
        return None

    extracted_points_x = []
    extracted_points_y = []
    extracted_points_z = []

    for fcurve in obj.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            if "location" in fcurve.data_path:
                if keyframe.co.x >= min and keyframe.co.x <= max:
                    if fcurve.array_index == 0:
                        extracted_points_x.append({"time": keyframe.co.x, "value": keyframe.co.y})
                    elif fcurve.array_index == 1:
                        extracted_points_y.append({"time": keyframe.co.x, "value": keyframe.co.y})
                    elif fcurve.array_index == 2:
                        extracted_points_z.append({"time": keyframe.co.x, "value": keyframe.co.y})

    # Sort points by time
    extracted_points_x = sorted(extracted_points_x, key=lambda x: x["time"])
    extracted_points_y = sorted(extracted_points_y, key=lambda x: x["time"])
    extracted_points_z = sorted(extracted_points_z, key=lambda x: x["time"])

    # Put points together with their time
    for point_x in extracted_points_x:
        point_y = next((x for x in extracted_points_y if x["time"] == point_x["time"]), None)
        point_z = next((x for x in extracted_points_z if x["time"] == point_x["time"]), None)
        points.append(Point(x=point_x["value"], y=point_y["value"], z=point_z["value"], time=(point_x["time"] - min) / (max - min)))

    if operator:
        operator.report({'INFO'}, f"Exported {len(points)} points for object {obj.name} with position keyframes {path.point_definition_name}")
        for p in points:
            operator.report({'INFO'}, str(p))

    return PositionPath(points, path.point_definition_name)

def export_object_keyframes_rot(obj, path: props.VivifyProp, operator=None):
    localtransforms = False # TODO: add some stuff to the panel parameters
    points = []
    min = path.start_frame
    max = path.end_frame

    if min > max:
        if operator:
            operator.report({'ERROR'}, "Start frame must be less than end frame")
        return None

    if int((max - min) / path.steps) == 0:
        if operator:
            operator.report({'ERROR'}, "Steps must be less than the range of frames")
        return None

    if obj.animation_data is None or obj.animation_data.action is None:
        if operator:
            operator.report({'ERROR'}, "No animation data found for object")
        return None

    extracted_points_x = []
    extracted_points_y = []
    extracted_points_z = []

    for fcurve in obj.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            if "rotation_euler" in fcurve.data_path:
                if keyframe.co.x >= min and keyframe.co.x <= max:
                    if fcurve.array_index == 0:
                        extracted_points_x.append({"time": keyframe.co.x, "value": keyframe.co.y})
                    elif fcurve.array_index == 1:
                        extracted_points_y.append({"time": keyframe.co.x, "value": keyframe.co.y})
                    elif fcurve.array_index == 2:
                        extracted_points_z.append({"time": keyframe.co.x, "value": keyframe.co.y})

    # Sort points by time
    extracted_points_x = sorted(extracted_points_x, key=lambda x: x["time"])
    extracted_points_y = sorted(extracted_points_y, key=lambda x: x["time"])
    extracted_points_z = sorted(extracted_points_z, key=lambda x: x["time"])

    # Put points together with their time
    for point_x in extracted_points_x:
        point_y = next((x for x in extracted_points_y if x["time"] == point_x["time"]), None)
        point_z = next((x for x in extracted_points_z if x["time"] == point_x["time"]), None)
        points.append(Point(x=point_x["value"], y=point_y["value"], z=point_z["value"], time=(point_x["time"] - min) / (max - min)))

    if operator:
        operator.report({'INFO'}, f"Exported {len(points)} points for object {obj.name} with position keyframes {path.point_definition_name}")
        for p in points:
            operator.report({'INFO'}, str(p))

    return PositionPath(points, path.point_definition_name)

def export_object_keyframes_scale(obj, path: props.VivifyProp, operator=None):
    localtransforms = False # TODO: add some stuff to the panel parameters
    points = []
    min = path.start_frame
    max = path.end_frame

    if min > max:
        if operator:
            operator.report({'ERROR'}, "Start frame must be less than end frame")
        return None

    if int((max - min) / path.steps) == 0:
        if operator:
            operator.report({'ERROR'}, "Steps must be less than the range of frames")
        return None

    if obj.animation_data is None or obj.animation_data.action is None:
        if operator:
            operator.report({'ERROR'}, "No animation data found for object")
        return None

    extracted_points_x = []
    extracted_points_y = []
    extracted_points_z = []

    for fcurve in obj.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            if "scale" in fcurve.data_path:
                if keyframe.co.x >= min and keyframe.co.x <= max:
                    if fcurve.array_index == 0:
                        extracted_points_x.append({"time": keyframe.co.x, "value": keyframe.co.y})
                    elif fcurve.array_index == 1:
                        extracted_points_y.append({"time": keyframe.co.x, "value": keyframe.co.y})
                    elif fcurve.array_index == 2:
                        extracted_points_z.append({"time": keyframe.co.x, "value": keyframe.co.y})

    # Sort points by time
    extracted_points_x = sorted(extracted_points_x, key=lambda x: x["time"])
    extracted_points_y = sorted(extracted_points_y, key=lambda x: x["time"])
    extracted_points_z = sorted(extracted_points_z, key=lambda x: x["time"])

    # Put points together with their time
    for point_x in extracted_points_x:
        point_y = next((x for x in extracted_points_y if x["time"] == point_x["time"]), None)
        point_z = next((x for x in extracted_points_z if x["time"] == point_x["time"]), None)
        points.append(Point(x=point_x["value"], y=point_y["value"], z=point_z["value"], time=(point_x["time"] - min) / (max - min)))

    if operator:
        operator.report({'INFO'}, f"Exported {len(points)} points for object {obj.name} with position keyframes {path.point_definition_name}")
        for p in points:
            operator.report({'INFO'}, str(p))

    return PositionPath(points, path.point_definition_name)
