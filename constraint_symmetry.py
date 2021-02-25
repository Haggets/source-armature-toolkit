import bpy
from . import functions
from .functions import Prefixes

def constraint_symmetry(action, side): #Creates symmetry by using constraints, keeping corrected roll value
    
    #Constraint checks
    loc = ''
    rot = ''

    #Variables for end report
    loc_bonelist = []
    rot_bonelist = []

    def getconstraint(bone):
        armature = bpy.data.objects[functions.arm.name]

        nonlocal loc
        nonlocal rot

        try:
            loc = armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Location']
        except:
            loc = ''
        try:
            rot = armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Rotation']
        except:
            rot = ''

    def constraint(bone): 
        armature = bpy.data.objects[functions.arm.name]
        
        getconstraint(bone) #Checks for already existing constraints
        
        nonlocal loc
        nonlocal rot
        nonlocal loc_bonelist
        nonlocal rot_bonelist

        #Creation
        if action == 0:
            
            #Location
            if not loc:
                if side == 'OP1':
                    if bone.startswith('L_') or bone.endswith('_L'):
                        loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')
                        functions.arm.symmetry_left = True
                elif side == 'OP2':
                    if bone.startswith('R_') or bone.endswith('_R'):
                        loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')
                        functions.arm.symmetry_right = True

                if loc:
                    #Constraint parameters
                    loc.name = "Constraint Symmetry Location"
                    loc.target = armature
                    loc.invert_x = True
                    if side == 'OP1':
                        if bone.startswith('L_'):
                            loc.subtarget = prefix + 'R_' + bone.replace('L_', '')
                        elif bone.endswith('_L'):
                            loc.subtarget = prefix + bone.replace('_L', '') + '_R'
                    elif side == 'OP2':
                        if bone.startswith('R_'):
                            loc.subtarget = prefix + 'L_' + bone.replace('R_', '')
                        elif bone.startswith('_R'):
                            loc.subtarget = prefix + bone.replace('_R', '') + '_L'
            else:
                loc_bonelist.append(bone)

            #Rotation
            if not rot:
                if side == 'OP1':
                    if bone.startswith('L_') or bone.endswith('_L'):
                        rot = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')
                        functions.arm.symmetry_left = True
                elif side == 'OP2':
                    if bone.startswith('R_') or bone.endswith('_R'):
                        rot = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')
                        functions.arm.symmetry_right = True
                    
                if rot:
                    #Constraint parameters
                    rot.name = "Constraint Symmetry Rotation"
                    rot.target = armature
                    rot.target_space = 'LOCAL'
                    rot.owner_space = 'LOCAL'
                    rot.invert_y = True
                    rot.invert_x = True
                    if side == 'OP1':
                        if bone.startswith('L_'):
                            rot.subtarget = prefix + 'R_' + bone.replace('L_', '')
                        elif bone.endswith('_L'):
                            rot.subtarget = prefix + bone.replace('_L', '') + '_R'
                    elif side == 'OP2':
                        if bone.startswith('R_'):
                            rot.subtarget = prefix + 'L_' + bone.replace('R_', '')
                        elif bone.endswith('_R'):
                            rot.subtarget = prefix + bone.replace('_R', '') + '_L'
            else:
                rot_bonelist.append(bone)
            
        #Deletion
        elif action == 1:
            armature = bpy.data.objects[functions.arm.name]

            #Location
            if loc:
                if side == 'OP1':
                    if bone.startswith('L_') or bone.endswith('_L'):
                        armature.pose.bones[prefix + bone].constraints.remove(loc)
                        functions.arm.symmetry_left = False
                elif side == 'OP2':
                    if bone.startswith('R_') or bone.endswith('_R'):
                        armature.pose.bones[prefix + bone].constraints.remove(loc)
                        functions.arm.symmetry_right = False
            else:
                loc_bonelist.append(bone)

            #Rotation
            if rot:
                if side == 'OP1':
                    if bone.startswith('L_') or bone.endswith('_L'):
                        armature.pose.bones[prefix + bone].constraints.remove(rot)
                        functions.arm.symmetry_left = False
                elif side == 'OP2':
                    if bone.startswith('R_') or bone.endswith('_R'):
                        armature.pose.bones[prefix + bone].constraints.remove(rot)
                        functions.arm.symmetry_right = False
            else:
                rot_bonelist.append(bone)

    #Updates bone list in case it was modified
    functions.arm.get_bones()

    prefix = functions.arm.prefix
    for bone in functions.arm.symmetrical_bones:
        constraint(bone)

    if functions.arm.helper_bones:
        for bone in functions.arm.helper_bones:
            if bone.startswith('s.'):
                prefix = functions.arm.prefix
                constraint(bone.replace('s.', ''))

            elif bone.startswith('s2.'):
                prefix = Prefixes.helper2
                constraint(bone.replace('s2.', ''))
            else:
                prefix = Prefixes.helper
                constraint(bone)

    #If constraints could not be applied
    if loc_bonelist:
        if action == 0:
            print("Location constraints already exist for:", loc_bonelist)
        elif action == 1:
            print("Location constraints not found for:", loc_bonelist)
        
    if rot_bonelist:
        if action == 0:
            print("Rotation constraints already exist for:", rot_bonelist)
        elif action == 1:
            print("Rotation constraints not found for:", rot_bonelist)
