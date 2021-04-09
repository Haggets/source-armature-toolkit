import bpy

#Updater
from . import addon_updater_ops
from . import preferences

from . import armature_rename
from . import constraint_symmetry
from . import weight_armature
from . import utils
from . import props
from . import ops
from . import ui

bl_info = {
    "name": "Valve Armature Toolkit",
    "author": "Haggets",
    "version": (0, 6, 0),
    "blender": (2, 83, 10),
    "location": "Properties > Object Data (Armature)",
    "description": "Various utilities to ease the work while working with Source engine armatures.",
    "url": "https://github.com/Haggets/valve-armature-toolkit",
    "wiki_url": "https://github.com/Haggets/valve-armature-toolkit",
    "tracker_url": "https://github.com/Haggets/valve-armature-toolkit/issues",
    "category": "Armature"}
            
classes = [props.VAT_properties, props.VAT_info, preferences.VAT_updaterpreferences, ui.VAT_PT_mainpanel, ui.VAT_PT_armaturerename, ui.VAT_PT_constraintsymmetry, ui.VAT_PT_weightarmature, ui.VAT_PT_rigifyretarget, ops.VAT_OT_armaturerename_blender, ops.VAT_OT_armaturerename_source, ops.VAT_OT_constraintsymmetry_create, ops.VAT_OT_constraintsymmetry_delete, ops.VAT_OT_weightarmature_create, ops.VAT_OT_weightarmature_delete, ops.VAT_OT_rigifyretarget_create, ops.VAT_OT_rigifyretarget_delete, ops.VAT_OT_rigifyretarget_link]

def register():

    #Registers addon updater
    addon_updater_ops.register(bl_info)

    #Registers everything else
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.vatproperties = bpy.props.PointerProperty(type=props.VAT_properties)
    bpy.types.Scene.vatinfo = bpy.props.PointerProperty(type=props.VAT_info)

    bpy.app.handlers.load_post.append(utils.create_armature)
    bpy.app.handlers.undo_post.append(utils.armatures_reset)
    bpy.app.handlers.redo_post.append(utils.armatures_reset)

def unregister():

    addon_updater_ops.unregister()

    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    bpy.app.handlers.load_post.remove(utils.create_armature)
    bpy.app.handlers.undo_post.append(utils.armatures_reset)
    bpy.app.handlers.redo_post.append(utils.armatures_reset)
        
    del bpy.types.Scene.vatproperties

if __name__ == "__main__":
    register()