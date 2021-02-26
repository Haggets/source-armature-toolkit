import bpy
from . import utils
from .utils import update

def inverse_kinematics(action): #Adds IK to the armature

    def getconstraint():
        armature = bpy.data.objects[utils.arm.name]
    
        #List that will store constraint info for bones
        bonelist = {}

        for bone in utils.arm.symmetrical_bones:
            if bone.count('Hand') or bone.count('Foot'):
                try:
                    bonelist[bone] = armature.pose.bones[prefix + bone].constraints['IK']
                except:
                    bonelist[bone] = 'None'

        return bonelist

    def constraints():
        armature = bpy.data.objects[utils.arm.name]

        bonelist = getconstraint()

        #Creation
        if action == 0:
            for bone in bonelist:
                if bonelist[bone] == 'None':
                    ik = armature.pose.bones[prefix + bone].constraints.new('IK')
                    ik.chain_count = 3
                    ik.pole_target = utils.arm.name_full

                    if bone.count('Hand'):
                        if bone.startswith('L_') or bone.endswith('_L'):
                            ik.pole_subtarget = 'ForearmPole_L'
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            ik.pole_subtarget = 'ForearmPole_R'

                    elif bone.count('Foot'):
                        if bone.startswith('L_') or bone.endswith('_L'):
                            ik.pole_subtarget = 'CalfPole_L'
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            ik.pole_subtarget = 'CalfPole_R'
                else:
                    bonelist[bone] = 'Marked'
                    
            utils.arm.inverse_kinematics = True
                
        #Deletion
        elif action == 1:

            for bone in bonelist:
                if bonelist[bone] != 'None':
                    if bone.startswith('L_') or bone.endswith('_L'):
                        armature.pose.bones[prefix + bone].constraints.remove(bonelist[bone])
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        armature.pose.bones[prefix + bone].constraints.remove(bonelist[bone])
                else:
                    bonelist[bone] = 'Marked'

            utils.arm.inverse_kinematics = False

        return bonelist

    def poles():
        armature = bpy.data.objects[utils.arm.name]

        if action == 0:
            update(1, armature)

            for bone in utils.arm.central_bones:
                if bone.count('Pelvis'):
                    pelvis = armature.data.edit_bones[prefix + bone]
                    break

            #Gets forearm and calf position
            for bone in utils.arm.symmetrical_bones:
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
    utils.arm.get_bones(False)

    prefix = utils.arm.prefix

    poles()
    bonelist = constraints()
    
    #Final report that checks if some constraints are somehow missing or already applied
    final_report = []

    for bone in bonelist:
        if bonelist[bone] == 'Marked':
            final_report.append(bone)

    if final_report:
        if action == 0:
            print("IK constraints already exist for:", final_report)
        elif action == 1:
            print("IK constraints not found for:", final_report)