# pylint: disable=import-error

bl_info = {
    "name" : "Unity Easy Export",
    "description" : "",
    "author" : "Alexander Haas",
    "version" : (0, 0, 1),
    "blender" : (2, 80, 0),
    "location" : "",
    "warning" : "",
    "wiki_url": "",
    "tracker_url": "",
    "category" : "Development"
}

import bpy
import os
from bpy.props import (BoolProperty,
                      EnumProperty,
                      PointerProperty,
                      StringProperty,
                      )

from bpy.types import (PropertyGroup,
                      Panel,
                      Operator,
                      )

class MyProperties(PropertyGroup):

    exportOnSave: BoolProperty(
        name="Export on save",
        description="A bool property",
        default = False
    )
    path: StringProperty(
        name="Path",
        default="./"
    )
    collection_list: EnumProperty(
        name="",
        items=[]
    )

class ExportObjects(Operator):
    bl_idname = "easy_export.export_selected_object"
    bl_label = "Export Object(s)"
    # bl_description = ""
    
    @classmethod
    def poll(self, context):
        return True
        
    def execute(self, context):
        path = os.path.abspath(context.scene.my_tool.path)

        if not os.path.exists(path):
            os.makedirs(path)

        for obj in bpy.context.selected_objects:
            filename = obj.name + ".fbx"
            full_path = os.path.join(path, filename)
            bpy.ops.export_scene.fbx(
                filepath= str(full_path),
                check_existing=False, 
                use_selection=True, 
                bake_space_transform=True,
                axis_forward='-Z',
                axis_up='Y'
            )
            self.report({'INFO'}, "Exported {} to {}".format(obj.name, full_path))

        
        return{"FINISHED"}

class UNITYEASYEXPORT_PT_panel(Panel):
    bl_idname = 'test_world'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "easyExport"
    bl_label = "Unity Easy Export"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return context.object
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "path")
        col = layout.column(align = True)
        col.operator("easy_export.export_selected_object", icon = "EXPORT")

classes = (
    MyProperties,
    ExportObjects,
    UNITYEASYEXPORT_PT_panel,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)
    

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
