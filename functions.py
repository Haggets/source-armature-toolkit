import bpy

class Prefixes: #Container for other prefixes
    helper = "hlp_"
    helper2 = "ValveBiped.hlp_"
    attachment = "ValveBiped.attachment_"
    other = "ValveBiped."

def create_armature(self, context): #Creates new armature class
    global vatproperties
    vatproperties = bpy.context.scene.vatproperties
    if vatproperties.target_armature != None:
        global arm
        arm = Armature(vatproperties.target_armature)

class Armature: #Armature base

    def __init__(self, armature):
        #Basic armature information
        self.name = armature.name
        self.name_full = armature
        self.name_real = armature.data

        #Armature type, scheme and prefix
        self.scheme = -1 #-1 = No armature, 0 = Source, 1 = Blender, 2 = SFM, 3 = Custom 1, 4 = Custom 2
        self.sfm = False
        self.prefix = ""

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

        #Functions executed to gather previous information
        self.get_bones()
        self.get_scheme()
        self.get_armatures()
        self.get_constraints()
        self.set_groups()
        if self.helper_bones != []:
            self.set_procedural_bones()
        
    def get_bones(self): #Builds bone lists
        armature = bpy.data.objects[self.name]

        if self.name != "":

            #Cleans bone list
            self.full_bonelist = []
            self.symmetrical_bones = []
            self.central_bones = []
            self.helper_bones = []
            self.other_bones = []
            self.custom_bones = []

            self.full_bonelist = armature.data.bones.keys() #Gets all bones in armature

            for bone in self.full_bonelist:

                #Custom prefixes
                if vatproperties.custom_scheme_enabled == True and vatproperties.custom_scheme_prefix != "":
                    self.prefix = vatproperties.custom_scheme_prefix

                    if bone.startswith(self.prefix + bone.count("L_") == 0 or bone.count("R_") == 0 or bone.count("_L") == 0 or bone.count("_R") == 0):
                        if bone.count("L_") == 0 or bone.count("R_") == 0:
                            self.scheme = 3
                        elif bone.count("_L") == 0 or bone.count("L_") == 0:
                            self.scheme = 3
                        self.symmetrical_bones.append(bone.replace(self.prefix, ""))

                    elif bone.startswith(self.prefix):
                        self.central_bones.append(bone.replace(self.prefix, ""))

                #Helper prefix
                if bone.startswith("hlp_"): #Helper
                    self.helper_bones.append(bone.replace(Prefixes.helper, ""))

                #Source and Blender prefixes
                elif bone.startswith("ValveBiped."):
                    vatproperties.sfm_armature = False
                    self.prefix = "ValveBiped.Bip01_"

                    #Helper bones without helper prefix, differentiated with "s."
                    if bone.count("Ulna") != 0 or bone.count("Wrist") != 0 or bone.count("Elbow") != 0 or bone.count("Knee") != 0 or bone.count("Trapezius") != 0 or bone.count("Quadricep") != 0 or bone.count("Bicep") != 0 or bone.count("Shoulder") != 0:
                        self.helper_bones.append(bone.replace(self.prefix, "s."))

                    #Strange L4D2 helper prefix, must be differentiated from the usual helper bone with "s2."
                    elif bone.startswith("ValveBiped.hlp_"):
                        self.helper_bones.append(bone.replace("ValveBiped.hlp_", "s2."))

                    #Attachment bone prefix. They are supposed to be in other bones instead
                    elif bone.startswith("ValveBiped.attachment"):
                        self.other_bones.append(bone.replace("ValveBiped.attachment_", "a."))

                    #Default prefix
                    elif bone.startswith(self.prefix + "L_") or bone.startswith(self.prefix + "R_"): #Symmetrical
                        self.scheme = 0
                        self.symmetrical_bones.append(bone.replace(self.prefix, ""))

                    #Blender prefix
                    elif bone.endswith("_L") or bone.endswith("_R"):
                        self.scheme = 1
                        self.symmetrical_bones.append(bone.replace("ValveBiped.Bip01_", ""))

                    #Central bones prefix
                    elif bone.startswith("ValveBiped.Bip01_"): #Central
                        self.central_bones.append(bone.replace("ValveBiped.Bip01_", ""))
                        
                    else: #Other
                        self.other_bones.append(bone.replace("ValveBiped.", ""))

                #SFM prefix
                elif bone.startswith("bip_"): # Central
                    vatproperties.sfm_armature = True
                    self.scheme = 2
                    self.sfm = True
                    self.prefix = "bip_"

                    if bone.endswith("_L") or bone.endswith("_R"): #Symmetrical
                        self.symmetrical_bones.append(bone.replace("bip_", ""))

                    else:
                        self.central_bones.append(bone.replace("bip_", ""))

                #No/Different prefix
                else:
                    #Makes sure generated IK bones are not part of list
                    if bone.count("Pole") != 0:
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

    def get_scheme(self): #Gets current scheme
        armature = bpy.data.objects[self.name]

        for bone in self.symmetrical_bones:

            #If not an SFM armature, check if the armature has the Source or Blender armature
            if self.sfm == False:
                bone = self.prefix + bone

                if bone.startswith("ValveBiped.Bip01_L_") or bone.startswith("ValveBiped.Bip01_R_"):
                    vatproperties.scheme = 0

                elif bone.endswith("_L") or bone.endswith("_R"):
                    vatproperties.scheme = 1
                
        #Final scheme report
        if self.sfm == False:
            if vatproperties.scheme == 0:
                print("Current Scheme: Source")

            elif vatproperties.scheme == 1:
                print("Current Scheme: Blender")

        elif self.sfm == True:
            print("Current Scheme: Source (SFM)")

    def get_armatures(self): #Gets generated armatures for selected armature

        def get_weight_armature():
            try:
                self.weight_armature_name_full = bpy.data.objects[self.name + ".weight"]
                self.weight_armature_name = self.weight_armature_name_full.name
                self.weight_armature_real = bpy.data.armatures[self.name_real.name + ".weight"]
                self.weight_armature = True
                print("Weight armature detected")
            except:
                self.weight_armature = False
        
        def get_anim_armature():
            #Checks if it's a setup armature or a proper armature
            try:
                try:
                    self.animation_armature_name_full = bpy.data.objects[self.name + ".anim"]
                    self.animation_armature_setup = False
                except:
                    self.animation_armature_name_full = bpy.data.objects[self.name + ".anim_setup"]
                    self.animation_armature_setup = True

                self.animation_armature_name = self.animation_armature_name_full.name

                try:
                    self.animation_armature_real = bpy.data.armatures[self.name_real.name + ".anim"]
                    self.animation_armature_setup = False
                except:
                    self.animation_armature_real = bpy.data.armatures[self.name_real.name + ".anim_setup"]
                    self.animation_armature_setup = True

                self.animation_armature = True
                if self.animation_armature_setup == True:
                    print("Setup animation armature detected")
                elif self.animation_armature_setup == False:
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
                if bone.startswith("L_") or bone.endswith("_L"):
                    try:
                        armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Location']
                        armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Rotation']
                        self.symmetry_left = True
                    except:
                        self.symmetry_left = False

                elif bone.startswith("R_") or bone.endswith("_R"):
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
                if bone.count("Hand") != 0 or bone.count("Foot") != 0:
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
            for group, color in zip(["Center", "Left Arm", "Right Arm", "Left Leg", "Right Leg", "Helpers", "Others", "Custom"], ['THEME03', 'THEME01', 'THEME04', 'THEME01', 'THEME04', 'THEME09','THEME10', 'THEME06']):
                armature.pose.bone_groups.new(name=group)
                armature.pose.bone_groups[group].color_set = color
                
            for bone in self.symmetrical_bones:

                #Arms
                if bone.count("Clavicle") != 0 or bone.count("Trapezius") != 0 or bone.count("UpperArm") != 0 or bone.count("Bicep") != 0 or bone.count("Forearm") != 0 or bone.count("Hand") != 0 or bone.count("Finger") != 0:
                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.pose.bones[prefix + bone].bone_group_index = 1
                        armature.data.bones[prefix + bone].layers[1] = True
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        armature.pose.bones[prefix + bone].bone_group_index = 2
                        armature.data.bones[prefix + bone].layers[2] = True

                #Legs
                elif bone.count("Thigh") != 0 or bone.count("Calf") != 0 or bone.count("Foot") != 0 or bone.count("Toe") != 0:
                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.pose.bones[prefix + bone].bone_group_index = 3
                        armature.data.bones[prefix + bone].layers[3] = True
                        armature.pose.bones
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        armature.pose.bones[prefix + bone].bone_group_index = 4
                        armature.data.bones[prefix + bone].layers[4] = True

                armature.data.bones[prefix + bone].layers[0] = False

            for bone in self.central_bones:
                armature.pose.bones[prefix + bone].bone_group_index = 0

            for bone in self.helper_bones:

                if bone.startswith("s."):
                    prefix = self.prefix
                    armature.pose.bones[prefix + bone.replace("s.", "")].bone_group_index = 5
                    armature.data.bones[prefix + bone.replace("s.", "")].layers[5] = True
                    armature.data.bones[prefix + bone.replace("s.", "")].layers[0] = False

                #Special helper bones
                elif bone.startswith("s2."): 
                    prefix = Prefixes.helper2
                    armature.pose.bones[prefix + bone.replace("s2.", "")].bone_group_index = 5
                    armature.data.bones[prefix + bone.replace("s2.", "")].layers[5] = True
                    armature.data.bones[prefix + bone.replace("s2.", "")].layers[0] = False
                else: #Helper bones
                    prefix = Prefixes.helper
                    armature.pose.bones[prefix + bone].bone_group_index = 5
                    armature.data.bones[prefix + bone].layers[5] = True
                    armature.data.bones[prefix + bone].layers[0] = False

            for bone in self.other_bones:

                #Weapon bones
                if bone.count("weapon") != 0:
                    prefix = Prefixes.other
                    armature.pose.bones[prefix + bone].bone_group_index = 6
                    armature.data.bones[prefix + bone].layers[6] = True
                    armature.data.bones[prefix + bone].layers[0] = False

                #Attachments
                elif bone.startswith("a."):
                    prefix = Prefixes.attachment
                    armature.pose.bones[prefix + bone.replace("a.", "")].bone_group_index = 6
                    armature.data.bones[prefix + bone.replace("a.", "")].layers[6] = True
                    armature.data.bones[prefix + bone.replace("a.", "")].layers[0] = False
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
            if bone.count("Hand"):
                if bone.startswith("L_") or bone.endswith("_L"):
                    hand_l = armature.pose.bones[prefix + bone]
                elif bone.startswith("R_") or bone.endswith("_R"):
                    hand_r = armature.pose.bones[prefix + bone]
            elif bone.count("Forearm"):
                if bone.startswith("L_") or bone.endswith("_L"):
                    forearm_l = armature.pose.bones[prefix + bone]
                elif bone.startswith("R_") or bone.endswith("_R"):
                    forearm_r = armature.pose.bones[prefix + bone]
            elif bone.count("Calf") != 0:
                if bone.startswith("L_") or bone.endswith("_L"):
                    calf_l = armature.pose.bones[prefix + bone]
                elif bone.startswith("R_") or bone.endswith("_R"):
                    calf_r = armature.pose.bones[prefix + bone]
            elif bone.count("Thigh") != 0:
                if bone.startswith("L_") or bone.endswith("_L"):
                    thigh_l = armature.pose.bones[prefix + bone]
                elif bone.startswith("R_") or bone.endswith("_R"):
                    thigh_r = armature.pose.bones[prefix + bone]

        for bone in self.helper_bones:
            #Adds transforms to only these helper bones unless already existing
            if bone.count("Wrist") != 0 or bone.count("Ulna") != 0 or bone.count("Elbow") != 0 or bone.casefold().count("knee") != 0 or bone.count("Quadricep") != 0:
                new = 0
                if bone.startswith("s."):
                    prefix = self.prefix
                    try:
                        transform = armature.pose.bones[prefix + bone.replace("s.", "")].constraints["Procedural Bone"]
                    except:
                        transform = armature.pose.bones[prefix + bone.replace("s.", "")].constraints.new('TRANSFORM')
                        new = 1

                elif bone.startswith("s2."):
                    prefix = Prefixes.helper2
                    try:
                        transform = armature.pose.bones[prefix + bone.replace("s2.", "")].constraints["Procedural Bone"]
                    except:
                        transform = armature.pose.bones[prefix + bone.replace("s2.", "")].constraints.new('TRANSFORM')
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
                    if bone.count("Wrist") != 0 or bone.count("Ulna") != 0:
                        transform.from_min_x_rot = -1.5708
                        transform.from_max_x_rot = 1.5708

                        if bone.replace("s.", "").startswith("L_") or bone.replace("s.", "").endswith("_L"):
                            transform.subtarget = hand_l.name
                        elif bone.replace("s.", "").startswith("R_") or bone.replace("s.", "").endswith("_R"):
                            transform.subtarget = hand_r.name

                        if bone.count("Wrist") != 0:
                            transform.to_min_x_rot = -1.309
                            transform.to_max_x_rot = 1.309

                        elif bone.count("Ulna") != 0:
                            transform.to_min_x_rot = -0.872665
                            transform.to_max_x_rot = 0.872665

                    #Forearm and thigh rotation
                    elif bone.count("Elbow") != 0 or bone.casefold().count("knee") != 0 or bone.count("Quadricep") != 0:
                        transform.from_min_z_rot = -1.5708
                        transform.from_max_z_rot = 1.5708

                        transform.to_min_z_rot = -0.785398
                        transform.to_max_z_rot = 0.785398
                        
                        if bone.count("Elbow") != 0:
                            if bone.replace("s.", "").startswith("L_") or bone.replace("s.", "").endswith("_L"):
                                transform.subtarget = forearm_l.name
                            elif bone.replace("s.", "").startswith("R_") or bone.replace("s.", "").endswith("_R"):
                                transform.subtarget = forearm_r.name

                        #THE WAY THE CASE PROBLEM SHOULD BE SORTED
                        elif bone.title().count("Knee") != 0:
                            if bone.startswith("s."):
                                if bone.replace("s.", "").title().startswith("L_") or bone.replace("s.", "").title().endswith("_L"):
                                    transform.subtarget = calf_l.name
                                elif bone.replace("s.", "").title().startswith("R_") or bone.replace("s.", "").title().endswith("_R"):
                                    transform.subtarget = calf_r.name

                            elif bone.startswith("s2."):
                                if bone.replace("s2.", "").title().startswith("L_") or bone.replace("s.", "").title().endswith("_L"):
                                    transform.subtarget = calf_l.name
                                elif bone.replace("s2.", "").title().startswith("R_") or bone.replace("s.", "").title().endswith("_R"):
                                    transform.subtarget = calf_r.name

                        elif bone.count("Quadricep") != 0:
                            if bone.replace("s.", "").startswith("L_") or bone.replace("s.", "").endswith("_L"):
                                transform.subtarget = thigh_l.name
                            elif bone.replace("s.", "").startswith("R_") or bone.replace("s.", "").endswith("_R"):
                                transform.subtarget = thigh_r.name

        if new == 1:
            print("Procedural bones configured!")

def armature_rename(scheme): #Bone prefix/suffix repositioning

    def rename(bone):
        bpy.ops.object.mode_set(mode='OBJECT') #Forces object mode to avoid errors when being in edit mode

        #To which scheme
        if scheme == 1: #Source -> Blender
            if bone.startswith("L_"):
                armature.bones[prefix + bone].name = prefix + bone.replace("L_", "") + "_L"
            elif bone.startswith("R_"):
                armature.bones[prefix + bone].name = prefix + bone.replace("R_", "") + "_R"
            arm.scheme = 1
        elif scheme == 0: #Blender -> Source
            if bone.endswith("_L"):
                armature.bones[prefix + bone].name = prefix + "L_" + bone.replace("_L", "")
            elif bone.endswith("_R"):
                armature.bones[prefix + bone].name = prefix + "R_" + bone.replace("_R", "")
            arm.scheme = 0

    #Updates bone list in case it was modified
    arm.get_bones()

    prefix = arm.prefix
    armature = bpy.data.armatures[arm.name_real.name]
    for bone in arm.symmetrical_bones:
        rename(bone)
        
    if arm.helper_bones != []:
        for bone in arm.helper_bones:
            if bone.startswith("s."):
                prefix = arm.prefix
                rename(bone.replace("s.", ""))

            elif bone.startswith("s2."):

                #Their prefix is usually already in the end so they're left alone
                if bone.endswith("_L") or bone.endswith("_R"):
                    pass
                else:
                    prefix = Prefixes.helper2
                    rename(bone.replace("s2.", ""))

            else:
                prefix = Prefixes.helper
                rename(bone)

    #Renames generated armatures to be on par with the original armature

    #Renames weight armature
    if arm.weight_armature == True:
        armature = bpy.data.armatures[arm.weight_armature_real.name]
        for bone in arm.symmetrical_bones:
            rename(bone)

    #Renames animation armature
    if arm.animation_armature == True:
        armature = bpy.data.armatures[arm.animation_armature_real.name]
        for bone in arm.symmetrical_bones:
            rename(bone)

    arm.get_bones() #Refreshes bone list

def constraint_symmetry(action, side): #Creates symmetry by using constraints, keeping corrected roll value
    
    #Constraint checks
    loc = ""
    rot = ""

    #Variables for end report
    loc_bonelist = []
    rot_bonelist = []

    def getconstraint(bone):
        armature = bpy.data.objects[arm.name]

        nonlocal loc
        nonlocal rot

        try:
            loc = armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Location']
        except:
            loc = ""
        try:
            rot = armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Rotation']
        except:
            rot = ""

    def constraint(bone): 
        armature = bpy.data.objects[arm.name]
        
        getconstraint(bone) #Checks for already existing constraints
        
        nonlocal loc
        nonlocal rot
        nonlocal loc_bonelist
        nonlocal rot_bonelist

        #Creation
        if action == 0:
            
            #Location
            if loc == "":
                if side == 'OP1':
                    if bone.startswith("L_") or bone.endswith("_L"):
                        loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')
                        arm.symmetry_left = True
                elif side == 'OP2':
                    if bone.startswith("R_") or bone.endswith("_R"):
                        loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')
                        arm.symmetry_right = True

                if loc != "":
                    #Constraint parameters
                    loc.name = "Constraint Symmetry Location"
                    loc.target = armature
                    loc.invert_x = True
                    if side == 'OP1':
                        if bone.startswith("L_"):
                            loc.subtarget = prefix + "R_" + bone.replace("L_", "")
                        elif bone.endswith("_L"):
                            loc.subtarget = prefix + bone.replace("_L", "") + "_R"
                    elif side == 'OP2':
                        if bone.startswith("R_"):
                            loc.subtarget = prefix + "L_" + bone.replace("R_", "")
                        elif bone.startswith("_R"):
                            loc.subtarget = prefix + bone.replace("_R", "") + "_L"
            else:
                loc_bonelist.append(bone)

            #Rotation
            if rot == "":
                if side == 'OP1':
                    if bone.startswith("L_") or bone.endswith("_L"):
                        rot = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')
                        arm.symmetry_left = True
                elif side == 'OP2':
                    if bone.startswith("R_") or bone.endswith("_R"):
                        rot = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')
                        arm.symmetry_right = True
                    
                if rot != "":
                    #Constraint parameters
                    rot.name = "Constraint Symmetry Rotation"
                    rot.target = armature
                    rot.target_space = 'LOCAL'
                    rot.owner_space = 'LOCAL'
                    rot.invert_y = True
                    rot.invert_x = True
                    if side == 'OP1':
                        if bone.startswith("L_"):
                            rot.subtarget = prefix + "R_" + bone.replace("L_", "")
                        elif bone.endswith("_L"):
                            rot.subtarget = prefix + bone.replace("_L", "") + "_R"
                    elif side == 'OP2':
                        if bone.startswith("R_"):
                            rot.subtarget = prefix + "L_" + bone.replace("R_", "")
                        elif bone.endswith("_R"):
                            rot.subtarget = prefix + bone.replace("_R", "") + "_L"
            else:
                rot_bonelist.append(bone)
            
        #Deletion
        elif action == 1:
            armature = bpy.data.objects[arm.name]

            #Location
            if loc != "":
                if side == 'OP1':
                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.pose.bones[prefix + bone].constraints.remove(loc)
                        arm.symmetry_left = False
                elif side == 'OP2':
                    if bone.startswith("R_") or bone.endswith("_R"):
                        armature.pose.bones[prefix + bone].constraints.remove(loc)
                        arm.symmetry_right = False
            else:
                loc_bonelist.append(bone)

            #Rotation
            if rot != "":
                if side == 'OP1':
                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.pose.bones[prefix + bone].constraints.remove(rot)
                        arm.symmetry_left = False
                elif side == 'OP2':
                    if bone.startswith("R_") or bone.endswith("_R"):
                        armature.pose.bones[prefix + bone].constraints.remove(rot)
                        arm.symmetry_right = False
            else:
                rot_bonelist.append(bone)

    #Updates bone list in case it was modified
    arm.get_bones()

    prefix = arm.prefix
    for bone in arm.symmetrical_bones:
        constraint(bone)

    if arm.helper_bones != []:
        for bone in arm.helper_bones:
            if bone.startswith("s."):
                prefix = arm.prefix
                constraint(bone.replace("s.", ""))

            elif bone.startswith("s2."):
                prefix = Prefixes.helper2
                constraint(bone.replace("s2.", ""))
            else:
                prefix = Prefixes.helper
                constraint(bone)

    #If constraints could not be applied
    if loc_bonelist != []:
        if action == 0:
            print("Location constraints already exist for:", loc_bonelist)
        elif action == 1:
            print("Location constraints not found for:", loc_bonelist)
        
    if rot_bonelist != []:
        if action == 0:
            print("Rotation constraints already exist for:", rot_bonelist)
        elif action == 1:
            print("Rotation constraints not found for:", rot_bonelist)

def generate_armature(type, action): #Creates or deletes the weight armature
    real_armature = bpy.data.armatures[arm.name_real.name]
    
    #Creation
    if action == 0:

        #Weight armature datablock
        if type == "weight":
            arm.weight_armature_real = real_armature.copy()
            arm.weight_armature_real.name = arm.name_real.name + ".weight"

            #Creation and link to current scene
            arm.weight_armature_name_full = bpy.data.objects.new(arm.name + ".weight", arm.weight_armature_real)
            arm.weight_armature = True
            arm.weight_armature_name = arm.weight_armature_name_full.name
            try:
                collection = bpy.data.collections['Weight Armature']
            except:
                collection = bpy.data.collections.new("Weight Armature")
                bpy.context.scene.collection.children.link(collection)
            collection.objects.link(arm.weight_armature_name_full)

            armature = bpy.data.objects[arm.weight_armature_name]
            
        #Animation armature datablock
        elif type == "anim":
            arm.animation_armature_real = real_armature.copy()
            arm.animation_armature_real.name = arm.name_real.name + ".anim_setup"

            #Creation and link to current scene
            arm.animation_armature_name_full = bpy.data.objects.new(arm.name + ".anim_setup", arm.animation_armature_real)
            arm.animation_armature = True
            arm.animation_armature_name = arm.animation_armature_name_full.name
            try:
                collection = bpy.data.collections['Animation Armature']
            except:
                collection = bpy.data.collections.new("Animation Armature")
                bpy.context.scene.collection.children.link(collection)
            collection.objects.link(arm.animation_armature_name_full)

            armature = bpy.data.objects[arm.animation_armature_name]

        prefix = arm.prefix
        
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
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT') #You're required to be in edit mode to use "data.edit_bones", else there will be no bone info given.
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')

        for bone in arm.symmetrical_bones:
            parent = armature.pose.bones[prefix + bone].parent.name

            #Makes it so the hand bone is facing straight
            if parent.count("Hand") != 0:
                if bone.count("Finger0"):
                    pass
                else:
                    pbone = armature.pose.bones[prefix + bone].head
                    
                    armature.data.edit_bones[parent].tail.xz = pbone.x, pbone.z
                    armature.data.edit_bones[parent].length = 3
            else:

                #Keeps only the bare minimum bones for Rigify and connects the rest
                if type == "anim":
                    if bone.count("Trapezius") != 0 or bone.count("Bicep") != 0 or bone.count("Elbow") != 0 or bone.count("Ulna") != 0 or bone.count("Wrist") != 0 or bone.count("Knee") != 0 or bone.count("Quadricep") != 0:
                        ebone = armature.data.edit_bones[prefix + bone]
                        armature.data.edit_bones.remove(ebone)
                    else:
                        loc = armature.pose.bones[prefix + bone].head
                        armature.data.edit_bones[parent].tail = loc
                else:
                    loc = armature.pose.bones[prefix + bone].head
                    armature.data.edit_bones[parent].tail = loc
                    
                #Bones that should not be connected to parent on weight armatures
                if type == "weight":
                    if bone.count("Thigh") != 0 or bone.count("Clavicle") != 0 or bone.count("Forearm") != 0 or bone.count("Hand") != 0 or bone.count("Elbow") != 0 or bone.count("Wrist") or bone.count("UpperArm") or bone.count("Calf") != 0 or bone.count("Knee") != 0:
                        pass
                    else:
                        armature.data.edit_bones[prefix + bone].use_connect = True
                #Bones that will not be connected to parent on anim armatures, the rest were deleted and would cause an error
                elif type == "anim":
                    if bone.count("Thigh") != 0 or bone.count("Clavicle") != 0 or bone.count("Trapezius") != 0 or bone.count("Bicep") != 0 or bone.count("Elbow") != 0 or bone.count("Ulna") != 0 or bone.count("Wrist") != 0 or bone.count("Knee") != 0 or bone.count("Quadricep") != 0:
                        pass
                    else:
                        armature.data.edit_bones[prefix + bone].use_connect = True

            #Extends toe tip to be where the actual tip should be
            if bone.casefold().count("toe") != 0:
                pbone = armature.pose.bones[prefix + bone].head

                if bone.startswith("L_") or bone.endswith("_L"):
                    armature.data.edit_bones[prefix + bone].tail = pbone.x+0.5, pbone.y-2.5, pbone.z
                elif bone.startswith("R_") or bone.endswith("_R"):
                    armature.data.edit_bones[prefix + bone].tail = pbone.x-0.5, pbone.y-2.5, pbone.z

            if type == "weight":
                #Helper bones
                if bone.count("Knee") != 0:
                    pbone = armature.pose.bones[prefix + bone].tail

                    armature.data.edit_bones[prefix + bone].tail.y = pbone.y-5

                if bone.count("Elbow") != 0:
                    pbone = armature.pose.bones[prefix + bone].tail

                    armature.data.edit_bones[prefix + bone].tail.y = pbone.y+5

                #Other helper bones that need additional tweaking on their positioning
                if bone.count("Ulna") != 0:
                    ulna.append(bone)
                    if bone.startswith("L_") or bone.endswith("_L"):
                        ulna_l = armature.pose.bones[prefix + bone].head
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        ulna_r = armature.pose.bones[prefix + bone].head
                    ulna_present = 1
                
                if bone.count("Wrist") != 0:
                    wrist.append(bone)
                    wrist_present = 1

                if bone.count("Bicep") != 0:
                    bicep.append(bone)
                    if bone.startswith("L_") or bone.endswith("_L"):
                        bicep_l = armature.pose.bones[prefix + bone].head
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        bicep_r = armature.pose.bones[prefix + bone].head
                    bicep_present = 1

                if bone.count("Trapezius") != 0:
                    trapezius.append(bone)
                    trapezius_present = 1

                if bone.count("Quadricep") != 0:
                    quadricep.append(bone)
                    if bone.startswith("L_") or bone.endswith("_L"):
                        quadricep_l = armature.pose.bones[prefix + bone].head
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        quadricep_r = armature.pose.bones[prefix + bone].head
                    quadricep_present = 1

        for bone in arm.central_bones:
            if bone.casefold() == "pelvis": #No parent
                pass
            else:
                parent = armature.pose.bones[prefix + bone].parent.name
                loc = armature.pose.bones[prefix + bone].head
                armature.data.edit_bones[parent].tail = loc
                if bone.count("Neck") != 0:
                    pass
                else:
                    armature.data.edit_bones[prefix + bone].use_connect = True
                
            #Extends head's length to be on par with actual head height
            if bone.casefold().count("head") != 0:
                pbone = armature.pose.bones[prefix + bone].head
                
                armature.data.edit_bones[prefix + bone].tail = pbone.x, pbone.y, pbone.z+6

        if type == "weight":
            #Gets certain bone positions and avoids some bones not using bicep or ulna's location when they should
            for bone in arm.symmetrical_bones:
                if bicep_present == 1:
                    #Gets position
                    if bone.count("Forearm") != 0:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            forearm_l = armature.pose.bones[prefix + bone].head
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            forearm_r = armature.pose.bones[prefix + bone].head

                    #Forces upperarm to use bicep position
                    if bone.count("UpperArm") != 0:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            armature.data.edit_bones[prefix + bone].tail = bicep_l
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            armature.data.edit_bones[prefix + bone].tail = bicep_r
                else:
                    if bone.count("Forearm") != 0:
                        armature.data.edit_bones[prefix + bone].use_connect = True

                if ulna_present == 1 or wrist_present == 1:
                    #Gets position
                    if bone.count("Hand") != 0:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            hand_l = armature.pose.bones[prefix + bone].head
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            hand_r = armature.pose.bones[prefix + bone].head

                    #Forces forearm to use ulna position
                    if bone.count("Forearm") != 0:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            armature.data.edit_bones[prefix + bone].tail = ulna_l
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            armature.data.edit_bones[prefix + bone].tail = ulna_r
                else:
                    if bone.count("Hand") != 0:
                        armature.data.edit_bones[prefix + bone].use_connect = True

                if quadricep_present == 1:
                    #Gets position
                    if bone.count("Calf") != 0:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            calf_l = armature.pose.bones[prefix + bone].head
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            calf_r = armature.pose.bones[prefix + bone].head
                        
                    #Forces thigh to use quadricep position
                    if bone.count("Thigh") != 0:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            armature.data.edit_bones[prefix + bone].tail = quadricep_l
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            armature.data.edit_bones[prefix + bone].tail = quadricep_r
                else:
                    if bone.count("Calf") != 0:
                        armature.data.edit_bones[prefix + bone].use_connect = True

                if trapezius_present == 1:
                    if bone.count("UpperArm") != 0:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            upperarm_l = armature.pose.bones[prefix + bone].head
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            upperarm_r = armature.pose.bones[prefix + bone].head
                else:
                    if bone.count("UpperArm") != 0:
                        armature.data.edit_bones[prefix + bone].use_connect = True

            #Tweaks positioning of some helper bones

            #Bicep repositioning
            if bicep != []:
                for bone in bicep:
                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.data.edit_bones[prefix + bone].tail = forearm_l
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        armature.data.edit_bones[prefix + bone].tail = forearm_r

            if trapezius != []:
                for bone in trapezius:
                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.data.edit_bones[prefix + bone].tail = upperarm_l
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        armature.data.edit_bones[prefix + bone].tail = upperarm_r

            if quadricep != []:
                for bone in quadricep:
                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.data.edit_bones[prefix + bone].tail = calf_l
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        armature.data.edit_bones[prefix + bone].tail = calf_r

            #Ulna and wrist repositioning
            if ulna != [] or wrist != []:

                #If both ulna and wrist are present
                if ulna != [] and wrist != []:
                    for bone in ulna:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            armature.data.edit_bones[prefix + bone].tail = hand_l
                            ulna_l = armature.pose.bones[prefix + bone].tail
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            armature.data.edit_bones[prefix + bone].tail = hand_r
                            ulna_r = armature.pose.bones[prefix + bone].tail
                        
                        armature.data.edit_bones[prefix + bone].length = armature.data.edit_bones[prefix + bone].length / 1.6

                    #Mode change is required to update ulna's tail position (Since it was changed prior). If you know a better way please let me know.
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.mode_set(mode='EDIT')

                    for bone in wrist:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            armature.data.edit_bones[prefix + bone].head = ulna_l
                            armature.data.edit_bones[prefix + bone].tail = hand_l
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            armature.data.edit_bones[prefix + bone].head = ulna_r
                            armature.data.edit_bones[prefix + bone].tail = hand_r

                #Else if only ulna is present
                elif ulna != []:
                    for bone in ulna:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            armature.data.edit_bones[prefix + bone].tail = hand_l
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            armature.data.edit_bones[prefix + bone].tail = hand_r

                #Else if only wrist is present
                elif wrist != []:
                    for bone in arm.symmetrical_bones:
                        if bone.count("Forearm") != 0:
                            armature.data.edit_bones[prefix + bone].length = armature.data.edit_bones[prefix + bone].length / 1.3
                            if bone.startswith("L_") or bone.endswith("_L"):
                                forearm_l = armature.pose.bones[prefix + bone].tail
                            elif bone.startswith("R_") or bone.endswith("_R"):
                                forearm_r = armature.pose.bones[prefix + bone].tail

                    #Mode change is required to update ulna's tail position (Since it was changed prior). If you know a better way please let me know.
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.mode_set(mode='EDIT')

                    for bone in wrist:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            armature.data.edit_bones[prefix + bone].head = forearm_l
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            armature.data.edit_bones[prefix + bone].head = forearm_r

        if arm.other_bones != []:
            for bone in arm.other_bones:
                #Removes unimportant bones since they're of no use for the charactrer
                if bone.count("weapon") != 0:
                    prefix = Prefixes.other
                    bone = armature.data.edit_bones[prefix + bone]
                    armature.data.edit_bones.remove(bone)
                elif bone.startswith("a."):
                    prefix = Prefixes.attachment
                    bone = armature.data.edit_bones[prefix + bone.replace("a.", "")]
                    armature.data.edit_bones.remove(bone)
                elif bone.count("forward") != 0:
                    prefix = Prefixes.other
                    bone = armature.data.edit_bones[prefix + bone]
                    armature.data.edit_bones.remove(bone)

        #Removes pole bones if simple IK was used prior and not removed
        if arm.inverse_kinematics == True:
            for bone in ["ForearmPole_L", "ForearmPole_R", "CalfPole_L", "CalfPole_R"]:
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
        if type == "weight":
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

            if collection != None:
                if collection.objects.keys() == []:
                    bpy.data.collections.remove(collection)

            arm.weight_armature = False
            arm.weight_armature_name = None
            arm.weight_armature_name_full = None
            arm.weight_armature_real = None
            
        elif type == "anim":
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

            if collection != None:
                if collection.objects.keys() == []:
                    bpy.data.collections.remove(collection)

            #Checks if retarget empties are present, if so, remove them
            if action == 1:
                try:
                    collection = bpy.data.collections["Retarget Empties " + "(" + arm.name + ")"]
                except:
                    collection = None

                if collection != None:
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

def weight_armature(action): #Creates duplicate armature for more spread out weighting
        
    generate_armature("weight", action)
    print("Weight armature created!")

def inverse_kinematics(action): #Adds IK to the armature
    
    #Constraint checks
    ik_constraint = ""

    #Variables for finish report
    bonelist = []

    def getconstraint(bone):
        armature = bpy.data.objects[arm.name]

        nonlocal ik_constraint

        try:
            ik_constraint = armature.pose.bones[prefix + bone].constraints['IK']
        except:
            ik_constraint = ""

    def constraints(bone):
        armature = bpy.data.objects[arm.name]

        nonlocal bonelist
        nonlocal ik_constraint

        getconstraint(bone)

        #Creation
        if action == 0:

            if ik_constraint == "":
                if bone.startswith("L_") or bone.endswith("_L"):
                    ik = armature.pose.bones[prefix + bone].constraints.new('IK')
                    ik.chain_count = 3
                    ik.pole_target = arm.name_full
                    if bone.count("Hand"):
                        ik.pole_subtarget = "ForearmPole_L"
                    elif bone.count("Foot"):
                        ik.pole_subtarget = "CalfPole_L"
                elif bone.startswith("R_") or bone.endswith("_R"):
                    ik = armature.pose.bones[prefix + bone].constraints.new('IK')
                    ik.chain_count = 3
                    ik.pole_target = arm.name_full
                    if bone.count("Hand"):
                        ik.pole_subtarget = "ForearmPole_R"
                    elif bone.count("Foot"):
                        ik.pole_subtarget = "CalfPole_R"
                arm.inverse_kinematics = True
            else:
                bonelist.append(bone)
                
        #Deletion
        elif action == 1:

            if ik_constraint != "":
                if bone.startswith("L_") or bone.endswith("_L"):
                    armature.pose.bones[prefix + bone].constraints.remove(ik_constraint)
                elif bone.startswith("R_") or bone.endswith("_R"):
                    armature.pose.bones[prefix + bone].constraints.remove(ik_constraint)
                arm.inverse_kinematics = False
            else:
                bonelist.append(bone)

    def poles():
        armature = bpy.data.objects[arm.name]

        if action == 0:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT') #Apparently you're required to be in edit mode to use "data.edit_bones", else there will be no bone info given. Dumb
            armature.select_set(True)
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='EDIT')

            for bone in arm.central_bones:
                if bone.count("Pelvis") != 0:
                    pelvis = armature.data.edit_bones[prefix + bone]

            #Gets forearm and calf position
            for bone in arm.symmetrical_bones:
                if bone.count("Forearm") != 0:
                    forearm = armature.pose.bones[prefix + bone]
                elif bone.count("Calf") != 0:
                    calf = armature.pose.bones[prefix + bone]

            for bone in ["ForearmPole_L", "ForearmPole_R", "CalfPole_L", "CalfPole_R"]:
                ebone = armature.data.edit_bones.new(bone)
                ebone.use_deform = False
                ebone.parent = pelvis

                if bone.startswith("Forearm"):
                    if bone.endswith("_L"):
                        ebone.tail = -forearm.tail.x, forearm.tail.y+12, forearm.tail.z
                        ebone.head = -forearm.head.x, forearm.head.y+10, forearm.head.z
                    elif bone.endswith("_R"):
                        ebone.tail = forearm.tail.x, forearm.tail.y+12, forearm.tail.z
                        ebone.head = forearm.head.x, forearm.head.y+10, forearm.head.z
                elif bone.startswith("Calf"):
                    if bone.endswith("_L"):
                        ebone.tail = -calf.tail.x, calf.tail.y-10, calf.tail.z
                        ebone.head = -calf.head.x, calf.head.y-12, calf.head.z
                    elif bone.endswith("_R"):
                        ebone.tail = calf.tail.x, calf.tail.y-10, calf.tail.z
                        ebone.head = calf.head.x, calf.head.y-12, calf.head.z

            bpy.ops.object.mode_set(mode='OBJECT')

        elif action == 1:
            bpy.ops.object.mode_set(mode='EDIT')
            for bone in ["ForearmPole_L", "ForearmPole_R", "CalfPole_L", "CalfPole_R"]:
                ebone = armature.data.edit_bones[bone]
                armature.data.edit_bones.remove(ebone)
            bpy.ops.object.mode_set(mode='OBJECT')

    #Updates bone list in case it was modified
    arm.get_bones()

    prefix = arm.prefix

    poles()
    for bone in arm.symmetrical_bones:
        if bone.count("Hand") != 0 or bone.count("Foot") != 0:
            constraints(bone)
    
    #If constraints could not be applied
    if bonelist != []:
        if action == 0:
            print("IK constraints already exist for:")
            print(bonelist)
        elif action == 1:
            print("IK constraints not found for:")
            print(bonelist)

def anim_armature(action):

    def generate_rigify(): #Creates Rigify armature
        generate_armature("anim", action)
        
        if action == 0:
            armature = bpy.data.objects[arm.animation_armature_name]

            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT') 
            armature.select_set(True)
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='EDIT') #You're required to be in edit mode to use "data.edit_bones", else there will be no bone info given.

            #Hides all but the first layer
            for i in [1,2,3,5,4,6,7]:
                    armature.data.layers[i] = False

            #Rigify portion
            prefix = arm.prefix

            #Gets pelvis position and gets edit_bone name
            for bone in arm.central_bones:
                if bone.casefold() == "pelvis":
                    pelvis = armature.pose.bones[prefix + bone].head
                    epelvis = armature.data.edit_bones[prefix + bone]

            for bone in arm.symmetrical_bones:
                if bone.count("Foot") != 0:
                    if bone.startswith("L_") or bone.endswith("_L"):
                        foot_l = armature.pose.bones[prefix + bone].head
                        efoot_l = armature.data.edit_bones[prefix + bone]
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        foot_r = armature.pose.bones[prefix + bone].head
                        efoot_r = armature.data.edit_bones[prefix + bone]

            #Creates 2 pelvis bones for whatever Rigify does with em
            for bone in ["Pelvis_L", "Pelvis_R"]:
                ebone = armature.data.edit_bones.new(prefix + bone)

                ebone.head = pelvis
                ebone.parent = epelvis

                #New pelvis bone positioning
                if bone.startswith("L_") or bone.endswith("_L"):
                    ebone.tail.xyz = pelvis.x-3, pelvis.y-2, pelvis.z+4
                elif bone.startswith("R_") or bone.endswith("_R"):
                    ebone.tail.xyz = pelvis.x+3, pelvis.y-2, pelvis.z+4

            for bone in ["Heel_L", "Heel_R"]:
                ebone = armature.data.edit_bones.new(prefix + bone)

                if bone.endswith("_L"):
                    ebone.parent = efoot_l
                    ebone.tail.xyz = foot_l.x+1.5, foot_l.y+1, 0
                    ebone.head.xyz = foot_l.x-1.5, foot_l.y+1, 0
                    ebone.layers[13] = True
                    ebone.layers[0] = False
                elif bone.endswith("_R"):
                    ebone.parent = efoot_r
                    ebone.tail.xyz = foot_r.x-1.5, foot_r.y+1, 0
                    ebone.head.xyz = foot_r.x+1.5, foot_r.y+1, 0
                    ebone.layers[16] = True
                    ebone.layers[0] = False

            #Newly added bones are not added to the armature data until the user changes modes at least once, i know no other way around it. If you do please let me know.
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.mode_set(mode='EDIT')

            #Rigify parameters
            for bone in ["Pelvis_L", "Pelvis_R"]:
                pbone = armature.pose.bones[prefix + bone]
                ebone = armature.data.edit_bones[prefix + bone]
                
                pbone.rigify_type = "basic.super_copy"
                pbone.rigify_parameters.make_control = False
                ebone.layers[3] = True
                ebone.layers[0] = False

            for bone in arm.symmetrical_bones:

                #Bones deleted prior
                if bone.count("Trapezius") != 0 or bone.count("Bicep") != 0 or bone.count("Elbow") != 0 or bone.count("Ulna") != 0 or bone.count("Wrist") != 0 or bone.count("Knee") != 0 or bone.count("Quadricep") != 0:
                    pass
                else:
                    pbone = armature.pose.bones[prefix + bone]
                    param = pbone.rigify_parameters
                    ebone = armature.data.edit_bones[prefix + bone]

                #Placeholder layer must be 5 to avoid a big annoyance with Finger02 always being on layer 0 despite being extremely explicit about it, must be a Blender bug
                ebone.layers[5] = True

                for i in [1,2,3,4,5,6,7]:
                    ebone.layers[i] = False

                if bone.count("Finger") != 0:
                    ebone.layers[5] = True

                if bone.count("UpperArm") != 0 or bone.count("Forearm") != 0 or bone.count("Hand") != 0:
                    if bone.startswith("L_") or bone.endswith("_L"):
                        ebone.layers[7] = True
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        ebone.layers[10] = True

                if bone.count("Thigh") != 0 or bone.count("Calf") != 0 or bone.count("Foot") != 0 or bone.count("Toe") != 0:
                    if bone.startswith("L_") or bone.endswith("_L"):
                        ebone.layers[13] = True
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        ebone.layers[16] = True

                if bone.count("Clavicle") != 0:
                    pbone.rigify_type = "basic.super_copy"
                    param.make_widget = False
                    ebone.layers[3] = True

                if bone.count("UpperArm") != 0:
                    pbone.rigify_type = "limbs.super_limb"
                    param.tweak_layers[1] = False
                    param.fk_layers[1] = False

                    if bone.startswith("L_") or bone.endswith("_L"):
                        param.fk_layers[8] = True
                        param.tweak_layers[9] = True
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        param.fk_layers[11] = True
                        param.tweak_layers[12] = True
                    param.segments = 1

                if bone.count("Thigh") != 0:
                    pbone.rigify_type = "limbs.super_limb"
                    param.limb_type = 'leg'
                    param.tweak_layers[1] = False
                    param.fk_layers[1] = False

                    if bone.startswith("L_") or bone.endswith("_L"):
                        param.fk_layers[14] = True
                        param.tweak_layers[15] = True
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        param.fk_layers[17] = True
                        param.tweak_layers[18] = True
                    param.segments = 1

                ebone.layers[5] = False

            #Central
            for bone in arm.central_bones:
                pbone = armature.pose.bones[prefix + bone]
                param = pbone.rigify_parameters
                ebone = armature.data.edit_bones[prefix + bone]

                ebone.layers[3] = True

                if bone.count("Pelvis") != 0:
                    pbone.rigify_type = "spines.basic_spine"
                    param.pivot_pos = 2
                    param.tweak_layers[1] = False
                    param.tweak_layers[4] = True
                    param.fk_layers[1] = False
                    param.fk_layers[4] = True

                if bone.count("Neck1") != 0:
                    pbone.rigify_type = "spines.super_head"
                    param.connect_chain = True
                    param.tweak_layers[1] = False
                    param.tweak_layers[4] = True
                
                ebone.layers[0] = False

            armature = bpy.data.armatures[arm.animation_armature_real.name]

            #Creates bone groups
            for group in ['Root', 'IK', 'Special', 'Tweak', 'FK', 'Extra']:
                color = armature.rigify_colors.add()
                color.name = group

                armature.rigify_colors[group].select = (0.3140000104904175, 0.7839999794960022, 1.0)
                armature.rigify_colors[group].active = (0.5490000247955322, 1.0, 1.0)
                armature.rigify_colors[group].standard_colors_lock = True

                if group == "Root":
                    armature.rigify_colors[group].normal = (0.43529415130615234, 0.18431372940540314, 0.41568630933761597)
                if group == "IK":
                    armature.rigify_colors[group].normal = (0.6039215922355652, 0.0, 0.0)
                if group== "Special":
                    armature.rigify_colors[group].normal = (0.9568628072738647, 0.7882353663444519, 0.0470588281750679)
                if group== "Tweak":
                    armature.rigify_colors[group].normal = (0.03921568766236305, 0.21176472306251526, 0.5803921818733215)
                if group== "FK":
                    armature.rigify_colors[group].normal = (0.11764706671237946, 0.5686274766921997, 0.03529411926865578)
                if group== "Extra":
                    armature.rigify_colors[group].normal = (0.9686275124549866, 0.250980406999588, 0.0941176563501358)

            #Creates layers
            for i in range(0,29):
                armature.rigify_layers.add()

            #Rigify layers
            names = ["Torso", "Torso (Tweak)", "Fingers", "Fingers (Detail)", "Arm.L (IK)", "Arm.L (FK)", "Arm.L (Tweak)", "Arm.R (IK)", "Arm.R (FK)", "Arm.R (Tweak)", "Leg.L (IK)", "Leg.L (FK)", "Leg.L (Tweak)", "Leg.R (IK)", "Leg.R (FK)", "Leg.R (Tweak)"]

            row_groups = [3,4,5,6,7,8,9,7,8,9,10,11,12,10,11,12]

            layer_groups = [3,4,6,5,2,5,4,2,5,4,2,5,4,2,5,4]

            for i, name, row, group in zip(range(3,19), names, row_groups, layer_groups):
                armature.rigify_layers[i].name = name
                armature.rigify_layers[i].row = row
                armature.rigify_layers[i].group = group

            armature.layers[0] = False

            arm.animation_armature_setup = True

            for i in [3,5,7,10,13,16]:
                    armature.layers[i] = True

            bpy.ops.object.mode_set(mode='OBJECT')

            print("Animation armature created!")

    def empty_rotation(bone, type): #Sets empty rotation
        prefix = arm.prefix

        base = bpy.data.objects["base_" + prefix + bone]
        target = bpy.data.objects["target_" + prefix + bone]
        #Sets rotation

        #For reference:
        #1.5707963705062866 = 90°
        #3.1415927410125732 = 180°

        #Default empty rotation, fit for most bones
        if type == 0: #Symmetrical bones default
            target.rotation_euler[0] = 1.5707963705062866 #90°
            target.rotation_euler[1] = 3.1415927410125732 #180°
            target.rotation_euler[2] = -1.5707963705062866 #-90°
        elif type == 1: #Center bones default
            target.rotation_euler[0] = 0
            target.rotation_euler[1] = 0
            target.rotation_euler[2] = 0
        
        #Upper body
        if vatproperties.retarget_top_preset == 'OP1':
            if bone.count("Clavicle") != 0:
                if bone.startswith("L_") or bone.endswith("_L"):
                    target.rotation_euler[0] = -1.832595705986023 #-105°
                elif bone.startswith("R_") or bone.endswith("_R"):
                    target.rotation_euler[0] = 1.832595705986023 #105°

        elif vatproperties.retarget_top_preset == 'OP2':
            if bone.count("Clavicle") != 0:
                if bone.startswith("L_") or bone.endswith("_L"):
                    target.rotation_euler[0] = -1.5707963705062866 #-90°
                elif bone.startswith("R_") or bone.endswith("_R"):
                    pass

        #More specific empty rotations for bones that don't fit the default rotation
        if bone.count("Hand") != 0:
            if bone.startswith("L_") or bone.endswith("_L"):
                target.rotation_euler[0] = 2.96705961227417 #170°
                target.rotation_euler[1] = 3.2288591861724854 #185°
                target.rotation_euler[2] = -1.6057029962539673 #-92
            elif bone.startswith("R_") or bone.endswith("_R"):
                target.rotation_euler[0] = 0.1745329201221466 #10°
                target.rotation_euler[1] = 3.2288591861724854 #185°
                target.rotation_euler[2] = -1.535889744758606 #-88°

        elif bone.count("Finger") != 0:
            #Makes them smaller for the sake of readability
            base.empty_display_size = 0.5
            target.empty_display_size = 0.5

            if bone.count("Finger0") != 0:
                if bone.startswith("L_") or bone.endswith("_L"):
                    target.rotation_euler[0] = 3.1415927410125732 #180°
                elif bone.startswith("R_") or bone.endswith("_R"):
                    target.rotation_euler[0] = 0
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = 1.5707963705062866 #90°

                if bone.count("Finger02") != 0:
                    target.rotation_euler[0] = 0
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = 0

            elif bone.count("Finger1"):
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = 1.5707963705062866 #90°

                if bone.startswith("L_") or bone.endswith("_L"):
                    target.rotation_euler[0] = 1.5707963705062866 #90°
                elif bone.startswith("R_") or bone.endswith("_R"):
                    target.rotation_euler[0] = -1.5707963705062866 #-90°

                if bone.count("Finger12") != 0:
                    target.rotation_euler[0] = 0
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = 0

            elif bone.count("Finger2") != 0 or bone.count("Finger3") != 0 or bone.count("Finger4") != 0:
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = 1.5707963705062866 #90°

                if bone.startswith("L_") or bone.endswith("_L"):
                    pass
                elif bone.startswith("R_") or bone.endswith("_R"):
                    target.rotation_euler[0] = -1.5707963705062866 #-90°

                if bone.count("Finger22") != 0 or bone.count("Finger32") != 0 or bone.count("Finger42") != 0:
                    target.rotation_euler[0] = 0
                    target.rotation_euler[1] = 0
                    target.rotation_euler[2] = 0

        #Spine
        if vatproperties.retarget_center_preset == 'OP1':
            if bone.count("Spine") != 0 or bone.count("Neck") != 0 or bone.count("Head") != 0:
                target.rotation_euler[2] = 1.5707963705062866 #90°

        elif vatproperties.retarget_center_preset == 'OP2':
            if bone.count("Spine") != 0 or bone.count("Neck") != 0:
                target.rotation_euler[2] = 1.5707963705062866 #90°

            elif bone.count("Head") != 0:
                target.rotation_euler[2] = 1.3962633609771729 #80°

            elif bone.count("Pelvis") != 0:
                target.rotation_euler[0] = 0.3839724361896515 #22°

        #Lower body
        if vatproperties.retarget_bottom_preset == 'OP1':
            if bone.count("Thigh") != 0 or bone.count("Calf") != 0:
                target.rotation_euler[0] = 0
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = 1.5707963705062866 #90°
            elif bone.count("Foot") != 0:
                target.rotation_euler[0] = 1.5707963705062866 #90°
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = 1.5707963705062866 #90°

        elif vatproperties.retarget_bottom_preset == 'OP2':
            if bone.count("Thigh") != 0 or bone.count("Calf") != 0 or bone.count("Foot") != 0:
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = 1.5707963705062866 #90°

            elif bone.count("Toe0") != 0:
                target.rotation_euler[1] = 0
                target.rotation_euler[2] = 1.5707963705062866 #90°
                
                if bone.startswith("L_") or bone.endswith("_L"):
                    target.rotation_euler[0] = -1.535889744758606 #-88°
                elif bone.startswith("R_") or bone.endswith("_R"):
                    target.rotation_euler[0] = -1.675516128540039 #-96°

    def link(): #Organizes armature after empty creation

        def retarget(bone): #Creates empties and links them to Rigify armature/Source armature
            armature = bpy.data.objects["rig"]
            
            #Retarget empties creation
            try:
                collection = bpy.data.collections["Retarget Empties " + "(" + arm.name + ")"]
            except:
                collection = bpy.data.collections.new("Retarget Empties " + "(" + arm.name + ")")
                bpy.context.scene.collection.children.link(collection)

            collection.hide_viewport = True

            if bone.count("Trapezius") != 0 or bone.count("Bicep") != 0 or bone.count("Elbow") != 0 or bone.count("Knee") != 0 or bone.count("Ulna") != 0 or bone.count("Wrist") != 0:
                pass

            else:
                #Creates base empty and links
                base = bpy.data.objects.new("base_" + prefix + bone, None)
                collection.objects.link(base)
                base.empty_display_type = 'CUBE'
                base.hide_select = True

                #Location constraint
                loc = base.constraints.new('COPY_LOCATION')
                loc.target = armature
                loc.subtarget = "ORG-" + prefix + bone

                #Rotation constraint
                rot = base.constraints.new('COPY_ROTATION')
                rot.target = armature
                rot.subtarget = "ORG-" + prefix + bone

                #Creates target empty and links
                target = bpy.data.objects.new("target_" + prefix + bone, None)
                collection.objects.link(target)
                target.empty_display_type = 'SPHERE'

                #Parent to base
                base.parent = parent
                target.parent = base

                #Bone connection
                armature = bpy.data.objects[arm.name]
                loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')
                loc.name = "Retarget Location"
                loc.target = target
                rot = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')
                rot.name = "Retarget Rotation"
                rot.target = target


        #Creates parent for all bases for easier storage/manipulation
        parent = bpy.data.objects.new("parent_" + arm.name, None)

        prefix = arm.prefix

        for bone in arm.symmetrical_bones:
            retarget(bone)
            empty_rotation(bone, 0)

        for bone in arm.central_bones:
            retarget(bone)
            empty_rotation(bone, 1)

        #Connects parent to collection
        collection = bpy.data.collections["Retarget Empties " + "(" + arm.name + ")"]
        collection.objects.link(parent)

        #Renames armature to prior generated armature
        armature = bpy.data.objects["rig"]
        armature.name = arm.name + ".anim"
        armature.data.name = arm.name_real.name + ".anim"

        #Deletes generated armature
        generate_armature("anim", 2)

        #Links to animation armature
        try:
            collection = bpy.data.collections['Animation Armature']
        except:
            collection = None
            
        if collection != None:
            collection.objects.link(armature)

        arm.animation_armature = True
        arm.animation_armature_setup = False
        arm.animation_armature_name_full = armature
        arm.animation_armature_name = armature.name
        arm.animation_armature_real = armature.data

    #Updates bone list in case it was modified
    arm.get_bones()

    if action == 0 or action == 1: #Usual creation/deletion
        generate_rigify()

    elif action == 2: #Empty creation
        link()

    elif action == 3: #Empty rotation modification
        for bone in arm.symmetrical_bones:
            empty_rotation(bone, 0)
        for bone in arm.central_bones:
            empty_rotation(bone, 1)