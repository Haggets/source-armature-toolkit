import bpy
from bpy.types import (Panel, Menu)
from . import __init__
from . import ops

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
        layout = self.layout
        vatproperties = bpy.context.scene.vatproperties
        
        layout.prop(vatproperties, "target_armature") #Armature that will be affected by the utilities
        if vatproperties.target_armature != None:
            if vatproperties.custom_scheme_enabled == True and vatproperties.custom_scheme_prefix != "":
                layout.label(text="Type: Custom Prefix Armature")
            elif vatproperties.scheme == -1:
                layout.label(text="Type: Unknown Armature")
            elif vatproperties.sfm_armature == False:
                layout.label(text="Type: Default Source Armature")
            elif vatproperties.sfm_armature == True:
                layout.label(text="Type: Source Filmmaker Armature")
        else:
            layout.label(text="No Armature...")

        layout.prop(vatproperties, "custom_scheme_enabled")
        if vatproperties.custom_scheme_enabled == True:
            layout.prop(vatproperties, "custom_scheme_prefix")
        
class VAT_PT_armaturerename(bpy.types.Panel): #Armature rename panel
    bl_label = "Armature Renaming"
    bl_parent_id = "VAT_PT_mainpanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("vat.armaturerename_blender", text="Convert")
        row.operator("vat.armaturerename_source", text="Restore")
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
        scene = context.scene
        vatproperties = scene.vatproperties
        
        layout = self.layout
        row = layout.row()
        row.operator("vat.constraintsymmetry_create", text="Generate")
        row.operator("vat.constraintsymmetry_delete", text="Delete")
        row = layout.row()
        row.prop(vatproperties, "affected_side", expand=True)
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
        col = layout.column()
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
        col = layout.column()
        row = layout.row()
        row.operator("vat.inversekinematics_create", text="Generate")
        row.operator("vat.inversekinematics_delete", text="Delete")
        box = layout.box()
        box.label(text="Meant for simple animation", icon='INFO')
        box.label(text="Adds IK to hand and feet", icon='INFO')
        
class VAT_PT_rigifyretarget(bpy.types.Panel): #Rigify Retargetting panel
    bl_label = "Rigify Retarget (Advanced IK)"
    bl_parent_id = "VAT_PT_mainpanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw (self, context):
        layout = self.layout
        col = layout.column()
        row = layout.row()
        row.operator("vat.rigifyretarget_create", text="Generate")
        row.operator("vat.rigifyretarget_delete", text="Delete")
        box = layout.box()
        box.label(text="Meant for complex animation", icon='INFO')
        box.label(text="Creates animation ready armature", icon='INFO')
        box.label(text="Remember to bake action before export", icon='ERROR')
        box.label(text="(The original armature, not the generated)")

