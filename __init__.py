import bpy

#from . import addon_updater_ops
#from . import preferences

from . import armature_rename
from . import constraint_symmetry
from . import weight_armature
from . import simple_ik
from . import utils
from . import props
from . import ops
from . import ui

bl_info = {
    "name": "Valve Armature Toolkit",
    "author": "Haggets",
    "version": (0, 55),
    "blender": (2, 83, 10),
    "location": "Properties > Object Data (Armature)",
    "description": "Various utilities to make using the Valve armature more bearable",
    "category": "Armature"}
            
classes = [props.VAT_properties, ui.VAT_PT_mainpanel, ui.VAT_PT_armaturerename, ui.VAT_PT_constraintsymmetry, ui.VAT_PT_weightarmature, ui.VAT_PT_inversekinematics, ui.VAT_PT_rigifyretarget, ops.VAT_OT_armaturerename_blender, ops.VAT_OT_armaturerename_source, ops.VAT_OT_constraintsymmetry_create, ops.VAT_OT_constraintsymmetry_delete, ops.VAT_OT_weightarmature_create, ops.VAT_OT_weightarmature_delete, ops.VAT_OT_inversekinematics_create, ops.VAT_OT_inversekinematics_delete, ops.VAT_OT_rigifyretarget_create, ops.VAT_OT_rigifyretarget_delete, ops.VAT_OT_rigifyretarget_link, ops.VAT_OT_rigifyretarget_update]

def register():

    #addon_updater_ops.register(bl_info)

    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.vatproperties = bpy.props.PointerProperty(type=props.VAT_properties)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.vatproperties

if __name__ == "__main__":
    register()