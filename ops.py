import bpy
from .armature_rename import armature_rename
from .constraint_symmetry import constraint_symmetry
from .weight_armature import weight_armature
from .advanced_ik import anim_armature
from .advanced_ik import bake
from .advanced_ik import export
from .armature_creation import armature
from . import utils

class VAT_OT_create_armature(bpy.types.Operator):
    """Creates armature from scratch"""
    bl_idname = "vat.create_armature"
    bl_label = "Create armature from scratch"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        vatinfo = bpy.context.scene.vatinfo

        armature(0)
        vatinfo.creating_armature = 1
        
        return{'FINISHED'}

class VAT_OT_convert_armature(bpy.types.Operator):
    """Converts armature to be Source like"""
    bl_idname = 'vat.convert_armature'
    bl_label = 'Convert Armature'
    bl_description = 'Converts armature to be like Source armatures (Unconnected with different orientation)'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        pass
        
        return{"FINISHED"}

class VAT_OT_armaturerename_blender(bpy.types.Operator): #Converts armature scheme to become Blender friendly
    """Converts to Blender friendly scheme to allow for symmetry"""
    bl_idname = "vat.armaturerename_blender"
    bl_label = "Blender Friendly Scheme"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod #Checks if an armature is selected and it is not an SFM one, since it doesn't need it
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        if vatproperties.target_armature and vatinfo.scheme == 0:
            return (not vatinfo.sfm and not vatinfo.sbox)
    
    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        if not vatproperties.target_armature.hide_get() and not vatproperties.target_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, place it in an active collection.")
        else:
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

        if vatproperties.target_armature and vatinfo.scheme == 1:
            return (not vatinfo.sfm and not vatinfo.sbox)
    
    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        if not vatproperties.target_armature.hide_get() and not vatproperties.target_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, place it in an active collection.")
        else:
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

        if vatproperties.target_armature and vatinfo.scheme != -1:
            return (not vatinfo.symmetry)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        constraint_symmetry(0, vatproperties.affected_side)
        if vatproperties.affected_side == 'LTR':
            vatinfo.symmetry = 1
        elif vatproperties.affected_side == 'RTL':
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

        if vatproperties.target_armature and vatinfo.scheme != -1:
            if vatproperties.affected_side == 'LTR':
                return (vatinfo.symmetry == 1)
            elif vatproperties.affected_side == 'RTL':
                return (vatinfo.symmetry == 2)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        constraint_symmetry(1, vatproperties.affected_side)
        vatinfo.symmetry = 0
        
        return{'FINISHED'}
    
class VAT_OT_constraintsymmetry_apply(bpy.types.Operator):
    """Modifies default pose to be the current one"""
    bl_idname = "vat.constraintsymmetry_apply"
    bl_label = "Symmetry Constraints Apply and removal"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        if vatproperties.target_armature and vatinfo.scheme != -1:
            return(context.object.mode == 'POSE')

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        bpy.ops.pose.armature_apply(selected=False)
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

        if vatproperties.target_armature and vatinfo.scheme != -1:
            return (not vatinfo.weight_armature)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        if not vatproperties.target_armature.hide_get() and not vatproperties.target_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, place it in an active collection.")
        else:
            weight_armature(0)
            vatinfo.weight_armature = True

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

        if vatproperties.target_armature and vatinfo.scheme != -1:
            return (vatinfo.weight_armature)

    def execute(self, context):
        vatinfo = bpy.context.scene.vatinfo

        weight_armature(1)
        vatinfo.weight_armature = False

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

        if vatproperties.target_armature and vatinfo.scheme != -1:
            return (not vatinfo.animation_armature)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        if not vatproperties.target_armature.hide_get() and not vatproperties.target_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, place it in an active collection.")
        else:
            anim_armature(0)
            vatinfo.animation_armature = True
            vatinfo.animation_armature_setup = True

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

        if vatproperties.target_armature and vatinfo.scheme != -1:
            return (vatinfo.animation_armature)

    def execute(self, context):
        vatinfo = bpy.context.scene.vatinfo

        anim_armature(1)
        vatinfo.animation_armature = False
        vatinfo.animation_armature_setup = False

        return{'FINISHED'}

class VAT_OT_rigifyretarget_generate(bpy.types.Operator):
    """Generates Rigify armature"""
    bl_idname = "vat.rigifyretarget_generate"
    bl_label = "Animation Ready Armature Generation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        if vatproperties.target_armature and vatinfo.scheme != -1:
            return (context.object.name == vatproperties.target_armature.name + '.anim_setup')

    def execute(self, context):
        bpy.ops.pose.rigify_generate()
        armature = bpy.data.objects[utils.arm.armature.name + '.anim']
        armature.scale = utils.arm.armature.scale

        return{'FINISHED'}

class VAT_OT_rigifyretarget_link(bpy.types.Operator):
    """Connects original armature with generated Rigify armature"""
    bl_idname = "vat.rigifyretarget_link"
    bl_label = "Animation Ready Armature Link"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        if vatproperties.target_armature and vatinfo.scheme != -1:
            return (context.object.name == vatproperties.target_armature.name + '.anim')

    def execute(self, context):
        vatinfo = bpy.context.scene.vatinfo
        anim_armature(2)
        vatinfo.animation_armature_setup = False

        return{'FINISHED'}

class VAT_OT_rigifyretarget_bake_single(bpy.types.Operator):
    """Bakes selected NLA strip/current action from the animation armature onto the original armature"""
    bl_idname = "vat.rigifyretarget_bake_single"
    bl_label = "Single Animation Bake"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        if vatproperties.target_armature and vatinfo.scheme != -1:
            if vatinfo.animation_armature and not vatinfo.animation_armature_setup and vatproperties.retarget_constraints:
                if utils.arm.animation_armature.animation_data:
                    return (utils.arm.animation_armature.animation_data.action or utils.arm.animation_armature.animation_data.nla_tracks and utils.arm.animation_armature.animation_data.nla_tracks[0].strips)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties

        if not vatproperties.target_armature.hide_get() and not vatproperties.target_armature.visible_get() and not utils.arm.animation_armature.hide_get() and not utils.arm.animation_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, enable said collection.")
        else:
            bake(0)

        return{'FINISHED'}

class VAT_OT_rigifyretarget_bake_all(bpy.types.Operator):
    """Bakes all NLA strips from the animation armature onto the original armature"""
    bl_idname = "vat.rigifyretarget_bake_all"
    bl_label = "All Animations Bake"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo

        if vatproperties.target_armature and vatinfo.scheme != -1:
            if vatinfo.animation_armature and not vatinfo.animation_armature_setup and vatproperties.retarget_constraints:
                if utils.arm.animation_armature.animation_data:
                    return (utils.arm.animation_armature.animation_data.nla_tracks and utils.arm.animation_armature.animation_data.nla_tracks[0].strips)

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties

        if not vatproperties.target_armature.hide_get() and not vatproperties.target_armature.visible_get() and not utils.arm.animation_armature.hide_get() and not utils.arm.animation_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, enable said collection.")
        else:
            bake(1)

        return{'FINISHED'}

class VAT_OT_rigifyretarget_export_all(bpy.types.Operator):
    """Exports all baked data from the Source armature to SMD format through Blender Source Tools"""
    bl_idname = "vat.rigifyretarget_export_all"
    bl_label = "All Animations Export"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        
        if vatproperties.target_armature and vatinfo.scheme != -1 and not vatinfo.sbox:
            if vatinfo.animation_armature and not vatinfo.animation_armature_setup and utils.arm.animation_armature and not vatproperties.retarget_constraints:
                if utils.arm.animation_armature.animation_data:
                    return (utils.arm.animation_armature.animation_data.nla_tracks)

    def execute(self, context):
        export()

        return{'FINISHED'}