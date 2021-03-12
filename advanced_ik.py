import bpy
import math 
from . import utils
from .utils import Prefixes
from .utils import update
from .utils import generate_armature
from .utils import define_bone

def anim_armature(action):

    vatproperties = bpy.context.scene.vatproperties

    def generate_rigify(action): #Creates Rigify armature and fills in all the Rigify parameters

        #Armature creation
        generate_armature('anim', action)
        
        #Creation
        if action == 0:
            armature = bpy.data.objects[utils.arm.animation_armature_name]

            #Selects animation armature
            update(1, armature)

            #Creates driver so the original armature mimics the animation armature's scale
            driver = bpy.data.objects[utils.arm.name].driver_add('scale')

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
                    target.transform_type = 'SCALE_Z'
                
            #Hides all but the first layer
            for i in [1,2,3,5,4,6,7]:
                    armature.data.layers[i] = False

            #Rigify portion
            prefix = utils.arm.prefix
                    
            #Checks if there are shapekeys, if so, create driver bones for them
            if vatproperties.target_object:
                try:
                    shapekeys = bpy.data.objects[vatproperties.target_object.name].data.shape_keys.key_blocks.keys()
                except:
                    shapekeys = None
                    print("No shape keys detected")

                if shapekeys:

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

                    for shapekey in shapekeys:
                        #Eyebrows
                        if shapekey.count('AU1L+AU1R') or shapekey.count('AU2L+AU2R') or shapekey.count('AU4L+AU4R') or shapekey.count('AU1AU2L+AU1AU2R') or shapekey.count('AU1AU4L+AU1AU4R') or shapekey.count('AU2AU4L+AU2AU4R'):
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

                        #Eyes
                        elif shapekey.count('f01') or shapekey.count('f02') or shapekey.count('f03') or shapekey.count('f04') or shapekey.count('AU42'):
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
                            
                        #Cheek
                        elif shapekey.count('AU6L+AU6R') or shapekey.count('AU6ZL+AU6ZR') or shapekey.count('AU13L+AU13R'):
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

                        #Nose
                        elif shapekey.count('AU9L+AU9R') or shapekey.count('AU38'):
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

                        #Mouth 
                        elif shapekey.count('AU12L+AU12R') or shapekey.count('AU15L+AU15R') or shapekey.count('AU17L+AU17R') or shapekey.count('AU10L+AU10R') or shapekey.count('AU17DL+AU17DR') or shapekey.count('AU16L+AU16R') or shapekey.count('AU25L+AU25R') or shapekey.count('AU22L+AU22R') or shapekey.count('AU20L+AU20R') or shapekey.count('AU32') or shapekey.count('AU24') or shapekey.count('AU18L+AU18R') or shapekey.count('AU12AU25L+AU12AU25R') or shapekey.count('AU18ZL+AU18ZR') or shapekey.count('AU22ZL+AU22ZR') or shapekey.count('AU13L+AU13R') or shapekey.count('AD96L') or shapekey.count('AD96R'):
                            if not mouth:
                                #Mouth corners
                                if shapekey.count('AU12L+AU12R') or shapekey.count('AU15L+AU15R') or shapekey.count('AU22L+AU22R') or shapekey.count('AU20L+AU20R') or shapekey.count('AU24') or shapekey.count('AU18L+AU18R') or shapekey.count('AU12AU25L+AU12AU25R') or shapekey.count('AU18ZL+AU18ZR') or shapekey.count('AU22ZL+AU22ZR'):
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
                                if shapekey.count('AU10L+AU10R'):
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
                                if shapekey.count('AU17L+AU17R') or shapekey.count('AU17DL+AU17DR') or shapekey.count('AU16L+AU16R') or shapekey.count('AU25L+AU25R') or shapekey.count('AU32'):
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
                                if shapekey.count('AD96L') or shapekey.count('AD96R'):
                                    for bone in ['MiddleLip']:
                                        middle_lip = True
                                        utils.arm.facial_bones.append(bone)

                                        ebone = armature.data.edit_bones.new(bone)
                                        ebone.use_deform = False

                                        define_bone([bone, head], [0, 0, 4.5, 4, 0.25, 0])

                        #Chin
                        elif shapekey.count('AU31') or shapekey.count('AU26L+AU26R') or shapekey.count('AU27L+AU27R') or shapekey.count('AU26ZL+AU26ZR') or shapekey.count('AU27ZL+AU27ZR') or shapekey.count('AD30L') or shapekey.count('AD30R'):
                            if not chin:
                                for bone in ['Chin']:
                                    chin = True
                                    utils.arm.facial_bones.append(bone)

                                    ebone = armature.data.edit_bones.new(bone)
                                    ebone.use_deform = False
                                
                                    define_bone([bone, head], [0, 0, 4.5, 4, -1.5, 0.15])

                eyes = []
                utils.arm.eyes_material = []

                for material in bpy.data.objects[vatproperties.target_object.name].data.materials:
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
                    widget = bpy.data.objects['Chin']
                    pbone.custom_shape = widget
                    pbone.custom_shape_scale = 0.7
                    
                elif bone.count('MouthCorner'):
                    widget = bpy.data.objects['MouthCorner']
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

            armature = bpy.data.armatures[utils.arm.animation_armature_real.name]

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

            utils.arm.animation_armature_setup = True

            for i in [0,1,3,5,7,10,13,16]:
                    armature.layers[i] = True

            bpy.ops.object.mode_set(mode='OBJECT')

            print("Animation armature created!")

        elif action == 1:
            bpy.data.objects[utils.arm.name].driver_remove('scale')
            #Deletes Left/Right vertex groups if present
            try:
                left_group = bpy.data.objects[vatproperties.target_object.name].vertex_groups['Left']
                bpy.data.objects[vatproperties.target_object.name].vertex_groups.remove(left_group)
                del left_group
            except:
                pass
            
            try:
                right_group = bpy.data.objects[vatproperties.target_object.name].vertex_groups['Right']
                bpy.data.objects[vatproperties.target_object.name].vertex_groups.remove(right_group)
                del right_group
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

            print("Animation armature deleted")
                
    def empty_rotation(container, bone, type): #Sets empty rotation
        prefix = utils.arm.prefix

        scale = bpy.data.objects[utils.arm.animation_armature_name].scale

        base = bpy.data.objects['base_{} ({})'.format(bone, utils.arm.name)[0:60]]
        target = bpy.data.objects['target_{} ({})'.format(bone, utils.arm.name)[0:60]]
        
        #Default empty rotation, fit for most bones

        if type == 0: #Symmetrical bones default
            target.rotation_euler[0] = math.radians(90)
            target.rotation_euler[1] = math.radians(180)
            target.rotation_euler[2] = math.radians(-90)
        elif type == 1: #Center bones default
            target.rotation_euler[0] = 0
            target.rotation_euler[1] = 0
            target.rotation_euler[2] = 0
        
        #Upper body
        if vatproperties.retarget_top_preset == 'OP1':
            if container == 'clavicle':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-106)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(104)

        elif vatproperties.retarget_top_preset == 'OP2':
            if container == 'clavicle':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-95)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(90)

        #More specific empty rotations for bones that don't fit the default rotation
        if container == 'hand':
            if bone.startswith('L_') or bone.endswith('_L'):
                target.rotation_euler[0] = math.radians(169.25)
                target.rotation_euler[1] = math.radians(184.75)
                target.rotation_euler[2] = math.radians(-85)
            elif bone.startswith('R_') or bone.endswith('_R'):
                target.rotation_euler[0] = math.radians(10.5)
                target.rotation_euler[1] = math.radians(184.75)
                target.rotation_euler[2] = math.radians(-95)

        elif container.count('finger'):
            #Makes them smaller for the sake of readability
            base.empty_display_size = 0.5
            target.empty_display_size = 0.5

            #Finger0
            if container == 'finger0':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(136)
                    target.rotation_euler[1] = math.radians(180)
                    target.rotation_euler[2] = math.radians(-90)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(224)
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = math.radians(90)
            
            if container == 'finger01':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(135)
                    target.rotation_euler[1] = math.radians(180)
                    target.rotation_euler[2] = math.radians(-90)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(225)
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = math.radians(90)

            elif container == 'finger02':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-44.4)
                    target.rotation_euler[1] = math.radians(6.275)
                    target.rotation_euler[2] = math.radians(99.65)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(44.3)
                    target.rotation_euler[1] = math.radians(-186.25)
                    target.rotation_euler[2] = math.radians(-99.65)

            #Finger1
            elif container == 'finger1':
                target.rotation_euler[1] = math.radians(0)
                target.rotation_euler[2] = math.radians(90)

                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-95.85)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(-84.1)

            elif container == 'finger11':
                target.rotation_euler[1] = math.radians(0)
                target.rotation_euler[2] = math.radians(90)

                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-91.5)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(-88.45)

            elif container == 'finger12':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-91.5)
                    target.rotation_euler[1] = math.radians(-2)
                    target.rotation_euler[2] = math.radians(87.85)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(-88.45)
                    target.rotation_euler[1] = math.radians(-1.95)
                    target.rotation_euler[2] = math.radians(92.15)

            #Finger2
            elif container == 'finger2':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-85)
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = math.radians(90)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(-95)
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = math.radians(90)

            elif container == 'finger21':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(91.6)
                    target.rotation_euler[1] = math.radians(180)
                    target.rotation_euler[2] = math.radians(-90)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(88.5)
                    target.rotation_euler[1] = math.radians(180)
                    target.rotation_euler[2] = math.radians(-90)

            elif container == 'finger22':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-88.2)
                    target.rotation_euler[1] = math.radians(-9)
                    target.rotation_euler[2] = math.radians(89.05)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(-91.75)
                    target.rotation_euler[1] = math.radians(-8.95)
                    target.rotation_euler[2] = math.radians(90.93)

            #Finger3
            elif container == 'finger3':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-80)
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = math.radians(90)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(-100)
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = math.radians(90)

            elif container == 'finger31':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(95.5)
                    target.rotation_euler[1] = math.radians(180)
                    target.rotation_euler[2] = math.radians(-90)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(84.5)
                    target.rotation_euler[1] = math.radians(180)
                    target.rotation_euler[2] = math.radians(90)

            elif container == 'finger32':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-84)
                    target.rotation_euler[1] = math.radians(-13.85)
                    target.rotation_euler[2] = math.radians(88)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(-96)
                    target.rotation_euler[1] = math.radians(-13.75)
                    target.rotation_euler[2] = math.radians(91.95)

            #Finger4
            elif container == 'finger4':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-91.75)
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = math.radians(90)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(-88.2)
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = math.radians(90)

            elif container == 'finger41':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(90)
                    target.rotation_euler[1] = math.radians(180)
                    target.rotation_euler[2] = math.radians(-90)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(90.6)
                    target.rotation_euler[1] = math.radians(180)
                    target.rotation_euler[2] = math.radians(-90)

            elif container == 'finger42':
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-97.05)
                    target.rotation_euler[1] = math.radians(-16.925)
                    target.rotation_euler[2] = math.radians(100.75)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(-83)
                    target.rotation_euler[1] = math.radians(-16.95)
                    target.rotation_euler[2] = math.radians(79.26)

        #Spine
        if vatproperties.retarget_center_preset == 'OP1':
            if container.count('spine') or container == 'neck':
                target.rotation_euler[2] = math.radians(90)

            elif container == 'head':
                target.rotation_euler[2] = math.radians(89.5)

            elif container == 'pelvis':
                target.rotation_euler[0] = 0

        elif vatproperties.retarget_center_preset == 'OP2':
            if container.count('spine') or container == 'neck':
                target.rotation_euler[2] = math.radians(90)

            elif container == 'head':
                target.rotation_euler[2] = math.radians(80)

            elif container == 'pelvis':
                target.rotation_euler[0] = math.radians(22)

        #Lower body
        if vatproperties.retarget_bottom_preset == 'OP1':
            if container == 'thigh':
                target.rotation_euler[1] = math.radians(-3)
                target.rotation_euler[2] = math.radians(90)

                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(85)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(95)
            
            elif container == 'calf':
                target.rotation_euler[1] = math.radians(3.5)
                target.rotation_euler[2] = math.radians(90)

                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(85)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(95)

            elif container == 'foot':
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = math.radians(90)

            elif container == 'toe':
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = math.radians(90)
                
                if bone.startswith('L_') or bone.endswith('_L'):
                    target.rotation_euler[0] = math.radians(-88)
                elif bone.startswith('R_') or bone.endswith('_R'):
                    target.rotation_euler[0] = math.radians(-96)

        elif vatproperties.retarget_bottom_preset == 'OP2':
            if container == 'thigh' or container == 'calf':
                target.rotation_euler[0] = 0
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = math.radians(90)
            elif container == 'foot':
                target.rotation_euler[0] = math.radians(90)
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = math.radians(90)

    def link(): #Organizes armature after empty creation

        def retarget(container, bone): #Creates empties and links them to Rigify armature/Source armature
            armature = bpy.data.objects['rig']
            
            #Retarget empties creation
            try:
                collection = bpy.data.collections["Retarget Empties ({})".format(utils.arm.name)[0:60]] #Name length limit
            except:
                collection = bpy.data.collections.new("Retarget Empties ({})".format(utils.arm.name)[0:60])
                bpy.context.scene.collection.children.link(collection)

            collection.hide_viewport = True

            #Creates base empty and links
            base = bpy.data.objects.new('base_{} ({})'.format(bone, utils.arm.name)[0:60], None)
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
            target = bpy.data.objects.new('target_{} ({})'.format(bone, utils.arm.name)[0:60], None)
            collection.objects.link(target)
            target.empty_display_type = 'SPHERE'

            #Parent to base
            base.parent = parent
            target.parent = base

            #Bone connection
            armature = bpy.data.objects[utils.arm.name]
            loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')
            loc.name = "Retarget Location"
            loc.target = target
            rot = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')
            rot.name = "Retarget Rotation"
            rot.target = target

            #Counterweight for the small bump applied to the calf
            if container == 'calf':
                #Creates driver so the calf follows the animation armature's scale
                driver = bpy.data.objects[target.name].driver_add('location')

                for index, driver in enumerate(driver):
                    armature = bpy.data.objects['rig']
                    #Parameters and target
                    variable = driver.driver.variables.new() #Creates new variable onto the shapekey
                    variable.name = "scale"
                    if index == 1:
                        driver.driver.expression = '0.1*' + variable.name
                    elif index == 2:
                        driver.driver.expression = '1*' + variable.name #Changes expression to created variable's name
                    variable.type = 'TRANSFORMS' #Changes type of variable to transform

                    target = variable.targets[0]
                    target.id = armature #Links variable to animation armature
                    target.transform_space = 'LOCAL_SPACE'
                    if index == 1:
                        target.transform_type = 'SCALE_Y'
                    elif index == 2:
                        target.transform_type = 'SCALE_X'

        #Creates parent for all bases for easier storage/manipulation
        parent = bpy.data.objects.new('parent_' + utils.arm.name, None)

        prefix = utils.arm.prefix

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
        
        for cat in utils.arm.symmetrical_bones:
            for container, bone in utils.arm.symmetrical_bones[cat].items():
                for bone in bone:
                    retarget(container, bone)
                    empty_rotation(container, bone, 0)

        for container, bone in utils.arm.central_bones.items():
            for bone in bone:
                retarget(container, bone)
                empty_rotation(container, bone, 1)

        #Connects parent to collection
        collection = bpy.data.collections["Retarget Empties ({})".format(utils.arm.name)[0:60]]
        collection.objects.link(parent)

        #Forces Rigify armature to use setup armature's scale
        scale = bpy.data.objects[utils.arm.animation_armature_name].scale

        #Renames armature to prior generated armature
        armature = bpy.data.objects['rig']
        armature.name = utils.arm.name + '.anim'
        armature.data.name = utils.arm.name_real.name + '.anim'
        armature.scale = scale

        #Overrides driver so it now follows animation armature
        driver = bpy.data.objects[utils.arm.name].driver_add('scale')

        for index, driver in enumerate(driver):
            #Parameters and target
            variable = driver.driver.variables[0] #Creates new variable onto the shapekey
            driver.driver.expression = variable.name #Changes expression to created variable's name

            target = variable.targets[0]
            target.id = armature #Links variable to animation armature

        #Deletes generated armature
        generate_armature('anim', 2)

        #Links to animation armature
        try:
            collection = bpy.data.collections['Animation Armature']
        except:
            collection = None
            
        if collection:
            collection.objects.link(armature)

        utils.arm.animation_armature = True
        utils.arm.animation_armature_setup = False
        utils.arm.animation_armature_name_full = armature
        utils.arm.animation_armature_name = armature.name
        utils.arm.animation_armature_real = armature.data

    def face_flex_setup(): #Sets up drivers for face flexes that will be controlled by face bones
        prefix = utils.arm.prefix
            
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

            del vertex

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
                if shapekey.count('AU17L+AU17R') or shapekey.count('AU26L+AU26R') or shapekey.count('AU27L+AU27R') or shapekey.count('AU27ZL+AU27ZR') or shapekey.count('AD30L') or shapekey.count('AD30R') or shapekey.count('AU22ZL+AU22ZR') or shapekey.count('AD96L') or shapekey.count('AD96R'):
                    new_shapekeys.append(shapekey)

                #Skips basis, redundant halfway close eye, reduntant halfway squint, reduntant harsher frown, redudant lower lip drop, reduntant halfway puckering level 1 and 2 mouth open and odd individual eye shapekeys
                elif shapekey.lower().count('basis') or shapekey.lower().count('base') or shapekey.count('AU22L+AU22R') or shapekey.count('AU20L+AU20R') or shapekey.count('AU6L+AU6R') or shapekey.count('AU18L+AU18R')or shapekey.count('AU26ZL+AU26ZR') or shapekey.count('AU25L+AU25R') or shapekey.count('AU22ZL+AU22ZR') or shapekey.count('lower_right') or shapekey.count('lower_left') or shapekey.count('upper_right') or shapekey.count('upper_left') or shapekey.count('lower_right.001') or shapekey.count('lower_left.001') or shapekey.count('upper_right.001') or shapekey.count('upper_left.001'):
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

            del left_shapekey
            del right_shapekey

            for shapekey in new_shapekeys:
                #Creates driver
                driver = object[shapekey].driver_add('value') #Creates new driver for shapekey

                #Parameters and target
                variable = driver.driver.variables.new() #Creates new variable onto the shapekey
                variable.name = "flex"
                driver.driver.expression = variable.name #Changes expression to created variable's name
                variable.type = 'TRANSFORMS' #Changes type of variable to transform

                target = variable.targets[0]
                target.id = bpy.data.objects[utils.arm.animation_armature_name] #Links variable to animation armature

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
                elif shapekey.count('f01') or shapekey.count('f02') or shapekey.count('f03') or shapekey.count('f04') or shapekey.count('AU42'):
                    
                    #f01 = Upper eyelids close
                    #f02 = Upper eyelids raise
                    #f03 = Lower eyelids drop
                    #f04 = Lower eyelids raise
                    #AU42 = Upper eyelids drop

                    target.transform_space = 'LOCAL_SPACE'
                    target.transform_type = 'LOC_Z'

                    if shapekey.count('f01'):
                        pass
                    elif shapekey.count('AU42'):
                        driver.driver.expression = variable.name + '/4'
                    else:
                        #Creates another driver controlled by the corresponding eye bone
                        variable2 = driver.driver.variables.new()
                        variable2.name = "eye"
                            
                        driver.driver.expression = variable.name + '+' + variable2.name + '/4' #Combines the old driver with the new driver, making the latter have less influence
                        variable2.type = 'TRANSFORMS'

                        target2 = variable2.targets[0]
                        target2.id = bpy.data.objects[utils.arm.animation_armature_name]

                        target2.transform_space = 'LOCAL_SPACE'
                        target2.transform_type = 'LOC_Z'

                    if shapekey.count('f01'):
                        if shapekey.endswith('_L'):
                            target.bone_target = "UpperEye_L"
                        elif shapekey.endswith('_R'):
                            target.bone_target = "UpperEye_R"
                    
                    elif shapekey.count('f02'):
                        if shapekey.endswith('_L'):
                            target.bone_target = "UpperEye_L"
                            target2.bone_target = 'EyeLeft'
                        elif shapekey.endswith('_R'):
                            target.bone_target = "UpperEye_R"
                            target2.bone_target = 'EyeRight'

                    elif shapekey.count('f03') or shapekey.count('f04'):
                        if shapekey.endswith('_L'):
                            target.bone_target = "LowerEye_L"
                            target2.bone_target = 'EyeLeft'
                        elif shapekey.endswith('_R'):
                            target.bone_target = "LowerEye_R"
                            target2.bone_target = 'EyeRight'

                    elif shapekey.count('AU42'):
                        if shapekey.endswith('_L'):
                            target.bone_target = 'EyeLeft'
                        elif shapekey.endswith('_R'):
                            target.bone_target = 'EyeRight'
                        
                    if shapekey.count('f01') or shapekey.count('f03') or shapekey.count('AU42'):
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
                            driver.modifiers[0].coefficients[1] = -3
                            object[shapekey].slider_max = 1.5
                        elif shapekey.count('AU17DL+AU17DR'):
                            driver.modifiers[0].coefficients[1] = 2

                    elif shapekey.count('AU32'):
                        target.transform_type = 'LOC_Y'
                        driver.modifiers[0].coefficients[1] = -2

                #Chin
                elif shapekey.count('AU17L+AU17R') or shapekey.count('AU26L+AU26R') or shapekey.count('AU27L+AU27R') or shapekey.count('AU27ZL+AU27ZR') or shapekey.count('AD30L') or shapekey.count('AD30R'):

                    #AU17L+AU17R = Chin raise (sort of)
                    #AU26L+AU26R = Chin drop
                    #AU27L+AU27R = Chin drop 2
                    #AU27ZL+AU27ZR = Full mouth open
                    #AD30L/R = Chin sideways

                    target.bone_target = "Chin" 
                    target.transform_space = 'LOCAL_SPACE'
                    
                    #Upwards/Downwards movement
                    if shapekey.count('AU17L+AU17R') or shapekey.count('AU26L+AU26R') or shapekey.count('AU27L+AU27R') or shapekey.count('AU27ZL+AU27ZR'):
                        target.transform_type = 'LOC_Z'

                        #Documentation (Since i may be the first human on earth to find and/or utilize this)
                        #driver.keyframe_points.add(count) = Add keyframe
                        #driver.keyframe_points[keyframe] = Keyframe
                        #driver.keyframe_points[0].co_ui[0] = Horizontal position
                        #driver.keyframe_points[0].co_ui[1] = Vertical position
                        #driver.keyframe_points[0].handle_(left/right) = Keyframe handle (Location and type)
                        #driver.keyframe_points[0].handle_(left/right)_type = Interpolation type

                        #Chin lowers
                        if shapekey.count('AU26L+AU26R'):
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

                        elif shapekey.count('AU27L+AU27R'):
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

                        #Mouth fully opens
                        elif shapekey.count('AU27ZL+AU27ZR'):
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

            del shapekey

            if utils.arm.eyes_material:
                for material in utils.arm.eyes_material:
                    material = bpy.data.objects[vatproperties.target_object.name].data.materials[material.name]

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
                    target.id = bpy.data.objects[utils.arm.animation_armature_name]
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
                    target.id = bpy.data.objects[utils.arm.animation_armature_name]
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

        for widget in ['Chin', 'MouthCorner', 'Cheek', 'LowerLip', 'MiddleLip', 'UpperLip', 'Nostril_L', 'Nostril_R', 'UpDown', 'Circle']:
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
    utils.arm.get_bones(False)

    if action == 0 or action == 1: #Usual creation/deletion
        generate_rigify(action)

    elif action == 2: #Creates empties and links it to Source armature, also creates widgets and setups facial flexes
        link()
        face_flex_setup()

    elif action == 3: #Empty rotation modification
        for cat in utils.arm.symmetrical_bones.keys():
            for container, bone in utils.arm.symmetrical_bones[cat].items():
                for bone in bone:
                    empty_rotation(container, bone, 0)

        for container, bone in utils.arm.central_bones.items():
            for bone in bone:
                empty_rotation(container ,bone, 1)