import bpy
from . import utils

def constraint_symmetry(action, side): #Creates symmetry by using constraints, keeping corrected roll value
                    
    def getconstraint(bone):
        vatinfo = bpy.context.scene.vatinfo
        nonlocal armature

        nonlocal loc
        nonlocal rot

        try:
            loc[bone] = {'location': armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Location']}
        except:
            loc[bone] = {'location': None}
        try:
            rot[bone] = {'rotation': armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Rotation']}
        except:
            rot[bone] = {'rotation': None}

        return loc, rot

    def constraint(bone, cat, container, group): 
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        nonlocal armature

        nonlocal prefix

        loc, rot = getconstraint(bone) #Checks for already existing constraints

        #Gets bone's opposite, change prefix and bone name if helper bone
        if group == utils.arm.helper_bones:
            if side == 'OP1':
                prefix, bone2 = utils.helper_convert(group[cat][container][1])
            elif side == 'OP2':
                prefix, bone2 = utils.helper_convert(group[cat][container][0])
        else:
            if side == 'OP1':
                bone2 = group[cat][container][1]
            elif side == 'OP2':
                bone2 = group[cat][container][0]

        #Creation
        if action == 0:
            
            #Location
            if not loc[bone]['location']:
                loc[bone]['location'] = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')

                if not vatinfo.symmetry:
                    if side == 'OP1':
                        vatinfo.symmetry = 1
                    elif side == 'OP2':
                        vatinfo.symmetry = 2

                if loc[bone]['location']:
                    bloc = loc[bone]['location']
                    #Constraint parameters
                    bloc.name = "Constraint Symmetry Location"
                    bloc.target = armature
                    bloc.subtarget = prefix + bone2
                    constraint_update(prefix, bone)
            else:
                bloc = 'Marked'

            #Rotation
            if not rot[bone]['rotation']:
                rot[bone]['rotation'] = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')

                if not vatinfo.symmetry:
                    if side == 'OP1':
                        vatinfo.symmetry = 1
                    elif side == 'OP2':
                        vatinfo.symmetry = 2
                    
                if rot[bone]['rotation']:
                    brot = rot[bone]['rotation']
                    #Constraint parameters
                    brot.name = "Constraint Symmetry Rotation"
                    brot.target = armature
                    brot.target_space = 'LOCAL'
                    brot.owner_space = 'LOCAL'
                    brot.invert_y = True
                    brot.invert_x = True
                    brot.subtarget = prefix + bone2
            else:
                brot = 'Marked'
            
        #Deletion
        elif action == 1:

            #Location
            if loc[bone]['location']:
                armature.pose.bones[prefix + bone].constraints.remove(loc[bone]['location'])
                        
                if vatinfo.symmetry:
                    vatinfo.symmetry = 0
                
                loc[bone]['location'] = None
            else:
                loc[bone]['location'] = 'Marked'

            #Rotation
            if rot[bone]['rotation']:
                armature.pose.bones[prefix + bone].constraints.remove(rot[bone]['rotation'])

                if vatinfo.symmetry:
                    vatinfo.symmetry = 0

                rot[bone]['rotation'] = None
            else:
                rot[bone]['rotation'] = 'Marked'

        return loc, rot

    #Updates bone list in case it was modified
    utils.arm.get_bones(False)

    armature = utils.arm.armature
    prefix = utils.arm.prefix

    loc = {}
    rot = {}

    #Symmetrical
    for cat in utils.arm.symmetrical_bones.keys():
        for container, bone in utils.arm.symmetrical_bones[cat].items():
            if utils.arm.symmetrical_bones[cat][container]:
                if utils.arm.symmetrical_bones[cat][container][0] and utils.arm.symmetrical_bones[cat][container][1]: 
                    #Gets individual bone
                    if side == 'OP1':
                        bone = bone[0]
                    elif side == 'OP2':
                        bone = bone[1]

                    loc, rot = constraint(bone, cat, container, utils.arm.symmetrical_bones)
            
    #Helpers
    if utils.arm.helper_bones:
        for cat in utils.arm.helper_bones.keys():
            for container, bone in utils.arm.helper_bones[cat].items():
                if utils.arm.helper_bones[cat][container]:
                    if utils.arm.helper_bones[cat][container][0] and utils.arm.helper_bones[cat][container][1]: 
                        if side == 'OP1':
                            bone = bone[0]
                        elif side == 'OP2':
                            bone = bone[1]

                        prefix, bone = utils.helper_convert(bone)
                        loc, rot = constraint(bone, cat, container, utils.arm.helper_bones)

    #Final report that checks if some constraints are somehow missing or already applied
    final_report_loc = []
    final_report_rot = []

    for bone in list(loc.keys()):
        if loc[bone]['location'] == 'Marked':
            final_report_loc.append(bone)
    
    for bone in list(rot.keys()):
        if rot[bone]['rotation'] == 'Marked':
            final_report_rot.append(bone)

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
    vatproperties = bpy.context.scene.vatproperties
    constraint_update()

def constraint_update(prefix=None, bone=None):
    vatproperties = bpy.context.scene.vatproperties
    armature = utils.arm.armature

    if not prefix:
        prefix = utils.arm.prefix

    def update(bone):
        for constraint in armature.pose.bones[prefix + bone].constraints:
            if constraint.name == 'Constraint Symmetry Location':
                if vatproperties.symmetry_offset:
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
        update(bone)
    else:
        for cat in utils.arm.symmetrical_bones.keys():
            for container, bone in utils.arm.symmetrical_bones[cat].items():
                for bone in bone:
                    if bone:
                        update(bone)

        #Helpers
        if utils.arm.helper_bones:
            for cat in utils.arm.helper_bones.keys():
                for container, bone in utils.arm.helper_bones[cat].items():
                    for bone in bone:
                        if bone:
                            prefix, bone = utils.helper_convert(bone)
                            update(bone)

    prefix = utils.arm.prefix

    #Upperarm rotation fix
    if vatproperties.symmetry_upperarm_rotation_fix:
        for bone in utils.arm.symmetrical_bones['arms']['upperarm']:
            for constraint in armature.pose.bones[prefix + bone].constraints:
                if constraint.name == 'Constraint Symmetry Rotation':
                    constraint.invert_y = False
                    constraint.invert_z = True
    else:
        for bone in utils.arm.symmetrical_bones['arms']['upperarm']:
            for constraint in armature.pose.bones[prefix + bone].constraints:
                if constraint.name == 'Constraint Symmetry Rotation':
                    constraint.invert_y = True
                    constraint.invert_z = False