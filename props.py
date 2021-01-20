import bpy
from . import functions

class VAT_properties(bpy.types.PropertyGroup): #Defines global properties the plugin will use
    ''' #Not currently working, meant to only filter objects that are armatures
    def targetpoll(cls, context):
        return bpy.types.Armature
    '''
    target_armature : bpy.props.PointerProperty(type = bpy.types.Object, name = "Armature", update = functions.SchemeType.execute)
    
    sfm_armature : bpy.props.BoolProperty(name = "Source Filmmaker (SFM) armature")
    
    scheme : bpy.props.IntProperty(name = "Current naming scheme", default = 0)
    
    custom_scheme_enabled : bpy.props.BoolProperty(name = "Enable custom prefix", default = 0) 

    custom_scheme_prefix : bpy.props.StringProperty(name = "Prefix", default = "")

    affected_side : bpy.props.EnumProperty(
        name = "Affected side", 
        description = "Select affected side", 
        items = [
            ('OP1', "Left Side", "Left to Right"), 
            ('OP2', "Right Side", "Right to Left")
        ]
    )