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
        if vatproperties.target_armature != None:
            return (functions.arm.scheme == 0 and functions.arm.sfm == False and functions.arm.scheme != -1)
    
    def execute(self, context):
        functions.armature_rename(1)
        
        return{'FINISHED'}
    
class VAT_OT_armaturerename_source(bpy.types.Operator): #Converts armature scheme back to the original
    """Reverts back to original Source friendly scheme for export"""
    bl_idname = "vat.armaturerename_source"
    bl_label = "Original scheme"
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            return (functions.arm.scheme == 1 and functions.arm.sfm == False and functions.arm.scheme != -1)
    
    def execute(self, context):
        functions.armature_rename(0)
        
        return{'FINISHED'}
    
class VAT_OT_constraintsymmetry_create(bpy.types.Operator):
    """Creates symmetry with constraints to allow for armature reproportioning while keeping correct roll values"""
    bl_idname = "vat.constraintsymmetry_create"
    bl_label = "Roll Corrected Symmetry"
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            if functions.arm.scheme != -1:
                if vatproperties.affected_side == 'OP1':
                    return (functions.arm.symmetry_left == False and functions.arm.symmetry_right == False)
                elif vatproperties.affected_side == 'OP2':
                    return (functions.arm.symmetry_right == False and functions.arm.symmetry_left == False)


    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        functions.constraint_symmetry(0, vatproperties.affected_side)
        
        return{'FINISHED'}
    
class VAT_OT_constraintsymmetry_delete(bpy.types.Operator):
    """Removes previously added constraints"""
    bl_idname = "vat.constraintsymmetry_delete"
    bl_label = "Symmetry Constraints Removal"
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            if functions.arm.scheme != -1:
                if vatproperties.affected_side == 'OP1':
                    return (functions.arm.symmetry_left == True)
                elif vatproperties.affected_side == 'OP2':
                    return (functions.arm.symmetry_right == True)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        functions.constraint_symmetry(1, vatproperties.affected_side)
        
        return{'FINISHED'}
    
class VAT_OT_weightarmature_create(bpy.types.Operator):
    """Duplicates armature with connected bones"""
    bl_idname = "vat.weightarmature_create"
    bl_label = "Better Automatic Weighting"
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            return (functions.arm.weight_armature == False and functions.arm.scheme != -1)

    def execute(self, context):
        functions.weight_armature(0)

        return{'FINISHED'}

class VAT_OT_weightarmature_delete(bpy.types.Operator):
    """Removes duplicate armature"""
    bl_idname = "vat.weightarmature_delete"
    bl_label = "Duplicate Armature Removal"

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            return (functions.arm.weight_armature == True and functions.arm.scheme != -1)

    def execute(self, context):
        functions.weight_armature(1)

        return{'FINISHED'}

class VAT_OT_inversekinematics_create(bpy.types.Operator):
    """Creates simple Inverse Kinematics (IK)"""
    bl_idname = "vat.inversekinematics_create"
    bl_label = "Simple IK"
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            return (functions.arm.inverse_kinematics == False and functions.arm.scheme != -1)

    def execute(self, context):
        functions.inverse_kinematics(0)
        
        return{'FINISHED'}

class VAT_OT_inversekinematics_delete(bpy.types.Operator):
    """Deletes simple Inverse Kinematics (IK)"""
    bl_idname = "vat.inversekinematics_delete"
    bl_label = "Simple IK Removal"
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            return (functions.arm.inverse_kinematics == True and functions.arm.scheme != -1)

    def execute(self, context):
        functions.inverse_kinematics(1)
        
        return{'FINISHED'}
    
class VAT_OT_rigifyretarget_create(bpy.types.Operator):
    """Creates animation ready armature"""
    bl_idname = "vat.rigifyretarget_create"
    bl_label = "Custom Animation Ready Armature"

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            return (functions.arm.animation_armature == False and functions.arm.scheme != -1)

    def execute(self, context):
        functions.anim_armature(0)

        return{'FINISHED'}

class VAT_OT_rigifyretarget_delete(bpy.types.Operator):
    """Deletes generated armature"""
    bl_idname = "vat.rigifyretarget_delete"
    bl_label = "Animation Ready Armature Removal"

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            return (functions.arm.animation_armature == True and functions.arm.scheme != -1)

    def execute(self, context):
        functions.anim_armature(1)

        return{'FINISHED'}

class VAT_OT_rigifyretarget_link(bpy.types.Operator):
    """Connects original armature with generated Rigify armature"""
    bl_idname = "vat.rigifyretarget_link"
    bl_label = "Animation Ready Armature Link"

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            return (functions.arm.animation_armature == True and functions.arm.animation_armature_setup == True and functions.arm.scheme != -1)

    def execute(self, context):
        functions.anim_armature(2)

        return{'FINISHED'}

class VAT_OT_rigifyretarget_update(bpy.types.Operator):
    """Connects original armature with generated Rigify armature"""
    bl_idname = "vat.rigifyretarget_update"
    bl_label = "Animation Ready Armature Empty Update"

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            return (functions.arm.animation_armature == True and functions.arm.animation_armature_setup == False and functions.arm.scheme != -1)

    def execute(self, context):
        functions.anim_armature(3)

        return{'FINISHED'}