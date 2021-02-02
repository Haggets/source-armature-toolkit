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
        self.name_real = armature.data.name

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
        self.weight_armature_real = None

        #Animation armature
        self.animation_armature = False
        self.animation_armature_name = None
        self.animation_armature_real = None

        #Functions executed to gather previous information
        self.getbones()
        self.getscheme()
        
    def getbones(self):
        armature = bpy.data.objects[self.name]

        if self.name != "":

            #Cleans bone list
            self.full_bonelist = []
            self.symmetrical_bones = []
            self.central_bones = []
            self.helper_bones = []
            self.other_bones = []
            self.custom_bones = []

            self.full_bonelist = armature.data.bones.keys()

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

                #Source and Blender prefixes
                if bone.startswith("ValveBiped."):
                    vatproperties.sfm_armature = False
                    self.prefix = "ValveBiped.Bip01_"

                    #Usual prefix
                    if bone.startswith(self.prefix + "L_") or bone.startswith(self.prefix + "R_"): #Symmetrical
                        self.scheme = 0
                        self.symmetrical_bones.append(bone.replace(self.prefix, ""))

                    #Strange L4D2 helper prefix, must be differentiated from the usual helper bone with "s."
                    elif bone.startswith("ValveBiped.hlp_"):
                        self.helper_bones.append(bone.replace("ValveBiped.hlp_", "s."))

                    #Attachment bone prefix. They are supposed to be in other bones instead
                    elif bone.startswith("ValveBiped.attachment"):
                        self.other_bones.append(bone.replace("ValveBiped.attachment_", "a."))

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

                #Helper prefix
                elif bone.startswith("hlp_"): #Helper
                    self.helper_bones.append(bone.replace(Prefixes.helper, ""))

                #No/Different prefix
                else:
                    self.custom_bones.append(bone)

            if self.symmetrical_bones == [] and self.central_bones == [] and self.other_bones == []:
                #Unknown armature
                self.scheme = -1

            print("Symmetrical bones:", self.symmetrical_bones)
            print("Central bones:", self.central_bones)
            print("Helper bones:", self.helper_bones)
            print("Other bones:", self.other_bones)
            print("Custom bones:", self.custom_bones)

    def getscheme(self):
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[self.name]

        for bone in self.symmetrical_bones:
            #If not an SFM armature, check if the armature has the Source or Blender armature
            if self.sfm == False:
                bone = self.prefix + bone
                if bone.startswith("ValveBiped.Bip01_L_") or bone.startswith("ValveBiped.Bip01_R_"):
                    vatproperties.scheme = 0
                elif bone.endswith("_L") or bone.endswith("_R"):
                    vatproperties.scheme = 1
                
        if self.sfm == False:
            if vatproperties.scheme == 0:
                print("Current Scheme: Source")
            elif vatproperties.scheme == 1:
                print("Current Scheme: Blender")
        elif self.sfm == True:
            print("Current Scheme: Source (SFM)")

def armature_rename(scheme): #Bone prefix/suffix repositioning

    def rename(bone):
        armature = bpy.data.armatures[arm.name_real]

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

    prefix = arm.prefix
    for bone in arm.symmetrical_bones:
        rename(bone)
        
    if arm.helper_bones != []:
        for bone in arm.helper_bones:
            if bone.startswith("s."):
                #Their prefix is usually already in the end so they're left alone
                if bone.endswith("_L") or bone.endswith("_R"):
                    pass
                else:
                    prefix = Prefixes.helper2
                    rename(bone.replace("s.", ""))
            else:
                prefix = Prefixes.helper
                rename(bone)

    arm.getbones() #Refreshes bone list

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
        nonlocal loc_bonelist
        nonlocal rot_bonelist

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

    prefix = arm.prefix
    for bone in arm.symmetrical_bones:
        constraint(bone)

    if arm.helper_bones != []:
        for bone in arm.helper_bones:
            if bone.startswith("s."):
                prefix = Prefixes.helper2
                constraint(bone.replace("s.", ""))
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

def weight_armature(action): #Creates duplicate armature for more spread out weighting

    def armature(): #Creates or deletes the weight armature
        real_armature = bpy.data.armatures[arm.name_real]
        
        #Creation
        if action == 0:
            #Check for the armature datablock, to avoid having more than one copy 
            try:
                arm.weight_armature_real = bpy.data.armatures[arm.name_real + ".weight"]
            except:
                arm.weight_armature_real = real_armature.copy()
                arm.weight_armature_real.name = arm.name_real + ".weight"

            #Creation and link to current scene
            arm.weight_armature_name = bpy.data.objects.new(arm.name + ".weight", arm.weight_armature_real)
            arm.weight_armature = True
            collection = bpy.data.collections.new("Weight Armature")
            collection.objects.link(arm.weight_armature_name)
            bpy.context.scene.collection.children.link(collection)

            armature = bpy.data.objects[arm.name]
            prefix = arm.prefix
            
            #Variables used to store certain bones that require additional position tweaking
            ulna = []
            wrist = []
            bicep = []

            #Bone connection
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT') #You're required to be in edit mode to use "data.edit_bones", else there will be no bone info given.
            armature.select_set(1)
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
                    loc = armature.pose.bones[prefix + bone].head
                    armature.data.edit_bones[parent].tail = loc

                #Additional bone tweaking

                #Extends toe tip to be where the actual tip should be
                if bone.count("Toe") != 0:
                    pbone = armature.pose.bones[prefix + bone].head

                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.data.edit_bones[prefix + bone].tail = pbone.x+0.5, pbone.y-2.5, pbone.z
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        armature.data.edit_bones[prefix + bone].tail = pbone.x-0.5, pbone.y-2.5, pbone.z

                #Extends the length of the finger's tips to be closer to where the actual finger tip should be
                if bone.count("Finger12") != 0 or bone.count("Finger22") != 0 or bone.count("Finger32") != 0 or bone.count("Finger42") != 0:
                    pbone = armature.pose.bones[prefix + bone].tail

                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.data.edit_bones[prefix + bone].tail.xz = pbone.x-0.1, pbone.z-0.5
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        armature.data.edit_bones[prefix + bone].tail.xz = pbone.x+0.1, pbone.z-0.5

                #Same thing as before but with different location
                if bone.count("Finger02") != 0:
                    pbone = armature.pose.bones[prefix + bone].tail

                    armature.data.edit_bones[prefix + bone].tail.yz = pbone.y-0.8, pbone.z-0.4

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
                
                if bone.count("Wrist") != 0:
                    wrist.append(bone)

                if bone.count("Bicep") != 0:
                    bicep.append(bone)

            for bone in arm.central_bones:
                if bone == "Pelvis": #No parent
                    pass
                else:
                    parent = armature.pose.bones[prefix + bone].parent.name
                    loc = armature.pose.bones[prefix + bone].head
                    armature.data.edit_bones[parent].tail = loc
                    
                #Extends head's length to be on par with actual head height
                if bone == "Head1":
                    pbone = armature.pose.bones[prefix + bone].head
                    
                    armature.data.edit_bones[prefix + bone].tail = pbone.x, pbone.y, pbone.z+6

            #Tweaks positioning of some helper bones
            if bicep != []:
                for bone in arm.symmetrical_bones:
                    if bone.count("Forearm") != 0:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            loc_l = armature.pose.bones[prefix + bone].head
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            loc_r = armature.pose.bones[prefix + bone].head
                for bicep in bicep:
                    if bicep.startswith("L_") or bone.endswith("_L"):
                        armature.data.edit_bones[prefix + bicep].tail = loc_l
                    elif bicep.startswith("R_") or bone.endswith("_R"):
                        armature.data.edit_bones[prefix + bicep].tail = loc_r

            if ulna != [] or wrist != []:

                #Obtains hand head location
                for bone in arm.symmetrical_bones:
                    if bone.count("Hand") != 0:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            loc_l = armature.pose.bones[prefix + bone].head
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            loc_r = armature.pose.bones[prefix + bone].head

                if ulna != [] and wrist != []:
                    for ulna in ulna:
                        if bone.startswith("L_") or bone.endswith("_L"):
                            armature.data.edit_bones[prefix + ulna].tail = loc_l
                            loc2_l = armature.pose.bones[prefix + ulna].tail
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            armature.data.edit_bones[prefix + ulna].tail = loc_r
                            loc2_r = armature.pose.bones[prefix + ulna].tail

                        length = armature.pose.bones[prefix + ulna].length
                        armature.data.edit_bones[prefix + ulna].length = length / 1.5

                    for wrist in wrist:
                        if bone.startswith("L_") or bone.endswith("_L"):                      
                            armature.data.edit_bones[prefix + wrist].head = loc2_l
                            armature.data.edit_bones[prefix + wrist].tail = loc_l
                        elif bone.startswith("R_") or bone.endswith("_R"):
                            armature.data.edit_bones[prefix + wrist].head = loc2_r
                            armature.data.edit_bones[prefix + wrist].tail = loc_r

            if arm.other_bones != []:
                for bone in arm.other_bones:
                    #Removes weapon bones since they're not meant for the character weighting
                    #Also removes attachment bones for the same reason
                    if bone.count("weapon") != 0:
                        prefix = Prefixes.other
                        bone = armature.data.edit_bones[prefix + bone]
                        armature.data.edit_bones.remove(bone)
                    elif bone.startswith("a."):
                        prefix = Prefixes.attachment
                        bone = armature.data.edit_bones[prefix + bone.replace("a.", "")]
                        armature.data.edit_bones.remove(bone)


            #Final touches to the armature
            armature.data.display_type = 'OCTAHEDRAL'
            armature.data.show_bone_custom_shapes = False
            armature.show_in_front = 1

            bpy.ops.object.mode_set(mode='OBJECT')

        #Deletion    
        elif action == 1:
            bpy.data.objects.delete(arm.weightarmature_name)
            arm.weight_armature = False
        
    WeightArmature.armature(action)
    print("Weight armature created!")

class InverseKinematics: #Adds IK to the armature
    
    #Constraint checks
    ik_constraint = ""
    leftik = ""
    rightik =""

    #Variables for finish report
    op = 0
    bonelist = []

    def getconstraint(bone):
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]
        prefix = Prefixes.current

        #Cleans list
        InverseKinematics.bonelist = []

        try:
            InverseKinematics.ik_constraint = armature.pose.bones[prefix + bone].constraints['IK']
        except:
            InverseKinematics.ik_constraint = ""

    def IK(bone, action):
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]
        prefix = Prefixes.current

        InverseKinematics.getconstraint(bone)

        #Creation
        if action == 0:
            InverseKinematics.op = 0

            #Left IK
            if InverseKinematics.ik_constraint == "":
                if bone.startswith("L_") or bone.endswith("_L"):
                    ik = armature.pose.bones[prefix + bone].constraints.new('IK')
                    ik.chain_count = 3
                elif bone.startswith("R_") or bone.endswith("_R"):
                    ik = armature.pose.bones[prefix + bone].constraints.new('IK')
                    ik.chain_count = 3
            else:
                InverseKinematics.bonelist.append(bone)

        #Deletion
        elif action == 1:
            InverseKinematics.op = 1

            #Left IK
            if InverseKinematics.ik_constraint != "":
                if bone.startswith("L_") or bone.endswith("_L"):
                    armature.pose.bones[prefix + bone].constraints.remove(InverseKinematics.ik_constraint)
                elif bone.startswith("R_") or bone.endswith("_R"):
                    armature.pose.bones[prefix + bone].constraints.remove(InverseKinematics.ik_constraint)
            else:
                InverseKinematics.bonelist.append(bone)

    def execute(action):
        for bone in BoneList.symmetrical_bones:
            if bone.count("Hand") != 0 or bone.count("Foot") != 0:
                InverseKinematics.IK(bone, action)
        
        #If constraints could not be applied
        if InverseKinematics.bonelist != []:
            if InverseKinematics.op == 0:
                print("IK constraints already exist for:")
                print(InverseKinematics.bonelist)
            elif InverseKinematics.op == 1:
                print("IK constraints not found for:")
                print(InverseKinematics.bonelist)

class RigifyRetarget: #Creates animation ready rig

    #Name container of the created animation armature
    animarmature = ""

    def armature(action): #Creates or deletes the animation armature
        vatproperties = bpy.context.scene.vatproperties
        real_armature = bpy.data.armatures[vatproperties.target_armature.data.name]
        
        #Creation
        if action == 0:
            #Check for the armature datablock, to avoid copying it 
            try:
                real_animarmature = bpy.data.armatures[vatproperties.target_armature.data.name + ".anim"]
            except:
                real_animarmature = real_armature.copy()
                real_animarmature.name = vatproperties.target_armature.data.name + ".anim"

            #Creation and link to current scene
            RigifyRetarget.animarmature = bpy.data.objects.new(vatproperties.target_armature.name + ".anim", real_animarmature)
            collection = bpy.data.collections.new("Animation Armature")
            collection.objects.link(RigifyRetarget.animarmature)
            bpy.context.scene.collection.children.link(collection)

            armature = bpy.data.objects[RigifyRetarget.animarmature.name]
            prefix = Prefixes.current

            #Bone connection
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT') #Apparently you're required to be in edit mode to use "data.edit_bones", else there will be no bone info given. Dumb
            armature.select_set(1)
            bpy.ops.object.mode_set(mode='EDIT')

            for bone in BoneList.symmetrical_bones:
                parent = armature.pose.bones[prefix + bone].parent.name
                if parent.count("Hand") != 0:
                    if bone.count("Finger0") != 0:
                        pass
                    else:
                        pbone = armature.pose.bones[prefix + bone].head

                        armature.data.edit_bones[parent].tail.xz = pbone.x, pbone.z
                else:
                    loc = armature.pose.bones[prefix + bone].head
                    armature.data.edit_bones[parent].tail = loc

                #Additional bone tweaking
                if bone.count("Toe") != 0:
                    pbone = armature.pose.bones[prefix + bone].head

                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.data.edit_bones[prefix + bone].tail = pbone.x+0.5, pbone.y-2.5, pbone.z
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        armature.data.edit_bones[prefix + bone].tail = pbone.x-0.5, pbone.y-2.5, pbone.z

                if bone.count("Finger12") != 0 or bone.count("Finger22") != 0 or bone.count("Finger32") != 0 or bone.count("Finger42") != 0:
                    pbone = armature.pose.bones[prefix + bone].tail

                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.data.edit_bones[prefix + bone].tail.xz = pbone.x-0.1, pbone.z-0.5
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        armature.data.edit_bones[prefix + bone].tail.xz = pbone.x+0.1, pbone.z-0.5

                if bone.count("Finger02") != 0:
                    pbone = armature.pose.bones[prefix + bone].tail

                    armature.data.edit_bones[prefix + bone].tail.yz = pbone.y-0.8, pbone.z-0.4

            for bone in BoneList.central_bones:
                if bone == "Pelvis": #No parent
                    pass
                else:
                    parent = armature.pose.bones[prefix + bone].parent.name
                    loc = armature.pose.bones[prefix + bone].head
                    armature.data.edit_bones[parent].tail = loc

                if bone == "Head1":
                    pbone = armature.pose.bones[prefix + bone].head

                    armature.data.edit_bones[prefix + bone].tail = pbone.x, pbone.y, pbone.z+6

            #Deletes unimportant bones 
            if BoneList.helper_bones != []:
                prefix = Prefixes.helper
                for bone in BoneList.helper_bones:
                    bone = armature.data.edit_bones[prefix + bone]
                    armature.data.edit_bones.remove(bone)

            if BoneList.other_bones != []:
                prefix = Prefixes.other
                for bone in BoneList.other_bones:
                    bone = armature.data.edit_bones[prefix + bone]
                    armature.data.edit_bones.remove(bone)

            #Rigify portion
            bpy.ops.pose.rigify_layer_init()
            prefix = Prefixes.current

            #Creates layers
            for i in range(0,19):
                armature.data.rigify_layers.add()

            #Rigify layers
            names = ["Torso", "Torso (Tweak)", "Fingers", "Fingers (Detail)", "Arm.L (IK)", "Arm.L (FK)", "Arm.L (Tweak)", "Arm.R (IK)", "Arm.R (FK)", "Arm.R (Tweak)", "Leg.L (IK)", "Leg.L (FK)", "Leg.L (Tweak)", "Leg.R (IK)", "Leg.R (FK)", "Leg.R (Tweak)"]

            group = [3,4,6,5,2,5,4,2,5,4,2,5,4,2,5,4]

            for i, name, group in zip(range(3,19), names, group):
                armature.data.rigify_layers[i].name = name
                armature.data.rigify_layers[i].row = i
                armature.data.rigify_layers[i].group = group

            #Creates 2 pelvis bones for whatever Rigify does with em
            pbone = armature.pose.bones[prefix + "Pelvis"].head

            new_pelvis = []

            if vatproperties.scheme == 0:
                for bone in ["L_Pelvis", "R_Pelvis"]:
                    new_pelvis.append(bone)

            elif vatproperties.scheme <= 0:
                for bone in ["Pelvis_L", "Pelvis_R"]:
                    new_pelvis.append(bone)

            for bone in new_pelvis:
                ebone = armature.data.edit_bones.new(prefix + bone)

                #New pelvis bone positioning
                if bone.startswith("L_") or bone.endswith("_L"):
                    ebone.tail.xyz = pbone.x-3, pbone.y-2, pbone.z+4
                elif bone.startswith("R_") or bone.endswith("_R"):
                    ebone.tail.xyz = pbone.x+3, pbone.y-2, pbone.z+4

            #For some dumb reason, the newly added bone is not added to the armature data until the user changes modes at least once, i know no other way around it. If you do please let me know
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.mode_set(mode='EDIT')

            #Rigify parameters
            for bone in new_pelvis:
                pbone = armature.pose.bones[prefix + bone]
                dbone = armature.data.bones[prefix + bone]
                

                pbone.rigify_type = "basic.super_copy"
                pbone.rigify_parameters.make_control = False
                dbone.layers[0] = False
                dbone.layers[3] = True

            #Symmetrical
            for bone in BoneList.symmetrical_bones:
                pbone = armature.pose.bones[prefix + bone]
                param = pbone.rigify_parameters
                dbone = armature.data.bones[prefix + bone]

                dbone.layers[0] = False

                if bone.count("Finger") != 0:
                    dbone.layers[5] = True

                if bone.count("UpperArm") != 0 or bone.count("Forearm") != 0 or bone.count("Hand") != 0:
                    if bone.startswith("L_") or bone.endswith("_L"):
                        dbone.layers[7] = True
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        dbone.layers[10] = True

                if bone.count("Thigh") != 0 or bone.count("Calf") != 0 or bone.count("Foot") != 0 or bone.count("Toe") != 0:
                    if bone.startswith("L_") or bone.endswith("_L"):
                        dbone.layers[13] = True
                    elif bone.startswith("R_") or bone.endswith("_R"):
                        dbone.layers[16] = True

                if bone.count("Clavicle") != 0:
                    pbone.rigify_type = "basic.super_copy"
                    param.make_widget = False
                    dbone.layers[3] = True

                if bone.count("UpperArm") != 0:
                    pbone.rigify_type = "limbs.super_limb"
                    param.tweak_layers[1] = False
                    param.tweak_layers[8] = True
                    param.fk_layers[1] = False
                    param.fk_layers[9] = True

                if bone.count("Thigh") != 0:
                    pbone.rigify_type = "limbs.super_limb"
                    param.limb_type = 'leg'
                    param.tweak_layers[1] = False
                    param.tweak_layers[15] = True
                    param.fk_layers[1] = False
                    param.fk_layers[14] = True

            #Central
            for bone in BoneList.central_bones:
                pbone = armature.pose.bones[prefix + bone]
                param = pbone.rigify_parameters
                dbone = armature.data.bones[prefix + bone]

                dbone.layers[0] = False
                dbone.layers[3] = True

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

            #Final touches to the armature
            armature.data.display_type = 'OCTAHEDRAL'
            armature.data.show_bone_custom_shapes = False

            bpy.ops.object.mode_set(mode='OBJECT')

        #Deletion    
        elif action == 1:
            bpy.data.objects.delete(RigifyRetarget.animarmature.name)
        
    def execute(action):
        RigifyRetarget.armature(action)
