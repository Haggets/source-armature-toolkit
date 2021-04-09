import bpy
import math 
from . import utils
from .utils import Prefixes
from .utils import update
from .utils import generate_armature
from .utils import define_bone
from .utils import generate_shapekey_dict
from .utils import helper_convert

def anim_armature(action):

    vatproperties = bpy.context.scene.vatproperties
    vatinfo = bpy.context.scene.vatinfo

    def generate_rigify(action): #Creates Rigify armature and fills in all the Rigify parameters

        #Armature creation
        generate_armature('anim', action)
        
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

                    for cat in utils.arm.shapekeys.keys():
                        for container, shapekey in utils.arm.shapekeys[cat].items():
                            if cat == 'eyebrows':
                                if container:
                                    if not eyebrows: 
                                        #Inner, outer and full eyebrows
                                        for bone in ['Eyebrow_L', 'Eyebrow_R', 'Inner_Eyebrow_L', 'Inner_Eyebrow_R', 'Outer_Eyebrow_L', 'Outer_Eyebrow_R']:
                                            eyebrows = True
                                            utils.arm.facial_bones.append(bone)

                                            ebone = armature.data.edit_bones.new(bone)
                                            ebone.use_deform = False

                                            if bone == 'Eyebrow_L':
                                                define_bone([bone, head], [1.2, 1.2, 4.5, 4, 4, 0], '+')
                                            elif bone == 'Eyebrow_R':
                                                define_bone([bone, head], [1.2, 1.2, 4.5, 4, 4, 0], '-')
                                            elif bone == 'Inner_Eyebrow_L':
                                                define_bone([bone, head], [0.6, 0.6, 4.5, 4, 3.75, 0], '+')
                                            elif bone == 'Inner_Eyebrow_R':
                                                define_bone([bone, head], [0.6, 0.6, 4.5, 4, 3.75, 0], '-')
                                            elif bone == 'Outer_Eyebrow_L':
                                                define_bone([bone, head], [1.8, 1.8, 4.5, 4, 3.75, 0], '+')
                                            elif bone == 'Outer_Eyebrow_R':
                                                define_bone([bone, head], [1.8, 1.8, 4.5, 4, 3.75, 0], '-')

                            elif cat == 'eyes':
                                if container:
                                    if not eyes:
                                        #Upper and lower eyelids
                                        for bone in ['UpperEye_L', 'UpperEye_R', 'LowerEye_L', 'LowerEye_R']:
                                            eyes = True
                                            utils.arm.facial_bones.append(bone)

                                            ebone = armature.data.edit_bones.new(bone)
                                            ebone.use_deform = False
                                        
                                            if bone == 'UpperEye_L':
                                                define_bone([bone, head], [1.2, 1.2, 4, 3.5, 3.5, 0], '+')
                                            elif bone == 'UpperEye_R':
                                                define_bone([bone, head], [1.2, 1.2, 4, 3.5, 3.5, 0], '-')
                                            elif bone == 'LowerEye_L':
                                                define_bone([bone, head], [1.2, 1.2, 4, 3.5, 2.9, 0], '+')
                                            elif bone == 'LowerEye_R':
                                                define_bone([bone, head], [1.2, 1.2, 4, 3.5, 2.9, 0], '-')
                                
                            elif cat == 'cheek':
                                if container:
                                    if not cheek:
                                        #Cheeks for puffing and squinting
                                        for bone in ['Cheek_L', 'Cheek_R']:
                                            cheek = True
                                            utils.arm.facial_bones.append(bone)

                                            ebone = armature.data.edit_bones.new(bone)
                                            ebone.use_deform = False

                                            if bone == 'Cheek_L':
                                                define_bone([bone, head], [2, 1.5, 3, 2.5, 1, 0], '+')
                                            elif bone == 'Cheek_R':
                                                define_bone([bone, head], [2, 1.5, 3, 2.5, 1, 0], '-')

                                            ebone.length = 0.5

                            elif cat == 'nose':
                                if container:
                                    if not nose:
                                        #Nostrils
                                        for bone in ['Nostril_L', 'Nostril_R']:
                                            nose = True
                                            utils.arm.facial_bones.append(bone)

                                            ebone = armature.data.edit_bones.new(bone)
                                            ebone.use_deform = False

                                            if bone == 'Nostril_L':
                                                define_bone([bone, head], [0.8, 0.8, 4, 3.5, 1, 0], '+')
                                            elif bone == 'Nostril_R':
                                                define_bone([bone, head], [0.8, 0.8, 4, 3.5, 1, 0], '-')

                            if cat == 'mouth':
                                if container:
                                    if not mouth:
                                        #Mouth corners
                                        if container == 'AU12' or container == 'AU15' or container == 'AU24' or container == 'AU18Z' or container == 'AU22Z':
                                            for bone in ['MouthCorner_L', 'MouthCorner_R']:
                                                mouth = True
                                                utils.arm.facial_bones.append(bone)

                                                ebone = armature.data.edit_bones.new(bone)
                                                ebone.use_deform = False

                                                if bone == 'MouthCorner_L':
                                                    define_bone([bone, head], [1.2, 1, 4, 3.5, 0.25, 0], '+')
                                                elif bone == 'MouthCorner_R':
                                                    define_bone([bone, head], [1.2, 1, 4, 3.5, 0.25, 0], '-')

                                                ebone.length = 0.5

                                    elif not upper_lip:
                                        #Upper lip
                                        if container == 'AU10':
                                            for bone in ['UpperLip_L', 'UpperLip_R']:
                                                upper_lip = True
                                                utils.arm.facial_bones.append(bone)

                                                ebone = armature.data.edit_bones.new(bone)
                                                ebone.use_deform = False

                                                if bone == 'UpperLip_L':
                                                    define_bone([bone, head], [0.5, 0.5, 4.5, 4, 0.5, 0], '+')
                                                elif bone == 'UpperLip_R':
                                                    define_bone([bone, head], [-0.5, -0.5, 4.5, 4, 0.5, 0], '+')

                                    elif not lower_lip:
                                        #Lower lip
                                        if container == 'AU17D' or container == 'AU16' or container == 'AU32':
                                            for bone in ['LowerLip_L', 'LowerLip_R']:
                                                lower_lip = True
                                                utils.arm.facial_bones.append(bone)

                                                ebone = armature.data.edit_bones.new(bone)
                                                ebone.use_deform = False

                                                if bone == 'LowerLip_L':
                                                    define_bone([bone, head], [0.5, 0.5, 4.5, 4, 0, 0], '+')
                                                elif bone == 'LowerLip_R':
                                                    define_bone([bone, head], [0.5, 0.5, 4.5, 4, 0, 0], '-')

                                    elif not middle_lip:
                                        #Middle lip
                                        if container == 'AD96L' or container == 'AD96R':
                                            for bone in ['MiddleLip']:
                                                middle_lip = True
                                                utils.arm.facial_bones.append(bone)

                                                ebone = armature.data.edit_bones.new(bone)
                                                ebone.use_deform = False

                                                define_bone([bone, head], [0, 0, 4.5, 4, 0.25, 0])

                            if cat == 'chin':
                                if container:
                                    if not chin:
                                        for bone in ['Chin']:
                                            chin = True
                                            utils.arm.facial_bones.append(bone)

                                            ebone = armature.data.edit_bones.new(bone)
                                            ebone.use_deform = False
                                        
                                            define_bone([bone, head], [0, 0, 4.5, 4, -1.5, 0.15])

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
                            define_bone([bone, head], [1.2, 1.2, 10, 9.5, 3.2, 0], '+')
                        elif bone == 'EyeRight':
                            define_bone([bone, head], [1.2, 1.2, 10, 9.5, 3.2, 0], '-')

            #Creates 2 pelvis bones for whatever Rigify does with em
            rigify_pelvis = ['Pelvis_L', 'Pelvis_R']

            ppelvis = armature.pose.bones[prefix + utils.arm.central_bones['pelvis'][0]]
            epelvis = armature.data.edit_bones[prefix + utils.arm.central_bones['pelvis'][0]]
            
            for bone in rigify_pelvis:
                ebone = armature.data.edit_bones.new(bone)

                ebone.head = epelvis.head
                ebone.parent = epelvis
                ebone.layers[3] = True
                ebone.layers[0] = False

                #New pelvis bone positioning
                if bone.endswith('_L'):
                    ebone.tail.xyz = ppelvis.head.x-3, ppelvis.head.y-2, ppelvis.head.z+4
                elif bone.endswith('_R'):
                    ebone.tail.xyz = ppelvis.head.x+3, ppelvis.head.y-2, ppelvis.head.z+4
                
            #Creates multiple palm bones for fingers
            rigify_palm = {'finger1': [], 'finger2': [], 'finger3': [], 'finger4': []}

            for container, bone in utils.arm.symmetrical_bones['fingers'].items():
                for bone in bone:
                    if container == 'finger1' or container == 'finger2' or container == 'finger3' or container == 'finger3' or container == 'finger4':
                        palm = 'Palm_' + bone
                        ebone = armature.data.edit_bones[prefix + bone]
                        epalm = armature.data.edit_bones.new(palm)
                        rigify_palm[container].append(palm)
                        ebone.layers[5] = True
                        ebone.layers[0] = False
                        epalm.layers[5] = True
                        epalm.layers[0] = False

                        if bone.startswith('L_') or bone.endswith('_L'):
                            sign = '+'
                            parent = 0
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            sign = '-'
                            parent = 1

                        ebone.parent = epalm
                        epalm.parent = armature.data.edit_bones[prefix + utils.arm.symmetrical_bones['arms']['hand'][parent]]

                        define_bone([palm, prefix + bone, prefix + utils.arm.symmetrical_bones['arms']['hand'][0]], [], sign, False, 2)
                    else:
                        ebone = armature.data.edit_bones[prefix + bone]
                        ebone.layers[5] = True
                        ebone.layers[1] = False
                        ebone.layers[2] = False

            #Creates heels for easier leg tweaking
            rigify_heel = ['Heel_L', 'Heel_R']

            pfoot = armature.pose.bones[prefix + utils.arm.symmetrical_bones['legs']['foot'][0]]
            efoot = armature.data.edit_bones[prefix + utils.arm.symmetrical_bones['legs']['foot'][0]]

            for bone in rigify_heel:
                ebone = armature.data.edit_bones.new(bone)

                if bone.endswith('_L'):
                    ebone.layers[13] = True
                    ebone.tail.xyz = math.copysign(pfoot.head.x, 1)+1.5, pfoot.head.y+1, 0
                    ebone.head.xyz = math.copysign(pfoot.head.x, 1)-1.5, pfoot.head.y+1, 0
                    ebone.parent = armature.data.edit_bones[prefix + utils.arm.symmetrical_bones['legs']['foot'][0]]
                elif bone.endswith('_R'):
                    ebone.layers[16] = True
                    ebone.tail.xyz = math.copysign(pfoot.head.x, -1)-1.5, pfoot.head.y+1, 0
                    ebone.head.xyz = math.copysign(pfoot.head.x, -1)+1.5, pfoot.head.y+1, 0
                    ebone.parent = armature.data.edit_bones[prefix + utils.arm.symmetrical_bones['legs']['foot'][1]]
                
                ebone.layers[0] = False

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
                        limit_loc.min_x = -0.5

                    elif bone == 'Nostril_L':
                        limit_loc.min_x = 0

                    elif bone == 'Nostril_R':
                        limit_loc.min_x = -0.5

                    elif bone == 'EyeLeft' or bone == 'EyeRight':
                        limit_loc.min_x = -4

                    else:
                        limit_loc.min_x = -1

                    #Max X
                    limit_loc.use_max_x = True
                    if bone.count('MouthCorner') or bone == 'Nostril_L':
                        limit_loc.max_x = 0.5

                    elif bone == 'Nostril_R':
                        limit_loc.max_x = 0

                    elif bone == 'EyeLeft' or bone == 'EyeRight':
                        limit_loc.max_x = 4

                    else:
                        limit_loc.max_x = 1

                    #Min Y
                    limit_loc.use_min_y = True
                    if bone.count('Cheek'):
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
                        limit_loc.min_z = -1.5
                        
                    elif bone == 'EyeLeft' or bone == 'EyeRight':
                        limit_loc.min_z = -4

                    else:
                        limit_loc.min_z = -1

                    #Max Z
                    limit_loc.use_max_z = True

                    if bone.count('UpperEye') or bone.count('LowerEye'):
                        limit_loc.max_z = 0.2

                    elif bone.count('Eyebrow') or bone.count('UpperLip') or bone.count('MouthCorner') or bone.count('Nostril') or bone.count('LowerLip'):
                        limit_loc.max_z = 0.5

                    elif bone == 'EyeLeft' or bone == 'EyeRight':
                        limit_loc.max_z = 4

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
                        widget = bpy.data.objects['4Directions']
                        pbone.custom_shape = widget
                        pbone.custom_shape_scale = 0.7
                        
                    elif bone.count('MouthCorner'):
                        widget = bpy.data.objects['4Directions']
                        pbone.custom_shape = widget
                        pbone.custom_shape_scale = 0.4

                    elif bone == 'EyeLeft' or bone == 'EyeRight':
                        widget = bpy.data.objects['Circle']
                        pbone.custom_shape = widget
                        pbone.custom_shape_scale = 1.5

                    if bone.count('Inner_Eyebrow') or bone.count('Outer_Eyebrow') or bone.count('Nostril') or bone.count('Cheek') or bone.count('MiddleLip'):
                        ebone.layers[1] = True
                        ebone.layers[0] = False

            #Rigify pelvis
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
                            pbone = armature.pose.bones[prefix + bone]
                            param = pbone.rigify_parameters
                            ebone = armature.data.edit_bones[prefix + bone]

                            if container == 'finger0' or container == 'finger1' or container == 'finger2' or container == 'finger3' or container == 'finger4':
                                pbone.rigify_type = 'limbs.super_finger'
                                ebone.layers[5] = True

                                ebone.layers[0] = False

                                for i in [0,1,2,3,4,6,7]:
                                    ebone.layers[i] = False
                                
                elif cat == 'arms':
                    for container, bone in utils.arm.symmetrical_bones[cat].items():
                        for bone in bone:
                            pbone = armature.pose.bones[prefix + bone]
                            param = pbone.rigify_parameters
                            ebone = armature.data.edit_bones[prefix + bone]

                            if bone.startswith('L_') or bone.endswith('_L'):
                                ebone.layers[7] = True
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                ebone.layers[10] = True

                            if container == 'clavicle':
                                pbone.rigify_type = 'basic.super_copy'
                                param.make_widget = False
                                ebone.layers[3] = True
                            elif container == 'upperarm':
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

                            ebone.layers[0] = False
                            ebone.layers[1] = False
                            ebone.layers[2] = False

                elif cat == 'legs':
                    for container, bone in utils.arm.symmetrical_bones[cat].items():
                        for bone in bone:
                            pbone = armature.pose.bones[prefix + bone]
                            param = pbone.rigify_parameters
                            ebone = armature.data.edit_bones[prefix + bone]

                            if bone.startswith('L_') or bone.endswith('_L'):
                                ebone.layers[13] = True
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                ebone.layers[16] = True

                            if container == 'thigh':
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

                            ebone.layers[0] = False
                            ebone.layers[3] = False
                            ebone.layers[4] = False

            #Central
            for container, bone in utils.arm.central_bones.items():
                for bone in bone:
                    pbone = armature.pose.bones[prefix + bone]
                    param = pbone.rigify_parameters
                    ebone = armature.data.edit_bones[prefix + bone]

                    ebone.layers[3] = True

                    if container == 'pelvis':
                        pbone.rigify_type = 'spines.basic_spine'
                        param.pivot_pos = 2
                        param.tweak_layers[1] = False
                        param.tweak_layers[4] = True
                        param.fk_layers[1] = False
                        param.fk_layers[4] = True
                    elif container == 'neck':
                        pbone.rigify_type = 'spines.super_head'
                        param.connect_chain = True
                        param.tweak_layers[1] = False
                        param.tweak_layers[4] = True
                
                    ebone.layers[0] = False

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
            names = ['Face', 'Face (Primary)','Face (Secondary)','Torso', 'Torso (Tweak)', 'Fingers', 'Fingers (Detail)', 'Arm.L (IK)', 'Arm.L (FK)', 'Arm.L (Tweak)', 'Arm.R (IK)', 'Arm.R (FK)', 'Arm.R (Tweak)', 'Leg.L (IK)', 'Leg.L (FK)', 'Leg.L (Tweak)', 'Leg.R (IK)', 'Leg.R (FK)', 'Leg.R (Tweak)']

            row_groups = [1,2,2,3,4,5,6,7,8,9,7,8,9,10,11,12,10,11,12]

            layer_groups = [1,5,2,3,4,6,5,2,5,4,2,5,4,2,5,4,2,5,4]

            for i, name, row, group in zip(range(19), names, row_groups, layer_groups):
                armature.rigify_layers[i].name = name
                armature.rigify_layers[i].row = row
                armature.rigify_layers[i].group = group

            armature.layers[0] = False

            vatinfo.animation_armature_setup = True

            for i in [0,1,3,5,7,10,13,16]:
                    armature.layers[i] = True

            bpy.ops.object.mode_set(mode='OBJECT')

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

        def retarget(container, bone, helper=False, helper_target=None): #Creates empties and links them to Rigify armature/Source armature
            armature = bpy.data.objects['rig']
            
            if not helper:
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
                    retarget(container, bone)

        for container, bone in utils.arm.central_bones.items():
            for bone in bone:
                retarget(container, bone)

        #Creates additional location constraints for helper bones to copy their driver bone's location
        for bone in utils.arm.helper_bones['legs']['knee'] + utils.arm.helper_bones['arms']['elbow']:
            bone, prefix = helper_convert(bone)

            armature = utils.arm.armature
            loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')
            loc.name = "Retarget Location"

            if bone.casefold().count('knee'):
                if bone.startswith('L_') or bone.endswith('_L'):
                    loc.target = bpy.data.objects['target_{} ({})'.format(utils.arm.symmetrical_bones['legs']['calf'][0], utils.arm.armature.name)[0:60]]
                elif bone.startswith('R_') or bone.endswith('_R'):
                    loc.target = bpy.data.objects['target_{} ({})'.format(utils.arm.symmetrical_bones['legs']['calf'][1], utils.arm.armature.name)[0:60]]

            elif bone.casefold().count('elbow'):
                if bone.startswith('L_') or bone.endswith('_L'):
                    loc.target = bpy.data.objects['target_{} ({})'.format(utils.arm.symmetrical_bones['arms']['forearm'][0], utils.arm.armature.name)[0:60]]
                elif bone.startswith('R_') or bone.endswith('_R'):
                    loc.target = bpy.data.objects['target_{} ({})'.format(utils.arm.symmetrical_bones['arms']['forearm'][1], utils.arm.armature.name)[0:60]]

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
        for bone in utils.arm.isolatedbones:
            armature.data.edit_bones['ORG-' + bone].parent = armature.data.edit_bones['DEF-' + bone.replace('.isolated', '')]

        #Deletes generated armature
        generate_armature('anim', 2)

        #Links to animation armature
        try:
            collection = bpy.data.collections['Animation Armature']
        except:
            collection = None
            
        if collection:
            collection.objects.link(armature)

        vatinfo.animation_armature = True
        vatinfo.animation_armature_setup = False
        utils.arm.animation_armature = armature
        utils.arm.animation_armature_real = armature.data

        utils.arm._animation_armature = str(armature.name)
        utils.arm._animation_armature_real = str(armature.data.name)

    def face_flex_setup(): #Sets up drivers for face flexes that will be controlled by face bones
        prefix = utils.arm.prefix
        
        if utils.arm.shapekeys:
            keyblocks = vatproperties.target_object.data.shape_keys.key_blocks

            #Vertex group creation

            #Creates vertex groups
            left_group = vatproperties.target_object.vertex_groups.new(name='Left')
            right_group = vatproperties.target_object.vertex_groups.new(name='Right')

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
                                driver.modifiers[0].coefficients[1] = -2

                            elif container == 'AU1' or container == 'AU2' or container == 'AU1AU2':
                                driver.modifiers[0].coefficients[1] = 2

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
                                driver.modifiers[0].coefficients[1] = -5
                            
                            elif container == 'f02' or container == 'f04':
                                driver.modifiers[0].coefficients[1] = 5

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

                            elif container == 'AU13':
                                target.transform_type = 'LOC_Y'
                                driver.modifiers[0].coefficients[1] = -1

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
                                driver.modifiers[0].coefficients[1] = 2

                            elif container == 'AU38':
                                target.transform_type = 'LOC_X'

                                if shapekey.endswith('_L'):
                                    driver.modifiers[0].coefficients[1] = 2

                                elif shapekey.endswith('_R'):
                                    driver.modifiers[0].coefficients[1] = -2

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
                                        driver.modifiers[0].coefficients[1] = 2

                                    elif container == 'AU15':
                                        driver.modifiers[0].coefficients[1] = -2

                                elif container == 'AU24' or container == 'AU18Z':
                                    target.transform_type = 'LOC_X'

                                    if container == 'AU24':
                                        if shapekey.endswith('_L'):
                                            driver.modifiers[0].coefficients[1] = 2
                                        elif shapekey.endswith('_R'):
                                            driver.modifiers[0].coefficients[1] = -2
                                    
                                    elif container == 'AU18Z':
                                        if shapekey.endswith('_L'):
                                            driver.modifiers[0].coefficients[1] = -2
                                        elif shapekey.endswith('_R'):
                                            driver.modifiers[0].coefficients[1] = 2

                            #Upper lips
                            elif container == 'AU10':
                                target.transform_type = 'LOC_Z'
                                target.transform_space = 'LOCAL_SPACE'

                                if shapekey.endswith('_L'):
                                    target.bone_target = "UpperLip_L"
                                elif shapekey.endswith('_R'):
                                    target.bone_target = "UpperLip_R"

                                driver.modifiers[0].coefficients[1] = 2

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
                                        driver.modifiers[0].coefficients[1] = -3
                                        keyblocks[shapekey].slider_max = 1.5
                                    elif container == 'AU17D':
                                        driver.modifiers[0].coefficients[1] = 2

                                elif container == 'AU32':
                                    target.transform_type = 'LOC_Y'
                                    driver.modifiers[0].coefficients[1] = -2

                            #MiddleLip
                            elif container == 'AD96L' or container == 'AD96R' or container == 'AU22Z':
                                #AD96L/R = Mouth sideways
                                #AU22Z = Outside puckering

                                target.bone_target = "MiddleLip" 
                                target.transform_space = 'LOCAL_SPACE'

                                if container == 'AD96L' or container == 'AD96R':
                                    target.transform_type = 'LOC_X'

                                    if shapekey.endswith('R'):
                                        driver.modifiers[0].coefficients[1] = -1

                                elif container == 'AU22Z':
                                    target.transform_type = 'LOC_Y'

                                    driver.modifiers[0].coefficients[1] = -2

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

                                #Chin lowers
                                if container == 'AU26':
                                    driver.keyframe_points.add(3)

                                    #Keyframe positions and values
                                    driver.keyframe_points[0].co_ui[0] = 0
                                    driver.keyframe_points[0].co_ui[1] = 0
                                    driver.keyframe_points[1].co_ui[0] = -0.6
                                    driver.keyframe_points[1].co_ui[1] = 1
                                    driver.keyframe_points[2].co_ui[0] = -1.2
                                    driver.keyframe_points[2].co_ui[1] = 0

                                    #Handles
                                    driver.keyframe_points[1].handle_left_type = 'FREE'
                                    driver.keyframe_points[1].handle_right_type = 'FREE'
                                    driver.keyframe_points[1].handle_left[0] = -0.75
                                    driver.keyframe_points[1].handle_left[1] = 1
                                    driver.keyframe_points[1].handle_right[0] = -0.45
                                    driver.keyframe_points[1].handle_right[1] = 0.5

                                    driver.keyframe_points[2].handle_left_type = 'ALIGNED'
                                    driver.keyframe_points[2].handle_right_type = 'ALIGNED'
                                    driver.keyframe_points[2].handle_left[0] = -1.3
                                    driver.keyframe_points[2].handle_left[1] = 0
                                    driver.keyframe_points[2].handle_right[0] = -0.945
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
                                    driver.keyframe_points[1].co_ui[0] = -0.6
                                    driver.keyframe_points[1].co_ui[1] = 0
                                    driver.keyframe_points[2].co_ui[0] = -1
                                    driver.keyframe_points[2].co_ui[1] = 0.95
                                    driver.keyframe_points[3].co_ui[0] = -1.5
                                    driver.keyframe_points[3].co_ui[1] = 0

                                    driver.keyframe_points[1].handle_left_type = 'AUTO'
                                    driver.keyframe_points[1].handle_right_type = 'AUTO'

                                    driver.keyframe_points[2].handle_left_type = 'ALIGNED'
                                    driver.keyframe_points[2].handle_right_type = 'ALIGNED'
                                    driver.keyframe_points[2].handle_left[0] = -1.1
                                    driver.keyframe_points[2].handle_left[1] = 0.95
                                    driver.keyframe_points[2].handle_right[0] = -0.9
                                    driver.keyframe_points[2].handle_right[1] = 0.95

                                    driver.keyframe_points[3].handle_left_type = 'ALIGNED'
                                    driver.keyframe_points[3].handle_right_type = 'ALIGNED'
                                    driver.keyframe_points[3].handle_left[0] = -2
                                    driver.keyframe_points[3].handle_left[1] = 0
                                    driver.keyframe_points[3].handle_right[0] = -1.3
                                    driver.keyframe_points[3].handle_right[1] = 0

                                    #Forces refresh
                                    driver.auto_smoothing = 'CONT_ACCEL'

                                    try:
                                        driver.modifiers.remove(driver.modifiers[0])
                                    except:
                                        pass

                                elif container == 'AU27Z':
                                    driver.keyframe_points.add(2)

                                    driver.keyframe_points[0].co_ui[0] = -0.95
                                    driver.keyframe_points[0].co_ui[1] = 0
                                    driver.keyframe_points[1].co_ui[0] = -1.5
                                    driver.keyframe_points[1].co_ui[1] = 1

                                    driver.keyframe_points[0].handle_left_type = 'ALIGNED'
                                    driver.keyframe_points[0].handle_right_type = 'ALIGNED'
                                    driver.keyframe_points[0].handle_left[0] = -1.135
                                    driver.keyframe_points[0].handle_left[1] = 0.275
                                    driver.keyframe_points[0].handle_right[0] = -0.825
                                    driver.keyframe_points[0].handle_right[1] = -0.185

                                    driver.keyframe_points[1].handle_left_type = 'ALIGNED'
                                    driver.keyframe_points[1].handle_right_type = 'ALIGNED'
                                    driver.keyframe_points[1].handle_left[0] = -1.6
                                    driver.keyframe_points[1].handle_left[1] = 1
                                    driver.keyframe_points[1].handle_right[0] = -1.3
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

                                if container == 'AD30R':
                                    driver.modifiers[0].coefficients[1] = -1

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
        link()
        face_flex_setup()
