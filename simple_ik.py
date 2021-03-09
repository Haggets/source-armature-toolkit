import bpy
import math
from . import utils
from .utils import update

def inverse_kinematics(action): #Adds IK to the armature

    def getconstraint(bone):
        nonlocal armature
    
        nonlocal bonelist

        try:
            bonelist[bone] = armature.pose.bones[prefix + bone].constraints['IK']
        except:
            bonelist[bone] = None

        return bonelist

    def constraints(bone):
        nonlocal armature

        bonelist = getconstraint(bone)

        #Creation
        if action == 0:
            if not bonelist[bone]:
                ik = armature.pose.bones[prefix + bone].constraints.new('IK')
                ik.chain_count = 3
                ik.pole_target = utils.arm.name_full

                if bone.count('Hand'):
                    if bone.startswith('L_') or bone.endswith('_L'):
                        ik.pole_subtarget = utils.arm.poles['forearm'][0] + '_Pole'
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        ik.pole_subtarget = utils.arm.poles['forearm'][1] + '_Pole'

                elif bone.count('Foot'):
                    if bone.startswith('L_') or bone.endswith('_L'):
                        ik.pole_subtarget = utils.arm.poles['calf'][0] + '_Pole'
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        ik.pole_subtarget = utils.arm.poles['calf'][1] + '_Pole'
                else:
                    bonelist[bone] = 'Marked'
                    
            utils.arm.inverse_kinematics = True
                
        #Deletion
        elif action == 1:

            for bone in bonelist:
                if not bonelist[bone]:
                    if bone.startswith('L_') or bone.endswith('_L'):
                        armature.pose.bones[prefix + bone].constraints.remove(bonelist[bone])
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        armature.pose.bones[prefix + bone].constraints.remove(bonelist[bone])
                else:
                    bonelist[bone] = 'Marked'

            utils.arm.inverse_kinematics = False

        return bonelist

    def poles():
        nonlocal armature

        bpy.ops.object.mode_set(mode='EDIT')

        if action == 0:
            update(1, armature)

            #Cleans pole list
            utils.arm.poles = {'hand': [], 'foot': [], 'forearm': [], 'calf': []}

            if len(utils.arm.symmetrical_bones['arms']['forearm']):
                forearm = armature.pose.bones[prefix + utils.arm.symmetrical_bones['arms']['forearm'][0]]
                for bone in utils.arm.symmetrical_bones['arms']['forearm']:
                    utils.arm.poles['forearm'].append(bone)

            if len(utils.arm.symmetrical_bones['legs']['calf']):
                calf = armature.pose.bones[prefix + utils.arm.symmetrical_bones['legs']['calf'][0]]
                for bone in utils.arm.symmetrical_bones['legs']['calf']:
                    utils.arm.poles['calf'].append(bone)

            if len(utils.arm.symmetrical_bones['legs']['foot']):
                foot = armature.pose.bones[prefix + utils.arm.symmetrical_bones['legs']['foot'][0]]
                for bone in utils.arm.symmetrical_bones['legs']['foot']:
                    utils.arm.poles['foot'].append(bone)

            if len(utils.arm.symmetrical_bones['arms']['hand']):
                hand = armature.pose.bones[prefix + utils.arm.symmetrical_bones['arms']['hand'][0]]
                for bone in utils.arm.symmetrical_bones['arms']['hand']:
                    utils.arm.poles['hand'].append(bone)

            for container, bone in utils.arm.poles.items():
                for bone in bone:
                    if container == 'forearm' or container == 'calf':
                        ebone = armature.data.edit_bones.new(bone + '_Pole')
                    else:
                        ebone = armature.data.edit_bones.new(bone + '_Target')
                    ebone.use_deform = False
                    ebone.parent = armature.data.edit_bones[prefix + utils.arm.central_bones['pelvis'][0]]

                    if container == 'forearm':
                        if bone.startswith('L_') or bone.endswith('_L'):
                            ebone.tail = math.copysign(forearm.tail.x, 1), forearm.tail.y+12, forearm.tail.z
                            ebone.head = math.copysign(forearm.head.x, 1), forearm.head.y+10, forearm.head.z
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            ebone.tail = math.copysign(forearm.tail.x, -1), forearm.tail.y+12, forearm.tail.z
                            ebone.head = math.copysign(forearm.head.x, -1), forearm.head.y+10, forearm.head.z
                    elif container == 'calf':
                        if bone.startswith('L_') or bone.endswith('_L'):
                            ebone.tail = math.copysign(calf.tail.x, 1), calf.tail.y-10, calf.tail.z
                            ebone.head = math.copysign(calf.head.x, 1), calf.head.y-12, calf.head.z
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            ebone.tail = math.copysign(calf.tail.x, -1), calf.tail.y-10, calf.tail.z
                            ebone.head = math.copysign(calf.head.x, -1), calf.head.y-12, calf.head.z

                    elif container == 'hand':
                        if bone.startswith('L_') or bone.endswith('_L'):
                            ebone.tail = math.copysign(hand.tail.x, 1), hand.tail.y, hand.tail.z
                            ebone.head = math.copysign(hand.head.x, 1), hand.head.y, hand.head.z
                            ebone.length = 1
                            ebone.head = math.copysign(hand.tail.x, 1), hand.tail.y, hand.tail.z
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            ebone.tail = math.copysign(hand.tail.x, -1), hand.tail.y, hand.tail.z
                            ebone.head = math.copysign(hand.head.x, -1), hand.head.y, hand.head.z
                            ebone.length = 1
                            ebone.head = math.copysign(hand.tail.x, -1), hand.tail.y, hand.tail.z
                    elif container == 'foot':
                        if bone.startswith('L_') or bone.endswith('_L'):
                            ebone.tail = math.copysign(foot.tail.x, 1), foot.tail.y, foot.tail.z
                            ebone.head = math.copysign(foot.head.x, 1), foot.head.y, foot.head.z
                            ebone.length = 1
                            ebone.head = math.copysign(foot.tail.x, 1), foot.tail.y, foot.tail.z
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            ebone.tail = math.copysign(foot.tail.x, -1), foot.tail.y, foot.tail.z
                            ebone.head = math.copysign(foot.head.x, -1), foot.head.y, foot.head.z
                            ebone.length = 1
                            ebone.head = math.copysign(foot.tail.x, -1), foot.tail.y, foot.tail.z

        elif action == 1:            
            for container, bone in utils.arm.poles.items():
                for bone in bone:
                    if container == 'forearm' or container == 'calf':
                        ebone = armature.data.edit_bones[bone + '_Pole']
                    else:
                        ebone = armature.data.edit_bones[bone + '_Target']
                    armature.data.edit_bones.remove(ebone)
            
            utils.arm.poles = {'hand': [], 'foot': [], 'forearm': [], 'calf': []}

        bpy.ops.object.mode_set(mode='OBJECT')

    #Updates bone list in case it was modified
    utils.arm.get_bones(False)

    armature = bpy.data.objects[utils.arm.name]
    prefix = utils.arm.prefix

    current_mode = bpy.context.object.mode

    #List that will store constraint info for bones
    bonelist = {}

    if not utils.arm.poles:
        utils.arm.poles = {'hand': [], 'foot': [], 'forearm': [], 'calf': []}

    poles()
    for bone in utils.arm.symmetrical_bones['arms']['hand'] + utils.arm.symmetrical_bones['legs']['foot']:
        if bone:
            bonelist = constraints(bone)
    
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

    #Reverts back to previously used mode
    bpy.ops.object.mode_set(mode=current_mode)