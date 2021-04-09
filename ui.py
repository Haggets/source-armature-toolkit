import bpy
from . import __init__
from . import ops
from . import utils

class VAT_PT_mainpanel(bpy.types.Panel): #Main panel that subpanels will use
    bl_label = "Valve Armature Toolkit"
    bl_idname = 'VAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    @classmethod 
    def poll(cls, context): #Won't show up unless there is a selected armature
        return (context.object is not None and context.object.type == 'ARMATURE')

    def draw(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        layout = self.layout
        
        layout.prop(vatproperties, 'target_armature') #Armature that will be affected by the utilities
        if vatproperties.target_armature:
            if vatproperties.custom_scheme_enabled and vatproperties.custom_scheme_prefix:
                layout.label(text="Type: Custom Prefix Armature")
            elif vatinfo.scheme == -1:
                layout.label(text="Type: Unknown Armature")
            elif not utils.arm.sfm:
                layout.label(text="Type: Default Source Armature")
            elif utils.arm.sfm:
                layout.label(text="Type: Source Filmmaker Armature (Unsupported)")
        else:
            layout.label(text="No Armature...")

        layout.prop(vatproperties, 'custom_scheme_enabled')
        if vatproperties.custom_scheme_enabled:
            layout.prop(vatproperties, 'custom_scheme_prefix')
        
class VAT_PT_armaturerename(bpy.types.Panel): #Armature rename panel
    bl_label = "Armature Renaming"
    bl_parent_id = 'VAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        layout = self.layout

        row = layout.row()
        row.operator('vat.armaturerename_blender', text='Convert')
        row.operator('vat.armaturerename_source', text='Restore')
        col = layout.column()
        if vatproperties.target_armature:
            if vatinfo.scheme == 0:
                col.label(text="Current: Source Scheme")
            elif vatinfo.scheme == 1:
                col.label(text="Current: Blender Scheme")
        box = layout.box()
        box.label(text="Meant for weight painting", icon='INFO')
        box.label(text="Allows for weight symmetry", icon='INFO')
        box.label(text="Remember to restore before export", icon='ERROR')

class VAT_PT_constraintsymmetry(bpy.types.Panel): #Constraint Symmetry panel
    bl_label = "Constraint Symmetry"
    bl_parent_id = 'VAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        layout = self.layout
        
        row = layout.row()
        row.operator('vat.constraintsymmetry_create', text='Generate')
        row.operator('vat.constraintsymmetry_delete', text='Delete')
        row = layout.row()
        row.prop(vatproperties, 'affected_side', expand=True)
        col = layout.row()
        if vatproperties.target_armature:
            if vatproperties.affected_side == 'OP1' and vatinfo.symmetry == 2 or vatproperties.affected_side == 'OP2' and vatinfo.symmetry == 1:
                col.label(text="Already applied on the opposite side")
        
        row = layout.row()

        row.prop(vatproperties, 'symmetry_offset')

        box = layout.box()
        box.label(text="Meant for armature reproportioning", icon='INFO')
        box.label(text="Allows for symmetry while keeping", icon='INFO')
        box.label(text="corrected roll values")
        box.label(text="Remember to apply pose as rest pose", icon='ERROR')
        box.label(text="before removing the constraints")
        
class VAT_PT_weightarmature(bpy.types.Panel): #Weight Armature panel
    bl_label = "Weight Armature"
    bl_parent_id = 'VAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw (self, context):
        layout = self.layout

        row = layout.row()
        row.operator('vat.weightarmature_create', text='Generate')
        row.operator('vat.weightarmature_delete', text='Delete')
        box = layout.box()
        box.label(text="Meant for weight creation", icon='INFO')
        box.label(text="Allows more spread out", icon='INFO')
        box.label(text="vertex weights, requiring")
        box.label(text="less tweaking overall")

class VAT_PT_rigifyretarget(bpy.types.Panel): #Rigify Retargetting panel
    bl_label = "Rigify Retarget"
    bl_parent_id = 'VAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw (self, context):
        vatproperties = bpy.context.scene.vatproperties
        layout = self.layout

        row = layout.row()
        row.operator('vat.rigifyretarget_create', text='Generate')
        row.operator('vat.rigifyretarget_delete', text='Delete')

        if not utils.arm.animation_armature_created:
            layout.prop(vatproperties, 'target_object')
            layout.label(text="Used to check for facial expressions")

        if vatproperties.target_armature:
            if utils.arm.animation_armature_created:
                if utils.arm.animation_armature_setup:
                    col = layout.column()
                    try:
                        if bpy.context.object.name != 'rig':
                            col.label(text="Reposition facial drivers correctly", icon='INFO')
                            col.label(text="and edit bone parameters to your need")
                            col.operator('pose.rigify_generate', text="Generate rig", icon='OUTLINER_DATA_ARMATURE')
                    except:
                        col.label(text="Rigify is not installed", icon='CANCEL')

                    if bpy.context.object.name == 'rig':
                        col.operator('vat.rigifyretarget_link', text="Link to generated armature", icon='OUTLINER_DATA_ARMATURE')
                    
        box = layout.box()
        box.label(text="Meant for complex animation", icon='INFO')
        box.label(text="Creates animation ready armature", icon='INFO')
        box.label(text="Remember to bake action before export", icon='ERROR')
        box.label(text="(The original armature, not the generated)")

