import bpy
from . import utils
from .utils import bone_convert
from .utils import update

def armature_rename(scheme, armature=None): #Bone prefix/suffix repositioning
    satinfo = bpy.context.scene.satinfo

    def rename(prefix, bone, index):
        bpy.ops.object.mode_set(mode='OBJECT') #Forces object mode to avoid context errors

        if bone.startswith(utils.arm.side[0]) or bone.startswith(utils.arm.side[1]) or bone.endswith(utils.arm.side[2]) or bone.endswith(utils.arm.side[3]):
            if index == 0:
                old = utils.arm.side[0]
                new = utils.arm.side[2]
            elif index == 1:
                old = utils.arm.side[1]
                new = utils.arm.side[3]
        else:
            if index == 0:
                old = utils.arm.side[0].casefold()
                new = utils.arm.side[2].casefold()
            elif index == 1:
                old = utils.arm.side[1].casefold()
                new = utils.arm.side[3].casefold()

        #print(bone, old, new)

        #To which scheme
        if scheme == 1: #Source -> Blender
            armature.pose.bones[prefix + bone].name = prefix + bone.replace(old, '') + new

        elif scheme == 0: #Blender -> Source
            armature.pose.bones[prefix + bone].name = prefix + old + bone.replace(new, '')

    def convert(single):
        prefix = satinfo.prefix
        #Symmetrical
        for cat in utils.arm.symmetrical_bones.keys():
            for bone in utils.arm.symmetrical_bones[cat].values():
                for index, bone in enumerate(bone):
                    if bone:
                        prefix, bone = bone_convert(bone)
                        rename(prefix, bone, index)
        
        if not single:
            #Helpers
            if utils.arm.helper_bones:
                for cat in utils.arm.helper_bones.keys():
                    for bone in utils.arm.helper_bones[cat].values():
                        for index, bone in enumerate(bone):
                            if bone:
                                #Nick's helper wrist without side suffix
                                if bone == 'h2.wrist':
                                    continue
                                prefix, bone = bone_convert(bone)
                                if bone.title().startswith(utils.arm.side[0]) or bone.title().startswith(utils.arm.side[1]) or bone.title().endswith(utils.arm.side[2]) or bone.title().endswith(utils.arm.side[3]):
                                    rename(prefix, bone, index)

    #Updates bone list in case it was modified
    utils.arm.get_bones(False)

    current_mode = bpy.context.object.mode
    selected_objects = bpy.context.selected_objects
    active_object = bpy.context.view_layer.objects.active

    if not armature:
        armature = utils.arm.armature
        convert(False)
        if satinfo.weight_armature:
            armature = utils.arm.weight_armature
            convert(False)

        update(1, utils.arm.armature)
    else:
        convert(True)
    
    #Reselects all previous objects
    for object in selected_objects:
        object.select_set(True)
    bpy.context.view_layer.objects.active = active_object
    bpy.context.view_layer.objects.active = armature

    #Defaults back to object mode to force updates on vertex groups
    if current_mode != 'OBJECT' and current_mode != 'EDIT' and current_mode != 'POSE':
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        bpy.ops.object.mode_set(mode=current_mode)

    if not armature:
        utils.arm.get_bones(True)
    else:
        utils.arm.get_bones(False)

def bone_rename(scheme, bone, index):
    satinfo = bpy.context.scene.satinfo

    if bone.startswith(utils.arm.side[0]) or bone.startswith(utils.arm.side[1]) or bone.endswith(utils.arm.side[2]) or bone.endswith(utils.arm.side[3]):
        if index == 0:
            old = utils.arm.side[0]
            new = utils.arm.side[2]
        elif index == 1:
            old = utils.arm.side[1]
            new = utils.arm.side[3]
    else:
        if index == 0:
            old = utils.arm.side[0].casefold()
            new = utils.arm.side[2].casefold()
        elif index == 1:
            old = utils.arm.side[1].casefold()
            new = utils.arm.side[3].casefold()

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