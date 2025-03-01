import bpy
from . import props

class Point:
    x: float = 0
    y: float = 0
    z: float = 0
    precision: int = 4
    easing: str = None
    time: int = 0

    def __init__(self, x: float = 0, y: float = 0, z: float = 0, precision: int = 4, easing: str = None, time: float = 0):
        self.x = x
        self.y = y
        self.z = z
        self.precision = precision
        self.easing = easing
        self.time = time

    def __str__(self):
        return f"[{self.x:.{self.precision}f},{self.y:.{self.precision}f},{self.z:.{self.precision}f},{self.time}" + (f",\"{self.easing}\"" if self.easing else "") + "]"

class PositionPath:
    points: list[Point] = []
    name: str = "Animation"

    def __init__(self, points: list[Point], name: str):
        self.points = points
        self.name = name

    def __str__(self):
        return "[" + ",".join([str(p) for p in self.points]) + "]"

class RotationPath:
    points: list[Point] = []
    name: str = "Animation"

    def __init__(self, points: list[Point], name: str):
        self.points = points
        self.name = name

    def __str__(self):
        return "[" + ",".join([str(p) for p in self.points]) + "]"

class ScalePath:
    points: list[Point] = []
    name: str = "Animation"

    def __init__(self, points: list[Point], name: str):
        self.points = points
        self.name = name

    def __str__(self):
        return "[" + ",".join([str(p) for p in self.points]) + "]"

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