import bpy
from . import functions

class VAT_properties(bpy.types.PropertyGroup): #Defines global properties the plugin will use
    def targetpoll(cls, context):
        return bpy.types.Armature is None
    
    target_armature : bpy.props.PointerProperty(type = bpy.types.Object, name = "Armature", update = functions.SchemeType.execute)
    
    sfm_armature : bpy.props.BoolProperty(name = "Source Filmmaker (SFM) armature")
    
    scheme : bpy.props.BoolProperty(name = "Current naming scheme", default = 0)
    
    affected_side : bpy.props.EnumProperty(
        name = "Affected side", 
        description = "Select affected side", 
        items = [
            ('OP1', "Left Side", "Left to Right"), 
            ('OP2', "Right Side", "Right to Left")
        ]
    )