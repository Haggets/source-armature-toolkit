import bpy
import math
from bpy.app.handlers import persistent
from . import armature_rename
from .constraint_symmetry import constraint_update

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

def update_constraint(self, context):
    vatproperties = bpy.context.scene.vatproperties
    constraint_update()

@persistent
def armatures_reset(*args):
    vatproperties = bpy.context.scene.vatproperties
    vatinfo = bpy.context.scene.vatinfo

    #Revalidates important pointer variables after and undo or redo
    if vatproperties.target_armature:
        if arm._armature or arm._armature_real:
            arm.armature = bpy.data.objects[arm._armature]
            arm.armature_real = bpy.data.armatures[arm._armature_real]
        else:
            arm.armature = None
            arm.armature_real = None
    
        if vatinfo.weight_armature:
            if arm._weight_armature or arm._weight_armature_real:
                arm.weight_armature = bpy.data.objects[arm._weight_armature]
                arm.weight_armature_real = bpy.data.armatures[arm._weight_armature_real]
            else:
                arm.weight_armature = None
                arm.weight_armature_real = None

        if vatinfo.animation_armature:
            if arm._animation_armature or arm._animation_armature_real:
                arm.animation_armature = bpy.data.objects[arm._animation_armature]
                arm.animation_armature_real = bpy.data.armatures[arm._animation_armature_real]
            else:
                arm.animation_armature = None
                arm.animation_armature_real = None

class Armature: #Armature base

    def __init__(self, armature):
        vatinfo = bpy.context.scene.vatinfo

        #Basic armature information
        self.armature = armature
        self.armature_real = armature.data

        self._armature = str(armature.name)
        self._armature_real = str(armature.data.name)

        #Armature type, scheme and prefix
        self.sfm = False
        self.viewmodel = False
        self.goldsource = False
        self.prefix = ''

        #Bone information
        self.full_bonelist = []
        self.symmetrical_bones = {'arms': {'clavicle': [], 'upperarm': [], 'forearm': [], 'hand': []}, 'legs': {'thigh': [], 'calf': [], 'foot': [], 'toe': []}, 'fingers': {'finger0': [], 'finger01': [], 'finger02': [], 'finger1': [], 'finger11': [], 'finger12': [], 'finger2': [], 'finger21': [], 'finger22': [], 'finger3': [], 'finger31': [], 'finger32': [], 'finger4': [], 'finger41': [], 'finger42': []}}
        self.central_bones = {'pelvis': [], 'spine': [], 'spine1': [], 'spine2': [], 'spine3': [], 'spine4': [], 'neck': [], 'head': []}
        self.helper_bones = {'arms': {'trapezius': [], 'bicep': [], 'elbow': [], 'ulna': [], 'wrist': [], 'shoulder': []}, 'legs': {'quadricep': [], 'knee': []}, 'viewmodel': {'thumbroot': [], 'thumbfix': [], 'wrist_helper1': [], 'wrist_helper2': [], 'forearm_driven': [], 'ulna_extra1': [], 'ulna_extra2': [], 'wrist_extra': []}, 'others': {'others': []}}
        self.other_bones = {'forward': [], 'weapon': [], 'attachment': [], 'viewmodel': [], 'root': [], 'others': []}
        self.custom_bones = {'others': []}

        #Additional information for operations

        #Weight armature
        self.weight_armature = None
        self.weight_armature_real = None
        
        self._weight_armature = None
        self._weight_armature_real = None

        #Animation armature
        self.animation_armature = None
        self.animation_armature_real = None

        self._animation_armature = None
        self._animation_armature_real = None

        self.facial_bones = []

        #Object information
        self.shapekeys = None

        #Functions executed to gather previous information
        self.get_bones(True)
        if vatinfo.scheme != -1:
            self.get_scheme()
            self.get_armatures()
            self.get_constraints()
            self.set_groups()
            if self.helper_bones:
                self.set_procedural_bones()
        else:
            print("Empty armature, cannot proceed")
            
    def get_bones(self, report): #Builds bone lists
        vatinfo = bpy.context.scene.vatinfo
        armature = self.armature

        if self.armature:
            #Cleans bone list
            self.full_bonelist = []
            self.symmetrical_bones = {'arms': {'clavicle': [], 'upperarm': [], 'forearm': [], 'hand': []}, 'legs': {'thigh': [], 'calf': [], 'foot': [], 'toe': []}, 'fingers': {'finger0': [], 'finger01': [], 'finger02': [], 'finger1': [], 'finger11': [], 'finger12': [], 'finger2': [], 'finger21': [], 'finger22': [], 'finger3': [], 'finger31': [], 'finger32': [], 'finger4': [], 'finger41': [], 'finger42': []}}
            self.central_bones = {'pelvis': [], 'spine': [], 'spine1': [], 'spine2': [], 'spine3': [], 'spine4': [], 'neck': [], 'head': []}
            self.helper_bones = {'arms': {'trapezius': [], 'bicep': [], 'elbow': [], 'ulna': [], 'wrist': [], 'shoulder': []}, 'legs': {'quadricep': [], 'knee': []}, 'viewmodel': {'thumbroot': [], 'thumbfix': [], 'wrist_helper1': [], 'wrist_helper2': [], 'forearm_driven': [], 'ulna_extra1': [], 'ulna_extra2': [], 'wrist_extra': []}, 'others': {'others': []}}
            self.other_bones = {'forward': [], 'weapon': [], 'attachment': [], 'viewmodel': [], 'root': [], 'others': []}
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
                    if vatproperties.custom_scheme_enabled:
                        self.prefix = vatproperties.custom_scheme_prefix

                        if bone.startswith(self.prefix + bone.count('L_') == 0 or bone.count('R_') == 0 or bone.count('_L') == 0 or bone.count('_R') == 0):
                            if bone.count('L_') == 0 or bone.count('R_') == 0:
                                vatinfo.scheme = 3
                            elif bone.count('_L') == 0 or bone.count('L_') == 0:
                                vatinfo.scheme = 3
                            symmetrical_bones_raw.append(bone.replace(self.prefix, ''))

                        elif bone.startswith(self.prefix):
                            central_bones_raw.append(bone.replace(self.prefix, ''))

                    #Helper prefix
                    if bone.startswith('hlp_'):
                        helper_bones_raw.append(bone.replace(Prefixes.helper, ''))

                    #Source and Blender prefixes
                    elif bone.startswith('ValveBiped.'):
                        self.prefix = 'ValveBiped.Bip01_'

                        #Strange L4D2 helper prefix, must be differentiated from the usual helper bone with 's2.'
                        if bone.startswith('ValveBiped.hlp_'):
                            helper_bones_raw.append(bone.replace('ValveBiped.hlp_', 's2.'))

                        #Helper bones without helper prefix, differentiated with 's.'
                        elif bone.title().count('Ulna') or bone.title().count('Wrist') or bone.title().count('Elbow') or bone.title().count('Knee') or bone.title().count('Trapezius') or bone.title().count('Quad') or bone.title().count('Bicep') or bone.title().count('Shoulder') or bone.title().count('Thumbroot'):
                            helper_bones_raw.append(bone.replace(self.prefix, 's.'))

                        #Attachment bone prefix. They are supposed to be in other bones instead
                        elif bone.startswith('ValveBiped.attachment'):
                            other_bones_raw.append(bone.replace('ValveBiped.attachment_', 'a.'))
                        
                        elif bone.startswith('ValveBiped.Anim'):
                            other_bones_raw.append(bone.replace('ValveBiped.', 'a2.'))

                        #Default prefix
                        elif bone.startswith(self.prefix + 'L_') or bone.startswith(self.prefix + 'R_'): #Symmetrical
                            vatinfo.scheme = 0
                            symmetrical_bones_raw.append(bone.replace(self.prefix, ''))

                        #Blender prefix
                        elif bone.endswith('_L') or bone.endswith('_R'):
                            vatinfo.scheme = 1
                            symmetrical_bones_raw.append(bone.replace(self.prefix, ''))

                        #Central bones prefix
                        elif bone.startswith('ValveBiped.Bip01_'): #Central
                            central_bones_raw.append(bone.replace(self.prefix, ''))

                        elif bone == 'ValveBiped.ValveBiped' or bone == 'ValveBiped.Bip01' or bone == 'ValveBiped.Camera' or bone == 'ValveBiped.attach_camera':
                            self.viewmodel = True
                            other_bones_raw.append(bone.replace('ValveBiped.', ''))
                            
                        else: #Other
                            other_bones_raw.append(bone.replace('ValveBiped.', ''))

                    #SFM prefix
                    elif bone.startswith('bip_'): # Central
                        vatinfo.scheme = 2
                        self.sfm = True
                        self.prefix = 'bip_'

                        if bone.endswith('_L') or bone.endswith('_R'): #Symmetrical
                            symmetrical_bones_raw.append(bone.replace(self.prefix, ''))

                        else:
                            central_bones_raw.append(bone.replace(self.prefix, ''))

                    elif bone.startswith('Bip0'):
                        self.goldsource = True

                        if bone.startswith('Bip01'):
                            self.prefix = 'Bip01'
                        elif bone.startswith('Bip02'):
                            self.prefix = 'Bip02'
                        
                        if bone.count(' L ') or bone.count(' R ') or bone.endswith(' L') or bone.endswith(' R'):
                            symmetrical_bones_raw.append(bone.replace(self.prefix, ''))

                        elif bone == self.prefix:
                            other_bones_raw.append(bone)
                        
                        else:
                            central_bones_raw.append(bone.replace(self.prefix, ''))

                    #No/Different prefix
                    else:
                        custom_bones_raw.append(bone)
                        custom_bones_raw.sort()

                #Unknown armature
                if not symmetrical_bones_raw and not central_bones_raw and not self.other_bones:
                    vatinfo.scheme = -1

                #Organizes dictionary from raw lists

                #Symmetrical bones raw list
                if symmetrical_bones_raw:
                    for bone in symmetrical_bones_raw:
                        if self.goldsource:
                            if bone.title().count('Arm'):
                                if bone.title().count('Arm1'):
                                    self.symmetrical_bones['arms']['upperarm'].append(bone)
                                    self.symmetrical_bones['arms']['upperarm'].sort()
                                elif bone.title().count('Arm2'):
                                    self.symmetrical_bones['arms']['forearm'].append(bone)
                                    self.symmetrical_bones['arms']['forearm'].sort()
                                else:
                                    self.symmetrical_bones['arms']['clavicle'].append(bone)
                                    self.symmetrical_bones['arms']['clavicle'].sort()
                            
                            elif bone.title().count('Hand'):
                                self.symmetrical_bones['arms']['hand'].append(bone)
                                self.symmetrical_bones['arms']['hand'].sort()

                            elif bone.title().count('Leg'):
                                if bone.title().count('Leg1'):
                                    self.symmetrical_bones['legs']['calf'].append(bone)
                                    self.symmetrical_bones['legs']['calf'].sort()
                                else:
                                    self.symmetrical_bones['legs']['thigh'].append(bone)
                                    self.symmetrical_bones['legs']['thigh'].sort()

                            elif bone.title().count('Foot'):
                                self.symmetrical_bones['legs']['foot'].append(bone)
                                self.symmetrical_bones['legs']['foot'].sort()

                            elif bone.title().count('Toe'):
                                self.symmetrical_bones['legs']['toe'].append(bone)
                                self.symmetrical_bones['legs']['toe'].sort()

                        else:
                            if bone.title().count('Clavicle'):
                                self.symmetrical_bones['arms']['clavicle'].append(bone)
                                self.symmetrical_bones['arms']['clavicle'].sort()

                            elif bone.title().count('Upperarm'):
                                self.symmetrical_bones['arms']['upperarm'].append(bone)
                                self.symmetrical_bones['arms']['upperarm'].sort()

                            elif bone.title().count('Forearm'):
                                if bone.title().count('Driven'):
                                    self.helper_bones['viewmodel']['forearm_driven'].append('s.' + bone)
                                    self.helper_bones['viewmodel']['forearm_driven'].sort()
                                else:
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

                            elif bone.title().count('Spine3'):
                                self.central_bones['spine3'].append(bone)
                                self.central_bones['spine3'].sort()

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
                        
                        else:
                            self.custom_bones.setdefault(bone.casefold(), [])
                            self.custom_bones[bone.casefold()].append('s.' + bone)
                            self.custom_bones[bone.casefold()].sort()

                #Helper bones raw list
                if helper_bones_raw:
                    for bone in helper_bones_raw:
                        if bone.title().count('Trap'):
                            self.helper_bones['arms']['trapezius'].append(bone)
                            self.helper_bones['arms']['trapezius'].sort()

                        elif bone.title().count('Bicep'):
                            self.helper_bones['arms']['bicep'].append(bone)
                            self.helper_bones['arms']['bicep'].sort()

                        elif bone.title().count('Elbow'):
                            self.helper_bones['arms']['elbow'].append(bone)
                            self.helper_bones['arms']['elbow'].sort()

                        elif bone.title().count('Ulna'):
                            #Additional bone set only in viewmodels that need a separate container to avoid messing with wrist generation
                            if self.viewmodel:
                                if bone.count('ulna01'):
                                    self.helper_bones['viewmodel']['ulna_extra1'].append(bone)
                                    self.helper_bones['viewmodel']['ulna_extra1'].sort()
                                    continue

                                elif bone.count('ulna02'):
                                    self.helper_bones['viewmodel']['ulna_extra2'].append(bone)
                                    self.helper_bones['viewmodel']['ulna_extra2'].sort()
                                    continue

                            self.helper_bones['arms']['ulna'].append(bone)
                            self.helper_bones['arms']['ulna'].sort()

                        elif bone.title().count('Wrist'):
                            if self.viewmodel:
                                if bone.count('wrist0'):
                                    self.helper_bones['viewmodel']['wrist_extra'].append(bone)
                                    self.helper_bones['viewmodel']['wrist_extra'].sort()
                                    continue

                            if bone.title().count('Helper1'):
                                self.helper_bones['viewmodel']['wrist_helper1'].append(bone)
                                self.helper_bones['viewmodel']['wrist_helper1'].sort()
                            elif bone.title().count('Helper2'):
                                self.helper_bones['viewmodel']['wrist_helper2'].append(bone)
                                self.helper_bones['viewmodel']['wrist_helper2'].sort()
                            else:
                                self.helper_bones['arms']['wrist'].append(bone)
                                self.helper_bones['arms']['wrist'].sort()

                        elif bone.title().count('Shoulder'):
                            self.helper_bones['arms']['shoulder'].append(bone)
                            self.helper_bones['arms']['shoulder'].sort()

                        elif bone.title().count('Quad'):
                            self.helper_bones['legs']['quadricep'].append(bone)
                            self.helper_bones['legs']['quadricep'].sort()

                        elif bone.title().count('Knee'):
                            self.helper_bones['legs']['knee'].append(bone)
                            self.helper_bones['legs']['knee'].sort()

                        elif bone.title().count('Thumbroot'):
                            self.helper_bones['viewmodel']['thumbroot'].append(bone)
                            self.helper_bones['viewmodel']['thumbroot'].sort()

                        elif bone.title().count('Thumb_Fix'):
                            self.helper_bones['viewmodel']['thumbfix'].append(bone)
                            self.helper_bones['viewmodel']['thumbfix'].sort()
                            
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

                        elif bone.title().count('Weapon') or bone.title().count('Muzzle') or bone.title().count('Shell'):
                            self.other_bones['weapon'].append(bone)
                            self.other_bones['weapon'].sort()

                        elif bone.startswith('a.') or bone.startswith('a2.'):
                            self.other_bones['attachment'].append(bone)
                            self.other_bones['attachment'].sort()

                        elif bone == self.prefix:
                            self.other_bones['root'].append(bone)
                            self.other_bones['root'].sort()

                        elif bone.title().count('Camera') or bone.title().count('Bip01') or bone.count('ValveBiped'):
                            self.other_bones['viewmodel'].append(bone)
                            self.other_bones['viewmodel'].sort()

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

                #Adds blanks to lists for bones without pairs
                for cat in self.symmetrical_bones.keys():
                    for container in self.symmetrical_bones[cat].keys():
                        if len(self.symmetrical_bones[cat][container]) == 1:
                            if self.goldsource:
                                if self.symmetrical_bones[cat][container][0].count(' L') or self.symmetrical_bones[cat][container][0].endswith(' L'):
                                    self.symmetrical_bones[cat][container].insert(1, None)
                                elif self.symmetrical_bones[cat][container][0].count(' R ') or self.symmetrical_bones[cat][container][0].endswith(' R'):
                                    self.symmetrical_bones[cat][container].insert(0, None)
                            else:
                                if self.symmetrical_bones[cat][container][0].startswith('L_') or self.symmetrical_bones[cat][container][0].endswith('_L'):
                                    self.symmetrical_bones[cat][container].insert(1, None)
                                elif self.symmetrical_bones[cat][container][0].startswith('R_') or self.symmetrical_bones[cat][container][0].endswith('_R'):
                                    self.symmetrical_bones[cat][container].insert(0, None)

                for cat in self.helper_bones.keys():
                    for container in self.helper_bones[cat].keys():
                        if len(self.helper_bones[cat][container]) == 1:
                            bone = self.helper_bones[cat][container][0]
                            if bone.startswith('s.'):
                                bone = bone.replace('s.', '')

                            elif bone.startswith('s2.'):
                                bone = bone.replace('s2.', '')

                            if bone.startswith('L_') or bone.endswith('_L'):
                                self.helper_bones[cat][container].insert(1, None)
                            elif bone.startswith('R_') or bone.endswith('_R'):
                                self.helper_bones[cat][container].insert(0, None)
                            else: #Nick left wrist fix
                                self.helper_bones[cat][container].insert(1, None)

                if len(self.helper_bones['arms']['wrist']) == 2:
                    #Position fix for Nick's left wrist
                    if self.helper_bones['arms']['wrist'][1] == 's2.wrist':
                        self.helper_bones['arms']['wrist'].sort(reverse=True)

                #Final bone report
                if report:
                    print("Symmetrical bones:", list(self.symmetrical_bones.values()))
                    print("Central bones:", list(self.central_bones.values()))
                    print("Helper bones:", list(self.helper_bones.values()))
                    print("Other bones:", list(self.other_bones.values()))
                    print("Custom bones:", self.custom_bones)
                
            else:
                vatinfo.scheme = -1

    def get_scheme(self): #Gets current scheme
        armature = self.armature
        vatinfo = bpy.context.scene.vatinfo

        for bone in self.symmetrical_bones:

            #If not an SFM armature, check if the armature has the Source or Blender armature
            if not self.sfm:
                if bone.startswith('L_') or bone.startswith('R_'):
                    vatinfo.scheme = 0

                elif bone.endswith('_L') or bone.endswith('_R'):
                    vatinfo.scheme = 1
                
        #Final scheme report
        if not self.sfm:
            if vatinfo.scheme == 0:
                print("Current Scheme: Source")

            elif vatinfo.scheme == 1:
                print("Current Scheme: Blender")

        elif self.sfm:
            print("Current Scheme: Source (SFM)")

    def get_armatures(self): #Gets generated armatures for selected armature
        vatinfo = bpy.context.scene.vatinfo

        def get_weight_armature():
            try:
                self.weight_armature = bpy.data.objects[self.armature.name + '.weight']
                self.weight_armature_real = bpy.data.armatures[self.armature_real.name + '.weight']
                vatinfo.weight_armature = True
                self._weight_armature = str(self.weight_armature.name)
                self._weight_armature_real = str(self.weight_armature_real.name)
                print("Weight armature detected")
            except:
                vatinfo.weight_armature = False
        
        def get_anim_armature():
            #Checks if it's a setup armature or a proper armature
            try:
                try:
                    self.animation_armature = bpy.data.objects[self.armature.name + '.anim']
                    vatinfo.animation_armature_setup = False
                except:
                    self.animation_armature = bpy.data.objects[self.armature.name + '.anim_setup']
                    vatinfo.animation_armature_setup = True

                try:
                    self.animation_armature_real = bpy.data.armatures[self.armature_real.name + '.anim']
                    vatinfo.animation_armature_setup = False
                except:
                    self.animation_armature_real = bpy.data.armatures[self.armature_real.name + '.anim_setup']
                    vatinfo.animation_armature_setup = True

                vatinfo.animation_armature = True

                self._animation_armature = str(self.animation_armature.name)
                self._animation_armature_real = str(self.animation_armature_real.name)

                if vatinfo.animation_armature_setup:
                    print("Setup animation armature detected")
                elif not vatinfo.animation_armature_setup:
                    print("Animation armature detected")

            except:
                vatinfo.animation_armature = False

        get_weight_armature()
        get_anim_armature()

    def get_constraints(self): #Gets previously added constraints that have not been removed

        def get_symmetry(): 
            vatinfo = bpy.context.scene.vatinfo
            armature = self.armature
            prefix = self.prefix

            for bone in self.symmetrical_bones:
                if bone.startswith('L_') or bone.endswith('_L'):
                    for constraint in armature.pose.bones[prefix + bone].constraints:
                        if constraint.name == 'Constraint Symmetry Location' or constraint.name == 'Constraint Symmetry Rotation':
                            vatinfo.symmetry = 1
                            break
                        else:
                            vatinfo.symmetry = 0

                elif bone.startswith('R_') or bone.endswith('_R'):
                    for constraint in armature.pose.bones[prefix + bone].constraints:
                        if constraint.name == 'Constraint Symmetry Location' or constraint.name == 'Constraint Symmetry Rotation':
                            vatinfo.symmetry = 2
                            break
                        else:
                            vatinfo.symmetry = 0
            
        get_symmetry()

    def set_groups(self): #Organizes bones by bone group and bone layers
        armature = self.armature
        prefix = self.prefix

        #Checks if any groups exist already
        group = armature.pose.bone_groups.keys()

        if not group:
            #Creates groups and sets their color
            for group, color in zip(['Center', 'Left Arm', 'Right Arm', 'Left Leg', 'Right Leg', 'Helpers', 'Attachments', 'Weapon', 'Others', 'Custom'], ['THEME03', 'THEME01', 'THEME04', 'THEME01', 'THEME04', 'THEME09', 'THEME14', 'THEME07', 'THEME10', 'THEME06']):
                armature.pose.bone_groups.new(name=group)
                armature.pose.bone_groups[group].color_set = color
                
            
            for cat in self.symmetrical_bones.keys():
                #Arms and fingers
                if cat == 'arms' or cat == 'fingers':
                    for bone in self.symmetrical_bones[cat].values():
                        for index, bone in enumerate(bone):
                            if bone:
                                if index == 0:
                                    armature.pose.bones[prefix + bone].bone_group_index = 1
                                    armature.data.bones[prefix + bone].layers[1] = True

                                elif index == 1:
                                    armature.pose.bones[prefix + bone].bone_group_index = 2
                                    armature.data.bones[prefix + bone].layers[2] = True

                                armature.data.bones[prefix + bone].layers[0] = False

                #Legs
                elif cat == 'legs':
                    for bone in self.symmetrical_bones[cat].values():
                        for index, bone in enumerate(bone):
                            if bone:
                                if index == 0:
                                    armature.pose.bones[prefix + bone].bone_group_index = 3
                                    armature.data.bones[prefix + bone].layers[3] = True
                                    
                                elif index == 1:
                                    armature.pose.bones[prefix + bone].bone_group_index = 4
                                    armature.data.bones[prefix + bone].layers[4] = True

                                armature.data.bones[prefix + bone].layers[0] = False
                    
            for bone in self.central_bones.values():
                for bone in bone:
                    if bone:
                        armature.pose.bones[prefix + bone].bone_group_index = 0

            if self.helper_bones:
                for cat in self.helper_bones.keys():
                    for bone in self.helper_bones[cat].values():
                        for bone in bone:
                            if bone:
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
                    if bone:
                        if self.goldsource:
                            armature.pose.bones[bone].bone_group_index = 8
                            armature.data.bones[bone].layers[8] = True
                            armature.data.bones[bone].layers[0] = False
                        else:
                            if container == 'attachment':
                                if bone.startswith('a.'):
                                    prefix = Prefixes.attachment
                                    bone = bone.replace('a.', '')
                                elif bone.startswith('a2.'):
                                    prefix = Prefixes.other
                                    bone = bone.replace('a2.', '')

                                armature.pose.bones[prefix + bone].bone_group_index = 6
                                armature.data.bones[prefix + bone].layers[6] = True
                                armature.data.bones[prefix + bone].layers[0] = True

                            elif container == 'weapon':
                                prefix = Prefixes.other
                                armature.pose.bones[prefix + bone].bone_group_index = 7
                                armature.data.bones[prefix + bone].layers[7] = True
                                armature.data.bones[prefix + bone].layers[0] = False
                            else:
                                prefix = Prefixes.other
                                armature.pose.bones[prefix + bone].bone_group_index = 8
                                armature.data.bones[prefix + bone].layers[8] = True
                                armature.data.bones[prefix + bone].layers[0] = False
                    
            #Custom bones
            for bone in self.custom_bones.values():
                for bone in bone:
                    if bone:
                        if bone.startswith('s.'):
                            bone = self.prefix + bone.replace('s.', '')

                        armature.pose.bones[bone].bone_group_index = 9
                        armature.data.bones[bone].layers[9] = True
                        armature.data.bones[bone].layers[0] = False

            #Reveals used layers
            for i in [0,1,2,3,4,5,6,7,8, 9]:
                armature.data.layers[i] = True

            print("Bone groups set!")
            
    def set_procedural_bones(self):
        armature = self.armature
        prefix = self.prefix

        new = True

        for cat in self.helper_bones.keys():
            if cat == 'arms' or cat == 'legs' or cat == 'others':
                for container, bone in self.helper_bones[cat].items():
                    if container == 'wrist' or container == 'ulna' or container == 'elbow' or container == 'knee' or container == 'quadruped' or container == 'shoulder' or container == 'thumbroot':
                        for index, bone in enumerate(bone):
                            if bone:
                                if index > 1:
                                    break
                                if bone.startswith('s.'):
                                    prefix = self.prefix
                                    bone = bone.replace('s.', '')

                                elif bone.startswith('s2.'):
                                    prefix = Prefixes.helper2
                                    bone = bone.replace('s2.', '')
                                else:
                                    prefix = Prefixes.helper
                                
                                #Adds transforms to only these helper bones unless already existing
                                try:
                                    armature.pose.bones[prefix + bone].constraints['Procedural Bone']
                                    new = False
                                    break
                                except:
                                    transform = armature.pose.bones[prefix + bone].constraints.new('TRANSFORM')

                                    #Initial parameters
                                    transform.name = "Procedural Bone"
                                    transform.target = self.armature
                                    transform.map_from = 'ROTATION'
                                    transform.map_to = 'ROTATION'
                                    transform.target_space = 'LOCAL'
                                    transform.owner_space = 'LOCAL'
                                
                                    #Hand rotation
                                    if container == 'wrist' or container == 'ulna':
                                        transform.from_min_x_rot = math.radians(-90)
                                        transform.from_max_x_rot = math.radians(90)

                                        prefix = self.prefix

                                        transform.subtarget = prefix + self.symmetrical_bones['arms']['hand'][index]

                                        if container == 'wrist':
                                            transform.to_min_x_rot = math.radians(-75)
                                            transform.to_max_x_rot = math.radians(75)

                                        elif container == 'ulna':
                                            transform.to_min_x_rot = math.radians(-50)
                                            transform.to_max_x_rot = math.radians(50)

                                    #Forearm and thigh rotation
                                    elif container == 'elbow' or container == 'knee' or container == 'quadruped':
                                        transform.from_min_z_rot = math.radians(-90)
                                        transform.from_max_z_rot = math.radians(90)

                                        transform.to_min_z_rot = math.radians(-45)
                                        transform.to_max_z_rot = math.radians(45)

                                        prefix = self.prefix
                                        
                                        if container == 'elbow':
                                            transform.subtarget = prefix + self.symmetrical_bones['arms']['forearm'][index]

                                        elif container == 'knee':
                                            transform.subtarget = prefix + self.symmetrical_bones['legs']['calf'][index]

                                        elif container == 'quadruped':
                                            transform.subtarget = prefix + self.symmetrical_bones['legs']['thigh'][index]

                                    elif container == 'shoulder':
                                        transform.from_min_y_rot = math.radians(-45)
                                        transform.from_max_y_rot = math.radians(45)

                                        transform.to_min_y_rot = math.radians(20)
                                        transform.to_max_y_rot = math.radians(-20)

                                        prefix = self.prefix

                                        transform.subtarget = prefix + self.symmetrical_bones['arms']['upperarm'][index]

                                    elif container == 'thumbroot':
                                        transform.from_min_y_rot = math.radians(-45)
                                        transform.from_max_y_rot = math.radians(45)

                                        transform.from_min_z_rot = math.radians(-75)
                                        transform.from_max_z_rot = math.radians(75)

                                        transform.to_min_y_rot = math.radians(30)
                                        transform.to_max_y_rot = math.radians(-30)

                                        transform.to_min_z_rot = math.radians(-45)
                                        transform.to_max_z_rot = math.radians(45)

                                        prefix = self.prefix

                                        transform.subtarget = prefix + self.symmetrical_bones['fingers']['finger0'][index]
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
    vatinfo = bpy.context.scene.vatinfo
    
    real_armature = bpy.data.armatures[arm.armature_real.name]
    
    #Creation
    if action == 0:

        #Weight armature datablock
        if type == 'weight':
            arm.weight_armature_real = real_armature.copy()
            arm.weight_armature_real.name = arm.armature_real.name + '.weight'

            #Creation and link to current scene
            arm.weight_armature = bpy.data.objects.new(arm.armature.name + '.weight', arm.weight_armature_real)
            vatinfo.weight_armature = True

            arm._weight_armature = str(arm.weight_armature.name)
            arm._weight_armature_real = str(arm.weight_armature_real.name)

            #Checks if collection exists, else create a new one
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
            vatinfo.animation_armature = True

            arm._animation_armature = str(arm.animation_armature.name)
            arm._animation_armature_real = str(arm.animation_armature_real.name)

            try:
                collection = bpy.data.collections["Animation Armature"]
            except:
                collection = bpy.data.collections.new("Animation Armature")
                bpy.context.scene.collection.children.link(collection)

            collection.objects.link(arm.animation_armature)

            armature = arm.animation_armature
        
        #Focuses on newly created armature
        update(1, armature)

        #Removes unimportant bones such as weapon or attachment bones
        if arm.other_bones:
            for container, bone in arm.other_bones.items():
                for bone in bone:
                    if bone:
                        if type == 'weight':
                            if container == 'weapon':
                                prefix = Prefixes.other
                                bone = armature.data.edit_bones[prefix + bone]
                                armature.data.edit_bones.remove(bone)
                            elif container == 'attachment':
                                if bone.startswith('a.'):
                                    prefix = Prefixes.attachment
                                    bone = bone.replace('a.', '')
                                elif bone.startswith('a2.'):
                                    prefix = Prefixes.other
                                    bone = bone.replace('a2.', '')
                                bone = armature.data.edit_bones[prefix + bone]
                                armature.data.edit_bones.remove(bone)
                        elif container == 'forward':
                            prefix = Prefixes.other
                            bone = armature.data.edit_bones[prefix + bone]
                            armature.data.edit_bones.remove(bone)
                        elif container == 'viewmodel':
                            prefix = Prefixes.other
                            bone = armature.data.edit_bones[prefix + bone]
                            armature.data.edit_bones.remove(bone)
                        elif container == 'root':
                            bone = armature.data.edit_bones[bone]
                            armature.data.edit_bones.remove(bone)

        #Keeps only the bare minimum bones for Rigify
        if type == 'anim':
            for cat in arm.helper_bones.keys():
                for container, bone in arm.helper_bones[cat].items():
                    for bone in bone:
                        if bone:
                            prefix, bone = helper_convert(bone)
                            ebone = armature.data.edit_bones[prefix + bone]
                        
                            armature.data.edit_bones.remove(ebone)

        elif type == 'weight':
            #Removes wrist helpers for viewmodels since i've never seen them used for anything and they mess with weight generation
            for container, bone in arm.helper_bones['viewmodel'].items():
                if container == 'thumbroot' or container == 'forearm_driven':
                    continue
                else:
                    for bone in bone:
                        if bone:
                            prefix, bone = helper_convert(bone)
                            ebone = armature.data.edit_bones[prefix + bone]
                        
                            armature.data.edit_bones.remove(ebone)

        prefix = arm.prefix

        ##Setup for armatures, tweaking bone positions and the like##

        #Custom bones, they're placed first so if the symmetrical bone's parents override any position change these make to the default bones
        for cat in arm.custom_bones.keys():
            for bone in arm.custom_bones[cat]:
                if bone:
                    if bone.startswith('s.'):
                            bone = arm.prefix + bone.replace('s.', '')
                    ebone = armature.data.edit_bones[bone]
                    pbone = armature.pose.bones[bone]

                    marked = False

                    if ebone.parent:
                        parent = ebone.parent.name
                    
                        for bone2 in arm.central_bones.values():
                            for bone2 in bone2:
                                if bone2:
                                    if parent == prefix + bone2:
                                        marked = True
                                        break

                        for cat in arm.symmetrical_bones.keys():
                            for container, bone2 in arm.symmetrical_bones[cat].items():
                                for bone2 in bone2:
                                    if bone2:
                                        if parent == prefix + bone2:
                                            marked = True
                                            break

                        for cat in arm.helper_bones.keys():
                            for container, bone2 in arm.helper_bones[cat].items():
                                for bone2 in bone2:
                                    if bone2:
                                        prefix2, bone2 = helper_convert(bone2)
                                        if parent == prefix2 + bone2:
                                            marked = True
                                            break
                    
                        #If bone's parent is not any of the default ones
                        if not marked:
                            parent = ebone.parent
                            parent.tail = pbone.head

                            #Straightens the first bone of a line
                            if not ebone.children:
                                length = parent.length
                                parent.length = parent.length*2
                                ebone.tail = parent.tail
                                parent.length = length
                                first = False

                            ebone.use_connect = True

        #Symmetrical bones
        for cat in arm.symmetrical_bones.keys():
            for container, bone in arm.symmetrical_bones[cat].items():
                for index, bone in enumerate(bone):
                    if bone:
                        if type == 'anim':
                            #Creates copy of bone that retains the original rotation for the retarget empties
                            if vatinfo.scheme == 0:
                                bone2 = armature_rename.bone_rename(1, bone, index)
                                isolatedbone = armature.data.edit_bones.new(prefix + bone2 + ".isolated")
                            else:
                                isolatedbone = armature.data.edit_bones.new(prefix + bone + ".isolated")
                            isolatedbone.head = armature.pose.bones[prefix + bone].head
                            isolatedbone.tail = armature.pose.bones[prefix + bone].tail
                            isolatedbone.roll = armature.data.edit_bones[prefix + bone].roll
                            isolatedbone.use_deform = False
                            isolatedbone.layers[28] = True
                            for i in range(0, 9):
                                isolatedbone.layers[i] = False

                        ebone = armature.data.edit_bones[prefix + bone]
                        pbone = armature.pose.bones[prefix + bone]
                        parent = ebone.parent

                        parent.tail = pbone.head
                        
                        #Filters out bones whose parent should not be connected to them
                        if container == 'thigh' or container == 'clavicle' or container == 'finger0' or container == 'finger1' or container == 'finger2' or container == 'finger3' or container == 'finger4':
                            continue
                        else:
                            if type == 'weight':
                                if container == 'calf' or container == 'upperarm' or container == 'forearm' or container == 'hand':
                                    continue
                                
                        armature.data.edit_bones[prefix + bone].use_connect = True

                        ##Bone tweaks##

                        #Extends toe tip to be where the actual tip should be
                        if container == 'toe':
                            pbone = armature.pose.bones[prefix + bone].head

                            armature.data.edit_bones[prefix + bone].tail.xyz = pbone.x/0.93, pbone.y/0.56, pbone.z

        #Hand tweak so it's facing forward
        for index, bone in enumerate(arm.symmetrical_bones['arms']['forearm']):
            eforearm = armature.data.edit_bones[prefix + bone]

            if arm.symmetrical_bones['arms']['hand'] and arm.symmetrical_bones['arms']['hand'][index]:
                ehand = armature.data.edit_bones[prefix + arm.symmetrical_bones['arms']['hand'][index]]
                length = eforearm.length

                eforearm.length = eforearm.length*1.25
                ehand.tail = eforearm.tail
                eforearm.length = length

        #Extends feet bone if no toe bone is present
        for index, bone in enumerate(arm.symmetrical_bones['legs']['foot']):
            efoot = armature.data.edit_bones[prefix + bone]

            if not arm.symmetrical_bones['legs']['toe'] or not arm.symmetrical_bones['legs']['toe'][index]:
                if efoot.tail.y < 0:
                    efoot.tail.y = efoot.tail.y*5
                elif efoot.tail.y > 0:
                    efoot.tail.y = efoot.tail.y*-5

                efoot.tail.z = efoot.tail.z*0.4

        #Extends forearm bone if no hand bone is present
        for index, bone in enumerate(arm.symmetrical_bones['arms']['upperarm']):
            eupperarm = armature.data.edit_bones[prefix + bone]

            if not arm.symmetrical_bones['arms']['hand'] or not arm.symmetrical_bones['arms']['hand'][index]:
                if arm.symmetrical_bones['arms']['forearm'] and arm.symmetrical_bones['arms']['forearm'][index]:
                    pforearm = armature.pose.bones[prefix + arm.symmetrical_bones['arms']['forearm'][index]]
                    eforearm = armature.data.edit_bones[prefix + arm.symmetrical_bones['arms']['forearm'][index]]

                    length = eupperarm.length
                    eupperarm.length = eupperarm.length * 2.5

                    eforearm.tail = eupperarm.tail

                    eupperarm.length = length

        #Fix for legs/arms rotating the wrong way in most characters with the animation armature
        if type == 'anim':
            for cat in arm.symmetrical_bones.keys():
                if cat == 'arms' or cat == 'legs':
                    for container, bone in arm.symmetrical_bones[cat].items():
                        if container == 'calf' or container == 'forearm':
                            for bone in bone:
                                if bone:
                                    ebone = armature.data.edit_bones[prefix + bone]

                                    if container == 'calf':
                                        if ebone.head.y > 0:
                                            ebone.head.y = ebone.head.y-ebone.tail.y*0.5
                                        elif ebone.head.y > 0:
                                            ebone.head.y = ebone.head.y+ebone.tail.y*0.5

                                    elif container == 'forearm':
                                        if ebone.head.y > 0:
                                            ebone.head.y = ebone.head.y+ebone.tail.y*0.5
                                        elif ebone.head.y > 0:
                                            ebone.head.y = ebone.head.y-ebone.tail.y*0.5

        #Helper bones tweak if weight armature
        if type == 'weight':
            for cat in arm.helper_bones.keys():
                for container, bone in arm.helper_bones[cat].items():
                    for bone in bone:
                        if bone:
                            if container == 'thumbroot' or container.count('wrist_helper') or container == 'wrist_extra' or container.count('ulna_extra') or container == 'thumbfix':
                                continue
                            prefix2, bone2 = helper_convert(bone)
                            pbone = armature.pose.bones[prefix2 + bone2]
                            ebone = armature.data.edit_bones[prefix2 + bone2]
                            parent = armature.data.edit_bones[prefix2 + bone2].parent

                            parent.tail = pbone.head

                            #Filters out bones whose parent should not be connected to them
                            if container == 'knee' or container == 'elbow' or container == 'wrist' or container == 'quadruped' or container == 'bicep' or container == 'shoulder' or container == 'ulna':
                                continue
                            else:
                                ebone.use_connect = True
        
        #Central bones
        for container, bone in arm.central_bones.items():
            for index, bone in enumerate(bone):
                if bone:
                    if type == 'anim':
                        #Creates copy of bone that retains the original rotation for the retarget empties
                        isolatedbone = armature.data.edit_bones.new(prefix + bone + ".isolated")
                        isolatedbone.head = armature.pose.bones[prefix + bone].head
                        isolatedbone.tail = armature.pose.bones[prefix + bone].tail
                        isolatedbone.roll = armature.data.edit_bones[prefix + bone].roll
                        isolatedbone.parent = armature.data.edit_bones[prefix + bone]
                        isolatedbone.use_deform = False
                        isolatedbone.layers[28] = True

                        for i in range(0, 9):
                            isolatedbone.layers[i] = False
                    
                    pbone = armature.pose.bones[prefix + bone]
                    ebone = armature.data.edit_bones[prefix + bone]

                    #No parent
                    if container != 'pelvis':
                        if armature.data.edit_bones[prefix + bone].parent:
                            parent = armature.data.edit_bones[prefix + bone].parent

                            parent.tail = pbone.head

                            #Neck should not be connected to its parent
                            if container != 'neck':
                                ebone.use_connect = True

                    #Extends head's length to be on par with actual head height
                    if container == 'head':
                        if arm.goldsource:
                            ebone.tail.xyz = pbone.head.x, pbone.head.y, pbone.head.z/0.89
                        else:
                            ebone.tail.xyz = pbone.head.x, pbone.head.y, pbone.head.z/0.919

        if type == 'anim':
            prefix = Prefixes.other
            for container, bone in arm.other_bones.items():
                if container == 'weapon':
                    for bone in bone:
                        if bone:
                            #Creates copy of bone that retains the original rotation for the retarget empties
                            isolatedbone = armature.data.edit_bones.new(prefix + bone + ".isolated")
                            isolatedbone.head = armature.pose.bones[prefix + bone].head
                            isolatedbone.tail = armature.pose.bones[prefix + bone].tail
                            isolatedbone.roll = armature.data.edit_bones[prefix + bone].roll
                            isolatedbone.parent = armature.data.edit_bones[prefix + bone]
                            isolatedbone.use_deform = False
                            isolatedbone.layers[28] = True

                            for i in range(0, 10):
                                isolatedbone.layers[i] = False
            
            for container, bone in arm.custom_bones.items():
                for bone in bone:
                    if bone:
                        #Creates copy of bone that retains the original rotation for the retarget empties
                        isolatedbone = armature.data.edit_bones.new(bone + ".isolated")
                        isolatedbone.head = armature.pose.bones[bone].head
                        isolatedbone.tail = armature.pose.bones[bone].tail
                        isolatedbone.roll = armature.data.edit_bones[bone].roll
                        isolatedbone.parent = armature.data.edit_bones[bone]
                        isolatedbone.use_deform = False
                        isolatedbone.layers[28] = True

                        for i in range(0, 10):
                            isolatedbone.layers[i] = False

        #Tweaks knee and elbow bones if weight armature
        elif type == 'weight':
            prefix = arm.prefix

            for cat in arm.helper_bones.keys():
                if cat != 'others':
                    for container, bone in arm.helper_bones[cat].items():
                        for bone in bone:
                            if bone:
                                if container == 'thumbroot' or container.count('wrist_helper') or container == 'wrist_extra' or container.count('ulna_extra') or container == 'thumbfix':
                                    continue
                                prefix2, bone2 = helper_convert(bone)

                                pbone = armature.pose.bones[prefix2 + bone2]
                                ebone = armature.data.edit_bones[prefix2 + bone2]

                                if container == 'knee':
                                    if ebone.tail.y > 0:
                                        ebone.tail.y = pbone.head.y-pbone.tail.y*3
                                    else:
                                        ebone.tail.y = pbone.head.y+pbone.tail.y*3
                                elif container == 'elbow':
                                    if ebone.tail.y > 0:
                                        ebone.tail.y = pbone.head.y+pbone.tail.y*3
                                    else:
                                        ebone.tail.y = pbone.head.y-pbone.tail.y*3
                            
            ##Tweak section##

            #Trapezius#
            for index, bone in enumerate(arm.symmetrical_bones['arms']['clavicle']):
                dclavicle = armature.data.edit_bones[prefix + bone]
                
                if arm.helper_bones['arms']['trapezius'] and arm.helper_bones['arms']['trapezius'][index]:
                    prefix2, bone2 = helper_convert(arm.helper_bones['arms']['trapezius'][index])
                    etrapezius = armature.data.edit_bones[prefix2 + bone2]

                    if arm.symmetrical_bones['arms']['upperarm'] and arm.symmetrical_bones['arms']['upperarm'][index]:
                        pupperarm = armature.pose.bones[prefix + arm.symmetrical_bones['arms']['upperarm'][index]]
                        etrapezius.tail = pupperarm.head

            #Shoulder/Bicep#
            for index, bone in enumerate(arm.symmetrical_bones['arms']['upperarm']):
                eupperarm = armature.data.edit_bones[prefix + bone]

                #Forces upperarm to use shoulder's position if it exists
                if arm.helper_bones['arms']['shoulder'] and arm.helper_bones['arms']['shoulder'][index]:
                    prefix2, bone2 = helper_convert(arm.helper_bones['arms']['shoulder'][index])

                    pshoulder = armature.pose.bones[prefix2 + bone2]

                    eupperarm.tail = pshoulder.head

                #Forces upperarm to use bicep's position if they exist
                elif arm.helper_bones['arms']['bicep'] and arm.helper_bones['arms']['bicep'][index]:
                    prefix2, bone2 = helper_convert(arm.helper_bones['arms']['bicep'][index])

                    pbicep = armature.pose.bones[prefix2 + bone2]

                    eupperarm.tail = pbicep.head

                #If shoulder and bicep are present
                if arm.helper_bones['arms']['shoulder'] and arm.helper_bones['arms']['bicep'] and arm.helper_bones['arms']['shoulder'][index] and arm.helper_bones['arms']['bicep'][index]:
                    prefix2, bone2 = helper_convert(arm.helper_bones['arms']['shoulder'][index])
                    eshoulder = armature.data.edit_bones[prefix2 + bone2]

                    prefix2, bone2 = helper_convert(arm.helper_bones['arms']['bicep'][index])
                    pbicep = armature.pose.bones[prefix2 + bone2]
                    ebicep = armature.data.edit_bones[prefix2 + bone2]

                    eshoulder.head = eupperarm.head
                    eupperarm.head = eshoulder.tail
                    eupperarm.tail = pbicep.head

                    if arm.symmetrical_bones['arms']['forearm'] and arm.symmetrical_bones['arms']['forearm'][index]:
                        pforearm = armature.pose.bones[prefix + arm.symmetrical_bones['arms']['forearm'][index]]
                        ebicep.tail = pforearm.head

                #Else if only shoulder is present
                elif arm.helper_bones['arms']['shoulder'] and arm.helper_bones['arms']['shoulder'][index]:
                    prefix2, bone2 = helper_convert(arm.helper_bones['arms']['shoulder'][index])
                    pshoulder = armature.pose.bones[prefix2 + bone2]
                    eshoulder = armature.data.edit_bones[prefix2 + bone2]

                    eshoulder.head = eupperarm.head
                    eupperarm.head = eshoulder.tail

                    if arm.symmetrical_bones['arms']['forearm'] and arm.symmetrical_bones['arms']['forearm'][index]:
                        pforearm = armature.pose.bones[prefix + arm.symmetrical_bones['arms']['forearm'][index]]
                        eupperarm.tail = pforearm.head

                #Else if only shoulder is present
                elif arm.helper_bones['arms']['bicep'] and arm.helper_bones['arms']['bicep'][index]:
                    prefix2, bone2 = helper_convert(arm.helper_bones['arms']['bicep'][index])
                    pbicep = armature.pose.bones[prefix2 + bone2]
                    ebicep = armature.data.edit_bones[prefix2 + bone2]

                    eupperarm.tail = pbicep.head

                    if arm.symmetrical_bones['arms']['forearm'] and arm.symmetrical_bones['arms']['forearm'][index]:
                        pforearm = armature.pose.bones[prefix + arm.symmetrical_bones['arms']['forearm'][index]]
                        ebicep.tail = pforearm.head

            #Ulna/wrist#
            for index, bone in enumerate(arm.symmetrical_bones['arms']['forearm']):
                eforearm = armature.data.edit_bones[prefix + bone]

                #Gets hand position if it exists
                if arm.symmetrical_bones['arms']['hand'] and arm.symmetrical_bones['arms']['hand'][index]:
                    phand = armature.pose.bones[prefix + arm.symmetrical_bones['arms']['hand'][index]]
                    ehand = armature.data.edit_bones[prefix + arm.symmetrical_bones['arms']['hand'][index]]

                if not arm.helper_bones['viewmodel']['forearm_driven']:
                    #Forces forearm to use ulna's position
                    if arm.helper_bones['arms']['ulna'] and arm.helper_bones['arms']['ulna'][index]:
                        prefix2, bone2 = helper_convert(arm.helper_bones['arms']['ulna'][index])
                        pulna = armature.pose.bones[prefix2 + bone2]
                        
                        eforearm.tail = pulna.head

                elif arm.helper_bones['viewmodel']['forearm_driven'] and arm.helper_bones['viewmodel']['forearm_driven'][index]:
                    prefix2, bone2 = helper_convert(arm.helper_bones['viewmodel']['forearm_driven'][index])
                    pforearm_driven = armature.pose.bones[prefix2 + bone2]

                    eforearm.tail = pforearm_driven.head

                if arm.symmetrical_bones['arms']['hand'] and arm.symmetrical_bones['arms']['hand'][index]:
                    #Viewmodel exclusive
                    if arm.helper_bones['arms']['ulna'] and arm.helper_bones['viewmodel']['forearm_driven'] and arm.helper_bones['arms']['ulna'][index] and arm.helper_bones['viewmodel']['forearm_driven'][index]:
                        prefix2, bone2 = helper_convert(arm.helper_bones['arms']['ulna'][index])
                        eulna = armature.data.edit_bones[prefix2 + bone2]

                        eulna.tail = phand.head

                        prefix2, bone2 = helper_convert(arm.helper_bones['viewmodel']['forearm_driven'][index])
                        eforearm_driven = armature.data.edit_bones[prefix2 + bone2]

                        eforearm_driven.tail = eulna.head

                    #If both ulna and wrist are present
                    elif arm.helper_bones['arms']['ulna'] and arm.helper_bones['arms']['wrist'] and arm.helper_bones['arms']['ulna'][index] and arm.helper_bones['arms']['wrist'][index]:
                        prefix2, bone2 = helper_convert(arm.helper_bones['arms']['ulna'][index])
                        eulna = armature.data.edit_bones[prefix2 + bone2]

                        eulna.tail = phand.head
                        eulna.length = eulna.length/1.6

                        prefix2, bone2 = helper_convert(arm.helper_bones['arms']['wrist'][index])
                        ewrist = armature.data.edit_bones[prefix2 + bone2]

                        ewrist.head = eulna.tail
                        ewrist.tail = phand.head

                    #Else if only ulna is present
                    elif arm.helper_bones['arms']['ulna'] and arm.helper_bones['arms']['ulna'][index]:
                        prefix2, bone2 = helper_convert(arm.helper_bones['arms']['ulna'][index])
                        eulna = armature.data.edit_bones[prefix2 + bone2]

                        eulna.tail = phand.head

                    #Else if only wrist is present
                    elif arm.helper_bones['arms']['wrist'] and arm.helper_bones['arms']['wrist'][index]:
                        prefix2, bone2 = helper_convert(arm.helper_bones['arms']['wrist'][index])
                        ewrist = armature.data.edit_bones[prefix2 + bone2]

                        eforearm.length = eforearm.length/1.3

                        ewrist.head = eforearm.tail
                        ewrist.tail = phand.head

                        eforearm.tail = ewrist.head
                        ewrist.use_connect = True

                    else: #If neither are present
                        eforearm.tail = phand.head
                        ehand.use_connect = True

            #Quadricep#
            for index, bone in enumerate(arm.symmetrical_bones['legs']['thigh']):
                ethigh = armature.data.edit_bones[prefix + bone]
                
                #Force thigh to use quad's position if available
                if arm.helper_bones['legs']['quadricep'] and arm.helper_bones['legs']['quadricep'][index]:
                    prefix2, bone2 = helper_convert(arm.helper_bones['legs']['quadricep'][index])
                    pquadricep = armature.pose.bones[prefix2 + bone2]
                    equadricep = armature.data.edit_bones[prefix2 + bone2]

                    ethigh.tail = pquadricep.head

                    if arm.symmetrical_bones['legs']['calf'] and arm.symmetrical_bones['legs']['calf'][index]:
                        pcalf = armature.pose.bones[prefix + arm.symmetrical_bones['legs']['calf'][index]]
                        equadricep.tail = pcalf.head

            #Thumbroot# (Only for viewmodels)
            for index, bone in enumerate(arm.symmetrical_bones['arms']['hand']):
                if bone:
                    phand = armature.pose.bones[prefix + bone]
                    ehand = armature.data.edit_bones[prefix + bone]

                    if arm.helper_bones['viewmodel']['thumbroot'] and arm.helper_bones['viewmodel']['thumbroot'][index]:
                        prefix2, bone2 = helper_convert(arm.helper_bones['viewmodel']['thumbroot'][index])
                        pthumbroot = armature.pose.bones[prefix2 + bone2]
                        ethumbroot = armature.data.edit_bones[prefix2 + bone2]

                        ethumbroot.head = phand.head

                        if arm.symmetrical_bones['fingers']['finger0'] and arm.symmetrical_bones['fingers']['finger0'][index]:
                            pfinger0 = armature.pose.bones[prefix + arm.symmetrical_bones['fingers']['finger0'][index]]

                            ethumbroot.tail = pfinger0.head

        prefix = arm.prefix

        #Finger tips tweak
        for container, bone in arm.symmetrical_bones['fingers'].items():
            if container == 'finger0' or container == 'finger1' or container == 'finger2' or container == 'finger3' or container == 'finger4':
                for index, bone in enumerate(bone):
                    if bone:
                        tip = container[0:7] + '2'
                        middle = container[0:7] + '1'

                        if arm.symmetrical_bones['fingers'][tip] and arm.symmetrical_bones['fingers'][tip][index]:
                            ebone = armature.data.edit_bones[prefix + arm.symmetrical_bones['fingers'][middle][index]]
                            length = ebone.length
                            
                            ebone.length = length * 2

                            armature.data.edit_bones[prefix + arm.symmetrical_bones['fingers'][tip][index]].tail.xyz = ebone.tail.x, ebone.tail.y, ebone.tail.z

                            ebone.length = length

                        elif arm.symmetrical_bones['fingers'][middle] and arm.symmetrical_bones['fingers'][middle][index]:
                            ebone = armature.data.edit_bones[prefix + arm.symmetrical_bones['fingers'][container][index]]
                            length = ebone.length
                            
                            ebone.length = length * 2

                            armature.data.edit_bones[prefix + arm.symmetrical_bones['fingers'][middle][index]].tail = ebone.tail

                            ebone.length = length
        
        #If no head
        if not arm.central_bones['head'] and arm.central_bones['spine4'] and arm.central_bones['spine2']:
            espine2 = armature.data.edit_bones[prefix + arm.central_bones['spine2'][0]]
            espine4 = armature.data.edit_bones[prefix + arm.central_bones['spine4'][0]]

            length = espine2.length
            espine2.length = espine2.length * 1.75

            espine4.tail = espine2.tail

            espine2.length = length

            espine4.tail.y = espine4.head.y

        #Final touches to the armature
        armature.data.display_type = 'OCTAHEDRAL'
        armature.show_in_front = True

        if type == 'weight':
            armature.data.show_bone_custom_shapes = False
            
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
                if not collection.objects.keys():
                    bpy.data.collections.remove(collection)
            except:
                pass
                    
            vatinfo.weight_armature = False
            arm.weight_armature = None
            arm.weight_armature_real = None

            arm._weight_armature = None
            arm._weight_armature_real = None
            
        elif type == 'anim':
            try:
                bpy.data.objects.remove(arm.animation_armature)
            except:
                print("Animation armature already deleted, cleaning rest")
            try:
                bpy.data.armatures.remove(arm.animation_armature_real)
            except:
                pass

            #Gets collection and removes if it's empty
            try:
                collection = bpy.data.collections['Animation Armature']
                if not collection.objects.keys():
                    bpy.data.collections.remove(collection)
            except:
                pass

            #Checks if retarget empties are present, if so, remove them
            if action == 1:
                try:
                    collection = bpy.data.collections["Retarget Empties ({})".format(arm.armature.name)[0:60]]

                    if collection.objects.keys():
                        for object in collection.objects.keys():
                            object = bpy.data.objects[object]
                            bpy.data.objects.remove(object)

                            bpy.data.collections.remove(collection)
                except:
                    pass

                armature = arm.armature

                prefix = arm.prefix

                #Removes original armature constraints
                for cat in arm.symmetrical_bones.keys():
                    for bone in arm.symmetrical_bones[cat].values():
                        for bone in bone:
                            if bone:
                                try:
                                    constraint = armature.pose.bones[prefix + bone].constraints["Retarget Location"]
                                    armature.pose.bones[prefix + bone].constraints.remove(constraint)
                                except:
                                    pass
                            
                                try:
                                    constraint = armature.pose.bones[prefix + bone].constraints["Retarget Rotation"]
                                    armature.pose.bones[prefix + bone].constraints.remove(constraint)
                                except:
                                    pass
                
                for cat in arm.helper_bones.keys():
                    for container, bone in arm.helper_bones[cat].items():
                        if container == 'elbow' or container == 'knee':
                            for bone in bone:
                                if bone:
                                    prefix2, bone2 = helper_convert(bone)

                                    try:
                                        constraint = armature.pose.bones[prefix2 + bone2].constraints["Retarget Location"]
                                        armature.pose.bones[prefix2 + bone2].constraints.remove(constraint)
                                    except:
                                        pass

                                    try:
                                        constraint = armature.pose.bones[prefix2 + bone2].constraints["Retarget Rotation"]
                                        armature.pose.bones[prefix2 + bone2].constraints.remove(constraint)
                                    except:
                                        pass
                
                for container, bone in arm.custom_bones.items():
                    for bone in bone:
                        if bone:
                            try:
                                constraint = armature.pose.bones[bone].constraints["Retarget Location"]
                                armature.pose.bones[bone].constraints.remove(constraint)
                            except:
                                pass

                            try:
                                constraint = armature.pose.bones[bone].constraints["Retarget Rotation"]
                                armature.pose.bones[bone].constraints.remove(constraint)
                            except:
                                pass

                for container, bone in arm.central_bones.items():
                    for bone in bone:
                        if bone:
                            try:
                                constraint = armature.pose.bones[prefix + bone].constraints["Retarget Location"]
                                armature.pose.bones[prefix + bone].constraints.remove(constraint)
                            except:
                                pass

                            try:
                                constraint = armature.pose.bones[prefix + bone].constraints["Retarget Rotation"]
                                armature.pose.bones[prefix + bone].constraints.remove(constraint)
                            except:
                                pass

                for container, bone in arm.other_bones.items():
                    if container == 'weapon':
                        for bone in bone:
                            if bone:
                                try:
                                    constraint = armature.pose.bones[prefix + bone].constraints["Retarget Location"]
                                    armature.pose.bones[prefix + bone].constraints.remove(constraint)
                                except:
                                    pass

                                try:
                                    constraint = armature.pose.bones[prefix + bone].constraints["Retarget Rotation"]
                                    armature.pose.bones[prefix + bone].constraints.remove(constraint)
                                except:
                                    pass

                vatinfo.animation_armature = False
                arm.animation_armature = None
                arm.animation_armature_real = None

                arm._animation_armature = None
                arm._animation_armature_real = None
            
        #Reselects original armature for the sake of convenience
        armature = arm.armature

        if type == 'anim':
            if armature.hide_get() == True:
                armature.hide_set(False)

        if armature.visible_get():
            armature.select_set(True)
            bpy.context.view_layer.objects.active = armature

#Does not work inside this file
def helper_convert(bone):
    if bone.startswith('s.'):
        prefix = arm.prefix
        bone = bone.replace('s.', '')

    elif bone.startswith('s2.'):
        prefix = Prefixes.helper2
        bone = bone.replace('s2.', '')
    else:
        prefix = Prefixes.helper

    return prefix, bone

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