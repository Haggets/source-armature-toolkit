import bpy
from bpy.types import (Panel, Menu)
from . import __init__
from . import ops
from . import utils

class VAT_PT_mainpanel(bpy.types.Panel): #Main panel that subpanels will use
    bl_label = "Valve Armature Toolkit"
    bl_idname = "VAT_PT_mainpanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod 
    def poll(cls, context): #Won't show up unless there is a selected armature
        return (context.object is not None and context.object.type == 'ARMATURE')

    def draw(self, context):
        vatproperties = bpy.context.scene.vatproperties
        layout = self.layout
        
        layout.prop(vatproperties, "target_armature") #Armature that will be affected by the utilities
        if vatproperties.target_armature:
            if vatproperties.custom_scheme_enabled and vatproperties.custom_scheme_prefix:
                layout.label(text="Type: Custom Prefix Armature")
            elif utils.arm.scheme == -1:
                layout.label(text="Type: Unknown Armature")
            elif not utils.arm.sfm:
                layout.label(text="Type: Default Source Armature")
            elif utils.arm.sfm:
                layout.label(text="Type: Source Filmmaker Armature (Unsupported)")
        else:
            layout.label(text="No Armature...")

        layout.prop(vatproperties, "custom_scheme_enabled")
        if vatproperties.custom_scheme_enabled:
            layout.prop(vatproperties, "custom_scheme_prefix")
        
class VAT_PT_armaturerename(bpy.types.Panel): #Armature rename panel
    bl_label = "Armature Renaming"
    bl_parent_id = "VAT_PT_mainpanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        vatproperties = bpy.context.scene.vatproperties
        layout = self.layout

        row = layout.row()
        row.operator("vat.armaturerename_blender", text="Convert")
        row.operator("vat.armaturerename_source", text="Restore")
        col = layout.column()
        if vatproperties.target_armature:
            if utils.arm.scheme == 0:
                col.label(text="Current: Source Scheme")
            elif utils.arm.scheme == 1:
                col.label(text="Current: Blender Scheme")
        box = layout.box()
        box.label(text="Meant for weight painting", icon='INFO')
        box.label(text="Allows for weight symmetry", icon='INFO')
        box.label(text="Remember to restore before export", icon='ERROR')

class VAT_PT_constraintsymmetry(bpy.types.Panel): #Constraint Symmetry panel
    bl_label = "Constraint Symmetry"
    bl_parent_id = "VAT_PT_mainpanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        vatproperties = bpy.context.scene.vatproperties
        layout = self.layout
        
        row = layout.row()
        row.operator("vat.constraintsymmetry_create", text="Generate")
        row.operator("vat.constraintsymmetry_delete", text="Delete")
        row = layout.row()
        row.prop(vatproperties, "affected_side", expand=True)
        row = layout.row()
        if vatproperties.target_armature:
            if vatproperties.affected_side == 'OP1' and utils.arm.symmetry_right or vatproperties.affected_side == 'OP2' and utils.arm.symmetry_left:
                row.label(text="Already applied on the opposite side")

        box = layout.box()
        box.label(text="Meant for armature reproportioning", icon='INFO')
        box.label(text="Allows for symmetry while keeping", icon='INFO')
        box.label(text="corrected roll values")
        box.label(text="Remember to apply pose as rest pose", icon='ERROR')
        box.label(text="before removing the constraints")
        
class VAT_PT_weightarmature(bpy.types.Panel): #Weight Armature panel
    bl_label = "Weight Armature"
    bl_parent_id = "VAT_PT_mainpanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw (self, context):
        layout = self.layout

        row = layout.row()
        row.operator("vat.weightarmature_create", text="Generate")
        row.operator("vat.weightarmature_delete", text="Delete")
        box = layout.box()
        box.label(text="Meant for weight creation", icon='INFO')
        box.label(text="Allows more spread out", icon='INFO')
        box.label(text="vertex weights, requiring")
        box.label(text="less tweaking overall")
        
class VAT_PT_inversekinematics(bpy.types.Panel): #Inverse Kinematics panel
    bl_label = "Inverse Kinematics (Simple IK)"
    bl_parent_id = "VAT_PT_mainpanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw (self, context):
        layout = self.layout

        row = layout.row()
        row.operator("vat.inversekinematics_create", text="Generate")
        row.operator("vat.inversekinematics_delete", text="Delete")
        box = layout.box()
        box.label(text="Meant for simple animation", icon='INFO')
        box.label(text="Adds IK to hand and feet", icon='INFO')
        box.label(text="as well as pole bones")
class VAT_PT_rigifyretarget(bpy.types.Panel): #Rigify Retargetting panel
    bl_label = "Rigify Retarget (Advanced IK)"
    bl_parent_id = "VAT_PT_mainpanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw (self, context):
        vatproperties = bpy.context.scene.vatproperties
        layout = self.layout

        row = layout.row()
        row.operator("vat.rigifyretarget_create", text="Generate")
        row.operator("vat.rigifyretarget_delete", text="Delete")

        layout.prop(vatproperties, "target_object")
        layout.label(text="Used to check for facial expressions")

        if vatproperties.target_armature:
            if utils.arm.animation_armature:
                if utils.arm.animation_armature_setup:
                    row = layout.row()
                    row.operator("vat.rigifyretarget_link", text="Link to generated armature")
                    col = layout.column()
                    col.label(text="Link after armature is generated", icon='INFO')

                elif not utils.arm.animation_armature_setup:
                    #Presets
                    row = layout.row()
                    row.label(text="Upper limbs presets:")
                    row = layout.row()
                    row.prop(vatproperties, "retarget_top_preset", expand=True)

                    row = layout.row()
                    row.label(text="Spine presets:")
                    row = layout.row()
                    row.prop(vatproperties, "retarget_center_preset", expand=True)

                    row = layout.row()
                    row.label(text="Lower limbs presets:")
                    row = layout.row()
                    row.prop(vatproperties, "retarget_bottom_preset", expand=True)

                    #Refresh
                    row = layout.row()
                    row.operator("vat.rigifyretarget_update", text="Refresh")

        box = layout.box()
        box.label(text="Meant for complex animation", icon='INFO')
        box.label(text="Creates animation ready armature", icon='INFO')
        box.label(text="Remember to bake action before export", icon='ERROR')
        box.label(text="(The original armature, not the generated)")

