# Add-on description
# Copyright (C) YEAR AUTHOR
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# auto_load.py from https://github.com/JacquesLucke/blender_vscode
# Originally under the MIT License.

import importlib
import inspect
import pkgutil
import typing
from pathlib import Path
from . import panel_mypanel
from . import map
from . import handlers

import bpy

__all__ = (
    "init",
    "register",
    "unregister",
)

blender_version = typing.cast(typing.Tuple[int, int, int], bpy.app.version)

modules = None
ordered_classes = None

def init():
    global modules
    global ordered_classes

    if bpy is None or bpy.app is None or bpy.app.version is None:
        return

    modules = get_all_submodules(Path(__file__).parent)
    ordered_classes = get_ordered_classes_to_register(modules)

def register():
    bpy.types.TOPBAR_MT_editor_menus.append(panel_mypanel.draw_vivify_menu)
    bpy.types.Scene.vivify_export_path = bpy.props.StringProperty(
        name="Export File Path",
        description="Path to export the data",
        subtype='FILE_PATH',
    )
    bpy.types.Scene.vivify_convert_coordinates = bpy.props.BoolProperty(
        name="Convert Coordinates",
        description="Convert the coordinates to the Unity coordinates system (you might need this)",
        default=True,
    )
    bpy.types.Scene.vivify_preview_path_pos = bpy.props.EnumProperty(
        name="Position Path to preview",
        description="Position Path to preview",
        items=[]
    )
    bpy.types.Scene.vivify_preview_path_start_frame_pos = bpy.props.IntProperty(
        name="Start Frame",
        description="Start Frame",
        default=1,
    )
    bpy.types.Scene.vivify_preview_path_end_frame_pos = bpy.props.IntProperty(
        name="End Frame",
        description="End Frame",
        default=100,
    )
    bpy.types.Scene.vivify_preview_path_rot = bpy.props.EnumProperty(
        name="Rotation Path to preview",
        description="Rotation Path to preview",
        items=[]
    )
    bpy.types.Scene.vivify_preview_path_start_frame_rot = bpy.props.IntProperty(
        name="Start Frame",
        description="Start Frame",
        default=1,
    )
    bpy.types.Scene.vivify_preview_path_end_frame_rot = bpy.props.IntProperty(
        name="End Frame",
        description="End Frame",
        default=100,
    )
    bpy.types.Scene.vivify_preview_path_scale = bpy.props.EnumProperty(
        name="Scale Path to preview",
        description="Scale Path to preview",
        items=[]
    )
    bpy.types.Scene.vivify_preview_path_start_frame_scale = bpy.props.IntProperty(
        name="Start Frame",
        description="Start Frame",
        default=1,
    )
    bpy.types.Scene.vivify_preview_path_end_frame_scale = bpy.props.IntProperty(
        name="End Frame",
        description="End Frame",
        default=100,
    )
    bpy.app.handlers.save_post.append(handlers.save_map_handler)
    bpy.types.Scene.vivify_map_data = {}
    bpy.types.Scene.vivify_save_map_data_with_blend = bpy.props.BoolProperty()
    if ordered_classes is not None:
        for cls in ordered_classes:
            bpy.utils.register_class(cls)

    if modules is not None:
        for module in modules:
            if module.__name__ == __name__:
                continue
            if hasattr(module, "register"):
                module.register()

def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(panel_mypanel.draw_vivify_menu)
    bpy.app.handlers.load_pre.remove(handlers.load_map_handler)
    del bpy.types.Scene.vivify_export_path
    del bpy.types.Scene.vivify_map_data
    if ordered_classes is not None:
        for cls in reversed(ordered_classes):
            bpy.utils.unregister_class(cls)

    if modules is not None:
        for module in modules:
            if module.__name__ == __name__:
                continue
            if hasattr(module, "unregister"):
                module.unregister()


# Import modules
#################################################


def get_all_submodules(directory):
    return list(iter_submodules(directory, directory.name))


def iter_submodules(path, package_name):
    for name in sorted(iter_submodule_names(path)):
        yield importlib.import_module("." + name, package_name)


def iter_submodule_names(path, root=""):
    for _, module_name, is_package in pkgutil.iter_modules([str(path)]):
        if is_package:
            sub_path = path / module_name
            sub_root = root + module_name + "."
            yield from iter_submodule_names(sub_path, sub_root)
        else:
            yield root + module_name


# Find classes to register
#################################################


def get_ordered_classes_to_register(modules):
    return toposort(get_register_deps_dict(modules))


def get_register_deps_dict(modules):
    my_classes = set(iter_my_classes(modules))
    my_classes_by_idname = {
        cls.bl_idname: cls for cls in my_classes if hasattr(cls, "bl_idname")
    }

    deps_dict = {}
    for cls in my_classes:
        deps_dict[cls] = set(
            iter_my_register_deps(cls, my_classes, my_classes_by_idname)
        )
    return deps_dict


def iter_my_register_deps(cls, my_classes, my_classes_by_idname):
    yield from iter_my_deps_from_annotations(cls, my_classes)
    yield from iter_my_deps_from_parent_id(cls, my_classes_by_idname)


def iter_my_deps_from_annotations(cls, my_classes):
    for value in typing.get_type_hints(cls, {}, {}).values():
        dependency = get_dependency_from_annotation(value)
        if dependency is not None:
            if dependency in my_classes:
                yield dependency


def get_dependency_from_annotation(value):
    if blender_version >= (2, 93):
        if isinstance(value, bpy.props._PropertyDeferred):  # type: ignore
            return value.keywords.get("type")
    else:
        if isinstance(value, tuple) and len(value) == 2:
            if value[0] in (bpy.props.PointerProperty, bpy.props.CollectionProperty):
                return value[1]["type"]
    return None


def iter_my_deps_from_parent_id(cls, my_classes_by_idname):
    if bpy.types.Panel in cls.__bases__:
        parent_idname = getattr(cls, "bl_parent_id", None)
        if parent_idname is not None:
            parent_cls = my_classes_by_idname.get(parent_idname)
            if parent_cls is not None:
                yield parent_cls


def iter_my_classes(modules):
    base_types = get_register_base_types()
    for cls in get_classes_in_modules(modules):
        if any(base in base_types for base in cls.__bases__):
            if not getattr(cls, "is_registered", False):
                yield cls


def get_classes_in_modules(modules):
    classes = set()
    for module in modules:
        for cls in iter_classes_in_module(module):
            classes.add(cls)
    return classes


def iter_classes_in_module(module):
    for value in module.__dict__.values():
        if inspect.isclass(value):
            yield value


def get_register_base_types():
    return set(
        getattr(bpy.types, name)
        for name in [
            "Panel",
            "Operator",
            "PropertyGroup",
            "AddonPreferences",
            "Header",
            "Menu",
            "Node",
            "NodeSocket",
            "NodeTree",
            "UIList",
            "RenderEngine",
            "Gizmo",
            "GizmoGroup",
        ]
    )


# Find order to register to solve dependencies
#################################################

def toposort(deps_dict):
    sorted_list = []
    sorted_values = set()
    while len(deps_dict) > 0:
        unsorted = []
        for value, deps in deps_dict.items():
            if len(deps) == 0:
                sorted_list.append(value)
                sorted_values.add(value)
            else:
                unsorted.append(value)
        deps_dict = {value: deps_dict[value] - sorted_values for value in unsorted}
    return sorted_list
