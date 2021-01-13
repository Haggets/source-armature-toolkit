import bpy

class BoneList: #Lists of bones that will be used by other operations

    test_bones = ["Thigh", "Clavicle"]

    ik_bones = ["Hand", "Foot"]

    central_bones = ["Pelvis", "Spine", "Spine1", "Spine2", "Spine4", "Neck1", "Head1"]
    
    symmetrical_bones = ["Thigh", "Calf", "Foot", "Toe0", "Clavicle", "UpperArm", "Forearm", "Hand", "Finger0", "Finger01", "Finger02", "Finger1", "Finger11", "Finger12", "Finger2", "Finger21", "Finger22", "Finger3", "Finger31", "Finger32", "Finger4", "Finger41", "Finger42", "Knee", "Elbow", "Ulna", "Wrist"]
    
    symmetrical_bones_viewmodel = ["Forearm_driven", "Driven_ulna", "wrist_helper1", "wrist_helper2", "thumbroot"]
    
    symmetrical_bones_helper = ["Thigh", "Ulna"]
    
    symmetrical_bones_legacy = ["Shoulder", "Trapezius", "Bicep"]

class SchemeType: #Scheme type that's currently being used by the armature

    def getscheme(bone_name):
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]
        prefix = "ValveBiped.Bip01_"
        try:
            blender = armature.pose.bones[prefix + bone_name + "_L"]
        except:
            vatproperties.scheme = 0
        try:
            source = armature.pose.bones[prefix + "L_" + bone_name]
        except:
            vatproperties.scheme = 1

    def execute(self, context): #Checks for current scheme with specific bones
        vatproperties = bpy.context.scene.vatproperties
        if vatproperties.target_armature != None:
            for bone in BoneList.test_bones:
                SchemeType.getscheme(bone)
                
            if vatproperties.scheme == 0:
                print("Current Scheme: Source")
            elif vatproperties.scheme == 1:
                print("Current Scheme: Blender")

class ArmatureRename: #Name scheme changer
    
    def rename(bone_name, scheme, helper): #Which bone, to which scheme and if it's a helper bone
        vatproperties = bpy.context.scene.vatproperties
        real_armature = bpy.data.objects[vatproperties.target_armature.name].data.name
        armature = bpy.data.armatures[real_armature]
        if helper == 1:
            prefix = "hlp_"
        else:
            prefix = "ValveBiped.Bip01_"
        if scheme == 1: #Check if it's from Source to Blender or the opposite
            armature.bones[prefix + "L_" + bone_name].name = prefix + bone_name + "_L"
            armature.bones[prefix + "R_" + bone_name].name = prefix + bone_name + "_R"
            vatproperties.scheme = 1
        elif scheme == 0:
            armature.bones[prefix + bone_name + "_L"].name = prefix + "L_" + bone_name
            armature.bones[prefix + bone_name + "_R"].name = prefix + "R_" + bone_name
            vatproperties.scheme = 0
                
    def execute(scheme):
        for bone in BoneList.symmetrical_bones: #Normal bones
            try:
                ArmatureRename.rename(bone, scheme, 0)
            except:
                print(bone + " not found, cannot rename. Proceeding...")
                pass
            
        for bone in BoneList.symmetrical_bones_helper: #Helper bones
            try:
                ArmatureRename.rename(bone, scheme, 1)
            except:
                print(bone + " (helper bone) not found, cannot rename. Proceeding...")
                pass
            
        for bone in BoneList.symmetrical_bones_viewmodel: #Viewmodel exclusive bones
            try:
                ArmatureRename.rename(bone, scheme, 0)
            except:
                print(bone + " (viewmodel bone) not found, cannot rename. Proceeding...")
                pass
            
        for bone in BoneList.symmetrical_bones_legacy:
            try:
                ArmatureRename.rename(bone, scheme, 0)
            except:
                print(bone + " (legacy bone) not found, cannot rename. Proceeding...")
                pass

class ConstraintSymmetry: #Adds loc/rot constraints to the armature

    #Check if constraints already exist
    loc_leftconstraint = 0
    rot_leftconstraint = 0
    loc_rightconstraint = 0
    rot_rightconstraint = 0

    #Another constraint check but keeping a Constraint type value for deletion (Because Blender is really heck)
    locL = ""
    locR = ""
    rotL = ""
    rotR = ""

    def getconstraint(bone_name): #Checks if individual constraints are already in place
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]
        if vatproperties.sfm_armature == 0:
            prefix = "ValveBiped.Bip01_"
            if vatproperties.scheme == 0:
                try:
                    ConstraintSymmetry.locL = armature.pose.bones[prefix + "L_" + bone_name].constraints['Constraint Symmetry Location']
                except:
                    ConstraintSymmetry.locL = ""
                try:
                    ConstraintSymmetry.rotL = armature.pose.bones[prefix + "L_" + bone_name].constraints['Constraint Symmetry Rotation']
                except:
                    ConstraintSymmetry.rotL = ""
                try:
                    ConstraintSymmetry.locR = armature.pose.bones[prefix + "R_" + bone_name].constraints['Constraint Symmetry Location']
                except:
                    ConstraintSymmetry.locR = ""
                try:
                    ConstraintSymmetry.rotR = armature.pose.bones[prefix + "R_" + bone_name].constraints['Constraint Symmetry Rotation']
                except:
                    ConstraintSymmetry.rotR = ""

            elif vatproperties.scheme == 1:
                try:
                    ConstraintSymmetry.locL = armature.pose.bones[prefix + bone_name + "_L"].constraints['Constraint Symmetry Location']
                except:
                    ConstraintSymmetry.locL = ""
                try:
                    ConstraintSymmetry.rotL = armature.pose.bones[prefix + bone_name + "_L"].constraints['Constraint Symmetry Rotation']
                except:
                    ConstraintSymmetry.rotL = ""
                try:
                    ConstraintSymmetry.locR = armature.pose.bones[prefix + bone_name + "_R"].constraints['Constraint Symmetry Location']
                except:
                    ConstraintSymmetry.locR = ""
                try:
                    ConstraintSymmetry.rotR = armature.pose.bones[prefix + bone_name + "_R"].constraints['Constraint Symmetry Rotation']
                except:
                    ConstraintSymmetry.rotR = ""
            
        elif vatproperties.sfm_armature == 1:
            prefix = "bip_"
            try:
                ConstraintSymmetry.locL = armature.pose.bones[prefix + bone_name + "_L"].constraints['Constraint Symmetry Location']
            except:
                ConstraintSymmetry.locL = ""
            try:
                ConstraintSymmetry.rotL = armature.pose.bones[prefix + bone_name + "_L"].constraints['Constraint Symmetry Rotation']
            except:
                ConstraintSymmetry.rotL = ""
            try:
                ConstraintSymmetry.locR = armature.pose.bones[prefix + bone_name + "_R"].constraints['Constraint Symmetry Location']
            except:
                ConstraintSymmetry.locR = ""
            try:
                ConstraintSymmetry.rotR = armature.pose.bones[prefix + bone_name + "_R"].constraints['Constraint Symmetry Rotation']
            except:
                ConstraintSymmetry.rotR = ""

        if ConstraintSymmetry.locL != "":
            ConstraintSymmetry.loc_leftconstraint = 1
        else:
            ConstraintSymmetry.loc_leftconstraint = 0
        if ConstraintSymmetry.rotL != "":
            ConstraintSymmetry.rot_leftconstraint = 1
        else:
            ConstraintSymmetry.rot_leftconstraint = 0
        if ConstraintSymmetry.locR != "":
            ConstraintSymmetry.loc_rightconstraints = 1
        else:
            ConstraintSymmetry.loc_rightconstraints = 0
        if ConstraintSymmetry.rotR != "":
            ConstraintSymmetry.rot_rightconstraint = 1
        else:
            ConstraintSymmetry.rot_rightconstraint = 0

    def constraint(bone_name, side, action): #Creates or deletes constraints based on action
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]

        ConstraintSymmetry.getconstraint(bone_name) #Checks if constraints already exist

        if action == 0: #Constraint creation
            if vatproperties.sfm_armature == 0:
                prefix = "ValveBiped.Bip01_"
                if vatproperties.affected_side == 'OP1': #Left side
                    if ConstraintSymmetry.loc_leftconstraint == 0: #Right side for location
                        if vatproperties.scheme == 0: #Scheme type
                            loc = armature.pose.bones[prefix + "L_" + bone_name].constraints.new('COPY_LOCATION')
                        elif vatproperties.scheme == 1:
                            loc = armature.pose.bones[prefix + bone_name + "_L"].constraints.new('COPY_LOCATION')

                        loc.name = "Constraint Symmetry Location"
                        loc.target = armature
                        loc.invert_x = True
                        if vatproperties.scheme == 0:
                            loc.subtarget = prefix + "R_" + bone_name
                        elif vatproperties.scheme == 1:
                            loc.subtarget = prefix + bone_name + "_R"
                    else:
                        print("Right location constraint already in place for " + bone_name + ". Skipping")

                    if ConstraintSymmetry.rot_leftconstraint == 0: #Right side for rotation
                        if vatproperties.scheme == 0:
                            rot = armature.pose.bones[prefix + "L_" + bone_name].constraints.new('COPY_ROTATION')
                        elif vatproperties.scheme == 1:
                            rot = armature.pose.bones[prefix + bone_name + "_L"].constraints.new('COPY_ROTATION')

                        rot.name = "Constraint Symmetry Rotation"
                        rot.target = armature
                        rot.target_space = 'LOCAL'
                        rot.owner_space = 'LOCAL'
                        rot.invert_y = True
                        rot.invert_x = True
                        if vatproperties.scheme == 0:
                            rot.subtarget = prefix + "R_" + bone_name
                        elif vatproperties.scheme == 1:
                            rot.subtarget = prefix + bone_name + "_R"
                    else:
                        print("Right rotation constraint already in place for " + bone_name + ". Skipping")

                elif vatproperties.affected_side == 'OP2': #Right side for location
                    if ConstraintSymmetry.loc_rightconstraint == 0: #Left side for location
                        if vatproperties.scheme == 0:
                            loc = armature.pose.bones[prefix + "R_" + bone_name].constraints.new('COPY_LOCATION')
                        elif vatproperties.scheme == 1:
                            loc = armature.pose.bones[prefix + bone_name + "_R"].constraints.new('COPY_LOCATION')
                            
                        loc.name = "Constraint Symmetry Location"
                        loc.target = armature
                        loc.invert_x = True
                        if vatproperties.scheme == 0:
                            loc.subtarget = prefix + "L_" + bone_name
                        elif vatproperties.scheme == 1:
                            loc.subtarget = prefix + bone_name + "_L"
                    else:
                        print("Left location constraint already in place for " + bone_name + ". Skipping")
                    
                    if ConstraintSymmetry.rot_rightconstraint == 0: #Left side for rotation
                        if vatproperties.scheme == 0:
                            rot = armature.pose.bones[prefix + "R_" + bone_name].constraints.new('COPY_ROTATION')
                        elif vatproperties.scheme == 1:
                            rot = armature.pose.bones[prefix + bone_name + "_R"].constraints.new('COPY_ROTATION')

                        rot.name = "Constraint Symmetry Rotation"
                        rot.target = armature
                        rot.target_space = 'LOCAL'
                        rot.owner_space = 'LOCAL'
                        rot.invert_y = True
                        rot.invert_x = True
                        if vatproperties.scheme == 0:
                            rot.subtarget = prefix + "L_" + bone_name
                        elif vatproperties.scheme == 1:
                            rot.subtarget = prefix + bone_name + "_L"
                    else:
                        print("Left rotation constraint already in place for " + bone_name + ". Skipping")

            elif vatproperties.sfm_armature == 1:
                prefix = "bip_"
                if vatproperties.affected_side == 'OP1':
                    if ConstraintSymmetry.loc_leftconstraint == 0:
                        loc = armature.pose.bones[prefix + bone_name + "_L"].constraints.new('COPY_LOCATION')
                        
                        loc.name = "Constraint Symmetry Location"
                        loc.target = armature
                        loc.invert_x = True
                        loc.subtarget = prefix + bone_name + "_R"
                    else:
                        print("Right location constraint already in place for " + bone_name + ". Skipping")

                    if ConstraintSymmetry.rot_leftconstraint == 0:
                        rot = armature.pose.bones[prefix + bone_name + "_L"].constraints.new('COPY_ROTATION')

                        rot.name = "Constraint Symmetry Rotation"
                        rot.target = armature
                        rot.target_space = 'LOCAL'
                        rot.owner_space = 'LOCAL'
                        rot.invert_y = True
                        rot.invert_x = True
                        rot.subtarget = prefix + bone_name + "_R"

                    else:
                        print("Right rotation constraint already in place for " + bone_name + ". Skipping")

                elif vatproperties.affected_side == 'OP2':
                    if ConstraintSymmetry.loc_rightconstraint == 0:
                        loc = armature.pose.bones[prefix + bone_name + "_R"].constraints.new('COPY_LOCATION')

                        loc.name = "Constraint Symmetry Location"
                        loc.target = armature
                        loc.invert_x = True
                        loc.subtarget = prefix + bone_name + "_L"
                    else:
                        print("Left location constraint already in place for " + bone_name + ". Skipping")

                    if ConstraintSymmetry.rot_rightconstraint == 0:
                        rot = armature.pose.bones[prefix + bone_name + "_R"].constraints.new('COPY_ROTATION')  

                        rot.name = "Constraint Symmetry Rotation"
                        rot.target = armature
                        rot.target_space = 'LOCAL'
                        rot.owner_space = 'LOCAL'
                        rot.invert_y = True
                        rot.invert_x = True
                        rot.subtarget = prefix + bone_name + "_L"

        elif action == 1: #Constraint deletion
            vatproperties = bpy.context.scene.vatproperties
            armature = bpy.data.objects[vatproperties.target_armature.name]
            
            ConstraintSymmetry.getconstraint(bone_name)

            if vatproperties.sfm_armature == 0:
                prefix = "ValveBiped.Bip01_"
                if vatproperties.affected_side == 'OP1':
                    if ConstraintSymmetry.locL != "":
                        if vatproperties.scheme == 0:
                            armature.pose.bones[prefix + "L_" + bone_name].constraints.remove(ConstraintSymmetry.locL)
                        elif vatproperties.scheme == 1:
                            armature.pose.bones[prefix + bone_name + "_L"].constraints.remove(ConstraintSymmetry.locL)
                    else:
                        print("Left location constraint not found for " + bone_name + ". Skipping")
                    if ConstraintSymmetry.rotL != "":
                        if vatproperties.scheme == 0:
                            armature.pose.bones[prefix + "L_" + bone_name].constraints.remove(ConstraintSymmetry.rotL)
                        elif vatproperties.scheme == 1:
                            armature.pose.bones[prefix + bone_name + "_L"].constraints.remove(ConstraintSymmetry.rotL)
                    else:
                        print("Left rotation constraint not found for " + bone_name + ". Skipping")
                elif vatproperties.affected_side == 'OP2':
                    if ConstraintSymmetry.locR != "":
                        if vatproperties.scheme == 0:
                            armature.pose.bones[prefix + "R_" + bone_name].constraints.remove(ConstraintSymmetry.locR)
                        elif vatproperties.scheme == 1:
                            armature.pose.bones[prefix + bone_name + "_R"].constraints.remove(ConstraintSymmetry.locR)
                    else:
                        print("Right location constraint not found for " + bone_name + ". Skipping")
                    if ConstraintSymmetry.rotR != "":
                        if vatproperties.scheme == 0:
                            armature.pose.bones[prefix + "R_" + bone_name].constraints.remove(ConstraintSymmetry.rotR)
                        elif vatproperties.scheme == 1:
                            armature.pose.bones[prefix + bone_name + "_R"].constraints.remove(ConstraintSymmetry.rotR)
                    else:
                        print("Right rotation constraint not found for " + bone_name + ". Skipping")

            elif vatproperties.sfm_armature == 1:
                prefix = "bip_"
                if vatproperties.affected_side == 'OP1':
                    if ConstraintSymmetry.locL == "":
                        armature.pose.bones[prefix + bone_name + "_L"].constraints.remove(ConstraintSymmetry.locL)
                    else:
                        print("Left location constraint not found for " + bone_name + ". Skipping")
                    if ConstraintSymmetry.rotL == "":
                        armature.pose.bones[prefix + bone_name + "_L"].constraints.remove(ConstraintSymmetry.rotL)
                    else:
                        print("Left rotation constraint not found for " + bone_name + ". Skipping")
                elif vatproperties.affected_side == 'OP2':
                    if ConstraintSymmetry.locL == "":
                        armature.pose.bones[prefix + bone_name + "_R"].constraints.remove(ConstraintSymmetry.locR)
                    else:
                        print("Right location constraint not found for " + bone_name + ". Skipping")
                    if ConstraintSymmetry.rotL == "":
                        armature.pose.bones[prefix + bone_name + "_R"].constraints.remove(ConstraintSymmetry.rotR)
                    else:
                        print("Right rotation constraint not found for " + bone_name + ". Skipping")

    def execute(action):
        vatproperties = bpy.context.scene.vatproperties
        for bone in BoneList.symmetrical_bones:
            try:
                ConstraintSymmetry.constraint(bone, vatproperties.affected_side, action)
            except:
                print(bone + " not found, cannot modify constraints. Proceeding...")
                pass

        for bone in BoneList.symmetrical_bones_helper:
            try:
                ConstraintSymmetry.constraint(bone, vatproperties.affected_side, action)
            except:
                print(bone + " (helper bone) not found, cannot modify constraints. Proceeding...")
                pass
                
        for bone in BoneList.symmetrical_bones_viewmodel:
            try:
                ConstraintSymmetry.constraint(bone, vatproperties.affected_side, action)
            except:
                print(bone + " (viewmodel bone) not found, cannot modify constraints. Proceeding...")
                pass
                
        for bone in BoneList.symmetrical_bones_legacy:
            try:
                ConstraintSymmetry.constraint(bone, vatproperties.affected_side, action)
            except:
                print(bone + " (legacy bone) not found, cannot modify constraints. Proceeding...")
                pass

class WeightArmature: #Creates duplicate armature for more spread out weighting

    def create():
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]
        
        armature.copy()
        weightarmature = bpy.data.objects[vatproperties.target_armature.name + ".001"]
        weightarmature.name = vatproperties.target_armature.name + "_WeightArmature"
        collection = bpy.data.collections.new("WeightArmature")
        bpy.data.collections[collection.name].objects.link(weightarmature)

    def connect(bone_name):
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]
        
    def execute(action):
        WeightArmature.create()
        pass

class InverseKinematics: #Adds IK to the armature
    
    #Check if constraints exist
    rightconstraint = 0
    leftconstraint = 0

    #Additional check for deletion
    leftik = ""
    rightik = ""

    def getconstraint(bone_name):
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]
        if vatproperties.sfm_armature == 0:
            prefix = "ValveBiped.Bip01_"
            if vatproperties.scheme == 0:
                try:
                    InverseKinematics.leftik = armature.pose.bones[prefix + "L_" + bone_name].constraints['IK']
                except:
                    InverseKinematics.leftik = ""
                try:
                    InverseKinematics.rightik = armature.pose.bones[prefix + "R_" + bone_name].constraints['IK']
                except:
                    InverseKinematics.rightik = ""
            elif vatproperties.scheme == 1:
                try:
                    InverseKinematics.leftik = armature.pose.bones[prefix + bone_name + "_L"].constraints['IK']
                except:
                    InverseKinematics.leftik = ""
                try:
                    InverseKinematics.rightik = armature.pose.bones[prefix + bone_name + "_R"].constraints['IK']
                except:
                    InverseKinematics.rightik = ""

            if InverseKinematics.leftik != "":
                InverseKinematics.leftconstraint = 1
            else:
                InverseKinematics.leftconstraint = 0
            if InverseKinematics.rightik != "":
                InverseKinematics.rightconstraint = 1
            else:
                InverseKinematics.rightconstraint = 0

        elif vatproperties.sfm_armature == 1:
            prefix = "bip_"
            try:
                InverseKinematics.leftik = armature.pose.bones[prefix + bone_name + "_L"].constraints['IK']
            except:
                InverseKinematics.leftik = ""
            try:
                InverseKinematics.rightik = armature.pose.bones[prefix + bone_name + "_R"].constraints['IK']
            except:
                InverseKinematics.rightik = ""

    def IK(bone_name, action):
        vatproperties = bpy.context.scene.vatproperties
        armature = bpy.data.objects[vatproperties.target_armature.name]

        InverseKinematics.getconstraint(bone_name)

        if action == 0: #Generates IK constraints
            if vatproperties.sfm_armature == 0:
                prefix = "ValveBiped.Bip01_"
                if vatproperties.scheme == 0:
                    if InverseKinematics.leftconstraint == 0:
                        leftik = armature.pose.bones[prefix + "L_" + bone_name].constraints.new('IK')
                    else:
                        print("Left IK for " + bone_name + " already exists. Skipping")
                    if InverseKinematics.rightconstraint == 0:
                        rightik = armature.pose.bones[prefix + "R_" + bone_name].constraints.new('IK')
                    else:
                        print("Right IK for " + bone_name + " already exists. Skipping")
                elif vatproperties.scheme == 1:
                    if InverseKinematics.leftconstraint == 0:
                        leftik = armature.pose.bones[prefix + bone_name + "_L"].constraints.new('IK')
                    else:
                        print("Left IK for " + bone_name + " already exists. Skipping")
                    if InverseKinematics.rightconstraint == 0:
                        rightik = armature.pose.bones[prefix + bone_name + "_R"].constraints.new('IK') 
                    else:
                        print("Right IK for " + bone_name + " already exists. Skipping")

            elif vatproperties.sfm_armature == 1:
                prefix = "bip_"
                if InverseKinematics.leftconstraint == 0:
                    leftik = armature.pose.bones[prefix + bone_name + "_L"].constraints.new('IK')
                else:
                    print("Left IK for " + bone_name + " already exists. Skipping")
                if InverseKinematics.rightconstraint == 0:
                    rightik = armature.pose.bones[prefix + bone_name + "_R"].constraints.new('IK')
                else:
                    print("Right IK for " + bone_name + " already exists. Skipping")

            if InverseKinematics.leftconstraint == 0:
                leftik.chain_count = 3
            if InverseKinematics.rightconstraint == 0:
                rightik.chain_count = 3

        elif action == 1: #Deletes generated constraints
            if vatproperties.sfm_armature == 0:
                prefix = "ValveBiped.Bip01_"
                if vatproperties.scheme == 0:
                    if InverseKinematics.leftik != "": #Checks if there are any constraints on bone
                        armature.pose.bones[prefix + "L_" + bone_name].constraints.remove(InverseKinematics.leftik)
                    else:
                        print("Left IK constraint not found for " + bone_name + ". Skipping")
                    if InverseKinematics.rightik != "":
                        armature.pose.bones[prefix + "R_" + bone_name].constraints.remove(InverseKinematics.rightik)
                    else:
                        print("Right IK constraint not found for " + bone_name + ". Skipping")
                elif vatproperties.scheme == 1:
                    if InverseKinematics.leftik != "":
                        armature.pose.bones[prefix + bone_name + "_L"].constraints.remove(InverseKinematics.leftik)
                    else:
                        print("Left IK constraint not found for " + bone_name + ". Skipping")
                    if InverseKinematics.rightik != "":
                        armature.pose.bones[prefix + bone_name + "_R"].constraints.remove(InverseKinematics.rightik)
                    else:
                        print("Right IK constraint not found for " + bone_name + ". Skipping")
            elif vatproperties.sfm_armature == 1:
                prefix = "bip_"
                if InverseKinematics.leftik != "":
                    armature.pose.bones[prefix + bone_name + "_L"].constraints.remove(InverseKinematics.leftik)
                else:
                    print("Left IK constraint not found for " + bone_name + ". Skipping")
                if InverseKinematics.rightik != "":
                    armature.pose.bones[prefix + bone_name + "_R"].constraints.remove(InverseKinematics.rightik)
                else:
                    print("Right IK constraint not found for " + bone_name + ". Skipping")

    def execute(action): #Creates, or deletes IK
        for bone in BoneList.ik_bones:
            InverseKinematics.IK(bone, action)