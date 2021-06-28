import bpy
from . import __init__
from . import ops
from . import utils
from .addon_updater_ops import get_user_preferences

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
        col = layout.column()
        
        col.prop(vatproperties, 'target_armature') #Armature that will be affected by the utilities
        if vatproperties.target_armature:
            if vatproperties.custom_scheme_enabled and vatproperties.custom_scheme_prefix:
                col.label(text="Type: Custom Prefix Armature")
            elif vatinfo.scheme == -1:
                col.label(text="Type: Unknown Armature")
            elif utils.arm.goldsource:
                col.label(text="Type: GoldSource Armature")
            elif utils.arm.viewmodel:
                col.label(text="Type: Viewmodel Armature")
            elif utils.arm.sfm:
                col.label(text="Type: Source Filmmaker Armature (Unsupported)")
            elif not utils.arm.sfm:
                col.label(text="Type: Default Source Armature")
        else:
            col.label(text="No Armature...")

        col.prop(vatproperties, 'custom_scheme_enabled')
        if vatproperties.custom_scheme_enabled:
            col.prop(vatproperties, 'custom_scheme_prefix')
        
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
        preferences = get_user_preferences()
        layout = self.layout

        row = layout.row()
        row.operator('vat.armaturerename_blender', text='Convert')
        row.operator('vat.armaturerename_source', text='Restore')

        if vatproperties.target_armature:
            col = layout.column()
            if vatinfo.scheme == 0:
                col.label(text="Current: Default Scheme")
            elif vatinfo.scheme == 1:
                col.label(text="Current: Blender Scheme")

        if preferences.show_info:
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
        preferences = get_user_preferences()
        layout = self.layout
        
        row = layout.row()
        row.operator('vat.constraintsymmetry_create', text='Generate')
        row.operator('vat.constraintsymmetry_delete', text='Delete')

        row = layout.row()
        row.prop(vatproperties, 'affected_side', expand=True)

        col = layout.column()
        col.operator('vat.constraintsymmetry_apply', text='Apply', icon='OUTLINER_DATA_ARMATURE')
        if vatproperties.target_armature:
            if vatproperties.affected_side == 'OP1' and vatinfo.symmetry == 2 or vatproperties.affected_side == 'OP2' and vatinfo.symmetry == 1:
                col.label(text="Already applied on the opposite side")
        
        col = layout.column()
        col.prop(vatproperties, 'symmetry_offset')
        col.prop(vatproperties, 'symmetry_upperarm_rotation_fix')

        if preferences.show_info:
            box = layout.box()
            box.label(text="Meant for armature reproportioning", icon='INFO')
            box.label(text="Allows for symmetry while keeping", icon='INFO')
            box.label(text="corrected roll values")
        
class VAT_PT_weightarmature(bpy.types.Panel): #Weight Armature panel
    bl_label = "Weight Armature"
    bl_parent_id = 'VAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw (self, context):
        vatinfo = bpy.context.scene.vatinfo
        preferences = get_user_preferences()
        layout = self.layout

        row = layout.row()
        row.operator('vat.weightarmature_create', text='Generate')
        row.operator('vat.weightarmature_delete', text='Delete')

        if preferences.show_info:
            box = layout.box()
            box.label(text="Meant for weight creation", icon='INFO')
            box.label(text="Allows more spread out", icon='INFO')
            box.label(text="vertex weights, requiring")
            box.label(text="less tweaking overall")

class VAT_PT_rigifyretarget(bpy.types.Panel): #Rigify Retargetting panel
    bl_label = "Rigify Retarget"
    bl_idname = 'VAT_PT_rigifyretarget'
    bl_parent_id = 'VAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw (self, context):
        vatproperties = bpy.context.scene.vatproperties
        vatinfo = bpy.context.scene.vatinfo
        preferences = get_user_preferences()
        layout = self.layout

        if bpy.context.preferences.addons.get('rigify'):
            row = layout.row()
            row.operator('vat.rigifyretarget_create', text='Generate')
            row.operator('vat.rigifyretarget_delete', text='Delete')

            col = layout.column()

            if not vatinfo.animation_armature:
                col.prop(vatproperties, 'target_object')
                col.label(text="Used to check for facial expressions")

            if vatproperties.target_armature:
                if vatinfo.animation_armature:
                    if vatinfo.animation_armature_setup:
                        if bpy.context.object.name != 'rig':
                            if vatproperties.target_object:
                                col.label(text="Reposition facial drivers correctly", icon='INFO')
                                col.label(text="and edit bone parameters to your need")
                            else:
                                col.label(text="Edit bone parameters to your need", icon='INFO')

                            col.operator('pose.rigify_generate', text="Generate rig", icon='OUTLINER_DATA_ARMATURE')

                        else:
                            col.operator('vat.rigifyretarget_link', text="Link to generated armature", icon='OUTLINER_DATA_ARMATURE')

                    else:
                        col.prop(vatproperties, 'retarget_constraints')

            if preferences.show_info:
                box = layout.box()
                box.label(text="Meant for complex animation", icon='INFO')
                box.label(text="Creates animation ready armature", icon='INFO')
                box.label(text="Remember to bake action before export", icon='ERROR')
                box.label(text="(The original armature, not the generated)")
        else:
            col = layout.column()
            col.label(text="Rigify is not installed", icon='CANCEL')
            col.label(text="Please enable it in the preferences")

class VAT_PT_rigifyretargetexport(bpy.types.Panel):
    bl_label = "Bake/Export"
    bl_parent_id = 'VAT_PT_rigifyretarget'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        col.label(text="Action bake:")
        row = layout.row()
        row.operator('vat.rigifyretarget_bake_single', text='Single', icon='ACTION')
        row.operator('vat.rigifyretarget_bake_all', text='All', icon='ACTION')

        col = layout.column()

        if bpy.context.preferences.addons.get('io_scene_valvesource'):
            col.label(text="Export:")
            col.operator('vat.rigifyretarget_export_all', text="Export All", icon='ACTION')
        else:
            col.label(text="Blender Source Tools is not installed", icon='CANCEL')
            col.label(text="Please install if you want to use this feature")

class VAT_PT_rigifyretargetparameters(bpy.types.Panel):
    bl_label = "Parameters"
    bl_parent_id = 'VAT_PT_rigifyretarget'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    def draw(self, context):
        layout = self.layout
        if bpy.context.object.type == 'ARMATURE' and bpy.context.active_pose_bone and bpy.context.active_object.data.get("rig_id") is None:
            col = layout.column()
            id_store = bpy.context.window_manager
            bone = bpy.context.active_pose_bone
            col.prop_search(bone, "rigify_type", id_store, "rigify_types", text="Rig type")

        bone = bpy.context.selected_bones
        if bone:
            bone = bone[0]
            col = layout.column()
            col.active = (bone.parent is not None)
            col.prop(bone, "use_connect")