import bpy
from . import utils
from .utils import bone_convert

def constraint_symmetry(action, side): #Creates symmetry by using constraints, keeping corrected roll value
    satinfo = bpy.context.scene.satinfo

    #Checks if the constraint for a bone already exists
    def getconstraint(bone):
        try:
            loc[bone] = {'location': armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Location']}
        except:
            loc[bone] = {'location': None}
        try:
            rot[bone] = {'rotation': armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Rotation']}
        except:
            rot[bone] = {'rotation': None}

        return loc, rot

    def constraint(bone, bone2, type=''):
        satinfo = bpy.context.scene.satinfo

        loc, rot = getconstraint(bone)

        #Creation
        if action == 0:
            #Location
            if not loc[bone]['location']:
                loc[bone]['location'] = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')

                contraint = loc[bone]['location']
                #Constraint parameters
                contraint.name = "Constraint Symmetry Location"
                contraint.target = armature
                contraint.subtarget = prefix2 + bone2
                constraint_update(prefix, bone)
            else:
                final_report_loc.append(bone)

            #Rotation
            if not rot[bone]['rotation']:
                rot[bone]['rotation'] = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')
                    
                contraint = rot[bone]['rotation']
                #Constraint parameters
                contraint.name = "Constraint Symmetry Rotation"
                contraint.target = armature
                contraint.target_space = 'LOCAL_WITH_PARENT'
                contraint.owner_space = 'LOCAL_WITH_PARENT'
                if type == 'weapon':
                    contraint.invert_y = True
                    contraint.invert_x = False
                elif satinfo.titanfall or satinfo.special_viewmodel:
                    contraint.invert_y = False
                    contraint.invert_x = False
                else:
                    contraint.invert_y = True
                    contraint.invert_x = True
                contraint.subtarget = prefix2 + bone2
            else:
                final_report_rot.append(bone)
            
            if not satinfo.symmetry:
                if side == 'LTR':
                    satinfo.symmetry = 1
                elif side == 'RTL':
                    satinfo.symmetry = 2

        #Deletion
        elif action == 1:
            #Location
            if loc[bone]['location']:
                armature.pose.bones[prefix + bone].constraints.remove(loc[bone]['location'])
                
                loc[bone]['location'] = None
            else:
                final_report_loc.append(bone)

            #Rotation
            if rot[bone]['rotation']:
                armature.pose.bones[prefix + bone].constraints.remove(rot[bone]['rotation'])

                rot[bone]['rotation'] = None
            else:
                final_report_rot.append(bone)

            satinfo.symmetry = 0

    #Updates bone list in case it was modified
    utils.arm.get_bones(False)

    armature = utils.arm.armature
    prefix = satinfo.prefix

    loc = {}
    rot = {}

    #Final report that checks if some constraints are somehow missing or already applied
    final_report_loc = []
    final_report_rot = []

    #Symmetrical
    for cat in utils.arm.symmetrical_bones.keys():
        for container, bone in utils.arm.symmetrical_bones[cat].items():
            if bone:
                if bone[0] and bone[1]:
                    if side == 'LTR':
                        bone = bone = utils.arm.symmetrical_bones[cat][container][0]
                        bone2 = utils.arm.symmetrical_bones[cat][container][1]
                    elif side == 'RTL':
                        bone = bone = utils.arm.symmetrical_bones[cat][container][1]
                        bone2 = utils.arm.symmetrical_bones[cat][container][0]

                    prefix, bone = bone_convert(bone)
                    prefix2, bone2 = bone_convert(bone2)
                    constraint(bone, bone2)
            
    #Helpers
    if utils.arm.helper_bones:
        for cat in utils.arm.helper_bones.keys():
            for container, bone in utils.arm.helper_bones[cat].items():
                if bone:
                    if bone[0] and bone[1]:
                        if side == 'LTR':
                            bone = utils.arm.helper_bones[cat][container][0]
                            bone2 = utils.arm.helper_bones[cat][container][1]
                        elif side == 'RTL':
                            bone = utils.arm.helper_bones[cat][container][1]
                            bone2 = utils.arm.helper_bones[cat][container][0]

                        prefix, bone = bone_convert(bone)
                        prefix2, bone2 = bone_convert(bone2)
                        constraint(bone, bone2)

    if utils.arm.other_bones:
        try:
            weapon = utils.arm.other_bones['weapon']
            if side == 'LTR':
                bone = weapon[weapon.index('p2.L_weapon_bone')]
                bone2 = weapon[weapon.index('p2.weapon_bone')]
            elif side == 'RTL':
                bone = weapon[weapon.index('p2.weapon_bone')]
                bone2 = weapon[weapon.index('p2.L_weapon_bone')]

            prefix, bone = bone_convert(bone)
            prefix2, bone2 = bone_convert(bone2)
            constraint(bone, bone2, 'weapon')
        except:
            pass

        try:
            attachment = utils.arm.other_bones['attachment']
            if side == 'LTR':
                bone = attachment[attachment.index('a1.armL_T')]
                bone2 = attachment[attachment.index('a1.armR_T')]
            elif side == 'RTL':
                bone = attachment[attachment.index('a1.armR_T')]
                bone2 = attachment[attachment.index('a1.armL_T')]

            prefix, bone = bone_convert(bone)
            prefix2, bone2 = bone_convert(bone2)
            constraint(bone, bone2)
        except:
            pass

    #If constraints could not be applied
    if final_report_loc:
        if action == 0:
            print("Location constraints already exist for:", final_report_loc)
        elif action == 1:
            print("Location constraints not found for:", final_report_loc)
        
    if final_report_rot:
        if action == 0:
            print("Rotation constraints already exist for:", final_report_rot)
        elif action == 1:
            print("Rotation constraints not found for:", final_report_rot)

def update_constraint(self, context):
    constraint_update()

def constraint_update(prefix=None, bone=None):
    satproperties = bpy.context.scene.satproperties
    satinfo = bpy.context.scene.satinfo
    armature = utils.arm.armature

    def update(prefix, bone):
        for constraint in armature.pose.bones[prefix + bone].constraints:
            if constraint.name == 'Constraint Symmetry Location':
                if satproperties.symmetry_offset:
                    constraint.target_space = 'LOCAL'
                    constraint.owner_space = 'LOCAL'
                    constraint.invert_x = False
                    constraint.invert_z = True
                else:
                    constraint.target_space = 'WORLD'
                    constraint.owner_space = 'WORLD'
                    constraint.invert_x = True
                    constraint.invert_z = False

    #If to update bone individually or update them all
    if bone:
        update(prefix, bone)
    else:
        for cat in utils.arm.symmetrical_bones.keys():
            for container, bone in utils.arm.symmetrical_bones[cat].items():
                for bone in bone:
                    if bone:
                        prefix, bone = bone_convert(bone)
                        update(prefix, bone)

        #Helpers
        if utils.arm.helper_bones:
            for cat in utils.arm.helper_bones.keys():
                for container, bone in utils.arm.helper_bones[cat].items():
                    for bone in bone:
                        if bone:
                            prefix, bone = bone_convert(bone)
                            update(prefix, bone)

    #Upperarm rotation fix
    if satproperties.symmetry_upperarm_rotation_fix:
        for bone in utils.arm.symmetrical_bones['arms']['upperarm']:
            prefix, bone = bone_convert(bone)
            for constraint in armature.pose.bones[prefix + bone].constraints:
                if constraint.name == 'Constraint Symmetry Rotation':
                    constraint.invert_y = False
                    constraint.invert_z = True
    else:
        for bone in utils.arm.symmetrical_bones['arms']['upperarm']:
            prefix, bone = bone_convert(bone)
            for constraint in armature.pose.bones[prefix + bone].constraints:
                if constraint.name == 'Constraint Symmetry Rotation':
                    if satinfo.titanfall or satinfo.special_viewmodel:
                        constraint.invert_y = False
                    else:
                        constraint.invert_y = True
                    constraint.invert_z = False