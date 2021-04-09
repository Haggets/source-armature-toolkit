import bpy
from . import utils

class VAT_properties(bpy.types.PropertyGroup): #Defines global properties the plugin will use

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
        
    target_armature : bpy.props.PointerProperty(type=bpy.types.Object,
        name='Armature',
        description="Armature that will be used to perform operations on",
        poll=armature_poll, 
        update=utils.create_armature
        )
    
    target_object : bpy.props.PointerProperty(type=bpy.types.Object,
        name='Object',
        description="Object linked to the armature that will be used for shapekeys",
        poll=object_poll
        )

    custom_scheme_enabled : bpy.props.BoolProperty(name="Enable custom prefix",
        description="If to allow usage of custom prefixes that will replace the default Source prefixes",
        default=False
        ) 

    custom_scheme_prefix : bpy.props.StringProperty(
        name='Prefix',
        description="Custom prefix that will be used instead",
        default=''
        )

    affected_side : bpy.props.EnumProperty(
        name="Affected side", 
        description="Side that will be used for applying symmetry constraints", 
        items=[
            ('OP1', "Left Side", "Left to Right"), 
            ('OP2', "Right Side", "Right to Left")
        ]
    )

    symmetry_offset : bpy.props.BoolProperty(
        name="Symmetry offset",
        description="If disabled, the location of bones will be the opposite of the location of its pair, else its initial locationn ill be unchanged",
        default=False,
        update=utils.update_constraint
    )

class VAT_info(bpy.types.PropertyGroup):

    #Operator checks for undos and redos

    scheme : bpy.props.IntProperty(
        default=0
        #-1 = No armature, 0 = Source, 1 = Blender, 2 = SFM, 3 = Custom 1, 4 = Custom 2
    )

    symmetry : bpy.props.IntProperty(
        default=0
        #0 = Neither side, 1 = Left, 2 = Right
    )

    weight_armature : bpy.props.BoolProperty(
        default=False
    )

    animation_armature : bpy.props.BoolProperty(
        default=False
    )

    animation_armature_setup : bpy.props.BoolProperty(
        default=False
    )