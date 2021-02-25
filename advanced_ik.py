import bpy
import math 
from . import functions
from .functions import Prefixes
from .functions import update
from .functions import generate_armature

def anim_armature(action):

    vatproperties = bpy.context.scene.vatproperties

    def generate_rigify(action): #Creates Rigify armature
        generate_armature('anim', action)
        
        if action == 0:
            armature = bpy.data.objects[functions.arm.animation_armature_name]

            update(1, armature)

            #Hides all but the first layer
            for i in [1,2,3,5,4,6,7]:
                    armature.data.layers[i] = False

            #Rigify portion
            prefix = functions.arm.prefix

            #Gets pelvis position and gets edit_bone name
            for bone in functions.arm.central_bones:
                if bone.title().count("Pelvis"):
                    pelvis = armature.pose.bones[prefix + bone].head
                    epelvis = armature.data.edit_bones[prefix + bone]
                    
                elif bone.title().count('Head'):
                    head = armature.pose.bones[prefix + bone]
                    ehead = armature.data.edit_bones[prefix + bone]

            for bone in functions.arm.symmetrical_bones:
                if bone.count('Foot'):
                    if bone.startswith('L_') or bone.endswith('_L'):
                        foot_l = armature.pose.bones[prefix + bone].head
                        efoot_l = armature.data.edit_bones[prefix + bone]
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        foot_r = armature.pose.bones[prefix + bone].head
                        efoot_r = armature.data.edit_bones[prefix + bone]

                elif bone.count('Finger'):
                    if bone.count('Finger1'):
                        if bone.count('11') or bone.count('12'):
                            pass
                        else:
                            if bone.startswith('L_') or bone.endswith('_L'):
                                finger1_l = armature.pose.bones[prefix + bone].head
                                efinger1_l = armature.data.edit_bones[prefix + bone]
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                finger1_r = armature.pose.bones[prefix + bone].head
                                efinger1_r = armature.data.edit_bones[prefix + bone]
                    
                    elif bone.count('Finger2'):
                        if bone.count('21') or bone.count('22'):
                            pass
                        else:
                            if bone.startswith('L_') or bone.endswith('_L'):
                                finger2_l = armature.pose.bones[prefix + bone].head
                                efinger2_l = armature.data.edit_bones[prefix + bone]
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                finger2_r = armature.pose.bones[prefix + bone].head
                                efinger2_r = armature.data.edit_bones[prefix + bone]
                        
                    elif bone.count('Finger3'):
                        if bone.count('31') or bone.count('32'):
                            pass
                        else:
                            if bone.startswith('L_') or bone.endswith('_L'):
                                finger3_l = armature.pose.bones[prefix + bone].head
                                efinger3_l = armature.data.edit_bones[prefix + bone]
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                finger3_r = armature.pose.bones[prefix + bone].head
                                efinger3_r = armature.data.edit_bones[prefix + bone]

                    elif bone.count('Finger4'):
                        if bone.count('41') or bone.count('42'):
                            pass
                        else:
                            if bone.startswith('L_') or bone.endswith('_L'):
                                finger4_l = armature.pose.bones[prefix + bone].head
                                efinger4_l = armature.data.edit_bones[prefix + bone]
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                finger4_r = armature.pose.bones[prefix + bone].head
                                efinger4_r = armature.data.edit_bones[prefix + bone]

                elif bone.count('Hand'):
                    if bone.startswith('L_') or bone.endswith('_L'):
                        hand_l = armature.pose.bones[prefix + bone].head
                        ehand_l = armature.data.edit_bones[prefix + bone]
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        hand_r = armature.pose.bones[prefix + bone].head
                        ehand_r = armature.data.edit_bones[prefix + bone]

            #Checks if there are shapekeys, if so, create driver bones for them
            if vatproperties.target_object:
                try:
                    shapekeys = bpy.data.objects[vatproperties.target_object.name].data.shape_keys.key_blocks.keys()
                except:
                    shapekeys = None
                    print("No shape keys detected")

                if shapekeys:
                    
                    #Generates widgets for easier representation of every driver bone
                    create_widgets()

                    eyebrows = 0
                    eyes = 0
                    cheek = 0
                    nose = 0
                    mouth = 0
                    lower_lip = 0
                    upper_lip = 0
                    middle_lip = 0
                    chin = 0

                    for shapekey in shapekeys:
                        #Eyebrows
                        if shapekey.count('AU1L+AU1R') or shapekey.count('AU2L+AU2R') or shapekey.count('AU4L+AU4R') or shapekey.count('AU1AU2L+AU1AU2R') or shapekey.count('AU1AU4L+AU1AU4R') or shapekey.count('AU2AU4L+AU2AU4R'):
                            if eyebrows != 1: 
                                #Inner, outer and full eyebrows
                                for bone in ['Eyebrow_L', 'Eyebrow_R', 'Inner_Eyebrow_L', 'Inner_Eyebrow_R', 'Outer_Eyebrow_L', 'Outer_Eyebrow_R']:
                                    eyebrows = 1
                                    functions.arm.facial_bones.append(bone)

                                    ebone = armature.data.edit_bones.new(bone)
                                    ebone.use_deform = False

                                    if bone == 'Eyebrow_L':
                                        ebone.head.xyz = head.head.x + 1.2, head.head.y - 4.5, head.head.z + 4
                                        ebone.tail.xyz = head.tail.x + 1.2, head.tail.y - 4 , ebone.head.z
                                    elif bone == 'Eyebrow_R':
                                        ebone.head.xyz = head.head.x - 1.2, head.head.y - 4.5, head.head.z + 4
                                        ebone.tail.xyz = head.tail.x - 1.2, head.tail.y - 4, ebone.head.z
                                    elif bone == 'Inner_Eyebrow_L':
                                        ebone.head.xyz = head.head.x + 0.6, head.head.y - 4.5, head.head.z + 3.75
                                        ebone.tail.xyz = head.tail.x + 0.6, head.tail.y - 4 , ebone.head.z
                                    elif bone == 'Inner_Eyebrow_R':
                                        ebone.head.xyz = head.head.x - 0.6, head.head.y - 4.5, head.head.z + 3.75
                                        ebone.tail.xyz = head.tail.x - 0.6, head.tail.y - 4 , ebone.head.z
                                    elif bone == 'Outer_Eyebrow_L':
                                        ebone.head.xyz = head.head.x + 1.8, head.head.y - 4.5, head.head.z + 3.75
                                        ebone.tail.xyz = head.tail.x + 1.8, head.tail.y - 4, ebone.head.z
                                    elif bone == 'Outer_Eyebrow_R':
                                        ebone.head.xyz = head.head.x - 1.8, head.head.y - 4.5, head.head.z + 3.75
                                        ebone.tail.xyz = head.tail.x - 1.8, head.tail.y - 4, ebone.head.z

                        #Eyes
                        elif shapekey.count('f01') or shapekey.count('f02') or shapekey.count('f03') or shapekey.count('f04') or shapekey.count('AU42'):
                            if eyes != 1:
                                #Upper and lower eyelids
                                for bone in ['UpperEye_L', 'UpperEye_R', 'LowerEye_L', 'LowerEye_R']:
                                    eyes = 1
                                    functions.arm.facial_bones.append(bone)

                                    ebone = armature.data.edit_bones.new(bone)
                                    ebone.use_deform = False
                                
                                    if bone == 'UpperEye_L':
                                        ebone.head.xyz = head.head.x + 1.2, head.head.y - 4, head.head.z + 3.5
                                        ebone.tail.xyz = head.tail.x + 1.2, head.tail.y - 3.5 , ebone.head.z

                                    elif bone == 'UpperEye_R':
                                        ebone.head.xyz = head.head.x - 1.2, head.head.y - 4, head.head.z + 3.5
                                        ebone.tail.xyz = head.tail.x - 1.2, head.tail.y - 3.5 , ebone.head.z

                                    elif bone == 'LowerEye_L':
                                        ebone.head.xyz = head.head.x + 1.2, head.head.y - 4, head.head.z + 3
                                        ebone.tail.xyz = head.tail.x + 1.2, head.tail.y - 3.5, ebone.head.z

                                    elif bone == 'LowerEye_R':
                                        ebone.head.xyz = head.head.x - 1.2, head.head.y - 4, head.head.z + 3
                                        ebone.tail.xyz = head.tail.x - 1.2, head.tail.y - 3.5, ebone.head.z
                            
                        #Cheek
                        elif shapekey.count('AU6L+AU6R') or shapekey.count('AU6ZL+AU6ZR') or shapekey.count('AU13L+AU13R'):
                            if cheek != 1:
                                #Cheeks for puffing and squinting
                                for bone in ['Cheek_L', 'Cheek_R']:
                                    cheek = 1
                                    functions.arm.facial_bones.append(bone)

                                    ebone = armature.data.edit_bones.new(bone)
                                    ebone.use_deform = False

                                    if bone == 'Cheek_L':
                                        ebone.head.xyz = head.head.x + 2, head.head.y - 3, head.head.z + 1
                                        ebone.tail.xyz = head.tail.x + 1.5, head.tail.y - 2.5 , ebone.head.z
                                    elif bone == 'Cheek_R':
                                        ebone.head.xyz = head.head.x - 2, head.head.y - 3, head.head.z + 1
                                        ebone.tail.xyz = head.tail.x - 1.5, head.tail.y - 2.5 , ebone.head.z

                        #Nose
                        elif shapekey.count('AU9L+AU9R') or shapekey.count('AU38'):
                            if nose != 1:
                                #Nostrils
                                for bone in ['Nostril_L', 'Nostril_R']:
                                    nose = 1
                                    functions.arm.facial_bones.append(bone)

                                    ebone = armature.data.edit_bones.new(bone)
                                    ebone.use_deform = False

                                    if bone == 'Nostril_L':
                                        ebone.head.xyz = head.head.x + 0.8, head.head.y - 4, head.head.z + 1
                                        ebone.tail.xyz = head.tail.x + 0.8, head.tail.y - 3.5 , ebone.head.z
                                    elif bone == 'Nostril_R':
                                        ebone.head.xyz = head.head.x - 0.8, head.head.y - 4, head.head.z + 1
                                        ebone.tail.xyz = head.tail.x - 0.8, head.tail.y - 3.5 , ebone.head.z

                        #Mouth 
                        elif shapekey.count('AU12L+AU12R') or shapekey.count('AU15L+AU15R') or shapekey.count('AU17L+AU17R') or shapekey.count('AU10L+AU10R') or shapekey.count('AU17DL+AU17DR') or shapekey.count('AU16L+AU16R') or shapekey.count('AU25L+AU25R') or shapekey.count('AU22L+AU22R') or shapekey.count('AU20L+AU20R') or shapekey.count('AU32') or shapekey.count('AU24') or shapekey.count('AU18L+AU18R') or shapekey.count('AU12AU25L+AU12AU25R') or shapekey.count('AU18ZL+AU18ZR') or shapekey.count('AU22ZL+AU22ZR') or shapekey.count('AU13L+AU13R') or shapekey.count('AD96L') or shapekey.count('AD96R'):
                            if mouth != 1:
                                #Mouth corners
                                if shapekey.count('AU12L+AU12R') or shapekey.count('AU15L+AU15R') or shapekey.count('AU22L+AU22R') or shapekey.count('AU20L+AU20R') or shapekey.count('AU24') or shapekey.count('AU18L+AU18R') or shapekey.count('AU12AU25L+AU12AU25R') or shapekey.count('AU18ZL+AU18ZR') or shapekey.count('AU22ZL+AU22ZR'):
                                    for bone in ['MouthCorner_L', 'MouthCorner_R']:
                                        mouth = 1
                                        functions.arm.facial_bones.append(bone)

                                        ebone = armature.data.edit_bones.new(bone)
                                        ebone.use_deform = False

                                        if bone == 'MouthCorner_L':
                                            ebone.head.xyz = head.head.x + 1.2, head.head.y - 4, head.head.z + 0.25
                                            ebone.tail.xyz = head.tail.x + 1, head.tail.y - 3.5 , ebone.head.z
                                        elif bone == 'MouthCorner_R':
                                            ebone.head.xyz = head.head.x - 1.2, head.head.y - 4, head.head.z + 0.25
                                            ebone.tail.xyz = head.tail.x - 1, head.tail.y - 3.5 , ebone.head.z
                                        
                            elif upper_lip != 1:
                                #Upper lip
                                if shapekey.count('AU10L+AU10R'):
                                    for bone in ['UpperLip_L', 'UpperLip_R']:
                                        upper_lip = 1
                                        functions.arm.facial_bones.append(bone)

                                        ebone = armature.data.edit_bones.new(bone)
                                        ebone.use_deform = False

                                        if bone == 'UpperLip_L':
                                            ebone.head.xyz = head.head.x + 0.5, head.head.y - 4.5, head.head.z + 0.5
                                            ebone.tail.xyz = head.tail.x + 0.5, head.tail.y - 4 , ebone.head.z
                                        elif bone == 'UpperLip_R':
                                            ebone.head.xyz = head.head.x - 0.5, head.head.y - 4.5, head.head.z + 0.5
                                            ebone.tail.xyz = head.tail.x - 0.5, head.tail.y - 4 , ebone.head.z

                            elif lower_lip != 1:
                                #Lower lip
                                if shapekey.count('AU17L+AU17R') or shapekey.count('AU17DL+AU17DR') or shapekey.count('AU16L+AU16R') or shapekey.count('AU25L+AU25R') or shapekey.count('AU32'):
                                        for bone in ['LowerLip_L', 'LowerLip_R']:
                                            lower_lip = 1
                                            functions.arm.facial_bones.append(bone)

                                            ebone = armature.data.edit_bones.new(bone)
                                            ebone.use_deform = False

                                            if bone == 'LowerLip_L':
                                                ebone.head.xyz = head.head.x + 0.5, head.head.y - 4.5, head.head.z
                                                ebone.tail.xyz = head.tail.x + 0.5, head.tail.y - 4 , ebone.head.z
                                            elif bone == 'LowerLip_R':
                                                ebone.head.xyz = head.head.x - 0.5, head.head.y - 4.5, head.head.z
                                                ebone.tail.xyz = head.tail.x - 0.5, head.tail.y - 4 , ebone.head.z

                            elif middle_lip != 1:
                                #Middle lip
                                if shapekey.count('AD96L') or shapekey.count('AD96R'):
                                    for bone in ['MiddleLip']:
                                        middle_lip = 1
                                        functions.arm.facial_bones.append(bone)

                                        ebone = armature.data.edit_bones.new(bone)
                                        ebone.use_deform = False

                                        ebone.head.xyz = head.head.x, head.head.y - 4.5, head.head.z + 0.25
                                        ebone.tail.xyz = head.tail.x, head.tail.y - 4 , ebone.head.z


                        #Chin
                        elif shapekey.count('AU31') or shapekey.count('AU26L+AU26R') or shapekey.count('AU27L+AU27R') or shapekey.count('AU26ZL+AU26ZR') or shapekey.count('AU27ZL+AU27ZR') or shapekey.count('AD30L') or shapekey.count('AD30R'):
                            if chin != 1:
                                for bone in ['Chin']:
                                    chin = 1
                                    functions.arm.facial_bones.append(bone)

                                    ebone = armature.data.edit_bones.new(bone)
                                    ebone.use_deform = False
                                
                                    if bone == 'Chin':
                                        ebone.head.xyz = 0, head.head.y - 4.5, head.head.z - 1.5
                                        ebone.tail.xyz = 0, head.tail.y - 4 , ebone.head.z + 0.15

            #Creates 2 pelvis bones for whatever Rigify does with em
            for bone in ['Pelvis_L', 'Pelvis_R']:
                ebone = armature.data.edit_bones.new(prefix + bone)

                ebone.head = pelvis
                ebone.parent = epelvis

                #New pelvis bone positioning
                if bone.startswith('L_') or bone.endswith('_L'):
                    ebone.tail.xyz = pelvis.x-3, pelvis.y-2, pelvis.z+4
                elif bone.startswith('R_') or bone.endswith('_R'):
                    ebone.tail.xyz = pelvis.x+3, pelvis.y-2, pelvis.z+4

            #Creates multiple palm bones for fingers
            for bone in functions.arm.symmetrical_bones:
                if bone.count('Finger1') or bone.count('Finger2') or bone.count('Finger3') or bone.count('Finger4'):
                    if bone.count('11') or bone.count('12') or bone.count('21') or bone.count('22') or bone.count('31') or bone.count('32') or bone.count('41') or bone.count('42'):
                        pass
                    else:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            for bone in ['Palm_' + bone]:
                                ebone = armature.data.edit_bones.new(prefix + bone)

                                if bone.count('Finger1'):
                                    ebone.parent = ehand_l

                                    ebone.tail = finger1_l
                                    ebone.head.xyz = hand_l.x, finger1_l.y, hand_l.z
                                        
                                elif bone.count('Finger2'):
                                    ebone.parent = ehand_l

                                    ebone.tail = finger2_l
                                    ebone.head.xyz = hand_l.x, finger2_l.y, hand_l.z

                                elif bone.count('Finger3'):
                                    ebone.parent = ehand_l

                                    ebone.tail = finger3_l
                                    ebone.head.xyz = hand_l.x, finger3_l.y, hand_l.z

                                elif bone.count('Finger4'):
                                    ebone.parent = ehand_l

                                    ebone.tail = finger4_l
                                    ebone.head.xyz = hand_l.x, finger4_l.y, hand_l.z

                        elif bone.startswith('R_') or bone.endswith('_R'):
                            for bone in ['Palm_' + bone]:
                                ebone = armature.data.edit_bones.new(prefix + bone)

                                if bone.count('Finger1'):
                                    ebone.parent = ehand_r

                                    ebone.tail = finger1_r
                                    ebone.head.xyz = hand_r.x, finger1_r.y, hand_r.z

                                elif bone.count('Finger2'):
                                    ebone.parent = ehand_r

                                    ebone.tail = finger2_r
                                    ebone.head.xyz = hand_r.x, finger2_r.y, hand_r.z

                                elif bone.count('Finger3'):
                                    ebone.parent = ehand_r

                                    ebone.tail = finger3_r
                                    ebone.head.xyz = hand_r.x, finger3_r.y, hand_r.z

                                elif bone.count('Finger4'):
                                    ebone.parent = ehand_r

                                    ebone.tail = finger4_r
                                    ebone.head.xyz = hand_r.x, finger4_r.y, hand_r.z

            for bone in ['Heel_L', 'Heel_R']:
                ebone = armature.data.edit_bones.new(prefix + bone)

                if bone.endswith('_L'):
                    ebone.parent = efoot_l
                    ebone.tail.xyz = foot_l.x+1.5, foot_l.y+1, 0
                    ebone.head.xyz = foot_l.x-1.5, foot_l.y+1, 0
                    ebone.layers[13] = True
                    ebone.layers[0] = False
                elif bone.endswith('_R'):
                    ebone.parent = efoot_r
                    ebone.tail.xyz = foot_r.x-1.5, foot_r.y+1, 0
                    ebone.head.xyz = foot_r.x+1.5, foot_r.y+1, 0
                    ebone.layers[16] = True
                    ebone.layers[0] = False
                    
            update(0)

            #Rigify parameters
            for bone in functions.arm.facial_bones:
                pbone = armature.pose.bones[bone]
                ebone = armature.data.edit_bones[bone]

                pbone.rigify_type = 'basic.raw_copy'
                ebone.layers[0] = True
                ebone.parent = armature.data.edit_bones[prefix + "Head1"] #If bone is not explicitly described, it'll pick a random bone...for some reason

                #Locks rotation and scale since they aren't meant to be used
                pbone.lock_rotation_w = True
                pbone.lock_rotation[0] = True
                pbone.lock_rotation[1] = True
                pbone.lock_rotation[2] = True

                pbone.lock_scale[0] = True
                pbone.lock_scale[1] = True
                pbone.lock_scale[2] = True

                #None of them go forward or backward so Y is locked for them all
                if bone.count('Cheek') or bone.count('LowerLip') or bone.count('UpperLip'):
                    pbone.lock_location[0] = True

                elif bone.count('Eyebrow') or bone.count('UpperEye') or bone.count('LowerEye'):
                    pbone.lock_location[0] = True
                    pbone.lock_location[1] = True

                elif bone.count('MiddleLip'):
                    pbone.lock_location[2] = True

                elif bone.count('MouthCorner'):
                    pass

                else:
                    pbone.lock_location[1] = True

                limit_loc = pbone.constraints.new('LIMIT_LOCATION')
                limit_loc.owner_space = 'LOCAL'
                limit_loc.use_transform_limit = True

                #Min X
                limit_loc.use_min_x = True
                if bone.count('MouthCorner'):
                    limit_loc.min_x = -0.5

                elif bone == 'Nostril_L':
                    limit_loc.min_x = 0

                elif bone == 'Nostril_R':
                    limit_loc.min_x = -0.5

                else:
                    limit_loc.min_x = -1

                #Max X
                limit_loc.use_max_x = True
                if bone.count('MouthCorner') or bone == 'Nostril_L':
                    limit_loc.max_x = 0.5

                elif bone == 'Nostril_R':
                    limit_loc.max_x = 0
                else:
                    limit_loc.max_x = 1

                #Min Y
                limit_loc.use_min_y = True
                if bone.count('Cheek') or bone.count('MouthCorner'):
                    limit_loc.min_y = -1

                elif bone.count('MiddleLip') or bone.count('LowerLip'):
                    limit_loc.min_y = -0.5
                else:
                    limit_loc.min_y = 0

                #Max Y
                limit_loc.use_max_y = True
                limit_loc.max_y = 0

                #Min Z
                limit_loc.use_min_z = True
                if bone.count('Cheek') or bone.count('Nostril') or bone.count('UpperLip'):
                    limit_loc.min_z = 0
                    
                elif bone.count('UpperEye') or bone.count('LowerEye'):
                    limit_loc.min_z = -0.2

                elif bone.count('Eyebrow') or bone.count('LowerLip') or bone.count('MouthCorner'):
                    limit_loc.min_z = -0.5

                elif bone.count('Chin'):
                    limit_loc.min_z = -2
                else:
                    limit_loc.min_z = -1

                #Max Z
                limit_loc.use_max_z = True

                if bone.count('UpperEye') or bone.count('LowerEye'):
                    limit_loc.max_z = 0.2

                elif bone.count('Eyebrow') or bone.count('UpperLip') or bone.count('MouthCorner') or bone.count('Nostril') or bone.count('LowerLip'):
                    limit_loc.max_z = 0.5
                else:
                    limit_loc.max_z = 1

                #Assings Widgets to bone drivers

                if bone.count('Eyebrow') or bone.count('UpperEye') or bone.count('LowerEye'):
                    widget = bpy.data.objects['UpDown']
                    pbone.custom_shape = widget
                    
                    if bone.count('Eyebrow'):
                        pbone.custom_shape_scale = 0.3

                    elif bone.count('UpperEye') or bone.count('LowerEye'):
                        pbone.custom_shape_scale = 0.25

                elif bone.count('Cheek'):
                    widget = bpy.data.objects['Cheek']
                    pbone.custom_shape = widget

                    pbone.custom_shape_scale = 0.5

                elif bone.count('Nostril'):
                    if bone.endswith('_L'):
                        widget = bpy.data.objects['Nostril_L']

                    elif bone.endswith('_R'):
                        widget = bpy.data.objects['Nostril_R']
                        
                    pbone.custom_shape = widget
                    pbone.custom_shape_scale = 0.35

                elif bone.count('UpperLip'):
                    widget = bpy.data.objects['UpperLip']
                    pbone.custom_shape = widget
                    pbone.custom_shape_scale = 0.25

                elif bone.count('MiddleLip'):
                    widget = bpy.data.objects['MiddleLip']
                    pbone.custom_shape = widget
                    pbone.custom_shape_scale = 0.35
                
                elif bone.count('LowerLip'):
                    widget = bpy.data.objects['LowerLip']
                    pbone.custom_shape = widget
                    pbone.custom_shape_scale = 0.25

                elif bone.count('Chin'):
                    widget = bpy.data.objects['Chin']
                    pbone.custom_shape = widget
                    pbone.custom_shape_scale = 0.7
                    
                elif bone.count('MouthCorner'):
                    widget = bpy.data.objects['MouthCorner']
                    pbone.custom_shape = widget
                    pbone.custom_shape_scale = 0.4

            armature.data.show_bone_custom_shapes = True

            #Custom pelvis creation
            for bone in ['Pelvis_L', 'Pelvis_R']:
                pbone = armature.pose.bones[prefix + bone]
                ebone = armature.data.edit_bones[prefix + bone]
                
                pbone.rigify_type = 'basic.super_copy'
                pbone.rigify_parameters.make_control = False
                ebone.layers[3] = True
                ebone.layers[0] = False

            #Places created palm bones to corresponding bone layers and gets their position
            for bone in functions.arm.symmetrical_bones:
                if bone.count('Finger'):
                    if bone.count('0') or bone.count('11') or bone.count('12') or bone.count('21') or bone.count('22') or bone.count('31') or bone.count('31') or bone.count('32') or bone.count('41') or bone.count('42'):
                        pass
                    else:
                        pbone = armature.pose.bones[prefix + 'Palm_' + bone]
                        ebone = armature.data.edit_bones[prefix + 'Palm_' + bone]

                        ebone.layers[5] = True
                        ebone.layers[0] = False

                        if bone.count('Finger1'):
                            if bone.startswith('L_') or bone.endswith('_L'):
                                epalm_1_l = armature.data.edit_bones[prefix + 'Palm_' + bone]
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                epalm_1_r = armature.data.edit_bones[prefix + 'Palm_' + bone]

                            pbone.rigify_type = 'limbs.super_palm'
                            
                        elif bone.count('Finger2'):
                            if bone.startswith('L_') or bone.endswith('_L'):
                                epalm_2_l = armature.data.edit_bones[prefix + 'Palm_' + bone]
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                epalm_2_r = armature.data.edit_bones[prefix + 'Palm_' + bone]
                            
                        elif bone.count('Finger3'):
                            if bone.startswith('L_') or bone.endswith('_L'):
                                epalm_3_l = armature.data.edit_bones[prefix + 'Palm_' + bone]
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                epalm_3_r = armature.data.edit_bones[prefix + 'Palm_' + bone]

                        elif bone.count('Finger4'):
                            if bone.startswith('L_') or bone.endswith('_L'):
                                epalm_4_l = armature.data.edit_bones[prefix + 'Palm_' + bone]
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                epalm_4_r = armature.data.edit_bones[prefix + 'Palm_' + bone]
                
            for bone in functions.arm.symmetrical_bones:

                #Bones deleted prior
                if bone.count('Trapezius') or bone.count('Bicep') or bone.count('Elbow') or bone.count('Ulna') or bone.count('Wrist') or bone.count('Knee') or bone.count('Quadricep'):
                    pass
                else:
                    pbone = armature.pose.bones[prefix + bone]
                    param = pbone.rigify_parameters
                    ebone = armature.data.edit_bones[prefix + bone]

                #Placeholder layer must be 5 to avoid a big annoyance with Finger02 always being on layer 0 despite being extremely explicit about it, must be a Blender bug
                ebone.layers[5] = True

                for i in [1,2,3,4,5,6,7]:
                    ebone.layers[i] = False

                if bone.count('Finger'):
                    ebone.layers[5] = True

                    if bone.count('Finger0'):
                        if bone.count('01') or bone.count('02'):
                            pass
                        else:
                            pbone.rigify_type = 'limbs.super_finger'

                    if bone.count('Finger1'):
                        if bone.count('11') or bone.count('12'):
                            pass
                        else:
                            pbone.rigify_type = 'limbs.super_finger'

                            if bone.startswith('L_') or bone.endswith('_L'):
                                ebone.parent = epalm_1_l
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                ebone.parent = epalm_1_r

                    elif bone.count('Finger2'):
                        if bone.count('21') or bone.count('22'):
                            pass
                        else:
                            pbone.rigify_type = 'limbs.super_finger'

                            if bone.startswith('L_') or bone.endswith('_L'):
                                ebone.parent = epalm_2_l
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                ebone.parent = epalm_2_r

                    elif bone.count('Finger3'):
                        if bone.count('31') or bone.count('32'):
                            pass
                        else:
                            pbone.rigify_type = 'limbs.super_finger'

                            if bone.startswith('L_') or bone.endswith('_L'):
                                ebone.parent = epalm_3_l
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                ebone.parent = epalm_3_r

                    elif bone.count('Finger4'):
                        if bone.count('41') or bone.count('42'):
                            pass
                        else:
                            pbone.rigify_type = 'limbs.super_finger'

                            if bone.startswith('L_') or bone.endswith('_L'):
                                ebone.parent = epalm_4_l
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                ebone.parent = epalm_4_r

                if bone.count('UpperArm') or bone.count('Forearm') or bone.count('Hand'):
                    if bone.startswith('L_') or bone.endswith('_L'):
                        ebone.layers[7] = True
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        ebone.layers[10] = True

                if bone.count('Thigh') or bone.count('Calf') or bone.count('Foot') or bone.count('Toe'):
                    if bone.startswith('L_') or bone.endswith('_L'):
                        ebone.layers[13] = True
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        ebone.layers[16] = True

                if bone.count('Clavicle'):
                    pbone.rigify_type = 'basic.super_copy'
                    param.make_widget = False
                    ebone.layers[3] = True

                if bone.count('UpperArm'):
                    pbone.rigify_type = 'limbs.super_limb'
                    param.tweak_layers[1] = False
                    param.fk_layers[1] = False

                    if bone.startswith('L_') or bone.endswith('_L'):
                        param.fk_layers[8] = True
                        param.tweak_layers[9] = True
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        param.fk_layers[11] = True
                        param.tweak_layers[12] = True
                    param.segments = 1

                if bone.count('Thigh'):
                    pbone.rigify_type = 'limbs.super_limb'
                    param.limb_type = 'leg'
                    param.tweak_layers[1] = False
                    param.fk_layers[1] = False

                    if bone.startswith('L_') or bone.endswith('_L'):
                        param.fk_layers[14] = True
                        param.tweak_layers[15] = True
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        param.fk_layers[17] = True
                        param.tweak_layers[18] = True
                    param.segments = 1

                ebone.layers[5] = False

            #Central
            for bone in functions.arm.central_bones:
                pbone = armature.pose.bones[prefix + bone]
                param = pbone.rigify_parameters
                ebone = armature.data.edit_bones[prefix + bone]

                ebone.layers[3] = True

                if bone.count('Pelvis'):
                    pbone.rigify_type = 'spines.basic_spine'
                    param.pivot_pos = 2
                    param.tweak_layers[1] = False
                    param.tweak_layers[4] = True
                    param.fk_layers[1] = False
                    param.fk_layers[4] = True

                if bone.count('Neck1'):
                    pbone.rigify_type = 'spines.super_head'
                    param.connect_chain = True
                    param.tweak_layers[1] = False
                    param.tweak_layers[4] = True
                
                ebone.layers[0] = False

            armature = bpy.data.armatures[functions.arm.animation_armature_real.name]

            #Creates bone groups
            for group in ['Root', 'IK', 'Special', 'Tweak', 'FK', 'Extra']:
                color = armature.rigify_colors.add()
                color.name = group

                armature.rigify_colors[group].select = (0.3140000104904175, 0.7839999794960022, 1.0)
                armature.rigify_colors[group].active = (0.5490000247955322, 1.0, 1.0)
                armature.rigify_colors[group].standard_colors_lock = True

                if group == 'Root':
                    armature.rigify_colors[group].normal = (0.43529415130615234, 0.18431372940540314, 0.41568630933761597)
                if group == 'IK':
                    armature.rigify_colors[group].normal = (0.6039215922355652, 0.0, 0.0)
                if group== 'Special':
                    armature.rigify_colors[group].normal = (0.9568628072738647, 0.7882353663444519, 0.0470588281750679)
                if group== 'Tweak':
                    armature.rigify_colors[group].normal = (0.03921568766236305, 0.21176472306251526, 0.5803921818733215)
                if group== 'FK':
                    armature.rigify_colors[group].normal = (0.11764706671237946, 0.5686274766921997, 0.03529411926865578)
                if group== 'Extra':
                    armature.rigify_colors[group].normal = (0.9686275124549866, 0.250980406999588, 0.0941176563501358)

            #Creates layers
            for i in range(29):
                armature.rigify_layers.add()

            #Rigify layers
            names = ['Face', 'Face (Primary)','Face (Secondary)','Torso', 'Torso (Tweak)', 'Fingers', 'Fingers (Detail)', 'Arm.L (IK)', 'Arm.L (FK)', 'Arm.L (Tweak)', 'Arm.R (IK)', 'Arm.R (FK)', 'Arm.R (Tweak)', 'Leg.L (IK)', 'Leg.L (FK)', 'Leg.L (Tweak)', 'Leg.R (IK)', 'Leg.R (FK)', 'Leg.R (Tweak)']

            row_groups = [1,2,2,3,4,5,6,7,8,9,7,8,9,10,11,12,10,11,12]

            layer_groups = [1,5,2,3,4,6,5,2,5,4,2,5,4,2,5,4,2,5,4]

            for i, name, row, group in zip(range(19), names, row_groups, layer_groups):
                armature.rigify_layers[i].name = name
                armature.rigify_layers[i].row = row
                armature.rigify_layers[i].group = group

            armature.layers[0] = False

            functions.arm.animation_armature_setup = True

            for i in [3,5,7,10,13,16]:
                    armature.layers[i] = True

            bpy.ops.object.mode_set(mode='OBJECT')

            print("Animation armature created!")

        elif action == 1:

            #Deletes Left/Right vertex groups if present
            try:
                left_group = bpy.data.objects[vatproperties.target_object.name].vertex_groups['Left']
                bpy.data.objects[vatproperties.target_object.name].vertex_groups.remove(left_group)
            except:
                pass
            
            try:
                right_group = bpy.data.objects[vatproperties.target_object.name].vertex_groups['Right']
                bpy.data.objects[vatproperties.target_object.name].vertex_groups.remove(right_group)
            except:
                pass

            #Checks if shapekeys exist and deletes everything after the division line
            try:
                division_line = bpy.data.objects[vatproperties.target_object.name].data.shape_keys.key_blocks.find('----------')
                total_shapekeys = len(bpy.data.objects[vatproperties.target_object.name].data.shape_keys.key_blocks)

                for shapekey in range(division_line, total_shapekeys):
                    pass
            except:
                pass
                


    def empty_rotation(bone, type): #Sets empty rotation
        prefix = functions.arm.prefix

        base = bpy.data.objects['base_{}{} ({})'.format(prefix, bone, functions.arm.name)]
        target = bpy.data.objects['target_{}{} ({})'.format(prefix, bone, functions.arm.name)]
        
        #Default empty rotation, fit for most bones

        if type == 0: #Symmetrical bones default
            target.rotation_euler[0] = math.radians(90)
            target.rotation_euler[1] = math.radians(180)
            target.rotation_euler[2] = math.radians(-90)
        elif type == 1: #Center bones default
            target.rotation_euler[0] = 0
            target.rotation_euler[1] = 0
            target.rotation_euler[2] = 0
        
        #Counterweight for the small bump applied to the calf
        if bone.count('Calf'):
            target.location[2] = 1
            target.location[1] = 0.10000000149011612 #0.1°

        #Upper body
        if vatproperties.retarget_top_preset == 'OP1':
            if bone.count('Clavicle'):
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-106)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(104)

        elif vatproperties.retarget_top_preset == 'OP2':
            if bone.count('Clavicle'):
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-95)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(90)

        #More specific empty rotations for bones that don't fit the default rotation
        if bone.count('Hand'):
            if bone.startswith('L_') or bone.endswith('_L'):
                target.rotation_euler[0] = math.radians(170)
                target.rotation_euler[1] = math.radians(185)
                target.rotation_euler[2] = math.radians(-92)
            elif bone.startswith('R_') or bone.endswith('_R'):
                target.rotation_euler[0] = math.radians(10)
                target.rotation_euler[1] = math.radians(185)
                target.rotation_euler[2] = math.radians(-88)

        elif bone.count('Finger'):
            #Makes them smaller for the sake of readability
            base.empty_display_size = 0.5
            target.empty_display_size = 0.5

            if bone.count('Finger0'):
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(180)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(180)
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = math.radians(90)

                if bone.count('Finger02'):
                    if bone.startswith('L_') or bone.endswith('_L'):
                        target.rotation_euler[0] = math.radians(10)
                        target.rotation_euler[1] = math.radians(-110)
                        target.rotation_euler[2] = 0
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        target.rotation_euler[0] = 0
                        target.rotation_euler[1] = math.radians(-70)
                        target.rotation_euler[2] = math.radians(-10)

            elif bone.count('Finger1'):
                target.rotation_euler[0] = math.radians(-90)
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = math.radians(90)

                if bone.count('Finger12'):
                    target.rotation_euler[0] = 0
                    target.rotation_euler[1] = math.radians(-90)
                    target.rotation_euler[2] = 0

            elif bone.count('Finger2') or bone.count('Finger3') or bone.count('Finger4'):
                target.rotation_euler[0] = math.radians(-90)
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = math.radians(90)

                if bone.count('Finger22') or bone.count('Finger32'):
                    target.rotation_euler[0] = 0
                    target.rotation_euler[1] = math.radians(-90)
                    target.rotation_euler[2] = 0

                elif bone.count('Finger42'):
                    target.rotation_euler[0] = 0
                    target.rotation_euler[2] = 0

                    if bone.startswith('L_') or bone.endswith('_L'):
                        target.rotation_euler[1] = math.radians(-100)
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        target.rotation_euler[1] = math.radians(-80)

        #Spine
        if vatproperties.retarget_center_preset == 'OP1':
            if bone.count('Spine') or bone.count('Neck'):
                target.rotation_euler[2] = math.radians(90)
            elif bone.count('Head'):
                target.rotation_euler[2] = math.radians(89.5)

        elif vatproperties.retarget_center_preset == 'OP2':
            if bone.count('Spine') or bone.count('Neck'):
                target.rotation_euler[2] = math.radians(90)

            elif bone.count('Head'):
                target.rotation_euler[2] = math.radians(80)

            elif bone.count('Pelvis'):
                target.rotation_euler[0] = math.radians(22)

        #Lower body
        if vatproperties.retarget_bottom_preset == 'OP1':
            if bone.count('Thigh'):
                target.rotation_euler[1] = math.radians(-3)
                target.rotation_euler[2] = math.radians(90)

                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(85)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(95)
            
            elif bone.count('Calf'):
                target.rotation_euler[1] = math.radians(3.5)
                target.rotation_euler[2] = math.radians(90)

                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(85)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(95)

            elif bone.count('Foot'):
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = math.radians(90)

            elif bone.count('Toe0'):
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = math.radians(90)
                
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-88)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(-96)

        elif vatproperties.retarget_bottom_preset == 'OP2':
            if bone.count('Thigh') or bone.count('Calf'):
                target.rotation_euler[0] = 0
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = math.radians(90)
            elif bone.count('Foot'):
                target.rotation_euler[0] = math.radians(90)
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = math.radians(90)

    def link(): #Organizes armature after empty creation

        def retarget(bone): #Creates empties and links them to Rigify armature/Source armature
            armature = bpy.data.objects['rig']
            
            #Retarget empties creation
            try:
                collection = bpy.data.collections["Retarget Empties ({})".format(functions.arm.name)]
            except:
                collection = bpy.data.collections.new("Retarget Empties ({})".format(functions.arm.name))
                bpy.context.scene.collection.children.link(collection)

            collection.hide_viewport = True

            if bone.count('Trapezius') or bone.count('Bicep') or bone.count('Elbow') or bone.count('Knee') or bone.count('Ulna') or bone.count('Wrist'):
                pass
            else:
                #Creates base empty and links
                base = bpy.data.objects.new('base_{}{} ({})'.format(prefix, bone, functions.arm.name), None)
                collection.objects.link(base)
                base.empty_display_type = 'CUBE'
                base.hide_select = True

                #Location constraint
                loc = base.constraints.new('COPY_LOCATION')
                loc.target = armature
                loc.subtarget = 'ORG-' + prefix + bone

                #Rotation constraint
                rot = base.constraints.new('COPY_ROTATION')
                rot.target = armature
                rot.subtarget = 'ORG-' + prefix + bone

                #Creates target empty and links
                target = bpy.data.objects.new('target_{}{} ({})'.format(prefix, bone, functions.arm.name), None)
                collection.objects.link(target)
                target.empty_display_type = 'SPHERE'

                #Parent to base
                base.parent = parent
                target.parent = base

                #Bone connection
                armature = bpy.data.objects[functions.arm.name]
                loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')
                loc.name = "Retarget Location"
                loc.target = target
                rot = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')
                rot.name = "Retarget Rotation"
                rot.target = target

        #Creates parent for all bases for easier storage/manipulation
        parent = bpy.data.objects.new('parent_' + functions.arm.name, None)

        prefix = functions.arm.prefix

        #Gets armature name and applies presets based on names
        current = str(vatproperties.target_armature.name)

        #Automatic presets
        if current.casefold().count('alyx'):
            vatproperties.retarget_top_preset = 'OP1'
            vatproperties.retarget_center_preset = 'OP2'
            vatproperties.retarget_bottom_preset = 'OP1'
        else:
            vatproperties.retarget_top_preset = 'OP1'
            vatproperties.retarget_center_preset = 'OP1'
            vatproperties.retarget_bottom_preset = 'OP1'
        

        for bone in functions.arm.symmetrical_bones:
            retarget(bone)
            empty_rotation(bone, 0)

        for bone in functions.arm.central_bones:
            retarget(bone)
            empty_rotation(bone, 1)

        #Connects parent to collection
        collection = bpy.data.collections["Retarget Empties ({})".format(functions.arm.name)]
        collection.objects.link(parent)

        #Renames armature to prior generated armature
        armature = bpy.data.objects['rig']
        armature.name = functions.arm.name + '.anim'
        armature.data.name = functions.arm.name_real.name + '.anim'

        #Deletes generated armature
        generate_armature('anim', 2)

        #Links to animation armature
        try:
            collection = bpy.data.collections['Animation Armature']
        except:
            collection = None
            
        if collection:
            collection.objects.link(armature)

        functions.arm.animation_armature = True
        functions.arm.animation_armature_setup = False
        functions.arm.animation_armature_name_full = armature
        functions.arm.animation_armature_name = armature.name
        functions.arm.animation_armature_real = armature.data

    def face_flex_setup(): #Sets up drivers for face flexes that will be controlled by face bones
        prefix = functions.arm.prefix
            
        if vatproperties.target_object:
            try:
                shapekeys = bpy.data.objects[vatproperties.target_object.name].data.shape_keys.key_blocks.keys()
                object = bpy.data.objects[vatproperties.target_object.name].data.shape_keys.key_blocks
            except:
                shapekeys = None
                print("No shape keys detected")

        if shapekeys:
            #Vertex group creation

            #Creates vertex groups
            left_group = bpy.data.objects[vatproperties.target_object.name].vertex_groups.new(name='Left')
            right_group = bpy.data.objects[vatproperties.target_object.name].vertex_groups.new(name='Right')

            #Left side
            for vertex in bpy.data.objects[vatproperties.target_object.name].data.vertices:
                #Left side
                if vertex.co[0] > 0.005:
                    left_group.add([vertex.index], 1, 'REPLACE')

                #Right side
                elif vertex.co[0] < -0.005:
                    right_group.add([vertex.index], 1, 'REPLACE')

                elif vertex.co[0] <0.005 >-0.005:
                    left_group.add([vertex.index], 0.5, 'REPLACE')
                    right_group.add([vertex.index], 0.5, 'REPLACE')

            #Still need to add center vertices to both groups, will do once i figure out

            #Shapekey creation

            #Container for generated shapekeys
            new_shapekeys = []

            #Divides old shapekeys from generated ones
            bpy.data.objects[vatproperties.target_object.name].shape_key_add(name='----------', from_mix=False)
            bpy.data.objects[vatproperties.target_object.name].show_only_shape_key = False

            for shapekey in shapekeys:
                #Makes sure no other shapekey is active
                object[shapekey].value = 0

                #Appends central shapekeys, since they don't need L/R versions of them
                if shapekey.count('AU17L+AU17R') or shapekey.count('AU26L+AU26R') or shapekey.count('AU27ZL+AU27ZR') or shapekey.count('AD30L') or shapekey.count('AD30R') or shapekey.count('AU22ZL+AU22ZR') or shapekey.count('AD96L') or shapekey.count('AD96R'):
                    new_shapekeys.append(shapekey)

                #Skips basis, redundant halfway close eye, reduntant halfway squint, reduntant harsher frown, redudant lower lip drop, reduntant halfway puckering level 1 and 2 mouth open and odd individual eye shapekeys
                elif shapekey.lower().count('basis') or shapekey.count('AU42') or shapekey.count('AU22L+AU22R') or shapekey.count('AU20L+AU20R') or shapekey.count('AU6L+AU6R') or shapekey.count('AU18L+AU18R') or shapekey.count('AU27L+AU27R') or shapekey.count('AU26ZL+AU26ZR') or shapekey.count('AU25L+AU25R') or shapekey.count('AU22ZL+AU22ZR') or shapekey.count('lower_right') or shapekey.count('lower_left') or shapekey.count('upper_right') or shapekey.count('upper_left') or shapekey.count('lower_right.001') or shapekey.count('lower_left.001') or shapekey.count('upper_right.001') or shapekey.count('upper_left.001'):
                    pass

                else:
                    object[shapekey].value = 1
                    left_shapekey = bpy.data.objects[vatproperties.target_object.name].shape_key_add(name=shapekey + '_L', from_mix=True)
                    right_shapekey = bpy.data.objects[vatproperties.target_object.name].shape_key_add(name=shapekey + '_R', from_mix=True)

                    new_shapekeys.append(left_shapekey.name)
                    new_shapekeys.append(right_shapekey.name)

                    #Assigns shapekeys to group
                    left_shapekey.vertex_group = left_group.name
                    right_shapekey.vertex_group = right_group.name

                    object[shapekey].value = 0

            for shapekey in new_shapekeys:
                #Creates driver
                driver = object[shapekey].driver_add('value') #Creates new driver for shapekey

                #Parameters and target
                variable = driver.driver.variables.new() #Creates new variable onto the shapekey
                variable.name = "flex"
                driver.driver.expression = variable.name #Changes expression to created variable's name
                variable.type = 'TRANSFORMS' #Changes type of variable to transform

                target = variable.targets[0]
                target.id = bpy.data.objects[functions.arm.animation_armature_name] #Links variable to animation armature

                #Specific tweaks for each bone

                #Eyebrows
                if shapekey.count('AU1L+AU1R') or shapekey.count('AU2L+AU2R') or shapekey.count('AU4L+AU4R') or shapekey.count('AU1AU2L+AU1AU2R') or shapekey.count('AU1AU4L+AU1AU4R') or shapekey.count("AU2AU4L+AU2AU4R"): 

                    #AU1L+AU1R = Inner eyebrow raise
                    #AU2L+AU2R = Outer eyebrow raise
                    #AU4L+AU4R = Full eyebrow drop
                    #AU1AU2L+AU1AU2R = Full eyebrow raise
                    #AU1AU4L+AU1AU4R = Outer eyebrow drop
                    #AU2AU4L+AU2AU4R = Inner eyebrow drop

                    target.transform_space = 'LOCAL_SPACE'
                    target.transform_type = 'LOC_Z'

                    if shapekey.count('AU1L+AU1R') or shapekey.count('AU2AU4L+AU2AU4R'):
                        if shapekey.endswith('_L'):
                            target.bone_target = "Inner_Eyebrow_L"
                        elif shapekey.endswith('_R'):
                            target.bone_target = "Inner_Eyebrow_R"

                    elif shapekey.count('AU2L+AU2R') or shapekey.count('AU1AU4L+AU1AU4R'):
                        if shapekey.endswith('_L'):
                            target.bone_target = "Outer_Eyebrow_L"
                        elif shapekey.endswith('_R'):
                            target.bone_target = "Outer_Eyebrow_R"

                    elif shapekey.count('AU4L+AU4R') or shapekey.count('AU1AU2L+AU1AU2R'):
                        if shapekey.endswith('_L'):
                            target.bone_target = "Eyebrow_L"
                        elif shapekey.endswith('_R'):
                            target.bone_target = "Eyebrow_R"

                    if shapekey.count('AU4L+AU4R') or shapekey.count('AU1AU4L+AU1AU4R') or shapekey.count('AU2AU4L+AU2AU4R'):
                        driver.modifiers[0].coefficients[1] = -2

                    elif shapekey.count('AU1L+AU1R') or shapekey.count('AU2L+AU2R') or shapekey.count('AU1AU2L+AU1AU2R'):
                        driver.modifiers[0].coefficients[1] = 2

                #Eyes
                elif shapekey.count('f01') or shapekey.count('f02') or shapekey.count('f03') or shapekey.count('f04'):
                    
                    #f01 = Upper eyelids drop
                    #f02 = Upper eyelids raise
                    #f03 = Lower eyelids drop
                    #f04 = Lower eyelids raise

                    target.transform_space = 'LOCAL_SPACE'
                    target.transform_type = 'LOC_Z'

                    if shapekey.count('f01') or shapekey.count('f02'):
                        if shapekey.endswith('_L'):
                            target.bone_target = "UpperEye_L"
                        elif shapekey.endswith('_R'):
                            target.bone_target = "UpperEye_R"

                    elif shapekey.count('f03') or shapekey.count('f04'):
                        if shapekey.endswith('_L'):
                            target.bone_target = "LowerEye_L"
                        elif shapekey.endswith('_R'):
                            target.bone_target = "LowerEye_R"

                    if shapekey.count('f01') or shapekey.count('f03'):
                        driver.modifiers[0].coefficients[1] = -5
                    
                    elif shapekey.count('f02') or shapekey.count('f04'):
                        driver.modifiers[0].coefficients[1] = 5

                #Cheeks
                elif shapekey.count('AU6ZL+AU6ZR') or shapekey.count('AU13L+AU13R'):

                    #AU6ZL+AU6ZR = Squint
                    #AU13L+AU13R = Filling cheek with air

                    target.transform_space = 'LOCAL_SPACE'

                    if shapekey.endswith('_L'):
                        target.bone_target = "Cheek_L"
                    elif shapekey.endswith('_R'):
                        target.bone_target = "Cheek_R"

                    if shapekey.count('AU6ZL+AU6ZR'):
                        target.transform_type = 'LOC_Z'

                    elif shapekey.count('AU13L+AU13R'):
                        target.transform_type = 'LOC_Y'
                        driver.modifiers[0].coefficients[1] = -1

                #Nostrils
                elif shapekey.count('AU9L+AU9R') or shapekey.count('AU38'):
                    
                    #AU9L+AU9R = Nostril raise
                    #AU38 = Breath

                    target.transform_space = 'LOCAL_SPACE'

                    if shapekey.endswith('_L'):
                        target.bone_target = "Nostril_L"
                    elif shapekey.endswith('_R'):
                        target.bone_target = "Nostril_R"

                    if shapekey.count('AU9L+AU9R'):
                        target.transform_type = 'LOC_Z'
                        driver.modifiers[0].coefficients[1] = 2

                    elif shapekey.count('AU38'):
                        target.transform_type = 'LOC_X'

                        if shapekey.endswith('_L'):
                            driver.modifiers[0].coefficients[1] = 2

                        elif shapekey.count('_R'):
                            driver.modifiers[0].coefficients[1] = -2

                #Mouth Corners
                elif shapekey.count('AU12L+AU12R') or shapekey.count('AU15L+AU15R') or shapekey.count('AU24') or shapekey.count('AU12AU25L+AU12AU25R') or shapekey.count('AU18ZL+AU18ZR'):

                    #AU12L+AU12R = Smile
                    #AU15L+AU15R = Frown
                    #AU24 = Tightener
                    #AU12AU25L+AU12AU25R = Big smile
                    #AU18ZL+AU18ZR = Puckering

                    target.transform_space = 'LOCAL_SPACE'

                    if shapekey.endswith('_L'):
                        target.bone_target = "MouthCorner_L"
                    elif shapekey.endswith('_R'):
                        target.bone_target = "MouthCorner_R"

                    if shapekey.count('AU12L+AU12R') or shapekey.count('AU15L+AU15R'):
                        target.transform_type = 'LOC_Z'

                        if shapekey.count('AU12L+AU12R'):
                            driver.modifiers[0].coefficients[1] = 2

                        elif shapekey.count('AU15L+AU15R'):
                            driver.modifiers[0].coefficients[1] = -2

                    elif shapekey.count('AU24') or shapekey.count('AU18ZL+AU18ZR'):
                        target.transform_type = 'LOC_X'

                        if shapekey.count('AU24'):
                            if shapekey.endswith('_L'):
                                driver.modifiers[0].coefficients[1] = 2
                            elif shapekey.endswith('_R'):
                                driver.modifiers[0].coefficients[1] = -2
                        
                        elif shapekey.count('AU18ZL+AU18ZR'):
                            if shapekey.endswith('_L'):
                                driver.modifiers[0].coefficients[1] = -2
                            elif shapekey.endswith('_R'):
                                driver.modifiers[0].coefficients[1] = 2

                    elif shapekey.count('AU12AU25L+AU12AU25R'):
                        target.transform_type = 'LOC_Y'

                        driver.modifiers[0].coefficients[1] = -1

                #Upper lips
                elif shapekey.count('AU10L+AU10R'):

                    #AU10L+AU10R = Upper lip raise

                    target.transform_type = 'LOC_Z'
                    target.transform_space = 'LOCAL_SPACE'

                    if shapekey.endswith('_L'):
                        target.bone_target = "UpperLip_L"
                    elif shapekey.endswith('_R'):
                        target.bone_target = "UpperLip_R"

                    driver.modifiers[0].coefficients[1] = 2

                #Lower lips
                elif shapekey.count('AU17DL+AU17DR') or shapekey.count('AU16L+AU16R') or shapekey.count('AU32'):

                    #AU17DL+AU17DR = Lower lip raise
                    #AU16L+AU16R = Lower lip drop
                    #AU32 = Bite

                    target.transform_space = 'LOCAL_SPACE'

                    if shapekey.endswith('_L'):
                        target.bone_target = "LowerLip_L"
                    elif shapekey.endswith('_R'):
                        target.bone_target = "LowerLip_R"

                    if shapekey.count('AU16L+AU16R') or shapekey.count('AU17DL+AU17DR'):
                        target.transform_type = 'LOC_Z'

                        if shapekey.count('AU16L+AU16R'):
                            driver.modifiers[0].coefficients[1] = -2
                        elif shapekey.count('AU17DL+AU17DR'):
                            driver.modifiers[0].coefficients[1] = 2

                    elif shapekey.count('AU32'):
                        target.transform_type = 'LOC_Y'
                        driver.modifiers[0].coefficients[1] = -2

                #Chin
                elif shapekey.count('AU17L+AU17R') or shapekey.count('AU26L+AU26R') or shapekey.count('AU27ZL+AU27ZR') or shapekey.count('AD30L') or shapekey.count('AD30R'):

                    #AU17L+AU17R = Chin raise (sort of)
                    #AU26L+AU26R = Chin drop
                    #AU27ZL+AU27ZR = Full mouth open
                    #AD30L/R = Chin sideways

                    target.bone_target = "Chin" 
                    target.transform_space = 'LOCAL_SPACE'
                    
                    #Upwards/Downwards movement
                    if shapekey.count('AU17L+AU17R') or shapekey.count('AU26L+AU26R') or shapekey.count('AU27ZL+AU27ZR'):
                        target.transform_type = 'LOC_Z'

                        #Chin lowers
                        if shapekey.count('AU26L+AU26R'):
                            driver.modifiers[0].coefficients[1] = -1
                            driver.modifiers[0].use_restricted_range = True
                            driver.modifiers[0].frame_start = -0.6
                            driver.modifiers[0].blend_in = 0.1

                        #Mouth fully opens
                        elif shapekey.count('AU27ZL+AU27ZR'):
                            driver.modifiers[0].coefficients[1] = -0.5 #Negative coefficient = Activated when moved down
                            driver.modifiers[0].use_restricted_range = True
                            driver.modifiers[0].frame_start = -2.1
                            driver.modifiers[0].frame_end = -0.3
                            driver.modifiers[0].blend_out = 0.25
                    
                    #Sideways movement
                    elif shapekey.count('AD30L') or shapekey.count('AD30R'):
                        target.transform_type = 'LOC_X'

                        if shapekey.count('AD30R'):
                                driver.modifiers[0].coefficients[1] = -1

                #MiddleLip
                elif shapekey.count('AD96L') or shapekey.count('AD96R') or shapekey.count('AU22ZL+AU22ZR'):

                    #AD96L/R = Mouth sideways
                    #AU22ZL+AU22ZR = Outside puckering

                    target.bone_target = "MiddleLip" 
                    target.transform_space = 'LOCAL_SPACE'

                    if shapekey.count('AD96'):
                        target.transform_type = 'LOC_X'

                        if shapekey.endswith('R'):
                            driver.modifiers[0].coefficients[1] = -1

                    elif shapekey.count('AU22ZL+AU22ZR'):
                        target.transform_type = 'LOC_Y'

                        driver.modifiers[0].coefficients[1] = -2

    def create_widgets():

        #Creates widgets collection before Rigify
        collection = bpy.data.collections.new('Widgets')
        bpy.context.scene.collection.children.link(collection)

        collection.hide_viewport = True
        
        #Empty that stores all the generated widgets for easier storage/manipulation
        parent = bpy.data.objects.new('parent_widgets', None)

        for widget in ['Chin', 'MouthCorner', 'Cheek', 'LowerLip', 'MiddleLip', 'UpperLip', 'Nostril_L', 'Nostril_R', 'UpDown']:
            try:
                bpy.data.objects[widget]
            except:
                #Creates mesh datablock and object
                mesh = bpy.data.meshes.new(widget)
                object = bpy.data.objects.new(widget, mesh)
                object.parent = parent

                #Gets Rigify's collection and links to it
                collection = bpy.data.collections['Widgets']
                collection.objects.link(object)

                faces = []

                if widget == 'Chin':
                    vertices = [(0.0000, 0.0000, 1.0000), (-0.3827, 0.0000, 0.9239), (-0.7071, 0.0000, 0.7071), (-0.9239, 0.0000, 0.3827), (-1.0000, 0.0000, 0.0000), (-0.9239, -0.0000, -0.3827), (-0.7071, -0.0000, -0.7071), (-0.3827, -0.0000, -0.9239), (0.0000, -0.0000, -1.0000), (0.3827, -0.0000, -0.9239), (0.7071, -0.0000, -0.7071), (0.9239, -0.0000, -0.3827), (1.0000, 0.0000, 0.0000), (0.9239, 0.0000, 0.3827), (0.7071, 0.0000, 0.7071), (0.3827, 0.0000, 0.9239), (-0.3718, 0.0000, 1.8058), (-0.6592, 0.0000, 1.3381), (0.3718, 0.0000, 1.8058), (0.6592, 0.0000, 1.3381), (0.4179, 0.0000, 1.0882), (0.7722, 0.0000, 0.8515), (-0.7722, 0.0000, 0.8515), (-0.4179, 0.0000, 1.0882), (0.0000, 0.0000, 1.1805), (0.0000, 0.0000, 2.2000), (-2.2000, 0.0000, 0.0000), (-1.1805, 0.0000, 0.0000), (-1.0882, 0.0000, -0.4179), (-0.8515, 0.0000, -0.7722), (-0.8515, 0.0000, 0.7722), (-1.0882, 0.0000, 0.4179), (-1.3381, 0.0000, 0.6592), (-1.8058, 0.0000, 0.3718), (-1.3381, 0.0000, -0.6592), (-1.8058, 0.0000, -0.3718), (2.2000, 0.0000, -0.0000), (1.1805, 0.0000, -0.0000), (1.0882, 0.0000, 0.4179), (0.8515, 0.0000, 0.7722), (0.8515, 0.0000, -0.7722), (1.0882, 0.0000, -0.4179), (1.3381, 0.0000, -0.6592), (1.8058, 0.0000, -0.3718), (1.3381, 0.0000, 0.6592), (1.8058, 0.0000, 0.3718), (0.3718, 0.0000, -1.8058), (0.6592, 0.0000, -1.3381), (-0.3718, 0.0000, -1.8058), (-0.6592, 0.0000, -1.3381), (-0.4179, 0.0000, -1.0882), (-0.7722, 0.0000, -0.8515), (0.7722, 0.0000, -0.8515), (0.4179, 0.0000, -1.0882), (-0.0000, 0.0000, -1.1805), (-0.0000, 0.0000, -2.2000)]
                    edges = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13), (15, 14), (0, 15), (16, 25), (17, 22), (18, 25), (19, 21), (17, 16), (19, 18), (24, 20), (20, 21), (22, 23), (23, 24), (28, 27), (29, 28), (31, 30), (27, 31), (32, 33), (34, 35), (32, 30), (33, 26), (34, 29), (35, 26), (38, 37), (39, 38), (41, 40), (37, 41), (42, 43), (44, 45), (42, 40), (43, 36), (44, 39), (45, 36), (46, 55), (47, 52), (48, 55), (49, 51), (47, 46), (49, 48), (54, 50), (50, 51), (52, 53), (53, 54)]

                elif widget == 'MouthCorner':
                    vertices = [(0.0000, 0.0000, -1.0000), (0.3827, 0.0000, -0.9239), (0.7071, 0.0000, -0.7071), (0.9239, 0.0000, -0.3827), (1.0000, 0.0000, 0.0000), (0.9239, -0.0000, 0.3827), (0.7071, -0.0000, 0.7071), (0.3827, -0.0000, 0.9239), (-0.0000, -0.0000, 1.0000), (-0.3827, -0.0000, 0.9239), (-0.7071, -0.0000, 0.7071), (-0.9239, -0.0000, 0.3827), (-1.0000, 0.0000, -0.0000), (-0.9239, 0.0000, -0.3827), (-0.7071, 0.0000, -0.7071), (-0.3827, 0.0000, -0.9239), (0.3718, 0.0000, -1.8058), (0.6592, 0.0000, -1.3381), (-0.3718, 0.0000, -1.8058), (-0.6592, 0.0000, -1.3381), (-0.4179, 0.0000, -1.0882), (-0.7722, 0.0000, -0.8515), (0.7722, 0.0000, -0.8515), (0.4179, 0.0000, -1.0882), (-0.0000, 0.0000, -1.1805), (-0.0000, 0.0000, -2.2000), (2.2000, 0.0000, 0.0000), (1.1805, 0.0000, -0.0000), (1.0882, 0.0000, 0.4179), (0.8515, 0.0000, 0.7722), (0.8515, 0.0000, -0.7722), (1.0882, 0.0000, -0.4179), (1.3381, 0.0000, -0.6592), (1.8058, 0.0000, -0.3718), (1.3381, 0.0000, 0.6592), (1.8058, 0.0000, 0.3718), (-2.2000, 0.0000, -0.0000), (-1.1805, 0.0000, 0.0000), (-1.0882, 0.0000, -0.4179), (-0.8515, 0.0000, -0.7722), (-0.8515, 0.0000, 0.7722), (-1.0882, 0.0000, 0.4179), (-1.3381, 0.0000, 0.6592), (-1.8058, 0.0000, 0.3718), (-1.3381, 0.0000, -0.6592), (-1.8058, 0.0000, -0.3718), (-0.3718, 0.0000, 1.8058), (-0.6592, 0.0000, 1.3381), (0.3718, 0.0000, 1.8058), (0.6592, 0.0000, 1.3381), (0.4179, 0.0000, 1.0882), (0.7722, 0.0000, 0.8515), (-0.7722, 0.0000, 0.8515), (-0.4179, 0.0000, 1.0882), (0.0000, 0.0000, 1.1805), (-0.0000, 0.0000, 2.2000), (0.0000, 0.0000, -0.7000), (0.2679, 0.0000, -0.6467), (0.4950, 0.0000, -0.4950), (0.6467, 0.0000, -0.2679), (0.7000, 0.0000, 0.0000), (0.6467, -0.0000, 0.2679), (0.4950, -0.0000, 0.4950), (0.2679, -0.0000, 0.6467), (-0.0000, -0.0000, 0.7000), (-0.2679, -0.0000, 0.6467), (-0.4950, -0.0000, 0.4950), (-0.6467, -0.0000, 0.2679), (-0.7000, 0.0000, -0.0000), (-0.6467, 0.0000, -0.2679), (-0.4950, 0.0000, -0.4950), (-0.2679, 0.0000, -0.6467)]
                    edges = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13), (15, 14), (0, 15), (16, 25), (17, 22), (18, 25), (19, 21), (17, 16), (19, 18), (24, 20), (20, 21), (22, 23), (23, 24), (28, 27), (29, 28), (31, 30), (27, 31), (32, 33), (34, 35), (32, 30), (33, 26), (34, 29), (35, 26), (38, 37), (39, 38), (41, 40), (37, 41), (42, 43), (44, 45), (42, 40), (43, 36), (44, 39), (45, 36), (46, 55), (47, 52), (48, 55), (49, 51), (47, 46), (49, 48), (54, 50), (50, 51), (52, 53), (53, 54), (57, 56), (58, 57), (59, 58), (60, 59), (61, 60), (62, 61), (63, 62), (64, 63), (65, 64), (66, 65), (67, 66), (68, 67), (69, 68), (70, 69), (71, 70), (56, 71)]

                elif widget == 'Cheek':
                    vertices = [(0.0000, 0.0000, -1.0000), (0.3827, 0.0000, -0.9239), (0.7071, 0.0000, -0.7071), (0.9239, 0.0000, -0.3827), (1.0000, 0.0000, 0.0000), (0.9239, -0.0000, 0.3827), (0.7071, -0.0000, 0.7071), (0.3827, -0.0000, 0.9239), (-0.0000, -0.0000, 1.0000), (-0.3827, -0.0000, 0.9239), (-0.7071, -0.0000, 0.7071), (-0.9239, -0.0000, 0.3827), (-1.0000, 0.0000, -0.0000), (-0.9239, 0.0000, -0.3827), (-0.7071, 0.0000, -0.7071), (-0.3827, 0.0000, -0.9239), (-0.2679, 0.0000, -0.6467), (-0.4950, 0.0000, -0.4950), (-0.6467, 0.0000, -0.2679), (-0.7000, 0.0000, -0.0000), (-0.6467, -0.0000, 0.2679), (-0.4950, -0.0000, 0.4950), (-0.2679, -0.0000, 0.6467), (-0.0000, -0.0000, 0.7000), (0.2679, -0.0000, 0.6467), (0.4950, -0.0000, 0.4950), (0.6467, -0.0000, 0.2679), (0.7000, 0.0000, 0.0000), (0.6467, 0.0000, -0.2679), (0.4950, 0.0000, -0.4950), (0.2679, 0.0000, -0.6467), (0.0000, 0.0000, -0.7000), (-0.3718, 0.0000, 1.8058), (-0.6592, 0.0000, 1.3381), (0.3718, 0.0000, 1.8058), (0.6592, 0.0000, 1.3381), (0.4179, 0.0000, 1.0882), (0.7722, 0.0000, 0.8515), (-0.7722, 0.0000, 0.8515), (-0.4179, 0.0000, 1.0882), (0.0000, 0.0000, 1.1805), (-0.0000, 0.0000, 2.2000)]
                    edges = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13), (15, 14), (0, 15), (31, 16), (17, 18), (19, 20), (20, 21), (18, 19), (16, 17), (23, 24), (25, 26), (27, 28), (24, 25), (29, 30), (30, 31), (28, 29), (21, 22), (26, 27), (22, 23), (32, 41), (33, 38), (34, 41), (35, 37), (33, 32), (35, 34), (40, 36), (36, 37), (38, 39)]

                elif widget == 'LowerLip':
                    vertices = [(0.0000, 0.0000, 1.0000), (-0.3827, 0.0000, 0.9239), (-0.7071, 0.0000, 0.7071), (-0.9239, 0.0000, 0.3827), (-1.0000, 0.0000, 0.0000), (-0.9239, -0.0000, -0.3827), (-0.7071, -0.0000, -0.7071), (-0.3827, -0.0000, -0.9239), (0.0000, -0.0000, -1.0000), (0.3827, -0.0000, -0.9239), (0.7071, -0.0000, -0.7071), (0.9239, -0.0000, -0.3827), (1.0000, 0.0000, 0.0000), (0.9239, 0.0000, 0.3827), (0.7071, 0.0000, 0.7071), (0.3827, 0.0000, 0.9239), (0.2679, 0.0000, 0.6467), (0.4950, 0.0000, 0.4950), (0.6467, 0.0000, 0.2679), (0.7000, 0.0000, 0.0000), (0.6467, -0.0000, -0.2679), (0.4950, -0.0000, -0.4950), (0.2679, -0.0000, -0.6467), (0.0000, -0.0000, -0.7000), (-0.2679, -0.0000, -0.6467), (-0.4950, -0.0000, -0.4950), (-0.6467, -0.0000, -0.2679), (-0.7000, 0.0000, 0.0000), (-0.6467, 0.0000, 0.2679), (-0.4950, 0.0000, 0.4950), (-0.2679, 0.0000, 0.6467), (0.0000, 0.0000, 0.7000), (0.3718, 0.0000, -1.8058), (0.6592, 0.0000, -1.3381), (-0.3718, 0.0000, -1.8058), (-0.6592, 0.0000, -1.3381), (-0.4179, 0.0000, -1.0882), (-0.7722, 0.0000, -0.8515), (0.7722, 0.0000, -0.8515), (0.4179, 0.0000, -1.0882), (-0.0000, 0.0000, -1.1805), (-0.0000, 0.0000, -2.2000), (-0.3718, 0.0000, 1.8058), (-0.6592, 0.0000, 1.3381), (0.3718, 0.0000, 1.8058), (0.6592, 0.0000, 1.3381), (0.4179, 0.0000, 1.0882), (0.7722, 0.0000, 0.8515), (-0.7722, 0.0000, 0.8515), (-0.4179, 0.0000, 1.0882), (0.0000, 0.0000, 1.1805), (-0.0000, 0.0000, 2.2000)]
                    edges = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13), (15, 14), (0, 15), (31, 16), (17, 18), (19, 20), (20, 21), (18, 19), (16, 17), (23, 24), (25, 26), (27, 28), (24, 25), (29, 30), (30, 31), (28, 29), (21, 22), (26, 27), (22, 23), (32, 41), (33, 38), (34, 41), (35, 37), (33, 32), (35, 34), (40, 36), (36, 37), (38, 39), (39, 40), (42, 51), (43, 48), (44, 51), (45, 47), (43, 42), (45, 44), (50, 46), (46, 47), (48, 49), (49, 50)]

                elif widget == 'MiddleLip':
                    vertices = [(0.0000, 0.0000, -1.0000), (0.3827, 0.0000, -0.9239), (0.7071, 0.0000, -0.7071), (0.9239, 0.0000, -0.3827), (1.0000, 0.0000, 0.0000), (0.9239, -0.0000, 0.3827), (0.7071, -0.0000, 0.7071), (0.3827, -0.0000, 0.9239), (-0.0000, -0.0000, 1.0000), (-0.3827, -0.0000, 0.9239), (-0.7071, -0.0000, 0.7071), (-0.9239, -0.0000, 0.3827), (-1.0000, 0.0000, -0.0000), (-0.9239, 0.0000, -0.3827), (-0.7071, 0.0000, -0.7071), (-0.3827, 0.0000, -0.9239), (-0.2679, 0.0000, -0.6467), (-0.4950, 0.0000, -0.4950), (-0.6467, 0.0000, -0.2679), (-0.7000, 0.0000, -0.0000), (-0.6467, -0.0000, 0.2679), (-0.4950, -0.0000, 0.4950), (2.2000, 0.0000, 0.0000), (1.1805, 0.0000, -0.0000), (1.0882, 0.0000, 0.4179), (0.8515, 0.0000, 0.7722), (0.8515, 0.0000, -0.7722), (1.0882, 0.0000, -0.4179), (1.3381, 0.0000, -0.6592), (1.8058, 0.0000, -0.3718), (1.3381, 0.0000, 0.6592), (1.8058, 0.0000, 0.3718), (-2.2000, 0.0000, -0.0000), (-1.1805, 0.0000, 0.0000), (-1.0882, 0.0000, -0.4179), (-0.8515, 0.0000, -0.7722), (-0.8515, 0.0000, 0.7722), (-1.0882, 0.0000, 0.4179), (-1.3381, 0.0000, 0.6592), (-1.8058, 0.0000, 0.3718), (-1.3381, 0.0000, -0.6592), (-1.8058, 0.0000, -0.3718), (-0.2679, -0.0000, 0.6467), (-0.0000, -0.0000, 0.7000), (0.2679, -0.0000, 0.6467), (0.4950, -0.0000, 0.4950), (0.6467, -0.0000, 0.2679), (0.7000, 0.0000, 0.0000), (0.6467, 0.0000, -0.2679), (0.4950, 0.0000, -0.4950), (0.2679, 0.0000, -0.6467), (0.0000, 0.0000, -0.7000)]
                    edges = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13), (15, 14), (0, 15), (16, 17), (51, 16), (17, 18), (18, 19), (19, 20), (20, 21), (24, 23), (25, 24), (27, 26), (23, 27), (28, 29), (30, 31), (28, 26), (29, 22), (30, 25), (31, 22), (34, 33), (35, 34), (37, 36), (33, 37), (38, 39), (40, 41), (38, 36), (39, 32), (40, 35), (41, 32), (21, 42), (43, 44), (44, 45), (46, 47), (42, 43), (45, 46), (47, 48), (48, 49), (49, 50), (50, 51)]

                elif widget == 'UpperLip':
                    vertices = [(0.0000, 0.0000, -1.0000), (0.3827, 0.0000, -0.9239), (0.7071, 0.0000, -0.7071), (0.9239, 0.0000, -0.3827), (1.0000, 0.0000, 0.0000), (0.9239, -0.0000, 0.3827), (0.7071, -0.0000, 0.7071), (0.3827, -0.0000, 0.9239), (-0.0000, -0.0000, 1.0000), (-0.3827, -0.0000, 0.9239), (-0.7071, -0.0000, 0.7071), (-0.9239, -0.0000, 0.3827), (-1.0000, 0.0000, -0.0000), (-0.9239, 0.0000, -0.3827), (-0.7071, 0.0000, -0.7071), (-0.3827, 0.0000, -0.9239), (-0.3718, 0.0000, 1.8058), (-0.6592, 0.0000, 1.3381), (0.3718, 0.0000, 1.8058), (0.6592, 0.0000, 1.3381), (0.4179, 0.0000, 1.0882), (0.7722, 0.0000, 0.8515), (-0.7722, 0.0000, 0.8515), (-0.4179, 0.0000, 1.0882), (0.0000, 0.0000, 1.1805), (-0.0000, 0.0000, 2.2000)]
                    edges = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13), (15, 14), (0, 15), (16, 25), (17, 22), (18, 25), (19, 21), (17, 16), (19, 18), (24, 20), (20, 21), (22, 23), (23, 24)]

                elif widget == 'Nostril_L':
                    vertices = [(0.0000, 0.0000, -1.0000), (0.3827, 0.0000, -0.9239), (0.7071, 0.0000, -0.7071), (0.9239, 0.0000, -0.3827), (1.0000, 0.0000, 0.0000), (0.9239, -0.0000, 0.3827), (0.7071, -0.0000, 0.7071), (0.3827, -0.0000, 0.9239), (-0.0000, -0.0000, 1.0000), (-0.3827, -0.0000, 0.9239), (-0.7071, -0.0000, 0.7071), (-0.9239, -0.0000, 0.3827), (-1.0000, 0.0000, -0.0000), (-0.9239, 0.0000, -0.3827), (-0.7071, 0.0000, -0.7071), (-0.3827, 0.0000, -0.9239), (-0.3718, 0.0000, 1.8058), (-0.6592, 0.0000, 1.3381), (0.3718, 0.0000, 1.8058), (0.6592, 0.0000, 1.3381), (0.4179, 0.0000, 1.0882), (0.7722, 0.0000, 0.8515), (-0.7722, 0.0000, 0.8515), (-0.4179, 0.0000, 1.0882), (0.0000, 0.0000, 1.1805), (-0.0000, 0.0000, 2.2000), (1.8058, 0.0000, 0.3718), (1.3381, 0.0000, 0.6592), (1.8058, 0.0000, -0.3718), (1.3381, 0.0000, -0.6592), (1.0882, 0.0000, -0.4179), (0.8515, 0.0000, -0.7722), (0.8515, 0.0000, 0.7722), (1.0882, 0.0000, 0.4179), (1.1805, 0.0000, -0.0000), (2.2000, 0.0000, 0.0000)]
                    edges = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13), (15, 14), (0, 15), (16, 25), (17, 22), (18, 25), (19, 21), (17, 16), (19, 18), (24, 20), (20, 21), (22, 23), (23, 24), (26, 35), (27, 32), (28, 35), (29, 31), (27, 26), (29, 28), (34, 30), (30, 31), (32, 33), (33, 34)]

                elif widget == 'Nostril_R':
                    vertices = [(-0.0000, 0.0000, -1.0000), (-0.3827, 0.0000, -0.9239), (-0.7071, 0.0000, -0.7071), (-0.9239, 0.0000, -0.3827), (-1.0000, 0.0000, 0.0000), (-0.9239, -0.0000, 0.3827), (-0.7071, -0.0000, 0.7071), (-0.3827, -0.0000, 0.9239), (0.0000, -0.0000, 1.0000), (0.3827, -0.0000, 0.9239), (0.7071, -0.0000, 0.7071), (0.9239, -0.0000, 0.3827), (1.0000, 0.0000, -0.0000), (0.9239, 0.0000, -0.3827), (0.7071, 0.0000, -0.7071), (0.3827, 0.0000, -0.9239), (0.3718, 0.0000, 1.8058), (0.6592, 0.0000, 1.3381), (-0.3718, 0.0000, 1.8058), (-0.6592, 0.0000, 1.3381), (-0.4179, 0.0000, 1.0882), (-0.7722, 0.0000, 0.8515), (0.7722, 0.0000, 0.8515), (0.4179, 0.0000, 1.0882), (-0.0000, 0.0000, 1.1805), (0.0000, 0.0000, 2.2000), (-1.8058, 0.0000, 0.3718), (-1.3381, 0.0000, 0.6592), (-1.8058, 0.0000, -0.3718), (-1.3381, 0.0000, -0.6592), (-1.0882, 0.0000, -0.4179), (-0.8515, 0.0000, -0.7722), (-0.8515, 0.0000, 0.7722), (-1.0882, 0.0000, 0.4179), (-1.1805, 0.0000, -0.0000), (-2.2000, 0.0000, 0.0000)]
                    edges = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13), (15, 14), (0, 15), (16, 25), (17, 22), (18, 25), (19, 21), (17, 16), (19, 18), (24, 20), (20, 21), (22, 23), (23, 24), (26, 35), (27, 32), (28, 35), (29, 31), (27, 26), (29, 28), (34, 30), (30, 31), (32, 33), (33, 34)]

                elif widget == 'UpDown':
                    vertices = [(0.0000, 0.0000, 1.0000), (-0.3827, 0.0000, 0.9239), (-0.7071, 0.0000, 0.7071), (-0.9239, 0.0000, 0.3827), (-1.0000, 0.0000, 0.0000), (-0.9239, -0.0000, -0.3827), (-0.7071, -0.0000, -0.7071), (-0.3827, -0.0000, -0.9239), (0.0000, -0.0000, -1.0000), (0.3827, -0.0000, -0.9239), (0.7071, -0.0000, -0.7071), (0.9239, -0.0000, -0.3827), (1.0000, 0.0000, 0.0000), (0.9239, 0.0000, 0.3827), (0.7071, 0.0000, 0.7071), (0.3827, 0.0000, 0.9239), (0.3718, 0.0000, -1.8058), (0.6592, 0.0000, -1.3381), (-0.3718, 0.0000, -1.8058), (-0.6592, 0.0000, -1.3381), (-0.4179, 0.0000, -1.0882), (-0.7722, 0.0000, -0.8515), (0.7722, 0.0000, -0.8515), (0.4179, 0.0000, -1.0882), (-0.0000, 0.0000, -1.1805), (-0.0000, 0.0000, -2.2000), (-0.0000, 0.0000, 2.2000), (0.0000, 0.0000, 1.1805), (-0.4179, 0.0000, 1.0882), (-0.7722, 0.0000, 0.8515), (0.7722, 0.0000, 0.8515), (0.4179, 0.0000, 1.0882), (0.6592, 0.0000, 1.3381), (0.3718, 0.0000, 1.8058), (-0.6592, 0.0000, 1.3381), (-0.3718, 0.0000, 1.8058)]
                    edges = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13), (15, 14), (0, 15), (16, 25), (17, 22), (18, 25), (19, 21), (17, 16), (19, 18), (24, 20), (20, 21), (22, 23), (23, 24), (28, 27), (31, 30), (27, 31), (34, 35), (29, 28), (32, 33), (32, 30), (33, 26), (34, 29), (35, 26)]

                object.data.from_pydata(vertices, edges, faces)

        collection.objects.link(parent)

        print("Facial flex widgets generated!")

    #Updates bone list in case it was modified
    functions.arm.get_bones()

    if action == 0 or action == 1: #Usual creation/deletion
        generate_rigify(action)

    elif action == 2: #Creates empties and links it to Source armature, also creates widgets and setups facial flexes
        link()
        face_flex_setup()

    elif action == 3: #Empty rotation modification
        for bone in functions.arm.symmetrical_bones:
            empty_rotation(bone, 0)
        for bone in functions.arm.central_bones:
            empty_rotation(bone, 1)