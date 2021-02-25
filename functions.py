import bpy

class Prefixes: #Container for other prefixes
    helper = 'hlp_'
    helper2 = 'ValveBiped.hlp_'
    attachment = 'ValveBiped.attachment_'
    other = 'ValveBiped.'

def create_armature(self, context): #Creates new armature class
    vatproperties = bpy.context.scene.vatproperties
    if vatproperties.target_armature:
        global arm
        #bpy.data.objects[vatproperties.target_armature.name]['vatidentifier'] = float(hash(vatproperties.target_armature.name))
        arm = Armature(vatproperties.target_armature)

''' #No clue how to make it work.
def get_hash(): #Gets unique identifier
    armature = [armature for armature in bpy.data.objects if armature['vatidentifier'] == float(hash(self.name))]
    if armature == vatproperties.target_armature:
        arm.name = armature.name
        arm.name_full = armature
        arm.name_real = armature.data
'''

class Armature: #Armature base

    def __init__(self, armature):
        #Basic armature information
        self.name = armature.name
        self.name_full = armature
        self.name_real = armature.data

        #Armature type, scheme and prefix
        self.scheme = -1 #-1 = No armature, 0 = Source, 1 = Blender, 2 = SFM, 3 = Custom 1, 4 = Custom 2
        self.sfm = False
        self.prefix = ''

        #Bone information
        self.full_bonelist = []
        self.symmetrical_bones = []
        self.central_bones = []
        self.helper_bones = []
        self.other_bones = []
        self.custom_bones = []

        #Additional information for operations

        #Constraints
        self.symmetry_left = False
        self.symmetry_right = False
        self.inverse_kinematics = False

        #Weight armature
        self.weight_armature = False
        self.weight_armature_name = None
        self.weight_armature_name_full = None
        self.weight_armature_real = None

        #Animation armature
        self.animation_armature = False
        self.animation_armature_setup = True
        self.animation_armature_name = None
        self.animation_armature_real = None
        self.facial_bones = []

        #Functions executed to gather previous information
        self.get_bones()
        if self.scheme != -1:
            self.get_scheme()
            self.get_armatures()
            self.get_constraints()
            self.set_groups()
            if self.helper_bones:
                self.set_procedural_bones()
        else:
            print("Empty armature, cannot proceed")
            
    def get_bones(self): #Builds bone lists
        armature = bpy.data.objects[self.name]

        if self.name:

            #Cleans bone list
            self.full_bonelist = []
            self.symmetrical_bones = []
            self.central_bones = []
            self.helper_bones = []
            self.other_bones = []
            self.custom_bones = []

            self.full_bonelist = armature.data.bones.keys() #Gets all bones in armature

            #Checks if bone list is empty
            if self.full_bonelist:
                for bone in self.full_bonelist:

                    #Custom prefixes
                    if vatproperties.custom_scheme_enabled and vatproperties.custom_scheme_prefix:
                        self.prefix = vatproperties.custom_scheme_prefix

                        if bone.startswith(self.prefix + bone.count('L_') == 0 or bone.count('R_') == 0 or bone.count('_L') == 0 or bone.count('_R') == 0):
                            if bone.count('L_') == 0 or bone.count('R_') == 0:
                                self.scheme = 3
                            elif bone.count('_L') == 0 or bone.count('L_') == 0:
                                self.scheme = 3
                            self.symmetrical_bones.append(bone.replace(self.prefix, ''))

                        elif bone.startswith(self.prefix):
                            self.central_bones.append(bone.replace(self.prefix, ''))

                    #Helper prefix
                    if bone.startswith('hlp_'): #Helper
                        self.helper_bones.append(bone.replace(Prefixes.helper, ''))

                    #Source and Blender prefixes
                    elif bone.startswith('ValveBiped.'):
                        vatproperties.sfm_armature = False
                        self.prefix = 'ValveBiped.Bip01_'

                        #Helper bones without helper prefix, differentiated with 's.'
                        if bone.count('Ulna') or bone.count('Wrist') or bone.count('Elbow') or bone.count('Knee') or bone.count('Trapezius') or bone.count('Quadricep') or bone.count('Bicep') or bone.count('Shoulder'):
                            self.helper_bones.append(bone.replace(self.prefix, 's.'))

                        #Strange L4D2 helper prefix, must be differentiated from the usual helper bone with 's2.'
                        elif bone.startswith('ValveBiped.hlp_'):
                            self.helper_bones.append(bone.replace('ValveBiped.hlp_', 's2.'))

                        #Attachment bone prefix. They are supposed to be in other bones instead
                        elif bone.startswith('ValveBiped.attachment'):
                            self.other_bones.append(bone.replace('ValveBiped.attachment_', 'a.'))

                        #Default prefix
                        elif bone.startswith(self.prefix + 'L_') or bone.startswith(self.prefix + 'R_'): #Symmetrical
                            self.scheme = 0
                            self.symmetrical_bones.append(bone.replace(self.prefix, ''))

                        #Blender prefix
                        elif bone.endswith('_L') or bone.endswith('_R'):
                            self.scheme = 1
                            self.symmetrical_bones.append(bone.replace('ValveBiped.Bip01_', ''))

                        #Central bones prefix
                        elif bone.startswith('ValveBiped.Bip01_'): #Central
                            self.central_bones.append(bone.replace('ValveBiped.Bip01_', ''))
                            
                        else: #Other
                            self.other_bones.append(bone.replace('ValveBiped.', ''))

                    #SFM prefix
                    elif bone.startswith('bip_'): # Central
                        vatproperties.sfm_armature = True
                        self.scheme = 2
                        self.sfm = True
                        self.prefix = 'bip_'

                        if bone.endswith('_L') or bone.endswith('_R'): #Symmetrical
                            self.symmetrical_bones.append(bone.replace('bip_', ''))

                        else:
                            self.central_bones.append(bone.replace('bip_', ''))

                    #No/Different prefix
                    else:
                        #Makes sure generated IK bones are not part of list
                        if bone.count('Pole'):
                            pass
                        else:
                            self.custom_bones.append(bone)

                #Unknown armature
                if self.symmetrical_bones == [] and self.central_bones == [] and self.other_bones == []:
                    self.scheme = -1

                #Final bone report
                print("Symmetrical bones:", self.symmetrical_bones)
                print("Central bones:", self.central_bones)
                print("Helper bones:", self.helper_bones)
                print("Other bones:", self.other_bones)
                print("Custom bones:", self.custom_bones)
        else:
            self.scheme = -1

    def get_scheme(self): #Gets current scheme
        armature = bpy.data.objects[self.name]

        for bone in self.symmetrical_bones:

            #If not an SFM armature, check if the armature has the Source or Blender armature
            if not self.sfm:
                bone = self.prefix + bone

                if bone.startswith('ValveBiped.Bip01_L_') or bone.startswith('ValveBiped.Bip01_R_'):
                    vatproperties.scheme = 0

                elif bone.endswith('_L') or bone.endswith('_R'):
                    vatproperties.scheme = 1
                
        #Final scheme report
        if not self.sfm:
            if vatproperties.scheme == 0:
                print("Current Scheme: Source")

            elif vatproperties.scheme == 1:
                print("Current Scheme: Blender")

        elif self.sfm:
            print("Current Scheme: Source (SFM)")

    def get_armatures(self): #Gets generated armatures for selected armature

        def get_weight_armature():
            try:
                self.weight_armature_name_full = bpy.data.objects[self.name + '.weight']
                self.weight_armature_name = self.weight_armature_name_full.name
                self.weight_armature_real = bpy.data.armatures[self.name_real.name + '.weight']
                self.weight_armature = True
                print("Weight armature detected")
            except:
                self.weight_armature = False
        
        def get_anim_armature():
            #Checks if it's a setup armature or a proper armature
            try:
                try:
                    self.animation_armature_name_full = bpy.data.objects[self.name + '.anim']
                    self.animation_armature_setup = False
                except:
                    self.animation_armature_name_full = bpy.data.objects[self.name + '.anim_setup']
                    self.animation_armature_setup = True

                self.animation_armature_name = self.animation_armature_name_full.name

                try:
                    self.animation_armature_real = bpy.data.armatures[self.name_real.name + '.anim']
                    self.animation_armature_setup = False
                except:
                    self.animation_armature_real = bpy.data.armatures[self.name_real.name + '.anim_setup']
                    self.animation_armature_setup = True

                self.animation_armature = True
                if self.animation_armature_setup:
                    print("Setup animation armature detected")
                elif not self.animation_armature_setup:
                    print("Animation armature detected")

            except:
                self.animation_armature = False

        get_weight_armature()
        get_anim_armature()

    def get_constraints(self): #Gets previously added constraints that have not been removed

        def get_symmetry(): 
            armature = bpy.data.objects[self.name]
            prefix = self.prefix

            for bone in self.symmetrical_bones:
                if bone.startswith('L_') or bone.endswith('_L'):
                    try:
                        armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Location']
                        armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Rotation']
                        self.symmetry_left = True
                    except:
                        self.symmetry_left = False

                elif bone.startswith('R_') or bone.endswith('_R'):
                    try:
                        armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Location']
                        armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Rotation']
                        self.symmetry_right = True
                    except:
                        self.symmetry_right = False
            
        def get_inversekinematics():
            armature = bpy.data.objects[self.name]
            prefix = self.prefix
            
            for bone in self.symmetrical_bones:
                if bone.count('Hand') or bone.count('Foot'):
                    try:
                        armature.pose.bones[prefix + bone].constraints['IK']
                        self.inverse_kinematics = True
                    except:
                        self.inverse_kinematics = False

        get_symmetry()
        get_inversekinematics()

    def set_groups(self): #Organizes bones by bone group and bone layers
        armature = bpy.data.objects[self.name]
        prefix = self.prefix

        #Checks if any groups exist already
        group = armature.pose.bone_groups.keys()

        if group == []:
            #Creates groups and sets their color
            for group, color in zip(['Center', 'Left Arm', 'Right Arm', 'Left Leg', 'Right Leg', 'Helpers', 'Others', 'Custom'], ['THEME03', 'THEME01', 'THEME04', 'THEME01', 'THEME04', 'THEME09','THEME10', 'THEME06']):
                armature.pose.bone_groups.new(name=group)
                armature.pose.bone_groups[group].color_set = color
                
            for bone in self.symmetrical_bones:

                #Arms
                if bone.count('Clavicle') or bone.count('Trapezius') or bone.count('UpperArm') or bone.count('Bicep') or bone.count('Forearm') or bone.count('Hand') or bone.count('Finger'):
                    if bone.startswith('L_') or bone.endswith('_L'):
                        armature.pose.bones[prefix + bone].bone_group_index = 1
                        armature.data.bones[prefix + bone].layers[1] = True
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        armature.pose.bones[prefix + bone].bone_group_index = 2
                        armature.data.bones[prefix + bone].layers[2] = True

                #Legs
                elif bone.count('Thigh') or bone.count('Calf') or bone.count('Foot') or bone.count('Toe'):
                    if bone.startswith('L_') or bone.endswith('_L'):
                        armature.pose.bones[prefix + bone].bone_group_index = 3
                        armature.data.bones[prefix + bone].layers[3] = True
                        armature.pose.bones
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        armature.pose.bones[prefix + bone].bone_group_index = 4
                        armature.data.bones[prefix + bone].layers[4] = True

                armature.data.bones[prefix + bone].layers[0] = False

            for bone in self.central_bones:
                armature.pose.bones[prefix + bone].bone_group_index = 0

            for bone in self.helper_bones:

                if bone.startswith('s.'):
                    prefix = self.prefix
                    armature.pose.bones[prefix + bone.replace('s.', '')].bone_group_index = 5
                    armature.data.bones[prefix + bone.replace('s.', '')].layers[5] = True
                    armature.data.bones[prefix + bone.replace('s.', '')].layers[0] = False

                #Special helper bones
                elif bone.startswith('s2.'): 
                    prefix = Prefixes.helper2
                    armature.pose.bones[prefix + bone.replace('s2.', '')].bone_group_index = 5
                    armature.data.bones[prefix + bone.replace('s2.', '')].layers[5] = True
                    armature.data.bones[prefix + bone.replace('s2.', '')].layers[0] = False
                else: #Helper bones
                    prefix = Prefixes.helper
                    armature.pose.bones[prefix + bone].bone_group_index = 5
                    armature.data.bones[prefix + bone].layers[5] = True
                    armature.data.bones[prefix + bone].layers[0] = False

            for bone in self.other_bones:

                #Weapon bones
                if bone.count('weapon'):
                    prefix = Prefixes.other
                    armature.pose.bones[prefix + bone].bone_group_index = 6
                    armature.data.bones[prefix + bone].layers[6] = True
                    armature.data.bones[prefix + bone].layers[0] = False

                #Attachments
                elif bone.startswith('a.'):
                    prefix = Prefixes.attachment
                    armature.pose.bones[prefix + bone.replace('a.', '')].bone_group_index = 6
                    armature.data.bones[prefix + bone.replace('a.', '')].layers[6] = True
                    armature.data.bones[prefix + bone.replace('a.', '')].layers[0] = False
                else: #Others
                    prefix = Prefixes.other
                    armature.pose.bones[prefix + bone].bone_group_index = 6
                    armature.data.bones[prefix + bone].layers[6] = True
                    armature.data.bones[prefix + bone].layers[0] = False

            #Custom bones
            for bone in self.custom_bones:
                armature.pose.bones[bone].bone_group_index = 7
                armature.data.bones[bone].layers[7] = True
                armature.data.bones[bone].layers[0] = False

            #Reveals used layers
            for i in [0,1,2,3,4,5,6,7]:
                armature.data.layers[i] = True

            print("Bone groups set!")
            
    def set_procedural_bones(self):
        armature = bpy.data.objects[self.name]
        prefix = self.prefix

        #Gets position for helper bone transforms
        for bone in self.symmetrical_bones:
            if bone.count('Hand'):
                if bone.startswith('L_') or bone.endswith('_L'):
                    hand_l = armature.pose.bones[prefix + bone]
                elif bone.startswith('R_') or bone.endswith('_R'):
                    hand_r = armature.pose.bones[prefix + bone]
            elif bone.count('Forearm'):
                if bone.startswith('L_') or bone.endswith('_L'):
                    forearm_l = armature.pose.bones[prefix + bone]
                elif bone.startswith('R_') or bone.endswith('_R'):
                    forearm_r = armature.pose.bones[prefix + bone]
            elif bone.count('Calf'):
                if bone.startswith('L_') or bone.endswith('_L'):
                    calf_l = armature.pose.bones[prefix + bone]
                elif bone.startswith('R_') or bone.endswith('_R'):
                    calf_r = armature.pose.bones[prefix + bone]
            elif bone.count('Thigh'):
                if bone.startswith('L_') or bone.endswith('_L'):
                    thigh_l = armature.pose.bones[prefix + bone]
                elif bone.startswith('R_') or bone.endswith('_R'):
                    thigh_r = armature.pose.bones[prefix + bone]

        for bone in self.helper_bones:

            #Adds transforms to only these helper bones unless already existing
            if bone.title().count('Wrist') or bone.title().count('Ulna') or bone.title().count('Elbow') or bone.title().count('Knee') or bone.title().count('Quad'):
                new = 0
                if bone.startswith('s.'):
                    prefix = self.prefix
                    try:
                        transform = armature.pose.bones[prefix + bone.replace('s.', '')].constraints["Procedural Bone"]
                    except:
                        transform = armature.pose.bones[prefix + bone.replace('s.', '')].constraints.new('TRANSFORM')
                        new = 1

                elif bone.startswith('s2.'):
                    prefix = Prefixes.helper2
                    try:
                        transform = armature.pose.bones[prefix + bone.replace('s2.', '')].constraints["Procedural Bone"]
                    except:
                        transform = armature.pose.bones[prefix + bone.replace('s2.', '')].constraints.new('TRANSFORM')
                        new = 1
                else:
                    try:
                        transform = armature.pose.bones[prefix + bone].constraints["Procedural Bone"]
                    except:
                        transform = armature.pose.bones[prefix + bone].constraints.new('TRANSFORM')
                        new = 1

                if new == 1:
                    #Initial parameters
                    transform.name = "Procedural Bone"
                    transform.target = self.name_full
                    transform.map_from = 'ROTATION'
                    transform.map_to = 'ROTATION'
                    transform.target_space = 'LOCAL'
                    transform.owner_space = 'LOCAL'
                
                    #Hand rotation
                    if bone.title().count('Wrist') or bone.title().count('Ulna'):
                        transform.from_min_x_rot = math.radians(-90)
                        transform.from_max_x_rot = math.radians(90)

                        if bone.startswith('s.'):
                            if bone.replace('s.', '').title().startswith('L_') or bone.replace('s.', '').title().endswith('_L'):
                                transform.subtarget = hand_l.name
                            elif bone.replace('s.', '').title().startswith('R_') or bone.replace('s.', '').title().endswith('_R'):
                                transform.subtarget = hand_r.name
                        elif bone.startswith('s2.'):
                            if bone.replace('s2.', '').title().startswith('L_') or bone.replace('s2.', '').title().endswith('_L'):
                                transform.subtarget = hand_l.name
                            elif bone.replace('s2.', '').title().startswith('R_') or bone.replace('s2.', '').title().endswith('_R'):
                                transform.subtarget = hand_r.name

                        if bone.title().count('Wrist'):
                            transform.to_min_x_rot = math.radians(-75)
                            transform.to_max_x_rot = math.radians(75)

                            #Lame fix for Nick's left wrist bone not being labeled as left
                            if bone.replace('s2.', '').title().startswith('R_') or bone.replace('s2.', '').title().endswith('_R') or bone.replace('s2.', '').title().startswith('L_') or bone.replace('s2.', '').title().endswith('_L'):
                                pass
                            elif bone.replace('s2.', '').title().count('Wrist'):
                                transform.subtarget = hand_l.name

                        elif bone.title().count('Ulna'):
                            transform.to_min_x_rot = math.radians(-50)
                            transform.to_max_x_rot = math.radians(50)

                    #Forearm and thigh rotation
                    elif bone.title().count('Elbow') or bone.title().count('Knee') or bone.title().count('Quad'):
                        transform.from_min_z_rot = math.radians(-90)
                        transform.from_max_z_rot = math.radians(90)

                        transform.to_min_z_rot = math.radians(-45)
                        transform.to_max_z_rot = math.radians(45)
                        
                        if bone.title().count('Elbow'):
                            if bone.startswith('s.'):
                                if bone.replace('s.', '').title().startswith('L_') or bone.replace('s.', '').title().endswith('_L'):
                                    transform.subtarget = forearm_l.name
                                elif bone.replace('s.', '').title().startswith('R_') or bone.replace('s.', '').title().endswith('_R'):
                                    transform.subtarget = forearm_r.name
                            elif bone.startswith('s2.'):
                                if bone.replace('s2.', '').title().startswith('L_') or bone.replace('s2.', '').title().endswith('_L'):
                                    transform.subtarget = forearm_l.name
                                elif bone.replace('s2.', '').title().startswith('R_') or bone.replace('s2.', '').title().endswith('_R'):
                                    transform.subtarget = forearm_r.name

                        elif bone.title().count('Knee'):
                            if bone.startswith('s.'):
                                if bone.replace('s.', '').title().startswith('L_') or bone.replace('s.', '').title().endswith('_L'):
                                    transform.subtarget = calf_l.name
                                elif bone.replace('s.', '').title().startswith('R_') or bone.replace('s.', '').title().endswith('_R'):
                                    transform.subtarget = calf_r.name

                            elif bone.startswith('s2.'):
                                if bone.replace('s2.', '').title().startswith('L_') or bone.replace('s2.', '').title().endswith('_L'):
                                    transform.subtarget = calf_l.name
                                elif bone.replace('s2.', '').title().startswith('R_') or bone.replace('s2.', '').title().endswith('_R'):
                                    transform.subtarget = calf_r.name

                        elif bone.title().count('Quad'):
                            if bone.startswith('s.'):
                                if bone.replace('s.', '').title().startswith('L_') or bone.replace('s.', '').title().endswith('_L'):
                                    transform.subtarget = thigh_l.name
                                elif bone.replace('s.', '').title().startswith('R_') or bone.replace('s.', '').title().endswith('_R'):
                                    transform.subtarget = thigh_r.name
                            elif bone.startswith('s2.'):
                                if bone.replace('s2.', '').title().startswith('L_') or bone.replace('s2.', '').title().endswith('_L'):
                                    transform.subtarget = thigh_l.name
                                elif bone.replace('s2.', '').title().startswith('R_') or bone.replace('s2.', '').title().endswith('_R'):
                                    transform.subtarget = thigh_r.name

        if new == 1:
            print("Procedural bones configured!")

#Some functions (Namely creating new bones) do not add the newly created info to the object data until a mode change occurs at least once
def update(type, object = None):
    if type == 0: #Simple update, used for making new bones show up in data
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
    elif type == 1 and object: #Used to work with edit_bones, since it's not possible to use in anything other than edit mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT') #You're required to be in edit mode to use 'data.edit_bones', else there will be no bone info given.
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.mode_set(mode='EDIT')

def generate_armature(type, action): #Creates or deletes the weight armature
    real_armature = bpy.data.armatures[arm.name_real.name]
    
    #Creation
    if action == 0:

        #Weight armature datablock
        if type == 'weight':
            arm.weight_armature_real = real_armature.copy()
            arm.weight_armature_real.name = arm.name_real.name + '.weight'

            #Creation and link to current scene
            arm.weight_armature_name_full = bpy.data.objects.new(arm.name + '.weight', arm.weight_armature_real)
            arm.weight_armature = True
            arm.weight_armature_name = arm.weight_armature_name_full.name
            try:
                collection = bpy.data.collections['Weight Amature']
            except:
                collection = bpy.data.collections.new("Weight Armature")
                bpy.context.scene.collection.children.link(collection)
            collection.objects.link(arm.weight_armature_name_full)

            armature = bpy.data.objects[arm.weight_armature_name]
            
        #Animation armature datablock
        elif type == 'anim':
            arm.animation_armature_real = real_armature.copy()
            arm.animation_armature_real.name = arm.name_real.name + '.anim_setup'

            #Creation and link to current scene
            arm.animation_armature_name_full = bpy.data.objects.new(arm.name + '.anim_setup', arm.animation_armature_real)
            arm.animation_armature = True
            arm.animation_armature_name = arm.animation_armature_name_full.name
            try:
                collection = bpy.data.collections["Animation Armature"]
            except:
                collection = bpy.data.collections.new("Animation Armature")
                bpy.context.scene.collection.children.link(collection)
            collection.objects.link(arm.animation_armature_name_full)

            armature = bpy.data.objects[arm.animation_armature_name]
        
        #Variables for certain bones that require additional position tweaking
        ulna = []
        wrist = []
        bicep = []
        trapezius = []
        quadricep = []

        ulna_present = 0
        wrist_present = 0
        bicep_present = 0
        trapezius_present = 0
        quadricep_present = 0

        #Bone connection
        update(1, armature)

        #Keeps only the bare minimum bones for Rigify and connects the rest
        if type == 'anim':
            for bone in arm.helper_bones:
                if bone.startswith('s.'):
                    prefix = arm.prefix
                    ebone = armature.data.edit_bones[prefix + bone.replace('s.', '')]
                elif bone.startswith('s2.'):
                    prefix = Prefixes.helper2
                    ebone = armature.data.edit_bones[prefix + bone.replace('s2.', '')]
                else:
                    prefix = Prefixes.helper
                    ebone = armature.data.edit_bones[prefix + bone]
                    
                armature.data.edit_bones.remove(ebone)

        prefix = arm.prefix
    
        for bone in arm.symmetrical_bones:
            parent = armature.pose.bones[prefix + bone].parent.name

            #Makes it so the hand bone is facing straight
            if parent.count('Hand'):
                if bone.count('Finger0'):
                    pass
                else:
                    pbone = armature.pose.bones[prefix + bone].head
                    
                    armature.data.edit_bones[parent].tail.xz = pbone.x, pbone.z
                    armature.data.edit_bones[parent].length = 3
            else:
                loc = armature.pose.bones[prefix + bone].head
                armature.data.edit_bones[parent].tail = loc
                    
                #Bones that should not be connected to parent on weight armatures
                if type == 'weight':
                    if bone.count('Thigh') or bone.count('Clavicle') or bone.count('Forearm') or bone.count('Hand') or bone.count('Elbow') or bone.count('Wrist') or bone.count('UpperArm') or bone.count('Calf') or bone.count('Knee'):
                        pass
                    else:
                        armature.data.edit_bones[prefix + bone].use_connect = True
                #Bones that will not be connected to parent on anim armatures, the rest were deleted and would cause an error
                elif type == 'anim':
                    if bone.count('Thigh') or bone.count('Clavicle') or bone.count('Trapezius') or bone.count('Bicep') or bone.count('Elbow') or bone.count('Ulna') or bone.count('Wrist') or bone.count('Knee') or bone.count('Quadricep'):
                        pass
                    else:
                        armature.data.edit_bones[prefix + bone].use_connect = True

            #Extends toe tip to be where the actual tip should be
            if bone.title().count('Toe'):
                pbone = armature.pose.bones[prefix + bone].head

                if bone.startswith('L_') or bone.endswith('_L'):
                    armature.data.edit_bones[prefix + bone].tail = pbone.x+0.5, pbone.y-2.5, pbone.z
                elif bone.startswith('R_') or bone.endswith('_R'):
                    armature.data.edit_bones[prefix + bone].tail = pbone.x-0.5, pbone.y-2.5, pbone.z

            #Fix for legs rotating the wrong way in most characters
            if type == 'anim':
                if bone.count('Calf'):
                    armature.data.edit_bones[prefix + bone].head.y = armature.data.edit_bones[prefix + bone].head.y - 1

        for bone in arm.central_bones:
            if bone.casefold() == 'pelvis': #No parent
                pass
            else:
                parent = armature.pose.bones[prefix + bone].parent.name
                loc = armature.pose.bones[prefix + bone].head
                armature.data.edit_bones[parent].tail = loc
                if bone.count('Neck'):
                    pass
                else:
                    armature.data.edit_bones[prefix + bone].use_connect = True
                
            #Extends head's length to be on par with actual head height
            if bone.casefold().count('head'):
                pbone = armature.pose.bones[prefix + bone].head
                
                armature.data.edit_bones[prefix + bone].tail = pbone.x, pbone.y, pbone.z+6

        if type == 'weight':
            for bone in arm.helper_bones:
                #Helper bones
                if bone.count('Knee'):
                    pbone = armature.pose.bones[prefix + bone.replace('s.', '')].tail

                    armature.data.edit_bones[prefix + bone.replace('s.', '')].tail.y = pbone.y-5

                if bone.count('Elbow'):
                    pbone = armature.pose.bones[prefix + bone.replace('s.', '')].tail

                    armature.data.edit_bones[prefix + bone.replace('s.', '')].tail.y = pbone.y+5

                #Other helper bones that need additional tweaking on their positioning
                if bone.count('Ulna'):
                    ulna.append(bone)
                    if bone.replace('s.', '').startswith('L_') or bone.replace('s.', '').endswith('_L'):
                        ulna_l = armature.pose.bones[prefix + bone.replace('s.', '')].head
                    elif bone.replace('s.', '').startswith('R_') or bone.replace('s.', '').endswith('_R'):
                        ulna_r = armature.pose.bones[prefix + bone.replace('s.', '')].head
                    ulna_present = 1
                
                if bone.count('Wrist'):
                    wrist.append(bone)
                    wrist_present = 1

                if bone.count('Bicep'):
                    bicep.append(bone)
                    if bone.replace('s.', '').startswith('L_') or bone.replace('s.', '').endswith('_L'):
                        bicep_l = armature.pose.bones[prefix + bone.replace('s.', '')].head
                    elif bone.replace('s.', '').startswith('R_') or bone.replace('s.', '').endswith('_R'):
                        bicep_r = armature.pose.bones[prefix + bone.replace('s.', '')].head
                    bicep_present = 1

                if bone.count('Trapezius'):
                    trapezius.append(bone)
                    trapezius_present = 1

                if bone.count('Quadricep'):
                    quadricep.append(bone)
                    if bone.replace('s.', '').startswith('L_') or bone.replace('s.', '').endswith('_L'):
                        quadricep_l = armature.pose.bones[prefix + bone.replace('s.', '')].head
                    elif bone.replace('s.', '').startswith('R_') or bone.replace('s.', '').endswith('_R'):
                        quadricep_r = armature.pose.bones[prefix + bone.replace('s.', '')].head
                    quadricep_present = 1
            
            #Gets certain bone positions and avoids some bones not using bicep or ulna's location when they should
            for bone in arm.symmetrical_bones:
                if bicep_present == 1:
                    #Gets position
                    if bone.count('Forearm'):
                        if bone.startswith('L_') or bone.endswith('_L'):
                            forearm_l = armature.pose.bones[prefix + bone].head
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            forearm_r = armature.pose.bones[prefix + bone].head

                    #Forces upperarm to use bicep position
                    if bone.count('UpperArm'):
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].tail = bicep_l
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].tail = bicep_r
                else:
                    if bone.count('Forearm'):
                        armature.data.edit_bones[prefix + bone].use_connect = True

                if ulna_present == 1 or wrist_present == 1:
                    #Gets position
                    if bone.count('Hand'):
                        if bone.startswith('L_') or bone.endswith('_L'):
                            hand_l = armature.pose.bones[prefix + bone].head
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            hand_r = armature.pose.bones[prefix + bone].head

                    #Forces forearm to use ulna position
                    if bone.count('Forearm'):
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].tail = ulna_l
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].tail = ulna_r
                else:
                    if bone.count('Hand'):
                        armature.data.edit_bones[prefix + bone].use_connect = True

                if quadricep_present == 1:
                    #Gets position
                    if bone.count('Calf'):
                        if bone.startswith('L_') or bone.endswith('_L'):
                            calf_l = armature.pose.bones[prefix + bone].head
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            calf_r = armature.pose.bones[prefix + bone].head
                        
                    #Forces thigh to use quadricep position
                    if bone.count('Thigh'):
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].tail = quadricep_l
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].tail = quadricep_r
                else:
                    if bone.count('Calf'):
                        armature.data.edit_bones[prefix + bone].use_connect = True

                if trapezius_present == 1:
                    if bone.count('UpperArm'):
                        if bone.startswith('L_') or bone.endswith('_L'):
                            upperarm_l = armature.pose.bones[prefix + bone].head
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            upperarm_r = armature.pose.bones[prefix + bone].head
                else:
                    if bone.count('UpperArm'):
                        armature.data.edit_bones[prefix + bone].use_connect = True

            #Tweaks positioning of some helper bones

            #Bicep repositioning
            if bicep:
                for bone in bicep:
                    if bone.startswith('s.'):
                        prefix = arm.prefix
                        bone = bone.replace('s.', '')
                    elif bone.startswith('s2.'):
                        prefix = Prefixes.helper2
                        bone = bone.replace('s2.', '')
                    else:
                        prefix = Prefixes.helper

                    if bone.startswith('L_') or bone.endswith('_L'):
                        armature.data.edit_bones[prefix + bone].tail = forearm_l
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        armature.data.edit_bones[prefix + bone].tail = forearm_r

            if trapezius:
                for bone in trapezius:
                    if bone.startswith('s.'):
                        prefix = arm.prefix
                        bone = bone.replace('s.', '')
                    elif bone.startswith('s2.'):
                        prefix = Prefixes.helper2
                        bone = bone.replace('s2.', '')
                    else:
                        prefix = Prefixes.helper

                    if bone.startswith('L_') or bone.endswith('_L'):
                        armature.data.edit_bones[prefix + bone].tail = upperarm_l
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        armature.data.edit_bones[prefix + bone].tail = upperarm_r

            if quadricep:
                for bone in quadricep:
                    if bone.startswith('s.'):
                        prefix = arm.prefix
                        bone = bone.replace('s.', '')
                    elif bone.startswith('s2.'):
                        prefix = Prefixes.helper2
                        bone = bone.replace('s2.', '')
                    else:
                        prefix = Prefixes.helper

                    if bone.startswith('L_') or bone.endswith('_L'):
                        armature.data.edit_bones[prefix + bone].tail = calf_l
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        armature.data.edit_bones[prefix + bone].tail = calf_r

            #Ulna and wrist repositioning
            if ulna or wrist:

                #If both ulna and wrist are present
                if ulna and wrist:
                    for bone in ulna:
                        if bone.startswith('s.'):
                            prefix = arm.prefix
                            bone = bone.replace('s.', '')
                        elif bone.startswith('s2.'):
                            prefix = Prefixes.helper2
                            bone = bone.replace('s2.', '')
                        else:
                            prefix = Prefixes.helper

                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].tail = hand_l
                            ulna_l = armature.pose.bones[prefix + bone].tail
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].tail = hand_r
                            ulna_r = armature.pose.bones[prefix + bone].tail
                        
                        armature.data.edit_bones[prefix + bone].length = armature.data.edit_bones[prefix + bone].length / 1.6

                    update(0)

                    for bone in wrist:
                        if bone.startswith('s.'):
                            prefix = arm.prefix
                            bone = bone.replace('s.', '')
                        elif bone.startswith('s2.'):
                            prefix = Prefixes.helper2
                            bone = bone.replace('s2.', '')
                        else:
                            prefix = Prefixes.helper

                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].head = ulna_l
                            armature.data.edit_bones[prefix + bone].tail = hand_l
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].head = ulna_r
                            armature.data.edit_bones[prefix + bone].tail = hand_r

                #Else if only ulna is present
                elif ulna:
                    for bone in ulna:
                        if bone.startswith('s.'):
                            prefix = arm.prefix
                            bone = bone.replace('s.', '')
                        elif bone.startswith('s2.'):
                            prefix = Prefixes.helper2
                            bone = bone.replace('s2.', '')
                        else:
                            prefix = Prefixes.helper

                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].tail = hand_l
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].tail = hand_r

                #Else if only wrist is present
                elif wrist:
                    for bone in arm.symmetrical_bones:
                        if bone.count('Forearm'):
                            armature.data.edit_bones[prefix + bone].length = armature.data.edit_bones[prefix + bone].length / 1.3
                            if bone.startswith('L_') or bone.endswith('_L'):
                                forearm_l = armature.pose.bones[prefix + bone].tail
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                forearm_r = armature.pose.bones[prefix + bone].tail

                    update(0)

                    for bone in wrist:
                        if bone.startswith('s.'):
                            prefix = arm.prefix
                            bone = bone.replace('s.', '')
                        elif bone.startswith('s2.'):
                            prefix = Prefixes.helper2
                            bone = bone.replace('s2.', '')
                        else:
                            prefix = Prefixes.helper

                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].head = forearm_l
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].head = forearm_r

        #Removes unimportant bones such as weapon or attachment bones
        if arm.other_bones:
            for bone in arm.other_bones:
                if bone.count('weapon'):
                    prefix = Prefixes.other
                    bone = armature.data.edit_bones[prefix + bone]
                    armature.data.edit_bones.remove(bone)
                elif bone.startswith('a.'):
                    prefix = Prefixes.attachment
                    bone = armature.data.edit_bones[prefix + bone.replace('a.', '')]
                    armature.data.edit_bones.remove(bone)
                elif bone.count('forward'):
                    prefix = Prefixes.other
                    bone = armature.data.edit_bones[prefix + bone]
                    armature.data.edit_bones.remove(bone)

        #Removes pole bones if simple IK was used prior and not removed
        if arm.inverse_kinematics:
            for bone in ['ForearmPole_L', 'ForearmPole_R', 'CalfPole_L', 'CalfPole_R']:
                bone = armature.data.edit_bones[bone]
                armature.data.edit_bones.remove(bone)

        #Final touches to the armature
        armature.data.display_type = 'OCTAHEDRAL'
        armature.data.show_bone_custom_shapes = False
            
        armature.show_in_front = 1

        bpy.ops.object.mode_set(mode='OBJECT')

    #Deletion    
    elif action == 1 or action == 2:

        #Checks if they weren't deleted already
        if type == 'weight':
            try:
                bpy.data.objects.remove(arm.weight_armature_name_full)
            except:
                print("Weight armature already deleted, cleaning rest")
            try:
                bpy.data.armatures.remove(arm.weight_armature_real)
            except:
                pass

            #Gets collection and removes if it's empty
            try:
                collection = bpy.data.collections['Weight Armature']
            except:
                collection = None

            if collection:
                if collection.objects.keys() == []:
                    bpy.data.collections.remove(collection)

            arm.weight_armature = False
            arm.weight_armature_name = None
            arm.weight_armature_name_full = None
            arm.weight_armature_real = None
            
        elif type == 'anim':
            try:
                bpy.data.objects.remove(arm.animation_armature_name_full)
            except:
                print("Animation armature already deleted, cleaning rest")
            try:
                bpy.data.armatures.remove(arm.animation_armature_real)
            except:
                pass

            #Gets collection and removes if it's empty
            try:
                collection = bpy.data.collections['Animation Armature']
            except:
                collection = None

            if collection:
                if collection.objects.keys() == []:
                    bpy.data.collections.remove(collection)

            #Checks if retarget empties are present, if so, remove them
            if action == 1:
                try:
                    collection = bpy.data.collections["Retarget Empties ({})".format(arm.name)]
                except:
                    collection = None

                if collection:
                    for object in collection.objects.keys():
                        object = bpy.data.objects[object]
                        bpy.data.objects.remove(object)

                    bpy.data.collections.remove(collection)

                armature = bpy.data.objects[arm.name]
                prefix = arm.prefix

                #Removes original armature constraints
                for bone in arm.symmetrical_bones:
                    try:
                        loc = armature.pose.bones[prefix + bone].constraints["Retarget Location"]
                        armature.pose.bones[prefix + bone].constraints.remove(loc)
                    except:
                        pass
                        
                    try:
                        rot = armature.pose.bones[prefix + bone].constraints["Retarget Rotation"]
                        armature.pose.bones[prefix + bone].constraints.remove(rot)
                    except:
                        pass

                for bone in arm.central_bones:
                    try:
                        loc = armature.pose.bones[prefix + bone].constraints["Retarget Location"]
                        armature.pose.bones[prefix + bone].constraints.remove(loc)
                    except:
                        pass
                        
                    try:
                        rot = armature.pose.bones[prefix + bone].constraints["Retarget Rotation"]
                        armature.pose.bones[prefix + bone].constraints.remove(rot)
                    except:
                        pass

            arm.animation_armature = False
            arm.animation_armature_name = None
            arm.animation_armature_name_full = None
            arm.animation_armature_real = None
            
        #Reselects original armature for the sake of convenience
        armature = bpy.data.objects[arm.name]

        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature