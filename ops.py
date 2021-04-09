import bpy
from .armature_rename import armature_rename
from .constraint_symmetry import constraint_symmetry
from .weight_armature import weight_armature
from .advanced_ik import anim_armature
from . import utils
from . import props

class VAT_OT_armaturerename_blender(bpy.types.Operator): #Converts armature scheme to become Blender friendly
    """Converts to Blender friendly scheme to allow for symmetry"""
    bl_idname = "vat.armaturerename_blender"
    bl_label = "Blender Friendly Scheme"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod #Checks if an armature is selected and it is not an SFM one, since it doesn't need it
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        if vatproperties.target_armature:
            return (not utils.arm.sfm and vatinfo.scheme != -1 and vatinfo.scheme == 0)
    
    def execute(self, context):
        vatinfo = bpy.context.scene.vatinfo
        armature_rename(1)
        vatinfo.scheme = 1
        
        return{'FINISHED'}
    
class VAT_OT_armaturerename_source(bpy.types.Operator): #Converts armature scheme back to the original
    """Reverts back to original Source friendly scheme for export"""
    bl_idname = "vat.armaturerename_source"
    bl_label = "Original scheme"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        if vatproperties.target_armature:
            return (not utils.arm.sfm and vatinfo.scheme != -1 and vatinfo.scheme == 1)
    
    def execute(self, context):
        vatinfo = bpy.context.scene.vatinfo
        armature_rename(0)
        vatinfo.scheme = 0

        return{'FINISHED'}
    
class VAT_OT_constraintsymmetry_create(bpy.types.Operator):
    """Creates symmetry with constraints to allow for armature reproportioning while keeping correct roll values"""
    bl_idname = "vat.constraintsymmetry_create"
    bl_label = "Roll Corrected Symmetry"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        if vatproperties.target_armature:
            if vatinfo.scheme != -1:
                return (not vatinfo.symmetry)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        constraint_symmetry(0, vatproperties.affected_side)
        if vatproperties.affected_side == 'OP1':
            vatinfo.symmetry = 1
        elif vatproperties.affected_side == 'OP2':
            vatinfo.symmetry = 2
        
        return{'FINISHED'}
    
class VAT_OT_constraintsymmetry_delete(bpy.types.Operator):
    """Removes previously added constraints"""
    bl_idname = "vat.constraintsymmetry_delete"
    bl_label = "Symmetry Constraints Removal"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        if vatproperties.target_armature:
            if vatinfo.scheme != -1:
                if vatproperties.affected_side == 'OP1':
                    return (vatinfo.symmetry == 1)
                elif vatproperties.affected_side == 'OP2':
                    return (vatinfo.symmetry == 2)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        constraint_symmetry(1, vatproperties.affected_side)
        vatinfo.symmetry = 0
        
        return{'FINISHED'}
    
class VAT_OT_weightarmature_create(bpy.types.Operator):
    """Duplicates armature with connected bones"""
    bl_idname = "vat.weightarmature_create"
    bl_label = "Better Automatic Weighting"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        if vatproperties.target_armature:
            return (not utils.arm.weight_armature_created and vatinfo.scheme != -1)

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
        vatinfo = bpy.context.scene.vatinfo
        if vatproperties.target_armature:
            return (utils.arm.weight_armature_created and vatinfo.scheme != -1)

    def execute(self, context):
        weight_armature(1)

        return{'FINISHED'}
    
class VAT_OT_rigifyretarget_create(bpy.types.Operator):
    """Creates animation ready armature"""
    bl_idname = "vat.rigifyretarget_create"
    bl_label = "Custom Animation Ready Armature"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        if vatproperties.target_armature:
            return (not utils.arm.animation_armature_created and vatinfo.scheme != -1)

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
        vatinfo = bpy.context.scene.vatinfo
        if vatproperties.target_armature:
            return (utils.arm.animation_armature_created and vatinfo.scheme != -1)

    def execute(self, context):
        anim_armature(1)

        return{'FINISHED'}

class VAT_OT_rigifyretarget_link(bpy.types.Operator):
    """Connects original armature with generated Rigify armature"""
    bl_idname = "vat.rigifyretarget_link"
    bl_label = "Animation Ready Armature Link"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature:
            return (context.object.name == "rig")

    def execute(self, context):
        anim_armature(2)

        return{'FINISHED'}
