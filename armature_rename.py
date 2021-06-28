import bpy
from . import utils
from .utils import helper_convert
from .utils import update

def armature_rename(scheme, armature=None): #Bone prefix/suffix repositioning

    vatinfo = bpy.context.scene.vatinfo

    def rename(bone):
        bpy.ops.object.mode_set(mode='OBJECT') #Forces object mode to avoid context errors

        if utils.arm.goldsource:
            if index == 0:
                old = ' L '
                new = ' L'
            elif index == 1:
                old = ' R '
                new = ' R'
        elif bone.count('l_') or bone.count('r_') or bone.count('_l') or bone.count('_r'):
            if index == 0:
                old = 'l_'
                new = '_l'
            elif index == 1:
                old = 'r_'
                new = '_r'
        else:
            if index == 0:
                old = 'L_'
                new = '_L'
            elif index == 1:
                old = 'R_'
                new = '_R'

        #To which scheme
        if scheme == 1: #Source -> Blender
            armature.pose.bones[prefix + bone].name = prefix + bone.replace(old, '') + new

        elif scheme == 0: #Blender -> Source
            armature.pose.bones[prefix + bone].name = prefix + old + bone.replace(new, '')

    #Updates bone list in case it was modified
    utils.arm.get_bones(False)

    prefix = utils.arm.prefix

    current_mode = bpy.context.object.mode

    single = False

    if not armature:
        armature = utils.arm.armature

        #Symmetrical
        for cat in utils.arm.symmetrical_bones.keys():
            for bone in utils.arm.symmetrical_bones[cat].values():
                for index, bone in enumerate(bone):
                    if bone:
                        rename(bone)
        
        #Helpers
        if utils.arm.helper_bones:
            for cat in utils.arm.helper_bones.keys():
                for bone in utils.arm.helper_bones[cat].values():
                    for index, bone in enumerate(bone):
                        if bone:
                            #Nick's helper wrist without side suffix
                            if bone == 's2.wrist':
                                continue
                            prefix, bone = helper_convert(bone)
                            rename(bone)

        #Renames generated armatures to be on par with the original armature

        prefix = utils.arm.prefix

        #Weight armature
        if vatinfo.weight_armature:
            armature = utils.arm.weight_armature
            update(1, armature)

            for cat in utils.arm.symmetrical_bones.keys():
                for bone in utils.arm.symmetrical_bones[cat].values():
                    for index, bone in enumerate(bone):
                        if bone:
                            rename(bone)
            
            if utils.arm.helper_bones:
                for cat in utils.arm.helper_bones.keys():
                    for container, bone in utils.arm.helper_bones[cat].items():
                        #Wrist helper bone is removed from weight armature since it serves no purpose
                        if container.count('wrist_helper') != 1:
                            for index, bone in enumerate(bone):
                                if bone:
                                    #Nick's helper wrist without side suffix
                                    if bone == 's2.wrist':
                                        continue
                                    prefix, bone = helper_convert(bone)
                                    rename(bone)

            update(1, utils.arm.armature)

        #Reverts back to previously used mode
        bpy.ops.object.mode_set(mode=current_mode)
    else:
        single = True
        for cat in utils.arm.symmetrical_bones.keys():
            for container, bone in utils.arm.symmetrical_bones[cat].items():
                for index, bone in enumerate(bone):
                    if bone:
                        rename(bone)

    if not single:
        utils.arm.get_bones(True)
    else:
        utils.arm.get_bones(False)

def bone_rename(scheme, bone, index):
    if utils.arm.goldsource:
        if index == 0:
            old = ' L '
            new = ' L'
        elif index == 1:
            old = ' R '
            new = ' R'
    else:
        if index == 0:
            old = 'L_'
            new = '_L'
        elif index == 1:
            old = 'R_'
            new = '_R'


    #To which scheme
    if scheme == 1: #Source -> Blender
        bone = bone.replace(old, '') + new

    elif scheme == 0: #Blender -> Source
        bone = bone.replace(new, '')

    return bone

def strip(bone, index):

    if index == 0:
        suffix = '_L'
        if bone.startswith('L_'):
            bone = bone.replace('L_', '')
        elif bone.endswith('_L'):
            bone = bone.replace('_L', '')
    elif index == 1:
        suffix = '_R'
        if bone.startswith('R_'):
            bone = bone.replace('R_', '')
        elif bone.endswith('_R'):
            bone = bone.replace('_R', '')

    return bone, suffix