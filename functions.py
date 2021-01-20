import bpy

class Prefixes: #Self explanatory

    current = ""

    #Prefix variables for reference
    default = "ValveBiped.Bip_"
    sfm = "bip_"
    helper = "hlp_"

class BoneList: #Lists of bones used for other operations

    #List of bones that will be filled with the armature's
    symmetrical_bones = [] #L/R
    central_bones = [] #Head, spine...
    helper_bones = [] #Knee, wrist...
    other_bones = [] #Jacket, attachments...
    custom_bones = [] #User made bones with no, or other prefix

    def getbones():
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]

        #Cleans bone list
        BoneList.symmetrical_bones = []
        BoneList.central_bones = []
        BoneList.helper_bones = []
        BoneList.other_bones = []
        BoneList.custom_bones = []

        full_bonelist = armature.data.bones.keys() #Gets all bones available in the armature

        #Checks wether or not they're central, symmetrical, helper, other, or custom bones, then removes their prefix/suffix and adds them into a group
        for bone in full_bonelist:

            if vatproperties.custom_scheme_enabled == True and vatproperties.custom_scheme_prefix != "":
                if bone.startswith(custom_scheme_prefix + bone.count("L_") == 0 or bone.count("R_") == 0 or bone.count("_L") == 0 or bone.count("_R") == 0):
                    vatproperties.scheme = 3
                    BoneList.symmetrical_bones.append(bone.replace(custom_scheme_prefix, ""))
                elif bone.startswith(custom_scheme_prefix):
                    BoneList.central_bones.append(bone.replace(custom_scheme_prefix, ""))

            #Source and Blender prefixes
            if bone.startswith("ValveBiped."):
                vatproperties.sfm_armature = False
                Prefixes.current = "ValveBiped.Bip01_"

                if bone.startswith("ValveBiped.Bip01_L_") or bone.startswith("ValveBiped.Bip01_R_"): #Symmetrical
                    vatproperties.scheme = 0
                    BoneList.symmetrical_bones.append(bone.replace("ValveBiped.Bip01_", ""))

                elif bone.endswith("_L") or bone.endswith("_R"):
                    vatproperties.scheme = 1
                    BoneList.symmetrical_bones.append(bone.replace("ValveBiped.Bip01_", ""))

                elif bone.startswith("ValveBiped.Bip01_"): #Central
                    BoneList.central_bones.append(bone.replace("ValveBiped.Bip01_", ""))
                    
                else: #Other
                    BoneList.other_bones.append(bone.replace("ValveBiped.", ""))

            #SFM prefix
            elif bone.startswith("bip_"): # Central
                vatproperties.sfm_armature = True
                vatproperties.scheme = 2
                Prefixes.current = "bip_"

                if bone.endswith("_L") or bone.endswith("_R"): #Symmetrical
                    BoneList.symmetrical_bones.append(bone.replace("bip_", ""))

                else:
                    BoneList.central_bones.append(bone.replace("bip_", ""))

            #Helper prefix
            elif bone.startswith("hlp_"): #Helper
                BoneList.helper_bones.append(bone.replace("hlp_", ""))
            #No/Different prefix
            else:
                BoneList.custom_bones.append(bone)

        if BoneList.symmetrical_bones == [] and BoneList.central_bones == [] and BoneList.other_bones == []:
            #Unknown armature
            vatproperties.scheme = -1

        print(BoneList.symmetrical_bones)
        print(BoneList.central_bones)
        print(BoneList.helper_bones)
        print(BoneList.other_bones)
        print(BoneList.custom_bones)

class SchemeType: #Scheme type that's currently being used by the armature

    def getscheme(bone):
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]

        #If not an SFM armature, check if the armature has the Source or Blender armature
        if vatproperties.sfm_armature == False:
            bone = Prefixes.current + bone
            if bone.startswith("ValveBiped.Bip01_L_") or bone.startswith("ValveBiped.Bip01_R_"):
                vatproperties.scheme = 0
            elif bone.endswith("_L") or bone.endswith("_R"):
                vatproperties.scheme = 1

    def execute(self, context):
        vatproperties = bpy.context.scene.vatproperties

        if vatproperties.target_armature != None:
            BoneList.getbones()
            for bone in BoneList.symmetrical_bones:
                SchemeType.getscheme(bone)
                
            if vatproperties.sfm_armature == False:
                if vatproperties.scheme == 0:
                    print("Current Scheme: Source")
                elif vatproperties.scheme == 1:
                    print("Current Scheme: Blender")
            if vatproperties.sfm_armature == True:
                print("Current Scheme: Source (SFM)")

class ArmatureRename: #Scheme changer
    
    def rename(bone, scheme, helper): #Which bone, to which scheme and if it's a helper bone
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.armatures[vatproperties.target_armature.data.name]

        #Current or helper prefix
        if helper == 1:
            prefix = Prefixes.helper
        else:
            prefix = Prefixes.current

        #To which scheme
        if scheme == 1: #Source -> Blender
            if bone.startswith("L_"):
                armature.bones[prefix + bone].name = prefix + bone.replace("L_", "") + "_L"
            elif bone.startswith("R_"):
                armature.bones[prefix + bone].name = prefix + bone.replace("R_", "") + "_R"
            vatproperties.scheme = 1
        elif scheme == 0: #Blender -> Source
            if bone.endswith("_L"):
                armature.bones[prefix + bone].name = prefix + "L_" + bone.replace("_L", "")
            elif bone.endswith("_R"):
                armature.bones[prefix + bone].name = prefix + "R_" + bone.replace("_R", "")
            vatproperties.scheme = 0
                
    def execute(scheme):
        for bone in BoneList.symmetrical_bones:
                ArmatureRename.rename(bone, scheme, 0)
            
        if BoneList.helper_bones != []:
            for bone in BoneList.helper_bones:
                ArmatureRename.rename(bone, scheme, 1)

        BoneList.getbones() #Refreshes bone list
            
class ConstraintSymmetry: #Adds loc/rot constraints to the armature

    #Constraint checks
    loc = ""
    rot = ""

    op = 0
    loc_bonelist = []
    rot_bonelist = []

    def getconstraint(bone):
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]
        prefix = Prefixes.current

        try:
            ConstraintSymmetry.loc = armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Location']
        except:
            ConstraintSymmetry.loc = ""
        try:
            ConstraintSymmetry.rot = armature.pose.bones[prefix + bone].constraints['Constraint Symmetry Rotation']
        except:
            ConstraintSymmetry.rot = ""

    def constraint(bone, side, action, helper): #Creates or deletes constraints based on action
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]

        #Cleans bone list
        ConstraintSymmetry.loc_bonelist = []
        ConstraintSymmetry.rot_bonelist = []

        ConstraintSymmetry.getconstraint(bone) #Checks for already existing constraints

        if helper == 1:
            prefix = Prefixes.helper
        else:
            prefix = Prefixes.current

        #Creation
        if action == 0:
            ConstraintSymmetry.op = 0

            #Left side
            if vatproperties.affected_side == 'OP1':

                #Location
                if ConstraintSymmetry.loc == "":
                    if bone.startswith("L_") or bone.endswith("_L"):
                        loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')

                        #Constraint parameters
                        loc.name = "Constraint Symmetry Location"
                        loc.target = armature
                        loc.invert_x = True
                        if bone.startswith("L_"):
                            loc.subtarget = prefix + "R_" + bone.replace("L_", "")
                        elif bone.endswith("_L"):
                            loc.subtarget = prefix + bone.replace("_L", "") + "_R"
                else:
                    ConstraintSymmetry.loc_bonelist.append(bone)

                #Rotation
                if ConstraintSymmetry.rot == "":
                    if bone.startswith("L_") or bone.endswith("_L"):
                        rot = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')

                        #Constraint parameters
                        rot.name = "Constraint Symmetry Rotation"
                        rot.target = armature
                        rot.target_space = 'LOCAL'
                        rot.owner_space = 'LOCAL'
                        rot.invert_y = True
                        rot.invert_x = True
                        if bone.startswith("L_"):
                            rot.subtarget = prefix + "R_" + bone.replace("L_", "")
                        elif bone.endswith("_L"):
                            rot.subtarget = prefix + bone.replace("_L", "") + "_R"
                else:
                    ConstraintSymmetry.rot_bonelist.append(bone)

            #Right side
            elif vatproperties.affected_side == 'OP2':

                #Location
                if ConstraintSymmetry.loc == "":
                    if bone.startswith("R_") or bone.endswith("_R"):
                        loc = armature.pose.bones[prefix + bone].constraints.new('COPY_LOCATION')
                        
                        #Constraint parameters
                        loc.name = "Constraint Symmetry Location"
                        loc.target = armature
                        loc.invert_x = True
                        if bone.startswith("R_"):
                            loc.subtarget = prefix + "L_" + bone.replace("R_", "")
                        elif bone.startswith("_R"):
                            loc.subtarget = prefix + bone.replace("_R", "") + "_L"
                else:
                    ConstraintSymmetry.loc_bonelist.append(bone)
                
                #Rotation
                if ConstraintSymmetry.rot == "":
                    if bone.startswith("R_") or bone.endswith("_R"):
                        rot = armature.pose.bones[prefix + bone].constraints.new('COPY_ROTATION')

                        #Constraint parameters
                        rot.name = "Constraint Symmetry Rotation"
                        rot.target = armature
                        rot.target_space = 'LOCAL'
                        rot.owner_space = 'LOCAL'
                        rot.invert_y = True
                        rot.invert_x = True
                        if bone.startswith("R_"):
                            rot.subtarget = prefix + "L_" + bone.replace("R_", "")
                        elif bone.endswith("_R"):
                            rot.subtarget = prefix + bone.replace("_R", "") + "_L"
                else:
                    ConstraintSymmetry.rot_bonelist.append(bone)

        #Deletion
        elif action == 1:
            vatproperties = bpy.context.scene.vatproperties
            armature = bpy.data.objects[vatproperties.target_armature.name]
            ConstraintSymmetry.op = 1

            #Left side
            if vatproperties.affected_side == 'OP1':

                #Location
                if ConstraintSymmetry.loc != "":
                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.pose.bones[prefix + bone].constraints.remove(ConstraintSymmetry.loc)
                else:
                    ConstraintSymmetry.loc_bonelist.append(bone)

                #Rotation
                if ConstraintSymmetry.rot != "":
                    if bone.startswith("L_") or bone.endswith("_L"):
                        armature.pose.bones[prefix + bone].constraints.remove(ConstraintSymmetry.rot)
                else:
                   ConstraintSymmetry.rot_bonelist.append(bone)

            #Right side
            elif vatproperties.affected_side == 'OP2':

                #Location
                if ConstraintSymmetry.loc != "":
                    if bone.startswith("R_") or bone.endswith("_R"):
                        armature.pose.bones[prefix + bone].constraints.remove(ConstraintSymmetry.loc)
                else:
                    ConstraintSymmetry.loc_bonelist.append(bone)

                #Rotation
                if ConstraintSymmetry.rot != "":
                    if bone.startswith("R_") or bone.endswith("_R"):
                        armature.pose.bones[prefix + bone].constraints.remove(ConstraintSymmetry.rot)
                else:
                    ConstraintSymmetry.rot_bonelist.append(bone)

    def execute(action):
        vatproperties = bpy.context.scene.vatproperties
        for bone in BoneList.symmetrical_bones:
            ConstraintSymmetry.constraint(bone, vatproperties.affected_side, action, 0)

        if BoneList.helper_bones != []:
            for bone in BoneList.helper_bones:
                ConstraintSymmetry.constraint(bone, vatproperties.affected_side, action, 1)

        #If constraints could not be applied
        if ConstraintSymmetry.loc_bonelist != []:
            if ConstraintSymmetry.op == 0:
                print("Location constraints already exist for:")
                print(ConstraintSymmetry.loc_bonelist)
            elif ConstraintSymmetry.op == 1:
                print("Location constraints not found for:")
                print(ConstraintSymmetry.loc_bonelist)
                
        if ConstraintSymmetry.rot_bonelist != []:
            if ConstraintSymmetry.op == 0:
                print("Rotation constraints already exist for:")
                print(ConstraintSymmetry.rot_bonelist)
            elif ConstraintSymmetry.op == 1:
                print("Rotation constraints not found for:")
                print(ConstraintSymmetry.rot_bonelist)

class WeightArmature: #Creates duplicate armature for more spread out weighting

    #Name container of the created weight armature
    weightarmature = ""

    def armature(action): #Creates or deletes the weight armature
        vatproperties = bpy.context.scene.vatproperties
        real_armature = bpy.data.armatures[vatproperties.target_armature.data.name]
        
        #Creation
        if action == 0:
            #Check for the armature datablock, to avoid copying it 
            try:
                real_weightarmature = bpy.data.armatures[vatproperties.target_armature.data.name + ".weightarmature"]
            except:
                real_weightarmature = real_armature.copy()
                real_weightarmature.name = vatproperties.target_armature.data.name + ".weightarmature"

            #Creation and link to current scene
            WeightArmature.weightarmature = bpy.data.objects.new(vatproperties.target_armature.name + ".weightarmature", real_weightarmature)
            collection = bpy.data.collections.new("Weight Armature")
            collection.objects.link(WeightArmature.weightarmature)
            bpy.context.scene.collection.children.link(collection)

            armature = bpy.data.objects[WeightArmature.weightarmature.name]
            prefix = Prefixes.current

            #Bone connection
            bpy.ops.object.select_all(action='DESELECT') #Apparently you're required to be in edit mode to use "data.edit_bones", else there will be no bone info given. Dumb
            armature.select_set(1)
            bpy.ops.object.mode_set(mode='EDIT')

            for bone in BoneList.symmetrical_bones:
                parent = armature.pose.bones[prefix + bone].parent.name
                loc = armature.pose.bones[prefix + bone].head
                armature.data.edit_bones[parent].tail = loc

            for bone in BoneList.central_bones:
                if bone == "Pelvis": #No parent
                    pass
                else:
                    parent = armature.pose.bones[prefix + bone].parent.name
                    loc = armature.pose.bones[prefix + bone].head
                    armature.data.edit_bones[parent].tail = loc

            #Final touches to the armature
            armature.data.display_type = 'OCTAHEDRAL'
            armature.data.show_bone_custom_shapes = False

            if bone.count("Hand") != 0:
                y = armature.pose.bones[prefix + bone].head.y
                armature.data.edit_bones[prefix + bone].tail.y = y

            if bone.count("Toe") != 0:
                x = armature.pose.bones[prefix + bone].head.x
                y = armature.pose.bones[prefix + bone].head.y
                z = armature.pose.bones[prefix + bone].head.z

                if bone.startswith("L_") or bone.endswith("_L"):
                    armature.data.edit_bones[prefix + bone].tail = x+0.5 , y-2.5, z
                elif bone.startswith("R_") or bone.endswith("_R"):
                    armature.data.edit_bones[prefix + bone].tail = x-0.5, y-2.5, z

            if bone == "Head1":
                x = armature.pose.bones[prefix + bone].head.x
                y = armature.pose.bones[prefix + bone].head.y
                z = armature.pose.bones[prefix + bone].head.z

                armature.data.edit_bones[prefix + bone].tail = x, y, z+6


            bpy.ops.object.mode_set(mode='OBJECT')

        #Deletion    
        elif action == 1:
            bpy.data.objects.delete(WeightArmature.weightarmature.name)
        
    def execute(action):
        WeightArmature.armature(action)

class InverseKinematics: #Adds IK to the armature
    
    #Constraint checks
    leftik = ""
    rightik = ""

    op = 0
    bonelist = []

    def getconstraint(bone):
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]
        prefix = Prefixes.current

        #Cleans list
        bonelist = []

        if bone.startswith("L_") or bone.endswith("_L"):
            try:
                InverseKinematics.leftik = armature.pose.bones[prefix + bone].constraints['IK']
            except:
                InverseKinematics.leftik = ""

        elif bone.startswith("R_") or bone.endswith("_R"):
            try:
                InverseKinematics.rightik = armature.pose.bones[prefix + + bone_name].constraints['IK']
            except:
                InverseKinematics.rightik = ""

    def IK(bone_name, action):
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]
        prefix = Prefixes.current

        InverseKinematics.getconstraint(bone_name)

        #Creation
        if action == 0:

            #Left IK
            if InverseKinematics.leftik == "":
                if bone.startswith("L_") or bone.endswith("_L"):
                    leftik = armature.pose.bones[prefix + "L_" + bone_name].constraints.new('IK')
                    leftik.chain_count = 3
            else:
                InverseKinematics.bonelist.append(bone.name)

            #Right IK
            if InverseKinematics.rightik == "":
                if bone.startswith("R_") or bone.endswith("_R"):
                    rightik = armature.pose.bones[prefix + "L_" + bone_name].constraints.new('IK')
                    rightik.chain_count = 3
            else:
                InverseKinematics.bonelist.append(bone.name)

        #Deletion
        elif action == 1:

            #Left IK
            if InverseKinematics.leftik != "":
                if bone.startswith("L_") or bone.endswith("_L"):
                    armature.pose.bones[prefix + bone_name].constraints.remove(InverseKinematics.leftik)
            else:
                InverseKinematics.bonelist.append(bone.name)

            #Right IK
            if InverseKinematics.rightik != "":
                if bone.startswith("R_") or bone.endswith("_R"):
                    armature.pose.bones[prefix + bone_name].constraints.remove(InverseKinematics.rightik)
            else:
                InverseKinematics.bonelist.append(bone.name)

    def execute(action):
        vatproperties = bpy.context.scene.vatproperties

        for bone in BoneList.symmetrical_bones.count("Hand") != 0:
            InverseKinematics.IK(bone, action)
