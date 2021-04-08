import bpy
import math
from bpy.app.handlers import persistent

class Prefixes: #Container for other prefixes
    helper = 'hlp_'
    helper2 = 'ValveBiped.hlp_'
    attachment = 'ValveBiped.attachment_'
    other = 'ValveBiped.'

@persistent
def create_armature(self, context): #Creates new armature class
    global vatproperties
    vatproperties = bpy.context.scene.vatproperties
    if vatproperties.target_armature:
        global arm
        arm = Armature(vatproperties.target_armature)

@persistent
def armatures_reset(*args):
    vatproperties = bpy.context.scene.vatproperties
    if vatproperties.target_armature:
        arm.armature = bpy.data.objects[arm._armature]
        arm.armature_real = bpy.data.armatures[arm._armature_real]
    
        if arm.weight_armature_created:
            arm.weight_armature = bpy.data.objects[arm._weight_armature]
        if arm.animation_armature_created:
            arm.animation_armature = bpy.data.objects[arm._animation_armature]

class Armature: #Armature base

    def __init__(self, armature):
        #Basic armature information
        self.armature = armature
        self._armature = str(armature.name)
        self.armature_real = armature.data
        self._armature_real = str(armature.data.name)

        #Armature type, scheme and prefix
        self.scheme = -1 #-1 = No armature, 0 = Source, 1 = Blender, 2 = SFM, 3 = Custom 1, 4 = Custom 2
        self.sfm = False
        self.prefix = ''

        #Bone information
        self.full_bonelist = []
        self.symmetrical_bones = {'arms': {'clavicle': [], 'upperarm': [], 'forearm': [], 'hand': []}, 'legs': {'thigh': [], 'calf': [], 'foot': [], 'toe': []}, 'fingers': {'finger0': [], 'finger01': [], 'finger02': [], 'finger1': [], 'finger11': [], 'finger12': [], 'finger2': [], 'finger21': [], 'finger22': [], 'finger3': [], 'finger31': [], 'finger32': [], 'finger4': [], 'finger41': [], 'finger42': []}}
        self.central_bones = {'pelvis': [], 'spine': [], 'spine1': [], 'spine2': [], 'spine4': [], 'neck': [], 'head': []}
        self.helper_bones = {'arms': {'trapezius': [], 'bicep': [], 'elbow': [], 'ulna': [], 'wrist': []}, 'legs': {'quadricep': [], 'knee': []}, 'others': {'others': []}}
        self.other_bones = {'forward': [], 'weapon': [], 'attachment': [], 'others': []}
        self.custom_bones = {'others': []}

        #Additional information for operations

        #Constraints
        self.symmetry_left = False
        self.symmetry_right = False

        #Weight armature
        self.weight_armature_created = False
        self.weight_armature = None
        self.weight_armature_real = None

        #Animation armature
        self.animation_armature_created = False
        self.animation_armature_setup = True
        self.animation_armature = None
        self.animation_armature_real = None
        self.facial_bones = []

        self.isolatedbones = []

        #Object information
        self.shapekeys = None

        #Functions executed to gather previous information
        self.get_bones(True)
        if self.scheme != -1:
            self.get_scheme()
            self.get_armatures()
            self.get_constraints()
            self.set_groups()
            if self.helper_bones:
                self.set_procedural_bones()
        else:
            print("Empty armature, cannot proceed")
            
    def get_bones(self, report): #Builds bone lists
        armature = self.armature

        if self.armature:
            #Cleans bone list
            self.full_bonelist = []
            self.symmetrical_bones = {'arms': {'clavicle': [], 'upperarm': [], 'forearm': [], 'hand': []}, 'legs': {'thigh': [], 'calf': [], 'foot': [], 'toe': []}, 'fingers': {'finger0': [], 'finger01': [], 'finger02': [], 'finger1': [], 'finger11': [], 'finger12': [], 'finger2': [], 'finger21': [], 'finger22': [], 'finger3': [], 'finger31': [], 'finger32': [], 'finger4': [], 'finger41': [], 'finger42': []}}
            self.central_bones = {'pelvis': [], 'spine': [], 'spine1': [], 'spine2': [], 'spine4': [], 'neck': [], 'head': []}
            self.helper_bones = {'arms': {'trapezius': [], 'bicep': [], 'elbow': [], 'ulna': [], 'wrist': []}, 'legs': {'quadricep': [], 'knee': []}, 'others': {'others': []}}
            self.other_bones = {'forward': [], 'weapon': [], 'attachment': [], 'others': []}
            self.custom_bones = {'others': []}

            self.full_bonelist = armature.data.bones.keys() #Gets all bones in armature

            #Checks if bone list is empty
            if self.full_bonelist:

                symmetrical_bones_raw = []
                central_bones_raw = []
                helper_bones_raw = []
                other_bones_raw = []
                custom_bones_raw = []

                for bone in self.full_bonelist:

                    #Custom prefixes
                    if vatproperties.custom_scheme_enabled and vatproperties.custom_scheme_prefix:
                        self.prefix = vatproperties.custom_scheme_prefix

                        if bone.startswith(self.prefix + bone.count('L_') == 0 or bone.count('R_') == 0 or bone.count('_L') == 0 or bone.count('_R') == 0):
                            if bone.count('L_') == 0 or bone.count('R_') == 0:
                                self.scheme = 3
                            elif bone.count('_L') == 0 or bone.count('L_') == 0:
                                self.scheme = 3
                            symmetrical_bones_raw.append(bone.replace(self.prefix, ''))

                        elif bone.startswith(self.prefix):
                            central_bones_raw.append(bone.replace(self.prefix, ''))

                    #Helper prefix
                    if bone.startswith('hlp_'):
                        helper_bones_raw.append(bone.replace(Prefixes.helper, ''))

                    #Source and Blender prefixes
                    elif bone.startswith('ValveBiped.'):
                        vatproperties.sfm_armature = False
                        self.prefix = 'ValveBiped.Bip01_'

                        #Strange L4D2 helper prefix, must be differentiated from the usual helper bone with 's2.'
                        if bone.startswith('ValveBiped.hlp_'):
                            helper_bones_raw.append(bone.replace('ValveBiped.hlp_', 's2.'))

                        #Helper bones without helper prefix, differentiated with 's.'
                        elif bone.title().count('Ulna') or bone.title().count('Wrist') or bone.title().count('Elbow') or bone.title().count('Knee') or bone.title().count('Trapezius') or bone.title().count('Quad') or bone.title().count('Bicep') or bone.title().count('Shoulder'):
                            helper_bones_raw.append(bone.replace(self.prefix, 's.'))

                        #Attachment bone prefix. They are supposed to be in other bones instead
                        elif bone.startswith('ValveBiped.attachment'):
                            other_bones_raw.append(bone.replace('ValveBiped.attachment_', 'a.'))

                        #Default prefix
                        elif bone.startswith(self.prefix + 'L_') or bone.startswith(self.prefix + 'R_'): #Symmetrical
                            self.scheme = 0
                            symmetrical_bones_raw.append(bone.replace(self.prefix, ''))

                        #Blender prefix
                        elif bone.endswith('_L') or bone.endswith('_R'):
                            self.scheme = 1
                            symmetrical_bones_raw.append(bone.replace(self.prefix, ''))

                        #Central bones prefix
                        elif bone.startswith('ValveBiped.Bip01_'): #Central
                            central_bones_raw.append(bone.replace(self.prefix, ''))
                            
                        else: #Other
                            other_bones_raw.append(bone.replace('ValveBiped.', ''))

                    #SFM prefix
                    elif bone.startswith('bip_'): # Central
                        vatproperties.sfm_armature = True
                        self.scheme = 2
                        self.sfm = True
                        self.prefix = 'bip_'

                        if bone.endswith('_L') or bone.endswith('_R'): #Symmetrical
                            symmetrical_bones_raw.append(bone.replace(self.prefix, ''))

                        else:
                            central_bones_raw.append(bone.replace(self.prefix, ''))

                    #No/Different prefix
                    else:
                        custom_bones_raw.append(bone)
                        custom_bones_raw.sort()

                #Unknown armature
                if not symmetrical_bones_raw and not central_bones_raw and not self.other_bones:
                    self.scheme = -1

                #Organizes dictionary from raw lists

                #Symmetrical bones raw list
                if symmetrical_bones_raw:
                    for bone in symmetrical_bones_raw:

                        if bone.title().count('Clavicle'):
                            self.symmetrical_bones['arms']['clavicle'].append(bone)
                            self.symmetrical_bones['arms']['clavicle'].sort()

                        elif bone.title().count('Upperarm'):
                            self.symmetrical_bones['arms']['upperarm'].append(bone)
                            self.symmetrical_bones['arms']['upperarm'].sort()

                        elif bone.title().count('Forearm'):
                            self.symmetrical_bones['arms']['forearm'].append(bone)
                            self.symmetrical_bones['arms']['forearm'].sort()

                        elif bone.title().count('Hand'):
                            self.symmetrical_bones['arms']['hand'].append(bone)
                            self.symmetrical_bones['arms']['hand'].sort()

                        elif bone.title().count('Thigh'):
                            self.symmetrical_bones['legs']['thigh'].append(bone)
                            self.symmetrical_bones['legs']['thigh'].sort()

                        elif bone.title().count('Calf'):
                            self.symmetrical_bones['legs']['calf'].append(bone)
                            self.symmetrical_bones['legs']['calf'].sort()

                        elif bone.title().count('Foot'):
                            self.symmetrical_bones['legs']['foot'].append(bone)
                            self.symmetrical_bones['legs']['foot'].sort()

                        elif bone.title().count('Toe'):
                            self.symmetrical_bones['legs']['toe'].append(bone)
                            self.symmetrical_bones['legs']['toe'].sort()

                        elif bone.title().count('Finger0'):
                            if bone.count('01'):
                                self.symmetrical_bones['fingers']['finger01'].append(bone)
                                self.symmetrical_bones['fingers']['finger01'].sort()
                            elif bone.count('02'):
                                self.symmetrical_bones['fingers']['finger02'].append(bone)
                                self.symmetrical_bones['fingers']['finger02'].sort()
                            else:
                                self.symmetrical_bones['fingers']['finger0'].append(bone)
                                self.symmetrical_bones['fingers']['finger0'].sort()

                        elif bone.title().count('Finger1'):
                            if bone.count('11'):
                                self.symmetrical_bones['fingers']['finger11'].append(bone)
                                self.symmetrical_bones['fingers']['finger11'].sort()
                            elif bone.count('12'):
                                self.symmetrical_bones['fingers']['finger12'].append(bone)
                                self.symmetrical_bones['fingers']['finger12'].sort()
                            else:
                                self.symmetrical_bones['fingers']['finger1'].append(bone)
                                self.symmetrical_bones['fingers']['finger1'].sort()

                        elif bone.title().count('Finger2'):
                            if bone.count('21'):
                                self.symmetrical_bones['fingers']['finger21'].append(bone)
                                self.symmetrical_bones['fingers']['finger21'].sort()
                            elif bone.count('22'):
                                self.symmetrical_bones['fingers']['finger22'].append(bone)
                                self.symmetrical_bones['fingers']['finger22'].sort()
                            else:
                                self.symmetrical_bones['fingers']['finger2'].append(bone)
                                self.symmetrical_bones['fingers']['finger2'].sort()
                            
                        elif bone.title().count('Finger3'):
                            if bone.count('31'):
                                self.symmetrical_bones['fingers']['finger31'].append(bone)
                                self.symmetrical_bones['fingers']['finger31'].sort()
                            elif bone.count('32'):
                                self.symmetrical_bones['fingers']['finger32'].append(bone)
                                self.symmetrical_bones['fingers']['finger32'].sort()
                            else:
                                self.symmetrical_bones['fingers']['finger3'].append(bone)
                                self.symmetrical_bones['fingers']['finger3'].sort()

                        elif bone.title().count('Finger4'):
                            if bone.count('41'):
                                self.symmetrical_bones['fingers']['finger41'].append(bone)
                                self.symmetrical_bones['fingers']['finger41'].sort()
                            elif bone.count('42'):
                                self.symmetrical_bones['fingers']['finger42'].append(bone)
                                self.symmetrical_bones['fingers']['finger42'].sort()
                            else:
                                self.symmetrical_bones['fingers']['finger4'].append(bone)
                                self.symmetrical_bones['fingers']['finger4'].sort()

                #Central bones raw list
                if central_bones_raw:
                    for bone in central_bones_raw:
                        if bone.title().count('Pelvis'):
                            self.central_bones['pelvis'].append(bone)
                            self.central_bones['pelvis'].sort()

                        elif bone.title().count('Spine'):
                            if bone.title().count('Spine4'):
                                self.central_bones['spine4'].append(bone)
                                self.central_bones['spine4'].sort()

                            elif bone.title().count('Spine2'):
                                self.central_bones['spine2'].append(bone)
                                self.central_bones['spine2'].sort()

                            elif bone.title().count('Spine1'):
                                self.central_bones['spine1'].append(bone)
                                self.central_bones['spine1'].sort()
                            
                            else:
                                self.central_bones['spine'].append(bone)
                                self.central_bones['spine'].sort()

                        elif bone.title().count('Neck'):
                            self.central_bones['neck'].append(bone)
                            self.central_bones['neck'].sort()

                        elif bone.title().count('Head'):
                            self.central_bones['head'].append(bone)
                            self.central_bones['head'].sort()

                #Helper bones raw list
                if helper_bones_raw:
                    for bone in helper_bones_raw:
                        if bone.title().count('Trapezius'):
                            self.helper_bones['arms']['trapezius'].append(bone)
                            self.helper_bones['arms']['trapezius'].sort()

                        elif bone.title().count('Bicep'):
                            self.helper_bones['arms']['bicep'].append(bone)
                            self.helper_bones['arms']['bicep'].sort()

                        elif bone.title().count('Elbow'):
                            self.helper_bones['arms']['elbow'].append(bone)
                            self.helper_bones['arms']['elbow'].sort()

                        elif bone.title().count('Ulna'):
                            self.helper_bones['arms']['ulna'].append(bone)
                            self.helper_bones['arms']['ulna'].sort()

                        elif bone.title().count('Wrist'):
                            self.helper_bones['arms']['wrist'].append(bone)
                            self.helper_bones['arms']['wrist'].sort()

                        elif bone.title().count('Quad'):
                            self.helper_bones['legs']['quadricep'].append(bone)
                            self.helper_bones['legs']['quadricep'].sort()

                        elif bone.title().count('Knee'):
                            self.helper_bones['legs']['knee'].append(bone)
                            self.helper_bones['legs']['knee'].sort()

                        else:
                            #Creates pairs for helper bones that aren't the conventional
                            if bone.startswith('s.'):
                                bone2 = bone.replace('s.', '')
                            elif bone.startswith('s2.'):
                                bone2 = bone.replace('s2.', '')

                            if bone2.title().startswith('L_'):
                                self.helper_bones['others'].setdefault(bone2.title().replace('L_', '').casefold(), [])
                                self.helper_bones['others'][bone2.title().replace('L_', '').casefold()].append(bone)
                                self.helper_bones['others'][bone2.title().replace('L_', '').casefold()].sort()
                            elif bone2.title().endswith('_L'):
                                self.helper_bones['others'].setdefault(bone2.replace('_L', '').casefold(), [])
                                self.helper_bones['others'][bone2.title().replace('_L', '').casefold()].append(bone)
                                self.helper_bones['others'][bone2.title().replace('_L', '').casefold()].sort()
                            elif bone2.title().startswith('R_'):
                                self.helper_bones['others'].setdefault(bone2.replace('R_', '').casefold(), [])
                                self.helper_bones['others'][bone2.title().replace('R_', '').casefold()].append(bone)
                                self.helper_bones['others'][bone2.title().replace('R_', '').casefold()].sort()
                            elif bone2.title().endswith('_R'):
                                self.helper_bones['others'].setdefault(bone2.replace('_R', '').casefold(), [])
                                self.helper_bones['others'][bone2.title().replace('_R', '').casefold()].append(bone)
                                self.helper_bones['others'][bone2.title().replace('_R', '').casefold().casefold()].sort()
                            else:
                                self.helper_bones['others']['others'].append(bone)
                                self.helper_bones['others']['others'].sort()

                #Other bones raw list
                if other_bones_raw:
                    for bone in other_bones_raw:
                        if bone.title().count('Forward'):
                            self.other_bones['forward'].append(bone)
                            self.other_bones['forward'].sort()

                        elif bone.title().count('Weapon'):
                            self.other_bones['weapon'].append(bone)
                            self.other_bones['weapon'].sort()

                        elif bone.startswith('a.'):
                            self.other_bones['attachment'].append(bone)
                            self.other_bones['attachment'].sort()

                        else:
                            self.other_bones['others'].append(bone)
                            self.other_bones['others'].sort()

                if custom_bones_raw:
                    for bone in custom_bones_raw:
                        if bone.title().startswith('L_'):
                            self.custom_bones.setdefault(bone.title().replace('L_', '').casefold(), [])
                            self.custom_bones[bone.title().replace('L_', '').casefold()].append(bone)
                            self.custom_bones[bone.title().replace('L_', '').casefold()].sort()
                        elif bone.title().endswith('_L'):
                            self.custom_bones.setdefault(bone.title().replace('_L', '').casefold(), [])
                            self.custom_bones[bone.title().replace('_L', '').casefold()].append(bone)
                            self.custom_bones[bone.title().replace('_L', '').casefold()].sort()
                        elif bone.title().startswith('Left'):
                            self.custom_bones.setdefault(bone.title().replace('Left', '').casefold(), [])
                            self.custom_bones[bone.title().replace('Left', '').casefold()].append(bone)
                            self.custom_bones[bone.title().replace('Left', '').casefold()].sort()
                        elif bone.title().startswith('R_'):
                            self.custom_bones.setdefault(bone.title().replace('R_', '').casefold(), [])
                            self.custom_bones[bone.title().replace('R_', '').casefold()].append(bone)
                            self.custom_bones[bone.title().replace('R_', '').casefold()].sort()
                        elif bone.title().endswith('_R'):
                            self.custom_bones.setdefault(bone.title().replace('_R', '').casefold(), [])
                            self.custom_bones[bone.title().replace('_R', '').casefold()].append(bone)
                            self.custom_bones[bone.title().replace('_R', '').casefold()].sort()
                        elif bone.title().startswith('Right'):
                            self.custom_bones.setdefault(bone.title().replace('Right', '').casefold(), [])
                            self.custom_bones[bone.title().replace('Right', '').casefold()].append(bone)
                            self.custom_bones[bone.title().replace('Right', '').casefold()].sort()
                        else:
                            self.custom_bones['others'].append(bone)
                            self.custom_bones['others'].sort()
                
                #Final bone report
                if report:
                    print("Symmetrical bones:", list(self.symmetrical_bones.values()))
                    print("Central bones:", list(self.central_bones.values()))
                    print("Helper bones:", list(self.helper_bones.values()))
                    print("Other bones:", list(self.other_bones.values()))
                    print("Custom bones:", self.custom_bones)
                
            else:
                self.scheme = -1

    def get_scheme(self): #Gets current scheme
        armature = self.armature

        for bone in self.symmetrical_bones:

            #If not an SFM armature, check if the armature has the Source or Blender armature
            if not self.sfm:
                if bone.startswith('L_') or bone.startswith('R_'):
                    self.scheme = 0
                    vatproperties.check_armature_rename = False

                elif bone.endswith('_L') or bone.endswith('_R'):
                    self.scheme = 1
                    vatproperties.check_armature_rename = True
                
        #Final scheme report
        if not self.sfm:
            if self.scheme == 0:
                print("Current Scheme: Source")

            elif self.scheme == 1:
                print("Current Scheme: Blender")

        elif self.sfm:
            print("Current Scheme: Source (SFM)")

    def get_armatures(self): #Gets generated armatures for selected armature

        def get_weight_armature():
            try:
                self.weight_armature = bpy.data.objects[self.armature.name + '.weight']
                self.weight_armature_real = bpy.data.armatures[self.armature_real.name + '.weight']
                self.weight_armature_created = True
                print("Weight armature detected")
            except:
                self.weight_armature_created = False
        
        def get_anim_armature():
            #Checks if it's a setup armature or a proper armature
            try:
                try:
                    self.animation_armature = bpy.data.objects[self.armature.name + '.anim']
                    self.animation_armature_setup = False
                except:
                    self.animation_armature_name = bpy.data.objects[self.armature.name + '.anim_setup']
                    self.animation_armature_setup = True

                try:
                    self.animation_armature_real = bpy.data.armatures[self.armature_real.name + '.anim']
                    self.animation_armature_setup = False
                except:
                    self.animation_armature_real = bpy.data.armatures[self.armature_real.name + '.anim_setup']
                    self.animation_armature_setup = True

                self.animation_armature_created = True

                if self.animation_armature_setup:
                    print("Setup animation armature detected")
                elif not self.animation_armature_setup:
                    print("Animation armature detected")

            except:
                self.animation_armature_created = False

        get_weight_armature()
        get_anim_armature()

    def get_constraints(self): #Gets previously added constraints that have not been removed

        def get_symmetry(): 
            armature = self.armature
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
            
        get_symmetry()

    def set_groups(self): #Organizes bones by bone group and bone layers
        armature = self.armature
        prefix = self.prefix

        #Checks if any groups exist already
        group = armature.pose.bone_groups.keys()

        if not group:
            #Creates groups and sets their color
            for group, color in zip(['Center', 'Left Arm', 'Right Arm', 'Left Leg', 'Right Leg', 'Helpers', 'Attachments', 'Others', 'Custom'], ['THEME03', 'THEME01', 'THEME04', 'THEME01', 'THEME04', 'THEME09', 'THEME14', 'THEME10', 'THEME06']):
                armature.pose.bone_groups.new(name=group)
                armature.pose.bone_groups[group].color_set = color
                
            
            for cat in self.symmetrical_bones.keys():
                #Arms and fingers
                if cat == 'arms' or cat == 'fingers':
                    for bone in self.symmetrical_bones[cat].values():
                        for bone in bone:
                            if bone.startswith('L_') or bone.endswith('_L'):
                                armature.pose.bones[prefix + bone].bone_group_index = 1
                                armature.data.bones[prefix + bone].layers[1] = True

                            elif bone.startswith('R_') or bone.endswith('_R'):
                                armature.pose.bones[prefix + bone].bone_group_index = 2
                                armature.data.bones[prefix + bone].layers[2] = True

                            armature.data.bones[prefix + bone].layers[0] = False

                #Legs
                elif cat == 'legs':
                    for bone in self.symmetrical_bones[cat].values():
                        for bone in bone:
                            if bone.startswith('L_') or bone.endswith('_L'):
                                armature.pose.bones[prefix + bone].bone_group_index = 3
                                armature.data.bones[prefix + bone].layers[3] = True
                                
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                armature.pose.bones[prefix + bone].bone_group_index = 4
                                armature.data.bones[prefix + bone].layers[4] = True

                            armature.data.bones[prefix + bone].layers[0] = False
                    
            for bone in self.central_bones.values():
                for bone in bone:
                    armature.pose.bones[prefix + bone].bone_group_index = 0

            if self.helper_bones:
                for cat in self.helper_bones.keys():
                    for bone in self.helper_bones[cat].values():
                        for bone in bone:
                            if bone.startswith('s.'):
                                prefix = self.prefix
                                bone = bone.replace('s.', '')

                            elif bone.startswith('s2.'):
                                prefix = Prefixes.helper2
                                bone = bone.replace('s2.', '')
                            else:
                                prefix = Prefixes.helper

                            armature.pose.bones[prefix + bone].bone_group_index = 5
                            armature.data.bones[prefix + bone].layers[5] = True
                            armature.data.bones[prefix + bone].layers[0] = False

    
            for container, bone in self.other_bones.items():
                for bone in bone:
                    if container == 'attachment':
                        prefix = Prefixes.attachment
                        bone = bone.replace('a.', '')
                        armature.pose.bones[prefix + bone].bone_group_index = 6
                        armature.data.bones[prefix + bone].layers[6] = True
                    else:
                        prefix = Prefixes.other
                
                        armature.pose.bones[prefix + bone].bone_group_index = 7
                        armature.data.bones[prefix + bone].layers[7] = True
                        armature.data.bones[prefix + bone].layers[0] = False
                
            #Custom bones
            for bone in self.custom_bones.values():
                for bone in bone:
                    armature.pose.bones[bone].bone_group_index = 8
                    armature.data.bones[bone].layers[8] = True
                    armature.data.bones[bone].layers[0] = False

            #Reveals used layers
            for i in [0,1,2,3,4,5,6,7,8]:
                armature.data.layers[i] = True

            print("Bone groups set!")
            
    def set_procedural_bones(self):
        armature = self.armature
        prefix = self.prefix

        new = True

        for bone in self.helper_bones['arms']['elbow'] + self.helper_bones['arms']['ulna'] + self.helper_bones['arms']['wrist'] + self.helper_bones['legs']['quadricep'] + self.helper_bones['legs']['knee']:
            if bone.startswith('s.'):
                prefix = self.prefix
                bone = bone.replace('s.', '')

            elif bone.startswith('s2.'):
                prefix = Prefixes.helper2
                bone = bone.replace('s2.', '')
            else:
                prefix = Prefixes.helper
            
            #Adds transforms to only these helper bones unless already existing
            for constraint in armature.pose.bones[prefix + bone].constraints:
                if constraint == "Procedural Bone":
                    new = False
                    break
            
            if new:
                transform = armature.pose.bones[prefix + bone].constraints.new('TRANSFORM')

                #Initial parameters
                transform.name = "Procedural Bone"
                transform.target = self.armature
                transform.map_from = 'ROTATION'
                transform.map_to = 'ROTATION'
                transform.target_space = 'LOCAL'
                transform.owner_space = 'LOCAL'
            
                #Hand rotation
                if bone.title().count('Wrist') or bone.title().count('Ulna'):
                    transform.from_min_x_rot = math.radians(-90)
                    transform.from_max_x_rot = math.radians(90)

                    prefix = self.prefix

                    if bone.startswith('L_') or bone.endswith('_L'):
                        transform.subtarget = prefix + self.symmetrical_bones['arms']['hand'][0]
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        transform.subtarget = prefix + self.symmetrical_bones['arms']['hand'][1]
                    else:
                        #Fix for Nick's left wrist
                        transform.subtarget = prefix + self.symmetrical_bones['arms']['hand'][1]

                    if bone.title().count('Wrist'):
                        transform.to_min_x_rot = math.radians(-75)
                        transform.to_max_x_rot = math.radians(75)

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
                        if bone.startswith('L_') or bone.endswith('_L'):
                            transform.subtarget = prefix + self.symmetrical_bones['arms']['forearm'][0]
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            transform.subtarget = prefix + self.symmetrical_bones['arms']['forearm'][1]

                    elif bone.title().count('Knee'):
                        if bone.startswith('L_') or bone.endswith('_L'):
                            transform.subtarget = prefix + self.symmetrical_bones['legs']['calf'][0]
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            transform.subtarget = prefix + self.symmetrical_bones['legs']['calf'][1]

                    elif bone.title().count('Quad'):
                        if bone.startswith('L_') or bone.endswith('_L'):
                            transform.subtarget = prefix + self.symmetrical_bones['legs']['thigh'][0]
                        elif bone.startswith('R_') or bone.endswith('_R'):
                            transform.subtarget = prefix + self.symmetrical_bones['legs']['thigh'][1]
        if new:
            print("Procedural bones configured!")

#Some functions (Namely creating new bones) do not add the newly created info to the object data until a mode change occurs at least once
def update(type, object=None):
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
    real_armature = bpy.data.armatures[arm.armature_real.name]
    
    #Creation
    if action == 0:

        #Weight armature datablock
        if type == 'weight':
            arm.weight_armature_real = real_armature.copy()
            arm.weight_armature_real.name = arm.armature_real.name + '.weight'

            #Creation and link to current scene
            arm.weight_armature_created = True
            arm.weight_armature = bpy.data.objects.new(arm.armature.name + '.weight', arm.weight_armature_real)

            try:
                collection = bpy.data.collections['Weight Amature']
            except:
                collection = bpy.data.collections.new("Weight Armature")
                bpy.context.scene.collection.children.link(collection)
            collection.objects.link(arm.weight_armature)

            armature = arm.weight_armature
            
        #Animation armature datablock
        elif type == 'anim':
            arm.animation_armature_real = real_armature.copy()
            arm.animation_armature_real.name = arm.armature_real.name + '.anim_setup'

            #Creation and link to current scene
            arm.animation_armature = bpy.data.objects.new(arm.armature.name + '.anim_setup', arm.animation_armature_real)
            arm.animation_armature_created = True
            try:
                collection = bpy.data.collections["Animation Armature"]
            except:
                collection = bpy.data.collections.new("Animation Armature")
                bpy.context.scene.collection.children.link(collection)
            collection.objects.link(arm.animation_armature)

            armature = arm.animation_armature
        
        #Variables for certain bones that require additional position tweaking
        ulna = []
        wrist = []
        bicep = []
        trapezius = []
        quadricep = []

        #Bone connection
        update(1, armature)

        #Keeps only the bare minimum bones for Rigify and connects the rest
        if type == 'anim':
            for cat in arm.helper_bones.keys():
                for bone in arm.helper_bones[cat].values():
                    for bone in bone:
                        bone, prefix = helper_convert(bone)

                        ebone = armature.data.edit_bones[prefix + bone]
                    
                        armature.data.edit_bones.remove(ebone)

        #Refreshes bone list
        arm.get_bones(False)
    
        arm.isolatedbones = []

        #Setup for armatures, tweaking bone positions and the like
        for cat in arm.symmetrical_bones.keys():
            if cat == 'fingers':
                prefix = arm.prefix
                for container, bone in arm.symmetrical_bones[cat].items():
                    for bone in bone:
                        #Creates copy of bone that retains the original rotation for the retarget empties
                        isolatedbone = armature.data.edit_bones.new(prefix + bone + ".isolated")
                        isolatedbone.head = armature.pose.bones[prefix + bone].head
                        isolatedbone.tail = armature.pose.bones[prefix + bone].tail
                        isolatedbone.roll = armature.data.edit_bones[prefix + bone].roll
                        isolatedbone.use_deform = False
                        isolatedbone.layers[28] = True
                        isolatedbone.layers[0] = False

                        arm.isolatedbones.append(isolatedbone.name)

                        parent = armature.pose.bones[prefix + bone].parent.name

                        #Makes it so the hand bone is facing straight
                        if parent.title().count('Hand'):
                            if container == 'finger0':
                                continue
                            else:
                                pbone = armature.pose.bones[prefix + bone]
                                
                                armature.data.edit_bones[parent].tail.xz = pbone.head.x, pbone.head.z
                                armature.data.edit_bones[parent].length = 3
                        else:
                            loc = armature.pose.bones[prefix + bone].head
                            armature.data.edit_bones[parent].tail = loc
                            
                            armature.data.edit_bones[prefix + bone].use_connect = True
            else:
                prefix = arm.prefix
                for container, bone in list(arm.symmetrical_bones[cat].items()):
                    for bone in bone:
                        #Creates copy of bone that retains the original rotation for the retarget empties
                        isolatedbone = armature.data.edit_bones.new(prefix + bone + ".isolated")
                        isolatedbone.head = armature.pose.bones[prefix + bone].head
                        isolatedbone.tail = armature.pose.bones[prefix + bone].tail
                        isolatedbone.roll = armature.data.edit_bones[prefix + bone].roll
                        isolatedbone.use_deform = False
                        isolatedbone.layers[28] = True
                        isolatedbone.layers[0] = False

                        arm.isolatedbones.append(isolatedbone.name)

                        parent = armature.pose.bones[prefix + bone].parent.name

                        loc = armature.pose.bones[prefix + bone].head
                        armature.data.edit_bones[parent].tail = loc
                        
                        #Filters out bones whose parent should not be connected to them
                        if container == 'thigh' or container == 'clavicle':
                            continue
                        else:
                            if type == 'weight':
                                if container == 'calf' or container == 'upperarm' or container == 'forearm' or container == 'hand':
                                    continue
                                
                        armature.data.edit_bones[prefix + bone].use_connect = True

                        #Bone tweaks

                        #Extends toe tip to be where the actual tip should be
                        if container == 'toe':
                            pbone = armature.pose.bones[prefix + bone].head

                            if bone.startswith('L_') or bone.endswith('_L'):
                                armature.data.edit_bones[prefix + bone].tail = pbone.x+0.5, pbone.y-2.5, pbone.z
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                armature.data.edit_bones[prefix + bone].tail = pbone.x-0.5, pbone.y-2.5, pbone.z

                        #Fix for legs rotating the wrong way in most characters with the animation armature
                        if type == 'anim':
                            if container == 'calf':
                                armature.data.edit_bones[prefix + bone].head.y = armature.data.edit_bones[prefix + bone].head.y - 1

                if type == 'weight':
                    for container, bone in list(arm.helper_bones[cat].items()):
                        for bone in bone:
                            bone, prefix = helper_convert(bone)
                            parent = armature.pose.bones[prefix + bone].parent.name

                            loc = armature.pose.bones[prefix + bone].head
                            armature.data.edit_bones[parent].tail = loc

                            #Filters out bones whose parent should not be connected to them
                            if container == 'knee' or container == 'elbow' or container == 'wrist' or container == 'quadruped':
                                continue
                            else:
                                armature.data.edit_bones[prefix + bone].use_connect = True
        
        for container, bone in arm.central_bones.items():
            for bone in bone:
                #Creates copy of bone that retains the original rotation for the retarget empties
                isolatedbone = armature.data.edit_bones.new(prefix + bone + ".isolated")
                isolatedbone.head = armature.pose.bones[prefix + bone].head
                isolatedbone.tail = armature.pose.bones[prefix + bone].tail
                isolatedbone.roll = armature.data.edit_bones[prefix + bone].roll
                isolatedbone.parent = armature.data.edit_bones[prefix + bone]
                isolatedbone.use_deform = False
                isolatedbone.layers[28] = True
                isolatedbone.layers[0] = False
                
                #No parent
                if container == 'pelvis':
                    continue
                else:
                    #Connects current bone's parent to itself
                    parent = armature.pose.bones[prefix + bone].parent.name
                    loc = armature.pose.bones[prefix + bone].head
                    armature.data.edit_bones[parent].tail = loc

                    #Neck should not be connected to its parent
                    if container == 'neck':
                        continue
                    else:
                        armature.data.edit_bones[prefix + bone].use_connect = True

                #Extends head's length to be on par with actual head height
                if container == 'head':
                    pbone = armature.pose.bones[prefix + bone]
                    
                    armature.data.edit_bones[prefix + bone].tail.xyz = pbone.head.x, pbone.head.y, pbone.head.z+6

        if type == 'weight':
            for cat in arm.helper_bones.keys():
                if cat != 'others':
                    for container, bone in arm.helper_bones[cat].items():
                        for bone in bone:
                            bone, prefix = helper_convert(bone)

                            pbone = armature.pose.bones[prefix + bone].tail

                            #Modifies bones and gets other bones for further modification
                            if container == 'knee':
                                armature.data.edit_bones[prefix + bone].tail.y = pbone.y-5
                            elif container == 'elbow':
                                armature.data.edit_bones[prefix + bone].tail.y = pbone.y+5
                            elif container == 'ulna':
                                ulna.append(bone)
                                bone, ulna_prefix = helper_convert(arm.helper_bones['arms']['ulna'][0])
                                pulna = armature.pose.bones[prefix + bone]
                            elif container == 'wrist':
                                wrist.append(bone)
                                bone, wrist_prefix = helper_convert(arm.helper_bones['arms']['wrist'][0])
                                pwrist = armature.pose.bones[prefix + bone]
                            elif container == 'bicep':
                                bicep.append(bone)
                                bone, bicep_prefix = helper_convert(arm.helper_bones['arms']['bicep'][0])
                                pbicep = armature.pose.bones[prefix + bone]
                            elif container == 'trapezius':
                                trapezius.append(bone)
                                bone, trap_prefix = helper_convert(arm.helper_bones['arms']['trapezius'][0])
                                ptrapezius = armature.pose.bones[prefix + bone]
                            elif container == 'quadricep':
                                quadricep.append(bone)
                                bone, quad_prefix = helper_convert(arm.helper_bones['legs']['quadricep'][0])
                                pquadricep = armature.pose.bones[prefix + bone]

            prefix = arm.prefix

            #Bicep tweak
            if bicep:
                forearm = armature.pose.bones[prefix + arm.symmetrical_bones['arms']['forearm'][0]]

                #Check for characters who only have helper bone on one side (Like Louis)
                left = False
                right = False

                for bone in bicep:
                    if bone.title().startswith('L_') or bone.title().endswith('_L'):
                        left = True
                    elif bone.title().startswith('R_') or bone.title().endswith('_R'):
                        right = True

                #Forces uppeararm to use bicep's position
                for bone in arm.symmetrical_bones['arms']['upperarm']:
                    if left:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].tail.xyz = math.copysign(pbicep.head.x, 1), pbicep.head.y, pbicep.head.z
                    if right:
                        if bone.startswith('R_') or bone.endswith('_R'):
                                armature.data.edit_bones[prefix + bone].tail.xyz = math.copysign(pbicep.head.x, -1), pbicep.head.y, pbicep.head.z

                #Connects to parent if helper does not exist
                for bone in arm.symmetrical_bones['arms']['forearm']:
                    if not left:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].use_connect = True
                    if not right:
                        if bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].use_connect = True

                #Tweaks bicep position 
                for bone in bicep:
                    if bone.startswith('L_') or bone.endswith('_L'):
                        armature.data.edit_bones[bicep_prefix + bone].tail.xyz = math.copysign(forearm.head.x, 1), forearm.head.y, forearm.head.z
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        armature.data.edit_bones[bicep_prefix + bone].tail.xyz = math.copysign(forearm.head.x, -1), forearm.head.y, forearm.head.z
            else:
                for bone in arm.symmetrical_bones['arms']['upperarm']:
                    armature.data.edit_bones[prefix + bone].use_connect = True

            prefix = arm.prefix

            #Ulna/wrist tweak
            if ulna or wrist:
                hand = armature.pose.bones[prefix + arm.symmetrical_bones['arms']['hand'][0]]
                forearm = armature.pose.bones[prefix + arm.symmetrical_bones['arms']['forearm'][0]]

                #Check for characters who only have helper bone on one side (Like Louis)
                left = False
                left2 = False

                right = False
                right2 = False

                for bone in ulna:
                    if bone.title().startswith('L_') or bone.title().endswith('_L'):
                        left = True
                    elif bone.title().startswith('R_') or bone.title().endswith('_R'):
                        right = True

                for bone in wrist:
                    if bone.title().startswith('L_') or bone.title().endswith('_L'):
                        left2 = True
                    elif bone.title().startswith('R_') or bone.title().endswith('_R'):
                        right2 = True

                #Forces forearm to use ulna's position
                for bone in arm.symmetrical_bones['arms']['forearm']:
                    if left:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].tail.xyz = math.copysign(pulna.head.x, 1), pulna.head.y, pulna.head.z
                    if right:
                        if bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].tail.xyz = math.copysign(pulna.head.x, -1), pulna.head.y, pulna.head.z

                #If both ulna and wrist are present
                if ulna and wrist:
                    for bone in ulna:
                        if bone.title().startswith('L_') or bone.title().endswith('_L'):
                            armature.data.edit_bones[ulna_prefix + bone].tail.xyz = math.copysign(+hand.head.x, 1), hand.head.y, hand.head.z
                        elif bone.title().startswith('R_') or bone.title().endswith('_R'):
                            armature.data.edit_bones[ulna_prefix + bone].tail.xyz = math.copysign(hand.head.x, -1), hand.head.y, hand.head.z

                        armature.data.edit_bones[ulna_prefix + bone].length = armature.data.edit_bones[ulna_prefix + bone].length / 1.6

                        bone, prefix = helper_convert(arm.helper_bones['arms']['ulna'][0])

                    update(0)

                    for bone in wrist:
                        if bone.title().startswith('L_') or bone.title().endswith('_L'):
                            armature.data.edit_bones[wrist_prefix + bone].head.xyz = math.copysign(pulna.tail.x, 1), pulna.tail.y, pulna.tail.z
                            armature.data.edit_bones[wrist_prefix + bone].tail.xyz = math.copysign(hand.head.x, 1), hand.head.y, hand.head.z
                        elif bone.title().startswith('R_') or bone.title().endswith('_R'):
                            armature.data.edit_bones[wrist_prefix + bone].head.xyz = math.copysign(pulna.tail.x, -1), pulna.tail.y, pulna.tail.z
                            armature.data.edit_bones[wrist_prefix + bone].tail.xyz = math.copysign(hand.head.x, -1), hand.head.y, hand.head.z
                        else:
                            #Fix for Nick's wrist
                            armature.data.edit_bones[wrist_prefix + bone].head.xyz = math.copysign(pulna.tail.x, 1), pulna.tail.y, pulna.tail.z
                            armature.data.edit_bones[wrist_prefix + bone].tail.xyz = math.copysign(hand.head.x, 1), hand.head.y, hand.head.z

                #Else if only ulna is present
                elif ulna:
                    for bone in ulna:
                        bone, prefix = helper_convert(bone)

                        if bone.title().startswith('L_') or bone.title().endswith('_L'):
                            armature.data.edit_bones[ulna_prefix + bone].tail.xyz = math.copysign(hand.head.x, 1), hand.head.y, hand.head.z
                        elif bone.title().startswith('R_') or bone.title().endswith('_R'):
                            armature.data.edit_bones[ulna_prefix + bone].tail.xyz = math.copysign(hand.head.x, -1), hand.head.y, hand.head.z

                #Else if only wrist is present
                elif wrist:
                    for bone in arm.symmetrical_bones['arms']['forearm']:
                        armature.data.edit_bones[prefix + bone].length = armature.data.edit_bones[prefix + bone].length / 1.3

                        #Updates variable
                        forearm = armature.pose.bones[prefix + arm.symmetrical_bones['arms']['forearm'][0]]

                    update(0)

                    for bone in wrist:
                        bone, prefix = helper_convert(bone)

                        if bone.title().startswith('L_') or bone.title().endswith('_L'):
                            armature.data.edit_bones[wrist_prefix + bone].head.xyz = math.copysign(forearm.tail.x, 1), forearm.tail.y, forearm.tail.z
                            armature.data.edit_bones[wrist_prefix + bone].tail.xyz = math.copysign(hand.head.x, 1), hand.head.y, hand.head.z
                        elif bone.title().startswith('R_') or bone.title().endswith('_R'):
                            armature.data.edit_bones[wrist_prefix + bone].head.xyz = math.copysign(forearm.tail.x, -1), forearm.tail.y, forearm.tail.z
                            armature.data.edit_bones[wrist_prefix + bone].tail.xyz = math.copysign(hand.head.x, -1), hand.head.y, hand.head.z
                        else:
                            #Fix for Nick's wrist
                            armature.data.edit_bones[wrist_prefix + bone].head.xyz = math.copysign(forearm.tail.x, 1), forearm.tail.y, forearm.tail.z
                            armature.data.edit_bones[wrist_prefix + bone].tail.xyz = math.copysign(hand.head.x, 1), hand.head.y, hand.head.z

                #Updates wrist location variable if available
                if wrist:
                    update(0)
                    pwrist = armature.pose.bones[wrist_prefix + wrist[0]]

                #Connects to parent if helper is not present
                
                prefix = arm.prefix

                #Left side
                if not left and not left2: # No Ulna/Wrist
                    for bone in arm.symmetrical_bones['arms']['forearm']:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].tail.xyz = math.copysign(hand.head.x, 1), hand.head.y, hand.head.z
                    for bone in arm.symmetrical_bones['arms']['hand']:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].use_connect = True

                elif not left: #No Ulna
                    for bone in arm.symmetrical_bones['arms']['forearm']:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].tail.xyz = math.copysign(pwrist.head.x, 1), pwrist.head.y, pwrist.head.z
                    for bone in wrist:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[wrist_prefix + bone].use_connect = True

                elif not left2: #No Wrist
                    for bone in ulna:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[ulna_prefix + bone].tail.xyz = math.copysign(hand.head.x, 1), hand.head.y, hand.head.z

                #Right side
                if not right and not right2: #No Ulna/Wrist
                    for bone in arm.symmetrical_bones['arms']['forearm']:
                        if bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].tail.xyz = math.copysign(hand.head.x, -1), hand.head.y, hand.head.z
                    for bone in arm.symmetrical_bones['arms']['hand']:
                        if bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].use_connect = True

                elif not right: #No Ulna
                    for bone in arm.symmetrical_bones['arms']['forearm']:
                        if bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].tail.xyz = math.copysign(pwrist.head.x, -1), pwrist.head.y, pwrist.head.z
                    for bone in wrist:
                        if bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[wrist_prefix + bone].use_connect = True

                elif not right2: #No Wrist
                    for bone in ulna:
                        if bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[ulna_prefix + bone].tail.xyz = math.copysign(hand.head.x, -1), hand.head.y, hand.head.z
            else:
                for bone in arm.symmetrical_bones['arms']['hand']:
                    armature.data.edit_bones[prefix + bone].use_connect = True

            prefix = arm.prefix

            #Quadricep tweak
            if quadricep:
                calf = armature.pose.bones[prefix + arm.symmetrical_bones['legs']['calf'][0]]

                #Check for characters who only have helper bone on one side (Like Louis)
                left = False
                right = False

                for bone in quadricep:
                    if bone.title().startswith('L_') or bone.title().endswith('_L'):
                        left = True
                    elif bone.title().startswith('R_') or bone.title().endswith('_R'):
                        right = True

                #Forces thigh to use quadricep's position
                for bone in arm.symmetrical_bones['legs']['thigh']:
                    if left:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].tail = math.copysign(pquadricep.tail.x, 1), pquadricep.tail.y, pquadricep.tail.z
                    if right:
                        if bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].tail = math.copysign(pquadricep.tail.x, -1), pquadricep.tail.y, pquadricep.tail.z

                #Connects to parent if helper does not exist
                for bone in arm.symmetrical_bones['legs']['calf']:
                    if not left:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].use_connect = True
                    if not right:
                        if bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].use_connect = True

                for bone in quadricep:
                    bone, prefix = helper_convert(bone)

                    if bone.title().startswith('L_') or bone.title().endswith('_L'):
                        armature.data.edit_bones[quad_prefix + bone].tail.xyz = math.copysign(calf.head.x, 1), calf.head.y, calf.head.z
                    elif bone.title().startswith('R_') or bone.title().endswith('_R'):
                        armature.data.edit_bones[quad_prefix + bone].tail.xyz = math.copysign(calf.head.x, -1), calf.head.y, calf.head.z
            else:
                for bone in arm.symmetrical_bones['legs']['calf']:
                    armature.data.edit_bones[prefix + bone].use_connect = True

            prefix = arm.prefix

            #Trapezius tweak
            if trapezius:
                upperarm = armature.pose.bones[prefix + arm.symmetrical_bones['arms']['upperarm'][0]]

                #Check for characters who only have helper bone on one side
                left = False
                right = False

                for bone in trapezius:
                    if bone.title().startswith('L_') or bone.title().endswith('_L'):
                        left = True
                    elif bone.title().startswith('R_') or bone.title().endswith('_R'):
                        right = True

                #(Can't find an example that would make clavicle not use trapezius' position, hope this works)
                #Forces clavicle to use trapezius' position
                for bone in arm.symmetrical_bones['arms']['clavicle']:
                    if left:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].tail = math.copysign(ptrapezius.head.x, 1), ptrapezius.head.y, ptrapezius.head.z
                    if right:
                        if bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].tail = math.copysign(ptrapezius.head.x, -1), ptrapezius.head.y, ptrapezius.head.z

                #Connects to parent if helper does not exist
                for bone in arm.symmetrical_bones['arms']['upperarm']:
                    if not left:
                        if bone.startswith('L_') or bone.endswith('_L'):
                            armature.data.edit_bones[prefix + bone].use_connect = True
                    if not right:
                        if bone.startswith('R_') or bone.endswith('_R'):
                            armature.data.edit_bones[prefix + bone].use_connect = True

                #Tweaks trapezius' position
                for bone in trapezius:
                    bone, prefix = helper_convert(bone)

                    if bone.title().startswith('L_') or bone.title().endswith('_L'):
                        armature.data.edit_bones[trap_prefix + bone].tail = math.copysign(upperarm.head.x, 1), upperarm.head.y, upperarm.head.z
                    elif bone.title().startswith('R_') or bone.title().endswith('_R'):
                        armature.data.edit_bones[trap_prefix + bone].tail = math.copysign(upperarm.head.x, -1), upperarm.head.y, upperarm.head.z
            else:
                for bone in arm.symmetrical_bones['arms']['upperarm']:
                    armature.data.edit_bones[prefix + bone].use_connect = True

        #Finger tips tweak
        prefix = arm.prefix

        for container, bone in arm.symmetrical_bones['fingers'].items():
            for bone in bone:
                if container == 'finger01' or container == 'finger11' or container == 'finger21' or container == 'finger31' or container == 'finger41':
                    ebone = armature.data.edit_bones[prefix + bone]
                    length = ebone.length
                    
                    ebone.length = length * 2

                    tip = container[0:7] + '2'

                    if bone.startswith('L_') or bone.endswith('_L'):
                        armature.data.edit_bones[prefix + arm.symmetrical_bones['fingers'][tip][0]].tail.xyz = math.copysign(ebone.tail.x, 1), ebone.tail.y, ebone.tail.z
                    elif bone.startswith('R_') or bone.endswith('_R'):
                        armature.data.edit_bones[prefix + arm.symmetrical_bones['fingers'][tip][1]].tail.xyz = math.copysign(ebone.tail.x, -1), ebone.tail.y, ebone.tail.z

                    armature.data.edit_bones[prefix + bone].length = length

        #Removes unimportant bones such as weapon or attachment bones
        if arm.other_bones:
            for container, bone in arm.other_bones.items():
                for bone in bone:
                    if container == 'weapon':
                        prefix = Prefixes.other
                        bone = armature.data.edit_bones[prefix + bone]
                        armature.data.edit_bones.remove(bone)
                    elif container == 'attachment':
                        prefix = Prefixes.attachment
                        bone = bone.replace('a.', '')
                        bone = armature.data.edit_bones[prefix + bone]
                        armature.data.edit_bones.remove(bone)
                    elif container == 'forward':
                        prefix = Prefixes.other
                        bone = armature.data.edit_bones[prefix + bone]
                        armature.data.edit_bones.remove(bone)

        #Final touches to the armature
        armature.data.display_type = 'OCTAHEDRAL'

        if type == 'weight':
            armature.data.show_bone_custom_shapes = False
            
        armature.show_in_front = 1

        bpy.ops.object.mode_set(mode='OBJECT')

    #Deletion
    elif action == 1 or action == 2:

        #Checks if they weren't deleted already
        if type == 'weight':
            try:
                bpy.data.objects.remove(arm.weight_armature)
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

            arm.weight_armature_created = False
            arm.weight_armature = None
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
                    collection = bpy.data.collections["Retarget Empties ({})".format(arm.armature.name)]
                except:
                    collection = None

                if collection:
                    for object in collection.objects.keys():
                        object = bpy.data.objects[object]
                        bpy.data.objects.remove(object)

                    bpy.data.collections.remove(collection)

                armature = arm.armature
                prefix = arm.prefix

                #Removes original armature constraints
                for cat in arm.symmetrical_bones.keys():
                    for bone in arm.symmetrical_bones[cat].values():
                        for bone in bone:
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

                for bone in arm.central_bones.values():
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

            arm.animation_armature_created = False
            arm.animation_armature = None
            arm.animation_armature_real = None
            
        #Reselects original armature for the sake of convenience
        armature = arm.armature

        if armature.visible_get():
            armature.select_set(True)
            bpy.context.view_layer.objects.active = armature

#Does not work inside this file, for some reason
def helper_convert(bone):
    if bone.startswith('s.'):
        prefix = arm.prefix
        bone = bone.replace('s.', '')

    elif bone.startswith('s2.'):
        prefix = Prefixes.helper2
        bone = bone.replace('s2.', '')
    else:
        prefix = Prefixes.helper

    return bone, prefix

def define_bone(bone, location=[], sign='+', parent=False, type=0):
    armature = arm.animation_armature
    ebone = armature.data.edit_bones[bone[0]]
    ebone2 = armature.data.edit_bones[bone[1]]

    if type == 0:
        if location:
            if sign == '+':
                ebone.head.xyz = math.copysign(ebone2.head.x, 1) + location[0], ebone2.head.y - location[2], ebone2.head.z + location[4]
                ebone.tail.xyz = math.copysign(ebone2.tail.x, 1) + location[1], ebone2.tail.y - location[3], ebone.head.z + location[5]
            elif sign == '-':
                ebone.head.xyz = math.copysign(ebone2.head.x, -1) - location[0], ebone2.head.y - location[2], ebone2.head.z + location[4]
                ebone.tail.xyz = math.copysign(ebone2.tail.x, -1) - location[1], ebone2.tail.y - location[3], ebone.head.z + location[5]
    elif type == 1:
        if sign == '+':
            ebone.tail.xyz = math.copysign(ebone.head.x, 1), ebone.head.y, ebone.head.z
            ebone.head.xyz = math.copysign(ebone2.head.x, 1), ebone.head.y, ebone.head.z
        elif sign == '-':
            ebone.tail.xyz = math.copysign(ebone.head.x, -1), ebone.head.y, ebone.head.z
            ebone.head.xyz = math.copysign(ebone2.head.x, -1), ebone.head.y, ebone.head.z
    elif type == 2:
        ebone3 = armature.data.edit_bones[bone[2]]

        if sign == '+':
            ebone.tail.xyz = math.copysign(ebone2.head.x, 1), ebone2.head.y, ebone2.head.z
            ebone.head.xyz = math.copysign(ebone3.head.x, 1), ebone2.head.y, ebone3.head.z
        elif sign == '-':
            ebone.tail.xyz = math.copysign(ebone2.head.x, -1), ebone2.head.y, ebone2.head.z
            ebone.head.xyz = math.copysign(ebone3.head.x, -1), ebone2.head.y, ebone3.head.z
        
    if parent:
        if bone[0].startswith('L_') or bone[0].endswith('_L'):
            ebone.parent = ebone2
        elif bone[0].startswith('R_') or bone[0].endswith('_R'):
            ebone.parent = ebone3

def generate_shapekey_dict(dictionary, raw_list):
    for shapekey in raw_list:
        #Basis
        if shapekey.casefold().count('basis') or shapekey.casefold().count('base'):
            dictionary['basis']['basis'] = shapekey

        #Eyebrows
        if shapekey.upper().count('AU1AU2L') or shapekey.upper().count('AU1AU2R'):
            dictionary['eyebrows']['AU1AU2'] = shapekey
        elif shapekey.upper().count('AU1AU4L') or shapekey.upper().count('AU1AU4R'):
            dictionary['eyebrows']['AU1AU4'] = shapekey
        elif shapekey.upper().count('AU2AU4L') or shapekey.upper().count('AU2AU4R'):
            dictionary['eyebrows']['AU2AU4'] = shapekey
        elif shapekey.upper().count('AU1L') or shapekey.upper().count('AU1R'):
            dictionary['eyebrows']['AU1'] = shapekey
        elif shapekey.upper().count('AU2L') or shapekey.upper().count('AU2R'):
            dictionary['eyebrows']['AU2'] = shapekey
        elif shapekey.upper().count('AU4L') or shapekey.upper().count('AU4R'):
            dictionary['eyebrows']['AU4'] = shapekey

        #Eyes
        elif shapekey.lower().count('f01') or shapekey.lower().count('frame1'):
            dictionary['eyes']['f01'] = shapekey
        elif shapekey.lower().count('f02') or shapekey.lower().count('frame2'):
            dictionary['eyes']['f02'] = shapekey
        elif shapekey.lower().count('f03') or shapekey.lower().count('frame3'):
            dictionary['eyes']['f03'] = shapekey
        elif shapekey.lower().count('f04'):
            dictionary['eyes']['f04'] = shapekey
        elif shapekey.upper().count('AU42'):
            dictionary['eyes']['AU42'] = shapekey
        
        #Cheek
        elif shapekey.upper().count('AU6ZL') or shapekey.upper().count('AU6ZR'):
            dictionary['cheek']['AU6Z'] = shapekey
        elif shapekey.upper().count('AU13L') or shapekey.upper().count('AU13R'):
            dictionary['cheek']['AU13'] = shapekey

        #Nose
        elif shapekey.upper().count('AU9L') or shapekey.upper().count('AU9R'):
            dictionary['nose']['AU9'] = shapekey
        elif shapekey.upper().count('AU38'):
            dictionary['nose']['AU38'] = shapekey

        #Mouth
        elif shapekey.upper().count('AU12L') or shapekey.upper().count('AU12R'):
            dictionary['mouth']['AU12'] = shapekey
        elif shapekey.upper().count('AU15L') or shapekey.upper().count('AU15R'):
            dictionary['mouth']['AU15'] = shapekey
        elif shapekey.upper().count('AU10L') or shapekey.upper().count('AU10R'):
            dictionary['mouth']['AU10'] = shapekey
        elif shapekey.upper().count('AU17DL') or shapekey.upper().count('AU17DR'):
            dictionary['mouth']['AU17D'] = shapekey
        elif shapekey.upper().count('AU16L') or shapekey.upper().count('AU16R'):
            dictionary['mouth']['AU16'] = shapekey
        elif shapekey.upper().count('AU32'):
            dictionary['mouth']['AU32'] = shapekey
        elif shapekey.upper().count('AU24'):
            dictionary['mouth']['AU24'] = shapekey
        elif shapekey.upper().count('AU18ZL') or shapekey.upper().count('AU18ZR'):
            dictionary['mouth']['AU18Z'] = shapekey
        elif shapekey.upper().count('AU22ZL') or shapekey.upper().count('AU22ZR'):
            dictionary['mouth']['AU22Z'] = shapekey
        elif shapekey.upper().count('AD96L'):
            dictionary['mouth']['AD96L'] = shapekey
        elif shapekey.upper().count('AD96R'):
            dictionary['mouth']['AD96R'] = shapekey

        #Chin
        elif shapekey.upper().count('AU31'):
            dictionary['chin']['AU31'] = shapekey
        elif shapekey.upper().count('AU26L') or shapekey.upper().count('AU26R'):
            dictionary['chin']['AU26'] = shapekey
        elif shapekey.upper().count('AU27L') or shapekey.upper().count('AU27R'):
            dictionary['chin']['AU27'] = shapekey
        elif shapekey.upper().count('AU27ZL') or shapekey.upper().count('AU27ZR'):
            dictionary['chin']['AU27Z'] = shapekey
        elif shapekey.upper().count('AD30L'):
            dictionary['chin']['AD30L'] = shapekey
        elif shapekey.upper().count('AD30R'):
            dictionary['chin']['AD30R'] = shapekey
        elif shapekey.upper().count('AU17L') or shapekey.upper().count('AU17R'):
            dictionary['chin']['AU17'] = shapekey

    return dictionary