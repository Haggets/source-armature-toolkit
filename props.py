import bpy
from . import utils
from . import advanced_ik
from . import constraint_symmetry
from . import armature_creation

class SAT_properties(bpy.types.PropertyGroup): #Defines global properties the plugin will use

    #Thanks to Jeacom for this
    def armature_poll(self, object):
        #Generated armatures should not be part of the list
        if object.name.endswith('.weight') or object.name.endswith('.anim') or object.name.endswith('.anim_setup'):
            pass
        else:
            return object.type == 'ARMATURE'

    #Retuns only meshes
    def object_poll(self, object):
        return object.type == 'MESH'
        
    target_armature : bpy.props.PointerProperty(
        type=bpy.types.Object,
        name='Armature',
        description="Armature that will be used to perform operations on",
        poll=armature_poll, 
        update=utils.create_armature
        )
    
    target_object : bpy.props.PointerProperty(
        type=bpy.types.Object,
        name='Object',
        description="Object linked to the armature that will be used for shapekeys",
        poll=object_poll
        )

    affected_side : bpy.props.EnumProperty(
        name="Affected side", 
        description="Side that will be used for applying symmetry constraints", 
        items=[
            ('LTR', "Left Side", "Left to Right"), 
            ('RTL', "Right Side", "Right to Left")
        ]
    )

    symmetry_offset : bpy.props.BoolProperty(
        name="Symmetry Offset",
        description="If disabled, the location of bones will be the opposite of the location of its pair, else its initial locationn ill be unchanged",
        default=False,
        update=constraint_symmetry.update_constraint
    )

    symmetry_upperarm_rotation_fix : bpy.props.BoolProperty(
        name="Opposite Arm Rotation Fix",
        description="If the opposite arm rotates in the wrong direction, enable this",
        default=False,
        update=constraint_symmetry.update_constraint
    )

    retarget_constraints : bpy.props.BoolProperty(
        name="Retarget Constraints",
        description="Used to preview the animation for the armature after baking",
        default=True,
        update=advanced_ik.retarget_constraints
    )

    bake_helper_bones : bpy.props.BoolProperty(
        name="Bake Helper Bones",
        description="Only required for viewmodels",
        default=False,
    )

    #Armature creation selection

    game_armature_type : bpy.props.EnumProperty(
        name="Type",
        description="Armature type",
        items=[
            ('PM', "Playermodel", "World armature"),
            ('VM', "Viewmodel", "View armature")
        ],
        update=utils.update_armature
    )

    game_armature : bpy.props.EnumProperty(
        name="Game Armature", 
        description="Create armature from the selected game", 
        items=[
            ('HL2', "Half Life 2/Garry's Mod", "Citizen armature"), 
            ('L4D2', "Left 4 Dead 2", "Survivor armatures"),
            ('SBOX', "S&Box", "Standard S&Box armature"),
        ],
        update=utils.update_armature
    )

    game_armature_l4d2 : bpy.props.EnumProperty(
        name="L4D Survivor Armatures",
        description="Selection of survivor armatures",
        items=[
            ('BILL', "Bill", ""),
            ('FRANCIS', "Francis", ""),
            ('LOUIS', "Louis", ""),
            ('ZOEY', "Zoey", ""),
            ('COACH', "Coach", ""),
            ('ELLIS', "Ellis", ""),
            ('NICK', "Nick", ""),
            ('ROCHELLE', "Rochelle", "")
        ],
        update=utils.update_armature
    )

class SAT_info(bpy.types.PropertyGroup):

    unit : bpy.props.FloatProperty(
        default=0
    )

    ##Operator checks for undos and redos##
    creating_armature : bpy.props.BoolProperty(
        default=False
    )
    
    armature_name : bpy.props.StringProperty(
        default=''
    )

    generated_armature_name : bpy.props.StringProperty(
        default=''
    )

    unconverted_armature : bpy.props.BoolProperty(
        default=False
    )

    symmetry : bpy.props.IntProperty(
        default=0
        #0 = Neither side, 1 = Left, 2 = Right
    )

    ##Weight armature
    weight_armature : bpy.props.BoolProperty(
        default=False
    )

    ##Animation armature data##
    animation_armature : bpy.props.BoolProperty(
        default=False
    )

    animation_armature_setup : bpy.props.BoolProperty(
        default=False
    )

    ##Armature information
    prefix : bpy.props.StringProperty(
        default=''
    )

    scheme : bpy.props.IntProperty(
        default=0
        #-1 = No armature, 0 = Default, 1 = Blender Friendly
    )

    viewmodel : bpy.props.BoolProperty(
        default=False
    )

    special_viewmodel : bpy.props.BoolProperty(
        default=False
    )

    goldsource : bpy.props.BoolProperty(
        default=False
    )

    titanfall : bpy.props.BoolProperty(
        default=False
    )

    sbox : bpy.props.BoolProperty(
        default=False
    )

    sfm : bpy.props.BoolProperty(
        default=False
    )