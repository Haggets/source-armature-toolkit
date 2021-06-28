import bpy
import math 
from . import utils
from .utils import Prefixes
from .utils import update
from .utils import generate_armature
from .utils import generate_shapekey_dict
from .utils import helper_convert
from .armature_rename import armature_rename
from .armature_rename import bone_rename

def anim_armature(action):

    vatproperties = bpy.context.scene.vatproperties
    vatinfo = bpy.context.scene.vatinfo

    def generate_rigify(action): #Creates Rigify armature and fills in all the Rigify parameters

        #Armature creation
        generate_armature('anim', action)

        if utils.arm.central_bones['pelvis']:
            armature = utils.arm.armature
            prefix = utils.arm.prefix
            ppelvis = armature.pose.bones[prefix + utils.arm.central_bones['pelvis'][0]]
            #Equivalent to 1 meter relative to the pelvis location in order to maintain consistency between different scales
            global unit
            
            unit = ppelvis.head.z*1.02746481 #*0.1027464784
            #The scale used in the operations below are relative to the standard size of a Source model correctly matching the scene scale in Blender (Models scaled down by 0.0254)

        #Creation
        if action == 0:
            armature = utils.arm.animation_armature

            #Selects animation armature
            update(1, armature)

            '''#Creates driver so the original armature mimics the animation armature's scale
            driver = utils.arm.armature.driver_add('scale')

            for index, driver in enumerate(driver):
                #Parameters and target
                variable = driver.driver.variables.new() #Creates new variable onto the shapekey
                variable.name = "scale"
                driver.driver.expression = variable.name #Changes expression to created variable's name
                variable.type = 'TRANSFORMS' #Changes type of variable to transform

                target = variable.targets[0]
                target.id = armature #Links variable to animation armature
                target.transform_space = 'LOCAL_SPACE'
                if index == 0:
                    target.transform_type = 'SCALE_X'
                elif index == 1:
                    target.transform_type = 'SCALE_Y'
                elif index == 2:
                    target.transform_type = 'SCALE_Z'''
                
            #Hides all but the first layer
            for i in [1,2,3,5,4,6,7]:
                armature.data.layers[i] = False

            #Rigify portion
            prefix = utils.arm.prefix
                    
            #Checks if there are shapekeys, if so, create driver bones for them
            if vatproperties.target_object:
                try:
                    shapekeys_raw = vatproperties.target_object.data.shape_keys.key_blocks.keys()
                except:
                    shapekeys_raw = None
                    print("No shape keys detected")

                utils.arm.unused_shapekeys = ['AU6L+AU6R', 'AU25L+AU25R', 'AU22L+AU22R', 'AU20L+AU20R', 'AU18L+AU18R', 'AU26ZL+AU26ZR', 'AU12AU25L+AU12AU25R', 'upper_right', 'upper_right.001', 'lower_right', 'lower_right.001', 'upper_left', 'upper_left.001', 'lower_left', 'lower_left.001']

                utils.arm.shapekeys = {'basis': {'basis': ''}, 'eyebrows': {'AU1': '', 'AU2': '', 'AU4': '', 'AU1AU2': '', 'AU1AU4': '', 'AU2AU4': ''}, 'eyes': {'f01': '', 'f02': '', 'f03': '', 'f04': '', 'AU42': ''}, 'cheek': {'AU6Z': '', 'AU13': ''}, 'nose': {'AU9': '', 'AU38': ''}, 'mouth': {'AU12': '', 'AU15': '', 'AU10': '', 'AU17D': '', 'AU16': '', 'AU32': '', 'AU24': '', 'AU18Z': '', 'AU22Z': '', 'AD96L': '', 'AD96R': ''}, 'chin': {'AU31': '', 'AU26': '', 'AU27': '', 'AU27Z': '', 'AD30L': '', 'AD30R': '', 'AU17': ''}}

                if shapekeys_raw:
                    object_data = vatproperties.target_object.data.copy()
                    object_data.name = vatproperties.target_object.data.name + '.anim'
                    vatproperties.target_object.data = object_data

                    utils.arm.shapekeys = generate_shapekey_dict(utils.arm.shapekeys, shapekeys_raw)

                    head = prefix + utils.arm.central_bones['head'][0]
                    
                    #Generates widgets for easier representation of every driver bone
                    create_widgets()

                    #Checks to make sure bones aren't repeated
                    eyebrows = False
                    eyes = False
                    cheek = False
                    nose = False
                    mouth = False
                    lower_lip = False
                    upper_lip = False
                    middle_lip = False
                    chin = False

                    if utils.arm.central_bones['pelvis']:
                        ppelvis = armature.pose.bones[prefix + utils.arm.central_bones['pelvis'][0]]
                        for cat in utils.arm.shapekeys.keys():
                            for container, shapekey in utils.arm.shapekeys[cat].items():
                                if cat == 'eyebrows':
                                    if container:
                                        if not eyebrows: 
                                            eyebrows = True
                                            #Inner, outer and full eyebrows
                                            for bone in ['Eyebrow_L', 'Eyebrow_R', 'Inner_Eyebrow_L', 'Inner_Eyebrow_R', 'Outer_Eyebrow_L', 'Outer_Eyebrow_R']:
                                                utils.arm.facial_bones.append(bone)

                                                ebone = armature.data.edit_bones.new(bone)
                                                ebone.use_deform = False

                                                if bone == 'Eyebrow_L':
                                                    ebone.head.xyz = 0.030171*unit, -0.105926*unit, 1.74215*unit
                                                elif bone == 'Eyebrow_R':
                                                    ebone.head.xyz = -0.030171*unit, -0.105926*unit, 1.74215*unit
                                                elif bone == 'Inner_Eyebrow_L':
                                                    ebone.head.xyz = 0.014599*unit, -0.105926*unit, 1.73485*unit
                                                elif bone == 'Inner_Eyebrow_R':
                                                    ebone.head.xyz = -0.014599*unit, -0.105926*unit, 1.73485*unit
                                                elif bone == 'Outer_Eyebrow_L':
                                                    ebone.head.xyz = 0.04623*unit, -0.105926*unit, 1.73485*unit
                                                elif bone == 'Outer_Eyebrow_R':
                                                    ebone.head.xyz = -0.04623*unit, -0.105926*unit, 1.73485*unit

                                                ebone.tail.xyz = ebone.head.x, ebone.head.y+0.0127*unit, ebone.head.z

                                elif cat == 'eyes':
                                    if container:
                                        if not eyes:
                                            eyes = True
                                            #Upper and lower eyelids
                                            for bone in ['UpperEye_L', 'UpperEye_R', 'LowerEye_L', 'LowerEye_R']:
                                                utils.arm.facial_bones.append(bone)

                                                ebone = armature.data.edit_bones.new(bone)
                                                ebone.use_deform = False
                                            
                                                if bone == 'UpperEye_L':
                                                    ebone.head.xyz = 0.030171*unit, -0.08976*unit, 1.7295*unit
                                                elif bone == 'UpperEye_R':
                                                    ebone.head.xyz = -0.030171*unit, -0.08976*unit, 1.7295*unit
                                                elif bone == 'LowerEye_L':
                                                    ebone.head.xyz = 0.030171*unit, -0.08976*unit, 1.7149*unit
                                                elif bone == 'LowerEye_R':
                                                    ebone.head.xyz = -0.030171*unit, -0.08976*unit, 1.7149*unit
                                                    
                                                ebone.tail.xyz = ebone.head.x, ebone.head.y+0.0127*unit, ebone.head.z

                                elif cat == 'cheek':
                                    if container:
                                        if not cheek:
                                            cheek = True
                                            #Cheeks for puffing and squinting
                                            for bone in ['Cheek_L', 'Cheek_R']:
                                                utils.arm.facial_bones.append(bone)

                                                ebone = armature.data.edit_bones.new(bone)
                                                ebone.use_deform = False

                                                if bone == 'Cheek_L':
                                                    ebone.head.xyz = 0.048663*unit, -0.082728*unit, 1.66672*unit
                                                    ebone.tail.xyz = 0.044819*unit, -0.070624*unit, ebone.head.z
                                                elif bone == 'Cheek_R':
                                                    ebone.head.xyz = -0.048663*unit, -0.082728*unit, 1.66672*unit
                                                    ebone.tail.xyz = -0.044819*unit, -0.070624*unit, ebone.head.z

                                                ebone.length = 0.0127*unit
                                            
                                elif cat == 'nose':
                                    if container:
                                        if not nose:
                                            nose = True
                                            #Nostrils
                                            for bone in ['Nostril_L', 'Nostril_R']:
                                                utils.arm.facial_bones.append(bone)

                                                ebone = armature.data.edit_bones.new(bone)
                                                ebone.use_deform = False

                                                if bone == 'Nostril_L':
                                                    ebone.head.xyz = 0.019465*unit, -0.09976*unit, 1.66624*unit
                                                elif bone == 'Nostril_R':
                                                    ebone.head.xyz = -0.019465*unit, -0.09976*unit, 1.66624*unit

                                                ebone.tail.xyz = ebone.head.x, ebone.head.y+0.0127*unit, ebone.head.z


                                if cat == 'mouth':
                                    if container:
                                        if not mouth:
                                            #Mouth corners
                                            if container == 'AU12' or container == 'AU15' or container == 'AU24' or container == 'AU18Z' or container == 'AU22Z':
                                                mouth = True
                                                for bone in ['MouthCorner_L', 'MouthCorner_R']:
                                                    utils.arm.facial_bones.append(bone)

                                                    ebone = armature.data.edit_bones.new(bone)
                                                    ebone.use_deform = False

                                                    if bone == 'MouthCorner_L':
                                                        ebone.head.xyz = 0.030623*unit, -0.096764*unit, 1.64726*unit
                                                        ebone.tail.xyz = 0.024791*unit, -0.085483*unit, 1.64726*unit
                                                    elif bone == 'MouthCorner_R':
                                                        ebone.head.xyz = -0.030623*unit, -0.096764*unit, 1.64726*unit
                                                        ebone.tail.xyz = -0.024791*unit, -0.085483*unit, 1.64726*unit
                                                    
                                                    ebone.length = 0.0127*unit

                                        elif not upper_lip:
                                            #Upper lip
                                            if container == 'AU10':
                                                upper_lip = True
                                                for bone in ['UpperLip_L', 'UpperLip_R']:
                                                    utils.arm.facial_bones.append(bone)

                                                    ebone = armature.data.edit_bones.new(bone)
                                                    ebone.use_deform = False

                                                    if bone == 'UpperLip_L':
                                                        ebone.head.xyz = 0.011679*unit, -0.10706*unit, 1.65456*unit
                                                    elif bone == 'UpperLip_R':
                                                        ebone.head.xyz = -0.011679*unit, -0.10706*unit, 1.65456*unit

                                                    ebone.tail.xyz = ebone.head.x, ebone.head.y+0.0127*unit, ebone.head.z


                                        elif not lower_lip:
                                            #Lower lip
                                            if container == 'AU17D' or container == 'AU16' or container == 'AU32':
                                                lower_lip = True
                                                for bone in ['LowerLip_L', 'LowerLip_R']:
                                                    utils.arm.facial_bones.append(bone)

                                                    ebone = armature.data.edit_bones.new(bone)
                                                    ebone.use_deform = False

                                                    if bone == 'LowerLip_L':
                                                        ebone.head.xyz = 0.011679*unit, -0.105113*unit, 1.63996*unit
                                                    elif bone == 'LowerLip_R':
                                                        ebone.head.xyz = -0.011679*unit, -0.105113*unit, 1.63996*unit

                                                    ebone.tail.xyz = ebone.head.x, ebone.head.y+0.0127*unit, ebone.head.z


                                        elif not middle_lip:
                                            #Middle lip
                                            if container == 'AD96L' or container == 'AD96R':
                                                middle_lip = True
                                                for bone in ['MiddleLip']:
                                                    utils.arm.facial_bones.append(bone)

                                                    ebone = armature.data.edit_bones.new(bone)
                                                    ebone.use_deform = False

                                                    ebone.head.xyz = 0, -0.111926*unit, 1.64726*unit
                                                    ebone.tail.xyz = ebone.head.x, ebone.head.y+0.0127*unit, ebone.head.z

                                if cat == 'chin':
                                    if container:
                                        if not chin:
                                            chin = True
                                            for bone in ['Chin']:
                                                utils.arm.facial_bones.append(bone)

                                                ebone = armature.data.edit_bones.new(bone)
                                                ebone.use_deform = False
                                            
                                                ebone.head.xyz = 0, -0.109493*unit, 1.59616*unit
                                                ebone.tail.xyz = ebone.head.x, -0.097449*unit, 1.60015*unit

                                                ebone.length = 0.0127*unit

                eyes = []
                utils.arm.eyes_material = []

                for material in vatproperties.target_object.data.materials:
                    if material.name.casefold().count('eyeball_l'):
                        eyes.append('EyeLeft')
                        utils.arm.eyes_material.append(material)
                    elif material.name.casefold().count('eyeball_r'):
                        eyes.append('EyeRight')
                        utils.arm.eyes_material.append(material)
                    
                if eyes:
                    for bone in eyes:
                        utils.arm.facial_bones.append(bone)

                        ebone = armature.data.edit_bones.new(bone)
                        ebone.use_deform = False

                        if bone == 'EyeLeft':
                            ebone.head.xyz = 0.030171*unit, -0.16976*unit, 1.7222*unit
                        elif bone == 'EyeRight':
                            ebone.head.xyz = -0.030171*unit, -0.16976*unit, 1.7222*unit

                        ebone.tail.xyz = ebone.head.x, ebone.head.y+0.0127*unit, ebone.head.z

            #Checks how many spine bones there are for the spines.basic_spine Rigify parameter (At least 3 are required)
            spines = 0

            for container, bone in utils.arm.central_bones.items():
                if container.count('spine'):
                    if bone:
                        spines += 1

            #Creates 2 pelvis bones for whatever Rigify does with em
            rigify_pelvis = ['Pelvis_L', 'Pelvis_R']

            if spines > 2:
                if utils.arm.central_bones['pelvis']:
                    if utils.arm.viewmodel:
                        prefix = Prefixes.other
                    else:
                        prefix = utils.arm.prefix

                    ppelvis = armature.pose.bones[prefix + utils.arm.central_bones['pelvis'][0]]
                    epelvis = armature.data.edit_bones[prefix + utils.arm.central_bones['pelvis'][0]]
                    
                    for index, bone in enumerate(rigify_pelvis):
                        ebone = armature.data.edit_bones.new(bone)

                        ebone.head = epelvis.head
                        ebone.parent = epelvis
                        ebone.layers[3] = True
                        ebone.layers[0] = False
                        ebone.layers[8] = False
                        ebone.layers[9] = False

                        #New pelvis bone positioning
                        if index == 0:
                            ebone.tail.xyz = 0.097327*unit, -0.078756*unit, 1.09493*unit
                        elif index == 1:
                            ebone.tail.xyz = -0.097327*unit, -0.078756*unit, 1.09493*unit
                
            prefix = utils.arm.prefix

            #Creates multiple palm bones for fingers
            rigify_palm = {'finger1': [], 'finger2': [], 'finger3': [], 'finger4': []}

            #How many finger roots there are (There must be at least 2 for palm bones)
            fingers = 0

            for container, bone in utils.arm.symmetrical_bones['fingers'].items():
                if container == 'finger1' or container == 'finger2' or container == 'finger3' or container == 'finger3' or container == 'finger4':
                    if bone:
                        fingers += 1
            
            if fingers > 1:
                for container, bone in utils.arm.symmetrical_bones['fingers'].items():
                    if container == 'finger1' or container == 'finger2' or container == 'finger3' or container == 'finger3' or container == 'finger4':
                        for index, bone in enumerate(bone):
                            if bone:
                                if vatinfo.scheme == 0:
                                    bone2 = bone_rename(1, bone, index)
                                    palm = 'Palm_' + bone2
                                else:
                                    palm = 'Palm_' + bone
                                efinger = armature.data.edit_bones[prefix + bone]
                                epalm = armature.data.edit_bones.new(palm)
                                rigify_palm[container].append(palm)
                                efinger.layers[5] = True
                                efinger.layers[0] = False
                                epalm.layers[5] = True
                                epalm.layers[0] = False
                                epalm.layers[8] = False

                                efinger.parent = epalm

                                if utils.arm.symmetrical_bones['arms']['hand'] and utils.arm.symmetrical_bones['arms']['hand'][index]:
                                    ehand = armature.data.edit_bones[prefix + utils.arm.symmetrical_bones['arms']['hand'][index]]
                                    phand = armature.pose.bones[prefix + utils.arm.symmetrical_bones['arms']['hand'][index]]

                                    epalm.parent = ehand
                                    epalm.tail = efinger.head
                                    epalm.head.xyz = ehand.head.x, epalm.tail.y, ehand.head.z

            #Creates heels for easier leg tweaking
            rigify_heel = ['Heel_L', 'Heel_R']

            #Creates heel bone if none are present
            rigify_toe = ['Toe_L', 'Toe_R']

            if utils.arm.symmetrical_bones['legs']['foot']:
                for index, bone in enumerate(utils.arm.symmetrical_bones['legs']['foot']):
                    pfoot = armature.pose.bones[prefix + utils.arm.symmetrical_bones['legs']['foot'][index]]
                    efoot = armature.data.edit_bones[prefix + utils.arm.symmetrical_bones['legs']['foot'][index]]

                    ebone = armature.data.edit_bones.new(rigify_heel[index])
                    ebone.tail.xyz = pfoot.head.x/0.6, pfoot.head.y/0.4, 0
                    ebone.head.xyz = pfoot.head.x/3, pfoot.head.y/0.4, 0
                    ebone.parent = efoot

                    if index == 0:
                        ebone.layers[13] = True
                    elif index == 1:
                        ebone.layers[16] = True

                    ebone.layers[0] = False
                    ebone.layers[8] = False

                    if not utils.arm.symmetrical_bones['legs']['toe0']:
                        ebone = armature.data.edit_bones.new(rigify_toe[index])

                        ebone.head = pfoot.tail
                        if pfoot.tail.y < 0:
                            ebone.tail.xyz = pfoot.tail.x, pfoot.tail.y*1.25, pfoot.tail.z
                        elif pfoot.tail.y > 0:
                            ebone.tail.xyz = pfoot.tail.x, pfoot.tail.y*-1.25, pfoot.tail.z

                        ebone.parent = efoot
                        ebone.use_connect = True

                        if index == 0:
                            ebone.layers[13] = True
                        elif index == 1:
                            ebone.layers[16] = True

                        ebone.layers[0] = False
                        ebone.layers[8] = False

            #Creates hand bones 
            rigify_hands = ['Hand_L', 'Hand_R']

            if utils.arm.symmetrical_bones['arms']['forearm']:
                for index, bone in enumerate(utils.arm.symmetrical_bones['arms']['forearm']):
                    pforearm = armature.pose.bones[prefix + bone]
                    eforearm = armature.data.edit_bones[prefix + bone]

                    if not utils.arm.symmetrical_bones['arms']['hand'] or not utils.arm.symmetrical_bones['arms']['hand'][index]:
                        ebone = armature.data.edit_bones.new(rigify_hands[index])

                        ebone.head = eforearm.tail
                        length = eforearm.length
                        eforearm.length = eforearm.length*1.4
                        ebone.tail = eforearm.tail

                        eforearm.length = length

                        ebone.parent = eforearm
                        ebone.use_connect = True
            
            prefix = Prefixes.other

            #Creates camera target if armature is a viewmodel
            if utils.arm.viewmodel:
                if utils.arm.other_bones['viewmodel']:
                    for bone in utils.arm.other_bones['viewmodel']:
                        if bone == 'Camera':
                            pcamera = armature.pose.bones[prefix + bone]
                            etarget = armature.data.edit_bones.new('Camera_Target')
                            prefix = utils.arm.prefix
    
                            ppelvis = armature.pose.bones[prefix + utils.arm.central_bones['pelvis'][0]]
                            etarget.head.xyz = pcamera.head.x, -ppelvis.head.z, pcamera.head.z
                            etarget.tail.xyz = etarget.head.x, etarget.head.y*1.5, etarget.head.z
                            etarget.length = 2

            prefix = utils.arm.prefix

            update(0)

            #Parent and rigify parameters

            #Facial drivers
            if vatproperties.target_object:
                for bone in utils.arm.facial_bones:
                    pbone = armature.pose.bones[bone]
                    ebone = armature.data.edit_bones[bone]

                    pbone.rigify_type = 'basic.raw_copy'
                    ebone.layers[0] = True
                    ebone.parent = armature.data.edit_bones[prefix + utils.arm.central_bones['head'][0]]

                    #Locks rotation and scale since they aren't meant to be used
                    pbone.lock_rotation_w = True
                    pbone.lock_rotation[0] = True
                    pbone.lock_rotation[1] = True
                    pbone.lock_rotation[2] = True

                    pbone.lock_scale[0] = True
                    pbone.lock_scale[1] = True
                    pbone.lock_scale[2] = True

                    if utils.arm.central_bones['pelvis']:
                        prefix = utils.arm.prefix
                        ppelvis = armature.pose.bones[prefix + utils.arm.central_bones['pelvis'][0]]
                        #Equivalent to 1 meter relative to the pelvis location in order to maintain consistency between different scales
                        unit = ppelvis.head.z*0.02609761
                        #Unit change, relative to the size it would be if imported from Blender Source Tools (For the sake of readability, and my patience)

                    #Locks axis locations for bones who don't need it
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
                        limit_loc.min_x = -0.5*unit

                    elif bone == 'Nostril_L':
                        limit_loc.min_x = 0

                    elif bone == 'Nostril_R':
                        limit_loc.min_x = -0.5*unit

                    elif bone == 'EyeLeft' or bone == 'EyeRight':
                        limit_loc.min_x = -4*unit

                    else:
                        limit_loc.min_x = -1*unit

                    #Max X
                    limit_loc.use_max_x = True
                    if bone.count('MouthCorner') or bone == 'Nostril_L':
                        limit_loc.max_x = 0.5*unit

                    elif bone == 'Nostril_R':
                        limit_loc.max_x = 0

                    elif bone == 'EyeLeft' or bone == 'EyeRight':
                        limit_loc.max_x = 4*unit

                    else:
                        limit_loc.max_x = 1*unit

                    #Min Y
                    limit_loc.use_min_y = True
                    if bone.count('Cheek'):
                        limit_loc.min_y = -1*unit

                    elif bone.count('MiddleLip') or bone.count('LowerLip'):
                        limit_loc.min_y = -0.5*unit

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
                        limit_loc.min_z = -0.2*unit

                    elif bone.count('Eyebrow') or bone.count('LowerLip') or bone.count('MouthCorner'):
                        limit_loc.min_z = -0.5*unit

                    elif bone.count('Chin'):
                        limit_loc.min_z = -1.5*unit
                        
                    elif bone == 'EyeLeft' or bone == 'EyeRight':
                        limit_loc.min_z = -4*unit

                    else:
                        limit_loc.min_z = -1*unit

                    #Max Z
                    limit_loc.use_max_z = True

                    if bone.count('UpperEye') or bone.count('LowerEye'):
                        limit_loc.max_z = 0.2*unit

                    elif bone.count('Eyebrow') or bone.count('UpperLip') or bone.count('MouthCorner') or bone.count('Nostril') or bone.count('LowerLip'):
                        limit_loc.max_z = 0.5*unit

                    elif bone == 'EyeLeft' or bone == 'EyeRight':
                        limit_loc.max_z = 4*unit

                    else:
                        limit_loc.max_z = 1*unit

                    #Assings Widgets to bone drivers
                    if bone.count('Eyebrow') or bone.count('UpperEye') or bone.count('LowerEye'):
                        widget = bpy.data.objects['UpDown']
                        pbone.custom_shape = widget
                        
                        if bone.count('Eyebrow'):
                            pbone.custom_shape_scale = 0.3

                        elif bone.count('UpperEye') or bone.count('LowerEye'):
                            pbone.custom_shape_scale = 0.25

                        ebone.layers[1] = True
                        ebone.layers[0] = False

                    elif bone.count('Cheek'):
                        widget = bpy.data.objects['Cheek']
                        pbone.custom_shape = widget

                        pbone.custom_shape_scale = 0.5

                        ebone.layers[1] = True
                        ebone.layers[0] = False

                    elif bone.count('Nostril'):
                        if bone.endswith('_L'):
                            widget = bpy.data.objects['Nostril_L']

                        elif bone.endswith('_R'):
                            widget = bpy.data.objects['Nostril_R']
                            
                        pbone.custom_shape = widget
                        pbone.custom_shape_scale = 0.35

                        ebone.layers[1] = True
                        ebone.layers[0] = False

                    elif bone.count('UpperLip'):
                        widget = bpy.data.objects['UpperLip']
                        pbone.custom_shape = widget
                        pbone.custom_shape_scale = 0.25

                        ebone.layers[1] = True
                        ebone.layers[0] = False

                    elif bone.count('MiddleLip'):
                        widget = bpy.data.objects['MiddleLip']
                        pbone.custom_shape = widget
                        pbone.custom_shape_scale = 0.35

                        ebone.layers[1] = True
                        ebone.layers[0] = False

                    elif bone.count('LowerLip'):
                        widget = bpy.data.objects['LowerLip']
                        pbone.custom_shape = widget
                        pbone.custom_shape_scale = 0.25

                        ebone.layers[1] = True
                        ebone.layers[0] = False

                    elif bone.count('Chin'):
                        widget = bpy.data.objects['4Directions']
                        pbone.custom_shape = widget
                        pbone.custom_shape_scale = 0.7

                        ebone.layers[1] = True
                        ebone.layers[0] = False

                    elif bone.count('MouthCorner'):
                        widget = bpy.data.objects['4Directions']
                        pbone.custom_shape = widget
                        pbone.custom_shape_scale = 0.4

                        ebone.layers[1] = True
                        ebone.layers[0] = False

                    elif bone == 'EyeLeft' or bone == 'EyeRight':
                        widget = bpy.data.objects['Circle']
                        pbone.custom_shape = widget
                        pbone.custom_shape_scale = 1.5
                        
                        ebone.layers[1] = True
                        ebone.layers[0] = False

                    if bone.count('Inner_Eyebrow') or bone.count('Outer_Eyebrow') or bone.count('Nostril') or bone.count('Cheek') or bone.count('MiddleLip'):
                        ebone.layers[2] = True
                        ebone.layers[0] = False

                    ebone.layers[8] = False
                    ebone.layers[9] = False

            if spines > 2:
                #Rigify pelvis
                if utils.arm.central_bones['pelvis']:
                    for bone in rigify_pelvis:
                        pbone = armature.pose.bones[bone]
                        pbone.rigify_type = 'basic.super_copy'
                        pbone.rigify_parameters.make_control = False
                
            #Rigify palm
            for bone in rigify_palm['finger1']:
                pbone = armature.pose.bones[bone]
                pbone.rigify_type = 'limbs.super_palm'

            #For reference:
            #Face (Primary) = Layer 0
            #Face (Secondary) = Layer 1
            #Central bones + Clavicle = Layer 3
            #Finger = Layer 5
            #Left arm = Layer 7
            #Right arm = Layer 10
            #Left leg = Layer 13
            #Right leg = Layer 16

            #Symmetrical
            for cat in utils.arm.symmetrical_bones.keys():
                if cat == 'fingers':
                    for container, bone in utils.arm.symmetrical_bones[cat].items():
                        for bone in bone:
                            if bone:
                                if container == 'finger0' or container == 'finger1' or container == 'finger2' or container == 'finger3' or container == 'finger4':
                                    pbone = armature.pose.bones[prefix + bone]
                                    param = pbone.rigify_parameters
                                    ebone = armature.data.edit_bones[prefix + bone]

                                    pbone.rigify_type = 'limbs.super_finger'
                                    param.make_extra_ik_control = True
                                    param.tweak_layers[6] = True
                                    param.tweak_layers[1] = False

                                    ebone.layers[5] = True
                                    ebone.layers[0] = False
                                    ebone.layers[1] = False
                                    ebone.layers[2] = False
                                else:
                                    ebone = armature.data.edit_bones[prefix + bone]

                                    ebone.layers[5] = True
                                    ebone.layers[0] = False
                                    ebone.layers[1] = False
                                    ebone.layers[2] = False
                elif cat == 'arms':
                    for container, bone in utils.arm.symmetrical_bones[cat].items():
                        for index, bone in enumerate(bone):
                            if bone:
                                pbone = armature.pose.bones[prefix + bone]
                                param = pbone.rigify_parameters
                                ebone = armature.data.edit_bones[prefix + bone]

                                if index == 0:
                                    ebone.layers[7] = True
                                elif index == 1:
                                    ebone.layers[10] = True

                                if container == 'clavicle':
                                    pbone.rigify_type = 'basic.super_copy'
                                    param.make_widget = False
                                    if not utils.arm.viewmodel:
                                        ebone.layers[3] = True
                                elif container == 'upperarm':
                                    pbone.rigify_type = 'limbs.super_limb'
                                    param.tweak_layers[1] = False
                                    param.fk_layers[1] = False

                                    if index == 0:
                                        param.fk_layers[8] = True
                                        param.tweak_layers[9] = True
                                    elif index == 1:
                                        param.fk_layers[11] = True
                                        param.tweak_layers[12] = True

                                    param.segments = 1

                                ebone.layers[0] = False
                                ebone.layers[1] = False
                                ebone.layers[2] = False

                elif cat == 'legs':
                    for container, bone in utils.arm.symmetrical_bones[cat].items():
                        for index, bone in enumerate(bone):
                            if bone:
                                pbone = armature.pose.bones[prefix + bone]
                                param = pbone.rigify_parameters
                                ebone = armature.data.edit_bones[prefix + bone]

                                if index == 0:
                                    ebone.layers[13] = True
                                elif index == 1:
                                    ebone.layers[16] = True

                                if container == 'thigh':
                                    if utils.arm.symmetrical_bones['legs']['calf'] and utils.arm.symmetrical_bones['legs']['foot']:
                                        pbone.rigify_type = 'limbs.super_limb'
                                        param.limb_type = 'leg'
                                        param.tweak_layers[1] = False
                                        param.fk_layers[1] = False
                                    else:
                                        pbone.rigify_type = 'basic.copy_chain'

                                    if index == 0:
                                        param.fk_layers[14] = True
                                        param.tweak_layers[15] = True
                                    elif index == 1:
                                        param.fk_layers[17] = True
                                        param.tweak_layers[18] = True
                                    param.segments = 1

                                ebone.layers[0] = False
                                ebone.layers[3] = False
                                ebone.layers[4] = False

            #Central
            for container, bone in utils.arm.central_bones.items():
                for bone in bone:
                    if bone:
                        if bone == 'Bip01' and utils.arm.viewmodel:
                            prefix = Prefixes.other
                        else:
                            prefix = utils.arm.prefix

                        pbone = armature.pose.bones[prefix + bone]
                        param = pbone.rigify_parameters
                        ebone = armature.data.edit_bones[prefix + bone]

                        ebone.layers[3] = True

                        if container == 'pelvis':
                            if not utils.arm.viewmodel:
                                if spines > 2 :
                                    pbone.rigify_type = 'spines.basic_spine'
                                    param.pivot_pos = 2
                                    param.tweak_layers[1] = False
                                    param.tweak_layers[4] = True
                                    param.fk_layers[1] = False
                                    param.fk_layers[4] = True
                                else:
                                    pbone.rigify_type = 'basic.copy_chain'

                        elif container == 'neck':
                            if utils.arm.central_bones['head']:
                                pbone.rigify_type = 'spines.super_head'
                                param.connect_chain = True
                                param.tweak_layers[1] = False
                                param.tweak_layers[4] = True
                            else:
                                pbone.rigify_type = 'basic.super_copy'
                    
                        ebone.layers[0] = False

            prefix = Prefixes.other

            for container, bone in utils.arm.other_bones.items():
                if container == 'weapon':
                    for bone in bone:
                        if bone:
                            pbone = armature.pose.bones[prefix + bone]
                            param = pbone.rigify_parameters
                            ebone = armature.data.edit_bones[prefix + bone]

                            ebone.layers[20] = True

                            ebone.layers[0] = False
                            ebone.layers[7] = False

                            pbone.rigify_type = 'basic.super_copy'
                            param.super_copy_widget_type = 'bone'
                elif container == 'attachment':
                    prefix = Prefixes.attachment
                    for bone in bone:
                        if bone:
                            if bone.startswith('a.'):
                                prefix = Prefixes.attachment
                                bone = bone.replace('a.', '')
                            elif bone.startswith('a2.'):
                                prefix = Prefixes.other
                                bone = bone.replace('a2.', '')

                            pbone = armature.pose.bones[prefix + bone]
                            param = pbone.rigify_parameters
                            ebone = armature.data.edit_bones[prefix + bone]

                            ebone.layers[19] = True

                            ebone.layers[0] = False
                            ebone.layers[7] = False

                            pbone.rigify_type = 'basic.super_copy'
                            param.super_copy_widget_type = 'bone'
                    
                            
            if utils.arm.viewmodel:
                if utils.arm.other_bones['viewmodel']:
                    for bone in bone:
                        if bone == 'Camera':
                            pbone = armature.pose.bones[prefix + bone]
                            param = pbone.rigify_parameters
                            ebone = armature.data.edit_bones[prefix + bone]

                            ebone.layers[21] = True

                            ebone.layers[0] = False
                            ebone.layers[8] = False

                            pbone.rigify_type = 'basic.super_copy'
                            param.super_copy_widget_type = 'bone'
                            break

                    etarget = armature.data.edit_bones['Camera_Target']
                    ptarget = armature.pose.bones['Camera_Target']
                    param = ptarget.rigify_parameters

                    ptarget.rigify_type = 'basic.super_copy'
                    param.super_copy_widget_type = 'circle'

                    ptarget.lock_location[1] = True
                    ptarget.lock_rotation[0] = True
                    ptarget.lock_rotation[2] = True

                    etarget.layers[21] = True
                    etarget.layers[0] = False
                    etarget.layers[7] = False
                    etarget.layers[8] = False

            #Custom bones
            for container, bone in utils.arm.custom_bones.items():
                for bone in bone:
                    if bone:
                        if bone.startswith('s.'):
                            bone = utils.arm.prefix + bone.replace('s.', '')
                        elif bone.startswith('s3.'):
                            bone = Prefixes.other + bone.replace('s3.', '')

                        ebone = armature.data.edit_bones[bone]
                        pbone = armature.pose.bones[bone]
                        param = pbone.rigify_parameters

                        ebone.layers[22] = True
                        
                        ebone.layers[0] = False
                        ebone.layers[9] = False

                        pbone.rigify_type = 'basic.super_copy'
                        param.super_copy_widget_type = 'bone'

            armature = utils.arm.animation_armature_real

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
            names = ['Face', 'Face (Primary)','Face (Secondary)','Torso', 'Torso (Tweak)', 'Fingers', 'Fingers (Detail)', 'Arm.L (IK)', 'Arm.L (FK)', 'Arm.L (Tweak)', 'Arm.R (IK)', 'Arm.R (FK)', 'Arm.R (Tweak)', 'Leg.L (IK)', 'Leg.L (FK)', 'Leg.L (Tweak)', 'Leg.R (IK)', 'Leg.R (FK)', 'Leg.R (Tweak)', 'Attachments', 'Weapon', 'Others', 'Custom Bones']

            row_groups = [1,2,2,3,4,5,6,7,8,9,7,8,9,10,11,12,10,11,12,13,13,14,14]

            layer_groups = [5,2,3,3,4,6,5,2,5,4,2,5,4,2,5,4,2,5,4,6,6,6,6]

            for i, name, row, group in zip(range(22), names, row_groups, layer_groups):
                armature.rigify_layers[i].name = name
                armature.rigify_layers[i].row = row
                armature.rigify_layers[i]['group_prop'] = group

            armature.rigify_layers[28].name = 'Root'
            armature.rigify_layers[28].row = 14
            armature.rigify_layers[28]['group_prop'] = 1

            armature.layers[0] = False

            vatinfo.animation_armature_setup = True

            for i in [0,1,3,5,7,10,13,16,19,20]:
                    armature.layers[i] = True

            bpy.ops.object.mode_set(mode='OBJECT')

            #Renames armature to allow it being compatible with pose symmetry
            if vatinfo.scheme == 0:
                armature_rename(1, utils.arm.animation_armature)

            print("Animation armature created!")

        elif action == 1:
            #Deletes Left/Right vertex groups if present
            if vatproperties.target_object:
                print(vatproperties.target_object.data.name)
                data = vatproperties.target_object.data.name.replace('.anim', '')
                print(data)
                data = bpy.data.meshes[data]
                vatproperties.target_object.data = data

            print("Animation armature deleted")
                
    def link(): #Organizes armature after empty creation

        def retarget(bone): #Creates empties and links them to Rigify armature/Source armature
            armature = bpy.data.objects['rig']
            
            #Retarget empties creation
            try:
                collection = bpy.data.collections["Retarget Empties ({})".format(utils.arm.armature.name)[0:60]] #Name length limit
            except:
                collection = bpy.data.collections.new("Retarget Empties ({})".format(utils.arm.armature.name)[0:60])
                bpy.context.scene.collection.children.link(collection)

            collection.hide_viewport = True

            #Creates base empty and links
            base = bpy.data.objects.new('base_{} ({})'.format(bone, utils.arm.armature.name)[0:60], None)
            collection.objects.link(base)
            base.empty_display_type = 'CUBE'
            base.hide_select = True

            #Location constraint
            loc = base.constraints.new('COPY_LOCATION')
            loc.target = armature
            loc.subtarget = 'ORG-' + prefix + bone + '.isolated'

            #Rotation constraint
            rot = base.constraints.new('COPY_ROTATION')
            rot.target = armature
            rot.subtarget = 'ORG-' + prefix + bone + '.isolated'

            #Creates target empty and links
            target = bpy.data.objects.new('target_{} ({})'.format(bone, utils.arm.armature.name)[0:60], None)
            collection.objects.link(target)
            target.empty_display_type = 'SPHERE'

            #Parent to base
            base.parent = parent
            target.parent = base

            #Bone connection
            armature = utils.arm.armature
            loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')
            loc.name = "Retarget Location"
            loc.target = target
            rot = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')
            rot.name = "Retarget Rotation"
            rot.target = target

        #Creates parent for all bases for easier storage/manipulation
        parent = bpy.data.objects.new('parent_' + utils.arm.armature.name, None)

        prefix = utils.arm.prefix

        for cat in utils.arm.symmetrical_bones:
            for container, bone in utils.arm.symmetrical_bones[cat].items():
                for bone in bone:
                    if bone:
                        retarget(bone)

        for container, bone in utils.arm.central_bones.items():
            for bone in bone:
                if bone:
                    if bone == 'Bip01' and utils.arm.viewmodel:
                        prefix = Prefixes.other
                    else:
                        prefix = utils.arm.prefix

                    retarget(bone)

        prefix = Prefixes.other

        for container, bone in utils.arm.other_bones.items():
            if container == 'weapon':
                for bone in bone:
                    if bone:
                        retarget(bone)
            elif container == 'viewmodel':
                for bone in bone:
                    if bone == 'Camera' or bone == 'Bip01':
                        retarget(bone)

        prefix = ''

        for container, bone in utils.arm.custom_bones.items():
            for bone in bone:
                if bone:
                    if bone.startswith('s.'):
                        bone = utils.arm.prefix + bone.replace('s.', '')
                    elif bone.startswith('s3.'):
                        bone = Prefixes.other + bone.replace('s3.', '')
                    retarget(bone)

        #Creates additional location constraints for helper bones to copy their driver bone's location
        for cat in utils.arm.helper_bones.keys():
            if cat == 'legs' or cat == 'arms':
                for container, bone in utils.arm.helper_bones[cat].items():
                    if container == 'knee' or container == 'elbow':
                        for index, bone in enumerate(bone):
                            if bone:
                                prefix, bone = helper_convert(bone)
                                armature = utils.arm.armature
                                loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')
                                loc.name = "Retarget Location"

                                if container == 'knee':
                                    loc.target = bpy.data.objects['target_{} ({})'.format(utils.arm.symmetrical_bones['legs']['calf'][index], utils.arm.armature.name)[0:60]]
                                elif container == 'elbow':
                                    loc.target = bpy.data.objects['target_{} ({})'.format(utils.arm.symmetrical_bones['arms']['forearm'][index], utils.arm.armature.name)[0:60]]

        prefix = utils.arm.prefix

        #Connects parent to collection
        collection = bpy.data.collections["Retarget Empties ({})".format(utils.arm.armature.name)[0:60]]
        collection.objects.link(parent)

        #Forces Rigify armature to use setup armature's scale
        scale = utils.arm.animation_armature.scale

        #Renames armature to prior generated armature
        armature = bpy.data.objects['rig']
        armature.name = utils.arm.armature.name + '.anim'
        armature.data.name = utils.arm.armature_real.name + '.anim'
        armature.scale = scale

        utils.update(1, armature)

        #Parents isolated bones
        for cat in utils.arm.symmetrical_bones.keys():
            for container, bone in utils.arm.symmetrical_bones[cat].items():
                for bone in bone:
                    if bone:
                        armature.data.edit_bones['ORG-' + prefix + bone + '.isolated'].parent = armature.data.edit_bones['DEF-' + prefix + bone]

        #Deletes generated armature
        generate_armature('anim', 2)

        #Creates camera at camera bone if armature is a viewmodel
        if utils.arm.viewmodel:
            if utils.arm.other_bones['viewmodel']:
                camera_data = bpy.data.cameras.new('viewmodel_camera')
                camera = bpy.data.objects.new('viewmodel_camera', camera_data)
                prefix = Prefixes.other

                camera.data.angle = 0.942478
                camera.rotation_euler[0] = math.radians(-90)
                camera.rotation_euler[1] = math.radians(180)

                loc = camera.constraints.new('COPY_LOCATION')
                loc.target = utils.arm.armature
                loc.subtarget = prefix + 'Camera'
                rot = camera.constraints.new('COPY_ROTATION')
                rot.target = utils.arm.armature
                rot.subtarget = prefix + 'Camera'
                rot.invert_x = True
                rot.invert_z = True
                rot.target_space = 'LOCAL'
                rot.owner_space = 'LOCAL'

                try:
                    collection = bpy.data.collections['Animation Armature']
                    collection.objects.link(camera)
                except:
                    pass

                prefix = Prefixes.other

                for bone in utils.arm.other_bones['viewmodel']:
                    if bone == 'Camera':
                        pcamera = armature.pose.bones[prefix + bone]
                        ecamera = armature.data.edit_bones[prefix + bone]
                        
                        track = pcamera.constraints.new('DAMPED_TRACK')
                        track.target = armature
                        track.subtarget = 'Camera_Target'
                        track.track_axis = 'TRACK_Z'

                        rot = pcamera.constraints.new('COPY_ROTATION')
                        rot.target = armature
                        rot.subtarget = 'Camera_Target'
                        rot.use_x = False
                        rot.use_z = False
                        rot.invert_y = True
                        rot.target_space = 'LOCAL'

                        etarget = armature.data.edit_bones['Camera_Target']

                        ecamera.parent = None
                        etarget.parent = None

                        #Relocates the position of the camera to where it would be in game
                        if ecamera.head.z >= 0.25:
                            armature.pose.bones[prefix + bone].location[1] = -ecamera.head.z
                            armature.pose.bones['Camera_Target'].location[2] = -ecamera.head.z
                            armature.pose.bones[prefix + bone].location[2] = -ecamera.head.z*0.0713206

                            armature.pose.bones['root'].location[2] = -ecamera.head.z
                
        vatinfo.animation_armature = True
        vatinfo.animation_armature_setup = False
        utils.arm.animation_armature = armature
        utils.arm.animation_armature_real = armature.data

    def face_flex_setup(): #Sets up drivers for face flexes that will be controlled by face bones
        prefix = utils.arm.prefix
        
        if utils.arm.shapekeys:
            keyblocks = vatproperties.target_object.data.shape_keys.key_blocks

            #Vertex group creation

            #Creates vertex groups
            left_group = vatproperties.target_object.vertex_groups.new(name='Left')
            right_group = vatproperties.target_object.vertex_groups.new(name='Right')
            print('second?')

            #Left side
            for vertex in vatproperties.target_object.data.vertices:
                #Left side
                if vertex.co[0] > 0.005:
                    left_group.add([vertex.index], 1, 'REPLACE')

                #Right side
                elif vertex.co[0] < -0.005:
                    right_group.add([vertex.index], 1, 'REPLACE')

                elif vertex.co[0] <0.005 >-0.005:
                    left_group.add([vertex.index], 0.5, 'REPLACE')
                    right_group.add([vertex.index], 0.5, 'REPLACE')

            del vertex

            #Still need to add center vertices to both groups, will do once i figure out

            #Shapekey creation
            utils.arm.rigify_shapekeys = {'basis': {'basis': ''}, 'eyebrows': {'AU1': [], 'AU2': [], 'AU4': [], 'AU1AU2': [], 'AU1AU4': [], 'AU2AU4': []}, 'eyes': {'f01': [], 'f02': [], 'f03': [], 'f04': [], 'AU42': []}, 'cheek': {'AU6Z': [], 'AU13': []}, 'nose': {'AU9': [], 'AU38': []}, 'mouth': {'AU12': [], 'AU15': [], 'AU10': [], 'AU17D': [], 'AU16': [], 'AU32': [], 'AU24': [], 'AU18Z': [], 'AU22Z': [], 'AD96L': [], 'AD96R': []}, 'chin': {'AU31': [], 'AU26': [], 'AU27': [], 'AU27Z': [], 'AD30L': [], 'AD30R': [], 'AU17': []}}

            #Divides old shapekeys from generated ones
            vatproperties.target_object.shape_key_add(name='----------', from_mix=False)
            vatproperties.target_object.show_only_shape_key = False

            for cat in utils.arm.shapekeys.keys():
                for container, shapekey in utils.arm.shapekeys[cat].items():
                    if shapekey:
                        #Makes sure no other shapekey is active
                        if container != 'basis':
                            keyblocks[shapekey].value = 0

                        #Appends central shapekeys, since they don't need L/R versions of them
                        if container == 'AU17' or container == 'AU26' or container == 'AU27' or container == 'AU27Z' or container == 'AD30L' or container == 'AD30R' or container == 'AU22Z' or container == 'AD96L' or container == 'AD96R':
                            utils.arm.rigify_shapekeys[cat][container].append(shapekey)
                            continue

                        if container != 'basis':
                            keyblocks[shapekey].value = 1
                            left_shapekey = vatproperties.target_object.shape_key_add(name=shapekey + '_L', from_mix=True)
                            right_shapekey = vatproperties.target_object.shape_key_add(name=shapekey + '_R', from_mix=True)

                            utils.arm.rigify_shapekeys[cat][container].append(left_shapekey.name)
                            utils.arm.rigify_shapekeys[cat][container].append(right_shapekey.name)

                            #Assigns shapekeys to group
                            left_shapekey.vertex_group = left_group.name
                            right_shapekey.vertex_group = right_group.name

                            keyblocks[shapekey].value = 0

            #Removes single shapekeys as well as unused shapekeys
                for container, shapekey in utils.arm.shapekeys[cat].items():
                    if shapekey:
                        if container == 'basis' or container == 'AU17' or container == 'AU26' or container == 'AU27' or container == 'AU27Z' or container == 'AD30L' or container == 'AD30R' or container == 'AU22Z' or container == 'AD96L' or container == 'AD96R':
                            continue
                        else:
                            shapekey = vatproperties.target_object.data.shape_keys.key_blocks[shapekey]
                            vatproperties.target_object.shape_key_remove(shapekey)

            for shapekey in utils.arm.unused_shapekeys:
                try:
                    shapekey = vatproperties.target_object.data.shape_keys.key_blocks[shapekey]
                    vatproperties.target_object.shape_key_remove(shapekey)
                except:
                    pass

            del left_shapekey
            del right_shapekey

            for cat in utils.arm.rigify_shapekeys.keys():
                for container, shapekey in utils.arm.rigify_shapekeys[cat].items():
                    for shapekey in shapekey:
                        #Creates driver
                        driver = keyblocks[shapekey].driver_add('value') #Creates new driver for shapekey

                        #Parameters and target
                        variable = driver.driver.variables.new() #Creates new variable onto the shapekey
                        variable.name = "flex"
                        driver.driver.expression = variable.name #Changes expression to created variable's name
                        variable.type = 'TRANSFORMS' #Changes type of variable to transform

                        target = variable.targets[0]
                        target.id = utils.arm.animation_armature #Links variable to animation armature

                        #Specific tweaks for each bone

                        #Eyebrows
                        if cat == 'eyebrows':
                            #AU1 = Inner eyebrow raise
                            #AU2 = Outer eyebrow raise
                            #AU4 = Full eyebrow drop
                            #AU1AU2 = Full eyebrow raise
                            #AU1AU4 = Outer eyebrow drop
                            #AU2AU4 = Inner eyebrow drop

                            target.transform_space = 'LOCAL_SPACE'
                            target.transform_type = 'LOC_Z'

                            if container == 'AU1' or container == 'AU2AU4':
                                if shapekey.endswith('_L'):
                                    target.bone_target = "Inner_Eyebrow_L"
                                elif shapekey.endswith('_R'):
                                    target.bone_target = "Inner_Eyebrow_R"

                            elif container == 'AU2' or container == 'AU1AU4':
                                if shapekey.endswith('_L'):
                                    target.bone_target = "Outer_Eyebrow_L"
                                elif shapekey.endswith('_R'):
                                    target.bone_target = "Outer_Eyebrow_R"

                            elif container == 'AU4' or container == 'AU1AU2':
                                if shapekey.endswith('_L'):
                                    target.bone_target = "Eyebrow_L"
                                elif shapekey.endswith('_R'):
                                    target.bone_target = "Eyebrow_R"

                            if container == 'AU4' or container == 'AU1AU4' or container == 'AU2AU4':
                                driver.modifiers[0].coefficients[1] = -2/unit

                            elif container == 'AU1' or container == 'AU2' or container == 'AU1AU2':
                                driver.modifiers[0].coefficients[1] = 2/unit

                        if cat == 'eyes':
                            #f01 = Upper eyelids close
                            #f02 = Upper eyelids raise
                            #f03 = Lower eyelids drop
                            #f04 = Lower eyelids raise
                            #AU42 = Upper eyelids drop

                            target.transform_space = 'LOCAL_SPACE'
                            target.transform_type = 'LOC_Z'

                            if container == 'AU42':
                                driver.driver.expression = variable.name + '/4'

                            elif container != 'f01':
                                #Creates another driver controlled by the corresponding eye bone
                                variable2 = driver.driver.variables.new()
                                variable2.name = "eye"
                                    
                                driver.driver.expression = variable.name + '+' + variable2.name + '/4' #Combines the old driver with the new driver, making the latter have less influence
                                variable2.type = 'TRANSFORMS'

                                target2 = variable2.targets[0]
                                target2.id = utils.arm.animation_armature

                                target2.transform_space = 'LOCAL_SPACE'
                                target2.transform_type = 'LOC_Z'

                            if container == 'f01':
                                if shapekey.endswith('_L'):
                                    target.bone_target = "UpperEye_L"
                                elif shapekey.endswith('_R'):
                                    target.bone_target = "UpperEye_R"
                            
                            elif container == 'f02':
                                if shapekey.endswith('_L'):
                                    target.bone_target = "UpperEye_L"
                                    target2.bone_target = 'EyeLeft'
                                elif shapekey.endswith('_R'):
                                    target.bone_target = "UpperEye_R"
                                    target2.bone_target = 'EyeRight'

                            elif container == 'f03' or container == 'f04':
                                if shapekey.endswith('_L'):
                                    target.bone_target = "LowerEye_L"
                                    target2.bone_target = 'EyeLeft'
                                elif shapekey.endswith('_R'):
                                    target.bone_target = "LowerEye_R"
                                    target2.bone_target = 'EyeRight'

                            elif container == 'AU42':
                                if shapekey.endswith('_L'):
                                    target.bone_target = 'EyeLeft'
                                elif shapekey.endswith('_R'):
                                    target.bone_target = 'EyeRight'
                            
                            if container == 'f01' or container == 'f03' or container == 'AU42':
                                driver.modifiers[0].coefficients[1] = -5/unit
                            
                            elif container == 'f02' or container == 'f04':
                                driver.modifiers[0].coefficients[1] = 5/unit

                        if cat == 'cheek':
                            #AU6Z = Squint
                            #AU13 = Filling cheek with air

                            target.transform_space = 'LOCAL_SPACE'

                            if shapekey.endswith('_L'):
                                target.bone_target = "Cheek_L"
                            elif shapekey.endswith('_R'):
                                target.bone_target = "Cheek_R"

                            if container == 'AU6Z':
                                target.transform_type = 'LOC_Z'
                                driver.modifiers[0].coefficients[1] = 1/unit

                            elif container == 'AU13':
                                target.transform_type = 'LOC_Y'
                                driver.modifiers[0].coefficients[1] = -1/unit

                        elif cat == 'nose':
                            #AU9 = Nostril raise
                            #AU38 = Breath

                            target.transform_space = 'LOCAL_SPACE'

                            if shapekey.endswith('_L'):
                                target.bone_target = "Nostril_L"
                            elif shapekey.endswith('_R'):
                                target.bone_target = "Nostril_R"

                            if container == 'AU9':
                                target.transform_type = 'LOC_Z'
                                driver.modifiers[0].coefficients[1] = 2/unit

                            elif container == 'AU38':
                                target.transform_type = 'LOC_X'

                                if shapekey.endswith('_L'):
                                    driver.modifiers[0].coefficients[1] = 2/unit

                                elif shapekey.endswith('_R'):
                                    driver.modifiers[0].coefficients[1] = -2/unit

                        if cat == 'mouth':
                            #Mouth corners
                            #AU12 = Smile
                            #AU15 = Frown
                            #AU24 = Tightener
                            #AU18Z = Puckering

                            #Upper lips
                            #AU10 = Upper lip raise

                            #Lower lips
                            #AU17D = Lower lip raise
                            #AU16 = Lower lip drop
                            #AU32 = Bite

                            target.transform_space = 'LOCAL_SPACE'

                            #Mouth corners
                            if container == 'AU12' or container == 'AU15' or container == 'AU24' or container == 'AU18Z':
                                if shapekey.endswith('_L'):
                                    target.bone_target = "MouthCorner_L"
                                elif shapekey.endswith('_R'):
                                    target.bone_target = "MouthCorner_R"

                                if container == 'AU12' or container == 'AU15':
                                    target.transform_type = 'LOC_Z'

                                    if container == 'AU12':
                                        driver.modifiers[0].coefficients[1] = 2/unit

                                    elif container == 'AU15':
                                        driver.modifiers[0].coefficients[1] = -2/unit

                                elif container == 'AU24' or container == 'AU18Z':
                                    target.transform_type = 'LOC_X'

                                    if container == 'AU24':
                                        if shapekey.endswith('_L'):
                                            driver.modifiers[0].coefficients[1] = 2/unit
                                        elif shapekey.endswith('_R'):
                                            driver.modifiers[0].coefficients[1] = -2/unit
                                    
                                    elif container == 'AU18Z':
                                        if shapekey.endswith('_L'):
                                            driver.modifiers[0].coefficients[1] = -2/unit
                                        elif shapekey.endswith('_R'):
                                            driver.modifiers[0].coefficients[1] = 2/unit

                            #Upper lips
                            elif container == 'AU10':
                                target.transform_type = 'LOC_Z'
                                target.transform_space = 'LOCAL_SPACE'

                                if shapekey.endswith('_L'):
                                    target.bone_target = "UpperLip_L"
                                elif shapekey.endswith('_R'):
                                    target.bone_target = "UpperLip_R"

                                driver.modifiers[0].coefficients[1] = 2/unit

                            #Lower lips
                            elif container == 'AU17D' or container == 'AU16' or container == 'AU32':
                                target.transform_space = 'LOCAL_SPACE'

                                if shapekey.endswith('_L'):
                                    target.bone_target = "LowerLip_L"
                                elif shapekey.endswith('_R'):
                                    target.bone_target = "LowerLip_R"

                                if container == 'AU17D' or container == 'AU16':
                                    target.transform_type = 'LOC_Z'

                                    if container == 'AU16':
                                        driver.modifiers[0].coefficients[1] = -3/unit
                                        keyblocks[shapekey].slider_max = 1.5
                                    elif container == 'AU17D':
                                        driver.modifiers[0].coefficients[1] = 2/unit

                                elif container == 'AU32':
                                    target.transform_type = 'LOC_Y'
                                    driver.modifiers[0].coefficients[1] = -2/unit

                            #MiddleLip
                            elif container == 'AD96L' or container == 'AD96R' or container == 'AU22Z':
                                #AD96L/R = Mouth sideways
                                #AU22Z = Outside puckering

                                target.bone_target = "MiddleLip" 
                                target.transform_space = 'LOCAL_SPACE'

                                if container == 'AD96L' or container == 'AD96R':
                                    target.transform_type = 'LOC_X'

                                    if shapekey.endswith('L'):
                                        driver.modifiers[0].coefficients[1] = 1/unit
                                    elif shapekey.endswith('R'):
                                        driver.modifiers[0].coefficients[1] = -1/unit

                                elif container == 'AU22Z':
                                    target.transform_type = 'LOC_Y'

                                    driver.modifiers[0].coefficients[1] = -2/unit

                        elif cat == 'chin':
                            #AU17 = Chin raise (sort of)
                            #AU26 = Chin drop
                            #AU27 = Chin drop 2
                            #AU27Z = Full mouth open
                            #AD30L/R = Chin sideways

                            target.bone_target = "Chin" 
                            target.transform_space = 'LOCAL_SPACE'
                            
                            #Upwards/Downwards movement
                            if container == 'AU17' or container == 'AU26' or container == 'AU27' or container == 'AU27Z':
                                target.transform_type = 'LOC_Z'

                                #Documentation (Since i may be the first human on earth to find and/or utilize this)
                                #driver.keyframe_points.add(count) = Add keyframe
                                #driver.keyframe_points[keyframe] = Keyframe
                                #driver.keyframe_points[0].co_ui[0] = Horizontal position
                                #driver.keyframe_points[0].co_ui[1] = Vertical position
                                #driver.keyframe_points[0].handle_(left/right) = Keyframe handle (Location and type)
                                #driver.keyframe_points[0].handle_(left/right)_type = Interpolation type

                                if container == 'AU17':
                                    driver.modifiers[0].coefficients[1] = 1/unit

                                #Chin lowers
                                if container == 'AU26':
                                    driver.keyframe_points.add(3)

                                    #Keyframe positions and values
                                    driver.keyframe_points[0].co_ui[0] = 0
                                    driver.keyframe_points[0].co_ui[1] = 0
                                    driver.keyframe_points[1].co_ui[0] = -0.6*unit
                                    driver.keyframe_points[1].co_ui[1] = 1
                                    driver.keyframe_points[2].co_ui[0] = -1.2*unit
                                    driver.keyframe_points[2].co_ui[1] = 0

                                    #Handles
                                    driver.keyframe_points[1].handle_left_type = 'FREE'
                                    driver.keyframe_points[1].handle_right_type = 'FREE'
                                    driver.keyframe_points[1].handle_left[0] = -0.75*unit
                                    driver.keyframe_points[1].handle_left[1] = 1
                                    driver.keyframe_points[1].handle_right[0] = -0.45*unit
                                    driver.keyframe_points[1].handle_right[1] = 0.5

                                    driver.keyframe_points[2].handle_left_type = 'ALIGNED'
                                    driver.keyframe_points[2].handle_right_type = 'ALIGNED'
                                    driver.keyframe_points[2].handle_left[0] = -1.3*unit
                                    driver.keyframe_points[2].handle_left[1] = 0
                                    driver.keyframe_points[2].handle_right[0] = -0.945*unit
                                    driver.keyframe_points[2].handle_right[1] = 0

                                    #Forces refresh
                                    driver.auto_smoothing = 'CONT_ACCEL'

                                    try:
                                        driver.modifiers.remove(driver.modifiers[0])
                                    except:
                                        pass

                                elif container == 'AU27':
                                    driver.keyframe_points.add(4)

                                    driver.keyframe_points[0].co_ui[0] = 0
                                    driver.keyframe_points[0].co_ui[1] = 0
                                    driver.keyframe_points[1].co_ui[0] = -0.6*unit
                                    driver.keyframe_points[1].co_ui[1] = 0
                                    driver.keyframe_points[2].co_ui[0] = -1*unit
                                    driver.keyframe_points[2].co_ui[1] = 0.95
                                    driver.keyframe_points[3].co_ui[0] = -1.5*unit
                                    driver.keyframe_points[3].co_ui[1] = 0

                                    driver.keyframe_points[1].handle_left_type = 'AUTO'
                                    driver.keyframe_points[1].handle_right_type = 'AUTO'

                                    driver.keyframe_points[2].handle_left_type = 'ALIGNED'
                                    driver.keyframe_points[2].handle_right_type = 'ALIGNED'
                                    driver.keyframe_points[2].handle_left[0] = -1.1*unit
                                    driver.keyframe_points[2].handle_left[1] = 0.95
                                    driver.keyframe_points[2].handle_right[0] = -0.9*unit
                                    driver.keyframe_points[2].handle_right[1] = 0.95

                                    driver.keyframe_points[3].handle_left_type = 'ALIGNED'
                                    driver.keyframe_points[3].handle_right_type = 'ALIGNED'
                                    driver.keyframe_points[3].handle_left[0] = -2*unit
                                    driver.keyframe_points[3].handle_left[1] = 0
                                    driver.keyframe_points[3].handle_right[0] = -1.3*unit
                                    driver.keyframe_points[3].handle_right[1] = 0

                                    #Forces refresh
                                    driver.auto_smoothing = 'CONT_ACCEL'

                                    try:
                                        driver.modifiers.remove(driver.modifiers[0])
                                    except:
                                        pass

                                elif container == 'AU27Z':
                                    driver.keyframe_points.add(2)

                                    driver.keyframe_points[0].co_ui[0] = -0.95*unit
                                    driver.keyframe_points[0].co_ui[1] = 0
                                    driver.keyframe_points[1].co_ui[0] = -1.5*unit
                                    driver.keyframe_points[1].co_ui[1] = 1

                                    driver.keyframe_points[0].handle_left_type = 'ALIGNED'
                                    driver.keyframe_points[0].handle_right_type = 'ALIGNED'
                                    driver.keyframe_points[0].handle_left[0] = -1.135*unit
                                    driver.keyframe_points[0].handle_left[1] = 0.275
                                    driver.keyframe_points[0].handle_right[0] = -0.825*unit
                                    driver.keyframe_points[0].handle_right[1] = -0.185

                                    driver.keyframe_points[1].handle_left_type = 'ALIGNED'
                                    driver.keyframe_points[1].handle_right_type = 'ALIGNED'
                                    driver.keyframe_points[1].handle_left[0] = -1.6*unit
                                    driver.keyframe_points[1].handle_left[1] = 1
                                    driver.keyframe_points[1].handle_right[0] = -1.3*unit
                                    driver.keyframe_points[1].handle_right[1] = 1

                                    #Forces refresh
                                    driver.auto_smoothing = 'CONT_ACCEL'

                                    try:
                                        driver.modifiers.remove(driver.modifiers[0])
                                    except:
                                        pass

                            #Sideways movement
                            elif container == 'AD30L' or container == 'AD30R':
                                target.transform_type = 'LOC_X'

                                if container == 'AD30L':
                                    driver.modifiers[0].coefficients[1] = 1/unit

                                elif container == 'AD30R':
                                    driver.modifiers[0].coefficients[1] = -1/unit

            del shapekey

            if utils.arm.eyes_material:
                for material in utils.arm.eyes_material:
                    material = vatproperties.target_object.data.materials[material.name]

                    eye_texture = False

                    if not material.use_nodes:
                        material.use_nodes = True

                    link = material.node_tree.links
                    node = material.node_tree.nodes

                    try:
                        imgtexture = node['Image Texture']
                        output_loc = imgtexture.location
                        eye_texture = True
                    except:
                        try:
                            output_loc = node['Material Output'].location
                        except:
                            output_loc = (0,0)

                    #Checks if mapping node already exists
                    try:
                        mapping = node['VAT Eye Movement']
                    except:
                        mapping = node.new('ShaderNodeMapping')
                        mapping.name = "VAT Eye Movement"
                        mapping.width = 315 #So all the label is visible
                        if eye_texture:
                            mapping.location = output_loc[0] - 400, output_loc[1]
                        else:
                            mapping.location = output_loc[0], output_loc[1] + 420
                            mapping.label = "Connect to iris(+Normal/Specular) texture's vector input"

                    #Checks if texture coordinates node already exists
                    try:
                        texcoord = node['VAT Eye Movement Origin']
                    except:
                        texcoord = node.new('ShaderNodeTexCoord')
                        texcoord.name = "VAT Eye Movement Origin"
                        texcoord.location = mapping.location[0] - 200, mapping.location[1]
                    
                    if not texcoord.outputs['UV'].links:
                        link.new(texcoord.outputs['UV'], mapping.inputs['Vector'])

                    if eye_texture:
                        if not mapping.outputs['Vector'].links:
                            link.new(mapping.outputs['Vector'], imgtexture.inputs['Vector'])
                        imgtexture.extension = 'EXTEND'

                    #Driver portion
                    driver = mapping.inputs['Location'].driver_add('default_value')

                    variable = driver[0].driver.variables.new() #Creates new variable onto the shapekey
                    variable.name = "eye_x"
                    driver[0].driver.expression = variable.name #Changes expression to created variable's name
                    variable.type = 'TRANSFORMS' #Changes type of variable to transform

                    target = variable.targets[0]
                    target.id = utils.arm.animation_armature
                    target.transform_space = 'LOCAL_SPACE'
                    target.transform_type = 'LOC_X'

                    if material.name.count('eyeball_l'):
                        target.bone_target = 'EyeLeft'
                        driver[0].modifiers[0].coefficients[1] = -0.25
                    elif material.name.count('eyeball_r'):
                        target.bone_target = 'EyeRight'
                        driver[0].modifiers[0].coefficients[1] = 0.25

                    variable = driver[1].driver.variables.new() #Creates new variable onto the shapekey
                    variable.name = "eye_z"
                    driver[1].driver.expression = variable.name #Changes expression to created variable's name
                    variable.type = 'TRANSFORMS' #Changes type of variable to transform

                    target = variable.targets[0]
                    target.id = utils.arm.animation_armature
                    target.transform_space = 'LOCAL_SPACE'
                    target.transform_type = 'LOC_Z'

                    driver[1].modifiers[0].coefficients[1] = -0.25

                    if material.name.count('eyeball_l'):
                        target.bone_target = 'EyeLeft'
                    elif material.name.count('eyeball_r'):
                        target.bone_target = 'EyeRight'

                del utils.arm.eyes_material
                
    def create_widgets():

        #Creates widgets collection before Rigify
        collection = bpy.data.collections.new('Widgets')
        bpy.context.scene.collection.children.link(collection)

        collection.hide_viewport = True
        
        #Empty that stores all the generated widgets for easier storage/manipulation
        parent = bpy.data.objects.new('parent_widgets', None)

        for widget in ['4Directions', 'Cheek', 'LowerLip', 'MiddleLip', 'UpperLip', 'Nostril_L', 'Nostril_R', 'UpDown', 'Circle']:
            try:
                bpy.data.objects[widget]
            except:
                #Creates mesh datablock and object
                mesh = bpy.data.meshes.new(widget)
                if widget == 'Circle':
                    object = bpy.data.objects.new(widget, None)
                else:
                    object = bpy.data.objects.new(widget, mesh)
                object.parent = parent

                #Gets Rigify's collection and links to it
                collection = bpy.data.collections['Widgets']
                collection.objects.link(object)

                if widget == 'Circle':
                    object.empty_display_type = 'CIRCLE'
                    continue

                faces = []

                if widget == '4Directions':
                    vertices = [(0.0000, 0.0000, 1.0000), (-0.3827, 0.0000, 0.9239), (-0.7071, 0.0000, 0.7071), (-0.9239, 0.0000, 0.3827), (-1.0000, 0.0000, 0.0000), (-0.9239, -0.0000, -0.3827), (-0.7071, -0.0000, -0.7071), (-0.3827, -0.0000, -0.9239), (0.0000, -0.0000, -1.0000), (0.3827, -0.0000, -0.9239), (0.7071, -0.0000, -0.7071), (0.9239, -0.0000, -0.3827), (1.0000, 0.0000, 0.0000), (0.9239, 0.0000, 0.3827), (0.7071, 0.0000, 0.7071), (0.3827, 0.0000, 0.9239), (-0.3718, 0.0000, 1.8058), (-0.6592, 0.0000, 1.3381), (0.3718, 0.0000, 1.8058), (0.6592, 0.0000, 1.3381), (0.4179, 0.0000, 1.0882), (0.7722, 0.0000, 0.8515), (-0.7722, 0.0000, 0.8515), (-0.4179, 0.0000, 1.0882), (0.0000, 0.0000, 1.1805), (0.0000, 0.0000, 2.2000), (-2.2000, 0.0000, 0.0000), (-1.1805, 0.0000, 0.0000), (-1.0882, 0.0000, -0.4179), (-0.8515, 0.0000, -0.7722), (-0.8515, 0.0000, 0.7722), (-1.0882, 0.0000, 0.4179), (-1.3381, 0.0000, 0.6592), (-1.8058, 0.0000, 0.3718), (-1.3381, 0.0000, -0.6592), (-1.8058, 0.0000, -0.3718), (2.2000, 0.0000, -0.0000), (1.1805, 0.0000, -0.0000), (1.0882, 0.0000, 0.4179), (0.8515, 0.0000, 0.7722), (0.8515, 0.0000, -0.7722), (1.0882, 0.0000, -0.4179), (1.3381, 0.0000, -0.6592), (1.8058, 0.0000, -0.3718), (1.3381, 0.0000, 0.6592), (1.8058, 0.0000, 0.3718), (0.3718, 0.0000, -1.8058), (0.6592, 0.0000, -1.3381), (-0.3718, 0.0000, -1.8058), (-0.6592, 0.0000, -1.3381), (-0.4179, 0.0000, -1.0882), (-0.7722, 0.0000, -0.8515), (0.7722, 0.0000, -0.8515), (0.4179, 0.0000, -1.0882), (-0.0000, 0.0000, -1.1805), (-0.0000, 0.0000, -2.2000)]
                    edges = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (14, 13), (15, 14), (0, 15), (16, 25), (17, 22), (18, 25), (19, 21), (17, 16), (19, 18), (24, 20), (20, 21), (22, 23), (23, 24), (28, 27), (29, 28), (31, 30), (27, 31), (32, 33), (34, 35), (32, 30), (33, 26), (34, 29), (35, 26), (38, 37), (39, 38), (41, 40), (37, 41), (42, 43), (44, 45), (42, 40), (43, 36), (44, 39), (45, 36), (46, 55), (47, 52), (48, 55), (49, 51), (47, 46), (49, 48), (54, 50), (50, 51), (52, 53), (53, 54)]

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
    utils.arm.get_bones(False)

    if action == 0 or action == 1: #Usual creation/deletion
        generate_rigify(action)

    elif action == 2: #Creates empties and links it to Source armature, also creates widgets and setups facial flexes
        if vatinfo.scheme == 0:
            armature_rename(1, utils.arm.armature)
            link()
            face_flex_setup()
            armature_rename(0, utils.arm.armature)
        else:
            link()
            face_flex_setup()

        vatproperties.target_object = None

        if utils.arm.armature.visible_get() == True:
            utils.arm.armature.hide_set(True)
        bpy.context.view_layer.objects.active = utils.arm.animation_armature
        bpy.ops.object.mode_set(mode='OBJECT')

import bpy

def bake(mode):

    def bake_strip(track):
        strip = track.strips[0]

        track.mute = False

        armature.animation_data.nla_tracks.active = track

        #Changes the anim armature's action name so the original armature can have it
        if strip.action.name.startswith('_'):
            name = strip.action.name[1:]
        else:
            name = strip.action.name
            strip.action.name = '_' + strip.action.name
            
        #Original armature's NLA tracks
        track2 = armature2.animation_data.nla_tracks
        
        #Creates new action to store baked data in, track and strip, or overrides existing one
        try:
            action = bpy.data.actions[name]
        except:
            action = bpy.data.actions.new(name)
            
        try:
            new_track = track2[name]
        except:
            new_track = track2.new()
            new_track.name = name
            
        try:
            new_strip = new_track.strips[name]
        except:
            new_strip = new_track.strips.new(name, 0, action)
        
        #Selection, tweak mode and bake
        new_track.select = True
        new_strip.select = True
        armature2.animation_data.use_tweak_mode = True
        
        bpy.ops.nla.bake(frame_start=strip.frame_start, frame_end=strip.frame_end, only_selected=False, visual_keying=True, use_current_action=True, bake_types={'POSE'})
        
        armature2.animation_data.use_tweak_mode = False
        track.mute = True
        new_track.select = False
        new_track.mute = True
        bpy.ops.pose.transforms_clear()

    armature = utils.arm.animation_armature
    armature2 = utils.arm.armature

    if armature.select_get() == True:
        armature.select_set(False)
        
    #Gets current mode to set it back after operation completion
    current_mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')

    if armature2.select_get() == True:
        armature2.select_set(True)
        bpy.context.view_layer.objects.active = armature2

    bpy.ops.object.mode_set(mode='POSE')
    
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.transforms_clear()

    if armature.animation_data.use_tweak_mode == True:
        armature.animation_data.use_tweak_mode = False


    #Disables every track to avoid tracks overriding others
    for track in armature.animation_data.nla_tracks:
        track.mute = True

    if mode == 0:
        bake_strip(armature.animation_data.nla_tracks.active)

    elif mode == 1:
        for track in armature.animation_data.nla_tracks:
            bake_strip(track)

    bpy.ops.object.mode_set(mode=current_mode)

def export():
    armature = utils.arm.armature

    current_mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')

    if armature.select_get() == True:
        armature.select_set(True)

    bpy.context.view_layer.objects.active = armature
        
    if armature.animation_data.use_tweak_mode == True:
        armature.animation_data.use_tweak_mode = False

    #Workaround due to exporting updating the scene invalidating the armature variable
    track_count = len(armature.animation_data.nla_tracks)

    for track in armature.animation_data.nla_tracks:
        track.select = False

    for index in range(track_count):
        track = armature.animation_data.nla_tracks[index]
        strip = track.strips[0]

        armature.animation_data.nla_tracks.active = track

        #Selection, tweak mode and bake
        track.select = True
        strip.select = True
        armature.animation_data.use_tweak_mode = True

        bpy.ops.export_scene.smd()
        armature = utils.arm.armature
        
        armature.animation_data.use_tweak_mode = False
        track.select = False
        strip.select = False

def update_retarget_constraints(self, context):
    retarget_constraints()

def retarget_constraints():
    vatproperties = bpy.context.scene.vatproperties
    vatinfo = bpy.context.scene.vatinfo

    prefix = utils.arm.prefix
    armature = utils.arm.armature

    if vatproperties.retarget_constraints:
        value = False
    else:
        value = True

    if vatinfo.animation_armature and not vatinfo.animation_armature_setup:
        for cat in utils.arm.symmetrical_bones.keys():
            for container, bone in utils.arm.symmetrical_bones[cat].items():
                for bone in bone:
                    if bone:
                        try:
                            armature.pose.bones[prefix + bone].constraints['Retarget Location'].mute = value
                        except:
                            pass

                        try:
                            armature.pose.bones[prefix + bone].constraints['Retarget Rotation'].mute = value
                        except:
                            pass

        for container, bone in utils.arm.central_bones.items():
            for bone in bone:
                if bone:
                    if bone == 'Bip01' and utils.arm.viewmodel:
                        prefix = Prefixes.other
                    else:
                        prefix = utils.arm.prefix
                    try:
                        armature.pose.bones[prefix + bone].constraints['Retarget Location'].mute = value
                    except:
                        pass

                    try:
                        armature.pose.bones[prefix + bone].constraints['Retarget Rotation'].mute = value
                    except:
                        pass

        prefix = Prefixes.other

        for container, bone in utils.arm.other_bones.items():
            if container == 'weapon' or container == 'viewmodel':
                for bone in bone:
                    if bone:
                        try:
                            armature.pose.bones[prefix + bone].constraints['Retarget Location'].mute = value
                        except:
                            pass

                        try:
                            armature.pose.bones[prefix + bone].constraints['Retarget Rotation'].mute = value
                        except:
                            pass
        
        for cat in utils.arm.helper_bones.keys():
            for container, bone in utils.arm.helper_bones[cat].items():
                for bone in bone:
                    if bone:
                        prefix, bone = helper_convert(bone)
                        
                        try:
                            armature.pose.bones[prefix + bone].constraints['Procedural Bone'].mute = value
                        except:
                            pass

                        if container == 'knee' or container == 'elbow':
                            try:
                                armature.pose.bones[prefix + bone].constraints['Retarget Location'].mute = value
                            except:
                                pass