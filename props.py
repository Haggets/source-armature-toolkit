import bpy
from . import functions

class VAT_properties(bpy.types.PropertyGroup): #Defines global properties the plugin will use

    #Thanks to Jeacom for this
    def armature_poll(self, object):
        #Generated armatures should not be part of the list
        if object.name.endswith(".weight") or object.name.endswith(".anim"):
            pass
        else:
            return object.type == 'ARMATURE'
        
    target_armature : bpy.props.PointerProperty(type=bpy.types.Object, name="Armature", description="Armature that will be used to perform operations on", poll=armature_poll, update=functions.create_armature)
    
    custom_scheme_enabled : bpy.props.BoolProperty(name="Enable custom prefix", description="If to allow usage of custom prefixes that will replace the default Source prefixes", default=0) 

    custom_scheme_prefix : bpy.props.StringProperty(name="Prefix", description="Custom prefix that will be used instead", default="")

    affected_side : bpy.props.EnumProperty(
        name="Affected side", 
        description="Side that will be used for applying symmetry constraints", 
        items=[
            ('OP1', "Left Side", "Left to Right"), 
            ('OP2', "Right Side", "Right to Left")
        ]
    )

    retarget_top_preset : bpy.props.EnumProperty(
        name="Rigify arm presets",
        description="Empty rotation presets for arms",
        items=[
            ('OP1', "Default Preset", "Works with most characters"),
            ('OP2', "Second Preset", "Works with Bill and Nick (L4D Characters)")
        ]
    )

    retarget_center_preset : bpy.props.EnumProperty(
        name="Rigify center presets",
        description="Empty rotation presets for the spine/head",
        items=[
            ('OP1', "Default Preset", "Works with most characters"),
            ('OP2', "Second Preset", "Works with Bill and Nick (L4D Characters)")
        ]
    )

    retarget_bottom_preset : bpy.props.EnumProperty(
        name="Rigify leg presets",
        description="Empty rotation presets for legs",
        items=[
            ('OP1', "Default Preset", "Works with most characters"),
            ('OP2', "Second Preset", "Works with Bill and Nick (L4D Characters)")
        ]
    )
