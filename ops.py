import bpy
from . import functions
from . import props

class VAT_OT_armaturerename_blender(bpy.types.Operator): #Converts armature scheme to become Blender friendly
    """Converts to Blender friendly scheme to allow for symmetry"""
    bl_idname = "vat.armaturerename_blender"
    bl_label = "Blender Friendly Scheme"
    
    @classmethod #Checks if an armature is selected and it is not an SFM one, since it doesn't need it
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        return (vatproperties.target_armature is not None and vatproperties.sfm_armature is False and vatproperties.scheme is not True)
    
    def execute(self, context):
        functions.ArmatureRename.execute(1)
        
        return{'FINISHED'}
    
class VAT_OT_armaturerename_source(bpy.types.Operator): #Converts armature scheme back to the original
    """Reverts back to original Source friendly scheme for export"""
    bl_idname = "vat.armaturerename_source"
    bl_label = "Original scheme"
    
    @classmethod #Same as before
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        return (vatproperties.target_armature is not None and vatproperties.sfm_armature is False and vatproperties.scheme is not False)
    
    def execute(self, context):
        functions.ArmatureRename.execute(0)
        
        return{'FINISHED'}
    
class VAT_OT_constraintsymmetry_create(bpy.types.Operator):
    """Creates symmetry with constraints to allow for armature reproportioning while keeping correct roll values"""
    bl_idname = "vat.constraintsymmetry_create"
    bl_label = "Roll Corrected Symmetry"
    
    @classmethod #Same as before
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        return (vatproperties.target_armature is not None)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        functions.ConstraintSymmetry.execute(0)
        
        return{'FINISHED'}
    
class VAT_OT_constraintsymmetry_delete(bpy.types.Operator):
    """Removes previously added constraints"""
    bl_idname = "vat.constraintsymmetry_delete"
    bl_label = "Symmetry Constraints Removal"
    
    @classmethod #Same as before
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        return (vatproperties.target_armature is not None)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        functions.ConstraintSymmetry.execute(1)
        
        return{'FINISHED'}
    
class VAT_OT_weightarmature_create(bpy.types.Operator):
    """Duplicates armature with connected bones"""
    bl_idname = "vat.weightarmature_create"
    bl_label = "Better Automatic Weighting"
    
    @classmethod #Same as before
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        return (vatproperties.target_armature is not None)

    def execute(self, context):
        functions.WeightArmature.execute(0)

        return{'FINISHED'}

class VAT_OT_weightarmature_delete(bpy.types.Operator):
    """Removes duplicate armature"""
    bl_idname = "vat.weightarmature_delete"
    bl_label = "Duplicate Armature Removal"

    @classmethod #Same as before
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        return (vatproperties.target_armature is not None)

    def execute(self, context):
        functions.WeightArmature.execute(1)

        return{'FINISHED'}

class VAT_OT_inversekinematics_create(bpy.types.Operator):
    """Creates simple Inverse Kinematics (IK)"""
    bl_idname = "vat.inversekinematics_create"
    bl_label = "Simple IK"
    
    @classmethod #Same as before
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        return (vatproperties.target_armature is not None)

    def execute(self, context):
        functions.InverseKinematics.execute(0)
        
        return{'FINISHED'}

class VAT_OT_inversekinematics_delete(bpy.types.Operator):
    """Deletes simple Inverse Kinematics (IK)"""
    bl_idname = "vat.inversekinematics_delete"
    bl_label = "Simple IK Removal"
    
    @classmethod #Same as before
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        return (vatproperties.target_armature is not None)

    def execute(self, context):
        functions.InverseKinematics.execute(1)
        
        return{'FINISHED'}
    
class VAT_OT_rigifyretarget_create(bpy.types.Operator):
    """Creates animation ready armature"""
    bl_idname = "vat.rigifyretarget_create"
    bl_label = "Custom Animation Ready Armature"

class VAT_OT_rigifyretarget_delete(bpy.types.Operator):
    """Deletes generated armature"""
    bl_idname = "vat.rigifyretarget_delete"
    bl_label = "Animation Ready Armature Removal"