import bpy
import importlib
import sys

bl_info = {
    "name": "Reload",
    "blender": (4, 2, 0),
    "category": "Object",
}


def register():
    bpy.utils.register_class(ReloadPanel)
    bpy.utils.register_class(ReloadOperator)


def unregister():
    bpy.utils.unregister_class(ReloadPanel)
    bpy.utils.unregister_class(ReloadOperator)


bpy.types.Scene.reload_lib_name = bpy.props.StringProperty(  # type: ignore
    name="Library name field", description="Library name to reload"
)


class ReloadPanel(bpy.types.Panel):
    bl_label = "Reload"
    bl_idname = "OBJECT_PT_reload_library"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Reload"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "reload_lib_name", text="")
        layout.label(text=f"Target: {context.scene.reload_lib_name}")  # type: ignore
        layout.operator("object.reload_visual", text="Reload")


class ReloadOperator(bpy.types.Operator):
    bl_idname = "object.reload_visual"
    bl_label = "Reload Visual"

    def execute(self, context):
        addon_name = context.scene.reload_lib_name  # type: ignore
        self.report({"INFO"}, f"Test: {addon_name}")
        if addon_name in bpy.context.preferences.addons:
            bpy.ops.preferences.addon_disable(module=addon_name)

            package_name = addon_name
            for module_name in list(sys.modules.keys()):
                if module_name.startswith(package_name):
                    del sys.modules[module_name]
                    self.report({"INFO"}, f"Model has been deleted!")

            # Reload the main module
            importlib.import_module(addon_name)

            bpy.ops.preferences.addon_enable(module=addon_name)
        else:
            self.report({"INFO"}, f"Add-on '{addon_name}' is not found!")
            addon_list_str = ""
            for addon in bpy.context.preferences.addons:
                addon_list_str = addon_list_str + f"{addon.module}\n"

            self.report({"INFO"}, f"Add-ons:\n{addon_list_str}")
        return {"FINISHED"}
