import bpy
from .armature_rename import armature_rename
from .constraint_symmetry import constraint_symmetry
from .weight_armature import weight_armature
from .simple_ik import inverse_kinematics
from .advanced_ik import anim_armature
from . import functions
from . import props

class VAT_OT_armaturerename_blender(bpy.types.Operator): #Converts armature scheme to become Blender friendly
    """Converts to Blender friendly scheme to allow for symmetry"""
    bl_idname = "vat.armaturerename_blender"
    bl_label = "Blender Friendly Scheme"
    
    @classmethod #Checks if an armature is selected and it is not an SFM one, since it doesn't need it
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            return (functions.arm.scheme == 0 and not functions.arm.sfm and functions.arm.scheme != -1)
    
    def execute(self, context):
        bpy.ops.ed.undo_push()
        armature_rename(1)
        
        return{'FINISHED'}
    
class VAT_OT_armaturerename_source(bpy.types.Operator): #Converts armature scheme back to the original
    """Reverts back to original Source friendly scheme for export"""
    bl_idname = "vat.armaturerename_source"
    bl_label = "Original scheme"
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            return (functions.arm.scheme == 1 and not functions.arm.sfm and functions.arm.scheme != -1)
    
    def execute(self, context):
        bpy.ops.ed.undo_push()
        armature_rename(0)
        
        return{'FINISHED'}
    
class VAT_OT_constraintsymmetry_create(bpy.types.Operator):
    """Creates symmetry with constraints to allow for armature reproportioning while keeping correct roll values"""
    bl_idname = "vat.constraintsymmetry_create"
    bl_label = "Roll Corrected Symmetry"
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            if functions.arm.scheme != -1:
                if vatproperties.affected_side == 'OP1':
                    return (not functions.arm.symmetry_left and not functions.arm.symmetry_right)
                elif vatproperties.affected_side == 'OP2':
                    return (not functions.arm.symmetry_right and not functions.arm.symmetry_left)


    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        constraint_symmetry(0, vatproperties.affected_side)
        
        return{'FINISHED'}
    
class VAT_OT_constraintsymmetry_delete(bpy.types.Operator):
    """Removes previously added constraints"""
    bl_idname = "vat.constraintsymmetry_delete"
    bl_label = "Symmetry Constraints Removal"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            if functions.arm.scheme != -1:
                if vatproperties.affected_side == 'OP1':
                    return (functions.arm.symmetry_left)
                elif vatproperties.affected_side == 'OP2':
                    return (functions.arm.symmetry_right)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        constraint_symmetry(1, vatproperties.affected_side)
        
        return{'FINISHED'}
    
class VAT_OT_weightarmature_create(bpy.types.Operator):
    """Duplicates armature with connected bones"""
    bl_idname = "vat.weightarmature_create"
    bl_label = "Better Automatic Weighting"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            return (not functions.arm.weight_armature and functions.arm.scheme != -1)

    def execute(self, context):
        weight_armature(0)

        return{'FINISHED'}

class VAT_OT_weightarmature_delete(bpy.types.Operator):
    """Removes duplicate armature"""
    bl_idname = "vat.weightarmature_delete"
    bl_label = "Duplicate Armature Removal"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            return (functions.arm.weight_armature and functions.arm.scheme != -1)

    def execute(self, context):
        weight_armature(1)

        return{'FINISHED'}

class VAT_OT_inversekinematics_create(bpy.types.Operator):
    """Creates simple Inverse Kinematics (IK)"""
    bl_idname = "vat.inversekinematics_create"
    bl_label = "Simple IK"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            return (not functions.arm.inverse_kinematics and functions.arm.scheme != -1)

    def execute(self, context):
        inverse_kinematics(0)
        
        return{'FINISHED'}

class VAT_OT_inversekinematics_delete(bpy.types.Operator):
    """Deletes simple Inverse Kinematics (IK)"""
    bl_idname = "vat.inversekinematics_delete"
    bl_label = "Simple IK Removal"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            return (functions.arm.inverse_kinematics and functions.arm.scheme != -1)

    def execute(self, context):
        inverse_kinematics(1)
        
        return{'FINISHED'}
    
class VAT_OT_rigifyretarget_create(bpy.types.Operator):
    """Creates animation ready armature"""
    bl_idname = "vat.rigifyretarget_create"
    bl_label = "Custom Animation Ready Armature"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            return (not functions.arm.animation_armature and functions.arm.scheme != -1)

    def execute(self, context):
        anim_armature(0)

        return{'FINISHED'}

class VAT_OT_rigifyretarget_delete(bpy.types.Operator):
    """Deletes generated armature"""
    bl_idname = "vat.rigifyretarget_delete"
    bl_label = "Animation Ready Armature Removal"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            return (functions.arm.animation_armature and functions.arm.scheme != -1)

    def execute(self, context):
        anim_armature(1)

        return{'FINISHED'}

class VAT_OT_rigifyretarget_link(bpy.types.Operator):
    """Connects original armature with generated Rigify armature"""
    bl_idname = "vat.rigifyretarget_link"
    bl_label = "Animation Ready Armature Link"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            return (context.object.name == "rig")

    def execute(self, context):
        anim_armature(2)

        return{'FINISHED'}

class VAT_OT_rigifyretarget_update(bpy.types.Operator):
    """Connects original armature with generated Rigify armature"""
    bl_idname = "vat.rigifyretarget_update"
    bl_label = "Animation Ready Armature Empty Update"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            return (functions.arm.animation_armature and not functions.arm.animation_armature_setup and functions.arm.scheme != -1)

    def execute(self, context):
        anim_armature(3)

        return{'FINISHED'}