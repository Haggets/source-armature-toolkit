import bpy
from . import utils
from .utils import Prefixes

def armature_rename(scheme): #Bone prefix/suffix repositioning

    def rename(bone):
        bpy.ops.object.mode_set(mode='OBJECT') #Forces object mode to avoid context errors

        #To which scheme
        if scheme == 1: #Source -> Blender
            if bone.startswith('L_'):
                armature.bones[prefix + bone].name = prefix + bone.replace('L_', '') + '_L'
            elif bone.startswith('R_'):
                armature.bones[prefix + bone].name = prefix + bone.replace('R_', '') + '_R'

        elif scheme == 0: #Blender -> Source
            if bone.endswith('_L'):
                armature.bones[prefix + bone].name = prefix + 'L_' + bone.replace('_L', '')
            elif bone.endswith('_R'):
                armature.bones[prefix + bone].name = prefix + 'R_' + bone.replace('_R', '')

    #Updates bone list in case it was modified
    utils.arm.get_bones(False)

    prefix = utils.arm.prefix
    armature = bpy.data.armatures[utils.arm.name_real.name]

    current_mode = bpy.context.object.mode

    #Symmetrical
    for cat in utils.arm.symmetrical_bones.keys():
        for bone in utils.arm.symmetrical_bones[cat].values():
            for bone in bone:
                rename(bone)
    
    #Helpers
    if utils.arm.helper_bones:
        for cat in utils.arm.helper_bones.keys():
            for bone in utils.arm.helper_bones[cat].values():
                for bone in bone:
                    bone, prefix = utils.helper_convert(bone)
                    rename(bone)

    #Renames generated armatures to be on par with the original armature

    prefix = utils.arm.prefix

    #Weight armature
    if utils.arm.weight_armature:
        armature = bpy.data.armatures[utils.arm.weight_armature_real.name]
        for cat in utils.arm.symmetrical_bones.keys():
            for bone in utils.arm.symmetrical_bones[cat].values():
                for bone in bone:
                    rename(bone)
        
        if utils.arm.helper_bones:
            for cat in utils.arm.helper_bones.keys():
                for bone in utils.arm.helper_bones[cat].values():
                    for bone in bone:
                        bone, prefix = utils.helper_convert(bone)
                        rename(bone)

    prefix = utils.arm.prefix

    #Animation armature
    if utils.arm.animation_armature:
        armature = bpy.data.armatures[utils.arm.animation_armature_real.name]
        for cat in utils.arm.symmetrical_bones.keys():
            for bone in utils.arm.symmetrical_bones[cat].values():
                for bone in bone:
                    rename(bone)

    #Reverts back to previously used mode
    bpy.ops.object.mode_set(mode=current_mode)