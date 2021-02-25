import bpy
from . import functions
from .functions import Prefixes

def armature_rename(scheme): #Bone prefix/suffix repositioning

    def rename(bone):
        bpy.ops.object.mode_set(mode='OBJECT') #Forces object mode to avoid errors when being in edit mode

        #To which scheme
        if scheme == 1: #Source -> Blender
            if bone.startswith('L_'):
                armature.bones[prefix + bone].name = prefix + bone.replace('L_', '') + '_L'
            elif bone.startswith('R_'):
                armature.bones[prefix + bone].name = prefix + bone.replace('R_', '') + '_R'
            functions.arm.scheme = 1

        elif scheme == 0: #Blender -> Source
            if bone.endswith('_L'):
                armature.bones[prefix + bone].name = prefix + 'L_' + bone.replace('_L', '')
            elif bone.endswith('_R'):
                armature.bones[prefix + bone].name = prefix + 'R_' + bone.replace('_R', '')
            functions.arm.scheme = 0

    #Updates bone list in case it was modified
    functions.arm.get_bones()

    prefix = functions.arm.prefix
    armature = bpy.data.armatures[functions.arm.name_real.name]
    for bone in functions.arm.symmetrical_bones:
        rename(bone)
        
    if functions.arm.helper_bones:
        for bone in functions.arm.helper_bones:
            if bone.startswith('s.'):
                prefix = functions.arm.prefix
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
    if functions.arm.weight_armature:
        armature = bpy.data.armatures[functions.arm.weight_armature_real.name]
        for bone in functions.arm.symmetrical_bones:
            rename(bone)

    #Renames animation armature
    if functions.arm.animation_armature:
        armature = bpy.data.armatures[functions.arm.animation_armature_real.name]
        for bone in functions.arm.symmetrical_bones:
            rename(bone)

    functions.arm.get_bones() #Refreshes bone list
