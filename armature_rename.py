import bpy
from . import utils
from .utils import Prefixes

def armature_rename(scheme): #Bone prefix/suffix repositioning

    def rename(bone):
        bpy.ops.object.mode_set(mode='OBJECT') #Forces object mode to avoid errors when being in edit mode

        #To which scheme
        if scheme == 1: #Source -> Blender
            if bone.startswith('L_'):
                armature.bones[prefix + bone].name = prefix + bone.replace('L_', '') + '_L'
            elif bone.startswith('R_'):
                armature.bones[prefix + bone].name = prefix + bone.replace('R_', '') + '_R'
            utils.arm.scheme = 1

        elif scheme == 0: #Blender -> Source
            if bone.endswith('_L'):
                armature.bones[prefix + bone].name = prefix + 'L_' + bone.replace('_L', '')
            elif bone.endswith('_R'):
                armature.bones[prefix + bone].name = prefix + 'R_' + bone.replace('_R', '')
            utils.arm.scheme = 0

    #Updates bone list in case it was modified
    utils.arm.get_bones()

    prefix = utils.arm.prefix
    armature = bpy.data.armatures[utils.arm.name_real.name]
    for bone in utils.arm.symmetrical_bones:
        rename(bone)
        
    if utils.arm.helper_bones:
        for bone in utils.arm.helper_bones:
            if bone.startswith('s.'):
                prefix = utils.arm.prefix
                rename(bone.replace('s.', ''))

            elif bone.startswith('s2.'):

                #Their prefix is usually already in the end so they're left alone
                if not bone.endswith('_L') or not bone.endswith('_R'):
                    prefix = Prefixes.helper2
                    rename(bone.replace('s2.', ''))

            else:
                prefix = Prefixes.helper
                rename(bone)

    #Renames generated armatures to be on par with the original armature

    #Renames weight armature
    if utils.arm.weight_armature:
        armature = bpy.data.armatures[utils.arm.weight_armature_real.name]
        for bone in utils.arm.symmetrical_bones:
            rename(bone)

    #Renames animation armature
    if utils.arm.animation_armature:
        armature = bpy.data.armatures[utils.arm.animation_armature_real.name]
        for bone in utils.arm.symmetrical_bones:
            rename(bone)

    utils.arm.get_bones() #Refreshes bone list
