import bpy

#Updater
from . import addon_updater_ops
from . import preferences

from . import armature_rename
from . import constraint_symmetry
from . import weight_armature
from . import armature_creation
from . import utils
from . import props
from . import ops
from . import ui

bl_info = {
    "name": "Source Armature Toolkit",
    "author": "Haggets",
    "version": (0, 9, 0),
    "blender": (2, 83, 10),
    "location": "Properties > Object Data (Armature)",
    "description": "Various utilities to ease the work while working with Source engine armatures.",
    "url": "https://github.com/Haggets/valve-armature-toolkit",
    "wiki_url": "https://github.com/Haggets/valve-armature-toolkit",
    "tracker_url": "https://github.com/Haggets/valve-armature-toolkit/issues",
    "category": "Armature"}
            
classes = [props.SAT_properties, props.SAT_info, preferences.SAT_preferences, ui.SAT_PT_mainpanel, ui.SAT_PT_armaturerename, ui.SAT_PT_constraintsymmetry, ui.SAT_PT_weightarmature, ui.SAT_PT_rigifyretarget, ui.SAT_PT_rigifyretargetexport, ops.SAT_OT_create_armature, ops.SAT_OT_convert_armature, ops.SAT_OT_armaturerename_blender, ops.SAT_OT_armaturerename_source, ops.SAT_OT_constraintsymmetry_create, ops.SAT_OT_constraintsymmetry_delete, ops.SAT_OT_constraintsymmetry_apply, ops.SAT_OT_weightarmature_create, ops.SAT_OT_weightarmature_delete, ops.SAT_OT_rigifyretarget_create, ops.SAT_OT_rigifyretarget_delete, ops.SAT_OT_rigifyretarget_generate, ops.SAT_OT_rigifyretarget_link, ops.SAT_OT_rigifyretarget_bake_single, ops.SAT_OT_rigifyretarget_bake_all, ops.SAT_OT_rigifyretarget_export_all]

def register():

    #Registers addon updater
    addon_updater_ops.register(bl_info)

    #Registers everything else
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.satproperties = bpy.props.PointerProperty(type=props.SAT_properties)
    bpy.types.Scene.satinfo = bpy.props.PointerProperty(type=props.SAT_info)

    bpy.app.handlers.load_post.append(utils.create_armature)
    bpy.app.handlers.undo_post.append(utils.armatures_reset)
    bpy.app.handlers.redo_post.append(utils.armatures_reset)

def unregister():

    addon_updater_ops.unregister()

    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    bpy.app.handlers.load_post.remove(utils.create_armature)
    bpy.app.handlers.undo_post.remove(utils.armatures_reset)
    bpy.app.handlers.redo_post.remove(utils.armatures_reset)
        
    del bpy.types.Scene.satproperties
    del bpy.types.Scene.satinfo

if __name__ == "__main__":
    register()
