import bpy
from .armature_rename import armature_rename
from .constraint_symmetry import constraint_symmetry
from .weight_armature import weight_armature
from .advanced_ik import anim_armature
from .advanced_ik import bake
from .advanced_ik import export
from .armature_creation import armature
from . import utils

class SAT_OT_create_armature(bpy.types.Operator):
    """Creates armature from scratch"""
    bl_idname = "sat.create_armature"
    bl_label = "Create armature from scratch"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        satinfo = bpy.context.scene.satinfo

        armature(0)
        satinfo.creating_armature = 1
        
        return{'FINISHED'}

class SAT_OT_convert_armature(bpy.types.Operator):
    """Converts armature to be Source like"""
    bl_idname = 'sat.convert_armature'
    bl_label = 'Convert Armature'
    bl_description = 'Converts armature to be like Source armatures (Unconnected with different orientation)'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        pass
        
        return{"FINISHED"}

class SAT_OT_armaturerename_blender(bpy.types.Operator): #Converts armature scheme to become Blender friendly
    """Converts to Blender friendly scheme to allow for symmetry"""
    bl_idname = "sat.armaturerename_blender"
    bl_label = "Blender Friendly Scheme"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod #Checks if an armature is selected and it is not an SFM one, since it doesn't need it
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme == 0:
            return (not satinfo.sfm and not satinfo.sbox)
    
    def execute(self, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if not satproperties.target_armature.hide_get() and not satproperties.target_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, place it in an active collection.")
        else:
            armature_rename(1)
            satinfo.scheme = 1
        
        return{'FINISHED'}
    
class SAT_OT_armaturerename_source(bpy.types.Operator): #Converts armature scheme back to the original
    """Reverts back to original Source friendly scheme for export"""
    bl_idname = "sat.armaturerename_source"
    bl_label = "Original scheme"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme == 1:
            return (not satinfo.sfm and not satinfo.sbox)
    
    def execute(self, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if not satproperties.target_armature.hide_get() and not satproperties.target_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, place it in an active collection.")
        else:
            armature_rename(0)
            satinfo.scheme = 0

        return{'FINISHED'}
    
class SAT_OT_constraintsymmetry_create(bpy.types.Operator):
    """Creates symmetry with constraints to allow for armature reproportioning while keeping correct roll values"""
    bl_idname = "sat.constraintsymmetry_create"
    bl_label = "Roll Corrected Symmetry"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme != -1:
            return (not satinfo.symmetry)

    def execute(self, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        constraint_symmetry(0, satproperties.affected_side)
        if satproperties.affected_side == 'LTR':
            satinfo.symmetry = 1
        elif satproperties.affected_side == 'RTL':
            satinfo.symmetry = 2
        
        return{'FINISHED'}
    
class SAT_OT_constraintsymmetry_delete(bpy.types.Operator):
    """Removes previously added constraints"""
    bl_idname = "sat.constraintsymmetry_delete"
    bl_label = "Symmetry Constraints Removal"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme != -1:
            if satproperties.affected_side == 'LTR':
                return (satinfo.symmetry == 1)
            elif satproperties.affected_side == 'RTL':
                return (satinfo.symmetry == 2)

    def execute(self, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        constraint_symmetry(1, satproperties.affected_side)
        satinfo.symmetry = 0
        
        return{'FINISHED'}
    
class SAT_OT_constraintsymmetry_apply(bpy.types.Operator):
    """Modifies default pose to be the current one"""
    bl_idname = "sat.constraintsymmetry_apply"
    bl_label = "Symmetry Constraints Apply and removal"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme != -1:
            return(context.object.mode == 'POSE')

    def execute(self, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        bpy.ops.pose.armature_apply(selected=False)
        constraint_symmetry(1, satproperties.affected_side)
        satinfo.symmetry = 0

        return{'FINISHED'}

class SAT_OT_weightarmature_create(bpy.types.Operator):
    """Duplicates armature with connected bones"""
    bl_idname = "sat.weightarmature_create"
    bl_label = "Better Automatic Weighting"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme != -1:
            return (not satinfo.weight_armature)

    def execute(self, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if not satproperties.target_armature.hide_get() and not satproperties.target_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, place it in an active collection.")
        else:
            weight_armature(0)
            satinfo.weight_armature = True

        return{'FINISHED'}

class SAT_OT_weightarmature_delete(bpy.types.Operator):
    """Removes duplicate armature"""
    bl_idname = "sat.weightarmature_delete"
    bl_label = "Duplicate Armature Removal"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme != -1:
            return (satinfo.weight_armature)

    def execute(self, context):
        satinfo = bpy.context.scene.satinfo

        weight_armature(1)
        satinfo.weight_armature = False

        return{'FINISHED'}
    
class SAT_OT_rigifyretarget_create(bpy.types.Operator):
    """Creates animation ready armature"""
    bl_idname = "sat.rigifyretarget_create"
    bl_label = "Custom Animation Ready Armature"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme != -1:
            return (not satinfo.animation_armature)

    def execute(self, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if not satproperties.target_armature.hide_get() and not satproperties.target_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, place it in an active collection.")
        else:
            anim_armature(0)
            satinfo.animation_armature = True
            satinfo.animation_armature_setup = True

        return{'FINISHED'}

class SAT_OT_rigifyretarget_delete(bpy.types.Operator):
    """Deletes generated armature"""
    bl_idname = "sat.rigifyretarget_delete"
    bl_label = "Animation Ready Armature Removal"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme != -1:
            return (satinfo.animation_armature)

    def execute(self, context):
        satinfo = bpy.context.scene.satinfo

        anim_armature(1)
        satinfo.animation_armature = False
        satinfo.animation_armature_setup = False

        return{'FINISHED'}

class SAT_OT_rigifyretarget_generate(bpy.types.Operator):
    """Generates Rigify armature"""
    bl_idname = "sat.rigifyretarget_generate"
    bl_label = "Animation Ready Armature Generation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme != -1:
            return (context.object.name == satproperties.target_armature.name + '.anim_setup')

    def execute(self, context):
        bpy.ops.pose.rigify_generate()
        armature = bpy.data.objects[utils.arm.armature.name + '.anim']
        armature.scale = utils.arm.armature.scale

        return{'FINISHED'}

class SAT_OT_rigifyretarget_link(bpy.types.Operator):
    """Connects original armature with generated Rigify armature"""
    bl_idname = "sat.rigifyretarget_link"
    bl_label = "Animation Ready Armature Link"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme != -1:
            return (context.object.name == satproperties.target_armature.name + '.anim')

    def execute(self, context):
        satinfo = bpy.context.scene.satinfo
        anim_armature(2)
        satinfo.animation_armature_setup = False

        return{'FINISHED'}

class SAT_OT_rigifyretarget_bake_single(bpy.types.Operator):
    """Bakes selected NLA strip/current action from the animation armature onto the original armature"""
    bl_idname = "sat.rigifyretarget_bake_single"
    bl_label = "Single Animation Bake"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme != -1:
            if satinfo.animation_armature and not satinfo.animation_armature_setup and satproperties.retarget_constraints:
                if utils.arm.animation_armature.animation_data:
                    return (utils.arm.animation_armature.animation_data.action or utils.arm.animation_armature.animation_data.nla_tracks and utils.arm.animation_armature.animation_data.nla_tracks[0].strips)

    def execute(self, context):
        satproperties = bpy.context.scene.satproperties

        if not satproperties.target_armature.hide_get() and not satproperties.target_armature.visible_get() and not utils.arm.animation_armature.hide_get() and not utils.arm.animation_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, enable said collection.")
        else:
            bake(0)

        return{'FINISHED'}

class SAT_OT_rigifyretarget_bake_all(bpy.types.Operator):
    """Bakes all NLA strips from the animation armature onto the original armature"""
    bl_idname = "sat.rigifyretarget_bake_all"
    bl_label = "All Animations Bake"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo

        if satproperties.target_armature and satinfo.scheme != -1:
            if satinfo.animation_armature and not satinfo.animation_armature_setup and satproperties.retarget_constraints:
                if utils.arm.animation_armature.animation_data:
                    return (utils.arm.animation_armature.animation_data.nla_tracks and utils.arm.animation_armature.animation_data.nla_tracks[0].strips)

    def execute(self, context):
        satproperties = bpy.context.scene.satproperties

        if not satproperties.target_armature.hide_get() and not satproperties.target_armature.visible_get() and not utils.arm.animation_armature.hide_get() and not utils.arm.animation_armature.visible_get():
            self.report({'ERROR'}, "Selected armature is in an excluded collection, enable said collection.")
        else:
            bake(1)

        return{'FINISHED'}

class SAT_OT_rigifyretarget_export_all(bpy.types.Operator):
    """Exports all baked data from the Source armature to SMD format through Blender Source Tools"""
    bl_idname = "sat.rigifyretarget_export_all"
    bl_label = "All Animations Export"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo
        
        if satproperties.target_armature and satinfo.scheme != -1 and not satinfo.sbox:
            if satinfo.animation_armature and not satinfo.animation_armature_setup and utils.arm.animation_armature and not satproperties.retarget_constraints:
                if utils.arm.animation_armature.animation_data:
                    return (utils.arm.animation_armature.animation_data.nla_tracks)

    def execute(self, context):
        export()

        return{'FINISHED'}