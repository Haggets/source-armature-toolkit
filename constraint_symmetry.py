import bpy
from . import utils
from .utils import Prefixes

def constraint_symmetry(action, side): #Creates symmetry by using constraints, keeping corrected roll value
                    
    def getconstraint(bone):
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
        nonlocal armature

        nonlocal prefix

        loc, rot = getconstraint(bone) #Checks for already existing constraints

        #Gets bone's opposite, change prefix and bone name if helper bone
        if group == utils.arm.helper_bones:
            if side == 'OP1':
                bone2, prefix = utils.helper_convert(group[cat][container][1])
            elif side == 'OP2':
                bone2, prefix = utils.helper_convert(group[cat][container][0])
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

                if side == 'OP1':
                    utils.arm.symmetry_left = True
                elif side == 'OP2':
                    utils.arm.symmetry_right = True

                if loc[bone]['location']:
                    bloc = loc[bone]['location']
                    #Constraint parameters
                    bloc.name = "Constraint Symmetry Location"
                    bloc.target = armature
                    bloc.invert_x = True
                    bloc.subtarget = prefix + bone2
            else:
                bloc = 'Marked'

            #Rotation
            if not rot[bone]['rotation']:
                rot[bone]['rotation'] = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')

                if side == 'OP1':
                    utils.arm.symmetry_left = True
                elif side == 'OP2':
                    utils.arm.symmetry_right = True
                    
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
                        
                if side == 'OP1':
                    utils.arm.symmetry_left = False
                elif side == 'OP2':
                    utils.arm.symmetry_right = False
                
                loc[bone]['location'] = None
            else:
                loc[bone]['location'] = 'Marked'

            #Rotation
            if rot[bone]['rotation']:
                armature.pose.bones[prefix + bone].constraints.remove(rot[bone]['rotation'])

                if side == 'OP1':
                    utils.arm.symmetry_left = False
                elif side == 'OP2':
                    utils.arm.symmetry_right = False

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
            #Makes sure list is not empty
            if bone:
                #Checks if it has a pair, else skip it
                if len(bone) == 1:
                    continue
                else:
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
                if bone:
                    if len(bone) == 1:
                        continue
                    else:
                        if side == 'OP1':
                            bone = bone[0]
                        elif side == 'OP2':
                            bone = bone[1]

                        bone, prefix = utils.helper_convert(bone)
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
