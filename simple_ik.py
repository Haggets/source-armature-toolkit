import bpy
from . import functions
from .functions import update

def inverse_kinematics(action): #Adds IK to the armature
    
    #Constraint checks
    ik_constraint = ''

    #Variables for finish report
    bonelist = []

    def getconstraint(bone):
        armature = bpy.data.objects[functions.arm.name]

        nonlocal ik_constraint

        try:
            ik_constraint = armature.pose.bones[prefix + bone].constraints['IK']
        except:
            ik_constraint = ''

    def constraints(bone):
        armature = bpy.data.objects[functions.arm.name]

        nonlocal bonelist
        nonlocal ik_constraint

        getconstraint(bone)

        #Creation
        if action == 0:

            if not ik_constraint:
                if bone.startswith('L_') or bone.endswith('_L'):
                    ik = armature.pose.bones[prefix + bone].constraints.new('IK')
                    ik.chain_count = 3
                    ik.pole_target = functions.arm.name_full
                    if bone.count('Hand'):
                        ik.pole_subtarget = 'ForearmPole_L'
                    elif bone.count('Foot'):
                        ik.pole_subtarget = 'CalfPole_L'
                elif bone.startswith('R_') or bone.endswith('_R'):
                    ik = armature.pose.bones[prefix + bone].constraints.new('IK')
                    ik.chain_count = 3
                    ik.pole_target = functions.arm.name_full
                    if bone.count('Hand'):
                        ik.pole_subtarget = 'ForearmPole_R'
                    elif bone.count('Foot'):
                        ik.pole_subtarget = 'CalfPole_R'
                functions.arm.inverse_kinematics = True
            else:
                bonelist.append(bone)
                
        #Deletion
        elif action == 1:

            if ik_constraint:
                if bone.startswith('L_') or bone.endswith('_L'):
                    armature.pose.bones[prefix + bone].constraints.remove(ik_constraint)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    armature.pose.bones[prefix + bone].constraints.remove(ik_constraint)
                functions.arm.inverse_kinematics = False
            else:
                bonelist.append(bone)

    def poles():
        armature = bpy.data.objects[functions.arm.name]

        if action == 0:
            update(1, armature)

            for bone in functions.arm.central_bones:
                if bone.count('Pelvis'):
                    pelvis = armature.data.edit_bones[prefix + bone]

            #Gets forearm and calf position
            for bone in functions.arm.symmetrical_bones:
                if bone.count('Forearm'):
                    forearm = armature.pose.bones[prefix + bone]
                elif bone.count('Calf'):
                    calf = armature.pose.bones[prefix + bone]

            for bone in ['ForearmPole_L', 'ForearmPole_R', 'CalfPole_L', 'CalfPole_R']:
                ebone = armature.data.edit_bones.new(bone)
                ebone.use_deform = False
                ebone.parent = pelvis

                if bone.startswith('Forearm'):
                    if bone.endswith('_L'):
                        ebone.tail = -forearm.tail.x, forearm.tail.y+12, forearm.tail.z
                        ebone.head = -forearm.head.x, forearm.head.y+10, forearm.head.z
                    elif bone.endswith('_R'):
                        ebone.tail = forearm.tail.x, forearm.tail.y+12, forearm.tail.z
                        ebone.head = forearm.head.x, forearm.head.y+10, forearm.head.z
                elif bone.startswith('Calf'):
                    if bone.endswith('_L'):
                        ebone.tail = -calf.tail.x, calf.tail.y-10, calf.tail.z
                        ebone.head = -calf.head.x, calf.head.y-12, calf.head.z
                    elif bone.endswith('_R'):
                        ebone.tail = calf.tail.x, calf.tail.y-10, calf.tail.z
                        ebone.head = calf.head.x, calf.head.y-12, calf.head.z

            bpy.ops.object.mode_set(mode='OBJECT')

        elif action == 1:
            bpy.ops.object.mode_set(mode='EDIT')
            
            for bone in ['ForearmPole_L', 'ForearmPole_R', 'CalfPole_L', 'CalfPole_R']:
                ebone = armature.data.edit_bones[bone]
                armature.data.edit_bones.remove(ebone)

            bpy.ops.object.mode_set(mode='OBJECT')

    #Updates bone list in case it was modified
    functions.arm.get_bones()

    prefix = functions.arm.prefix

    poles()
    for bone in functions.arm.symmetrical_bones:
        if bone.count('Hand') or bone.count('Foot'):
            constraints(bone)
    
    #If constraints could not be applied
    if bonelist:
        if action == 0:
            print("IK constraints already exist for:", bonelist)
        elif action == 1:
            print("IK constraints not found for:", bonelist)