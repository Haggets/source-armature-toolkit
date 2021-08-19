import bpy
from . import __init__
from . import ops
from . import utils
from .addon_updater_ops import get_user_preferences

class SAT_PT_mainpanel(bpy.types.Panel): #Main panel that subpanels will use
    bl_label = "Source Armature Toolkit"
    bl_idname = 'SAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    def draw(self, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo
        layout = self.layout
        col = layout.column()
        
        col.prop(satproperties, 'target_armature') #Armature that will be affected by the utilities
        if not satproperties.target_armature and not satinfo.creating_armature:
            col.operator('sat.create_armature')
        
        if satinfo.creating_armature:
            col.prop(satproperties, 'game_armature_type')
            col.prop(satproperties, 'game_armature')

            #L4D2 survivors
            if satproperties.game_armature_type == 'PM' and satproperties.game_armature == 'L4D2':
                col.prop(satproperties, 'game_armature_l4d2')

            col.operator('sat.create_armature_apply')

            if satproperties.game_armature == 'SBOX' and satinfo.creating_armature:
                if satproperties.game_armature_type == 'PM':
                    col.label(text="These may be prone to changing...")
                else:
                    col.label(text="Not currently available...")

        if satinfo.unconverted_armature:
            col.operator('sat.convert_armature')

        if not satinfo.creating_armature:
            if satproperties.target_armature:
                if satinfo.scheme == -1:
                    col.label(text="Type: Unknown Armature")
                elif satinfo.viewmodel:
                    col.label(text="Type: Viewmodel Armature")
                elif satinfo.goldsource:
                    col.label(text="Type: GoldSource Armature")
                elif satinfo.titanfall:
                    col.label(text="Type: Titanfall Armature")
                elif satinfo.sbox:
                    col.label(text="Type: S&Box Armature")
                else:
                    col.label(text="Type: Default Source Armature")
            else:
                col.label(text="No Armature...")
        else:
            col.label(text="Select armature in plugin once done")
        
class SAT_PT_armaturerename(bpy.types.Panel): #Armature rename panel
    bl_label = "Armature Renaming"
    bl_parent_id = 'SAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo
        preferences = get_user_preferences()
        layout = self.layout

        row = layout.row()
        row.operator('sat.armaturerename_blender', text='Convert')
        row.operator('sat.armaturerename_source', text='Restore')

        if satproperties.target_armature:
            col = layout.column()
            if satinfo.sbox or satinfo.tf2:
                col.label(text="Already Blender friendly...")
            elif satinfo.scheme == 0:
                col.label(text="Current: Default Scheme")
            elif satinfo.scheme == 1:
                col.label(text="Current: Blender Friendly Scheme")


        if preferences.show_info:
            box = layout.box()
            box.label(text="Meant for weight painting", icon='INFO')
            box.label(text="Allows for weight symmetry", icon='INFO')
            box.label(text="Remember to restore before export", icon='ERROR')

class SAT_PT_constraintsymmetry(bpy.types.Panel): #Constraint Symmetry panel
    bl_label = "Constraint Symmetry"
    bl_parent_id = 'SAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo
        preferences = get_user_preferences()
        layout = self.layout
        
        row = layout.row()
        row.operator('sat.constraintsymmetry_create', text='Add')
        row.operator('sat.constraintsymmetry_delete', text='Remove')

        row = layout.row()
        row.prop(satproperties, 'affected_side', expand=True)

        col = layout.column()
        col.operator('sat.constraintsymmetry_apply', text='Apply', icon='OUTLINER_DATA_ARMATURE')
        if satproperties.target_armature:
            if satproperties.affected_side == 'LTR' and satinfo.symmetry == 2 or satproperties.affected_side == 'RTL' and satinfo.symmetry == 1:
                col.label(text="Already applied on the opposite side")
            
            if satinfo.tf2:
                col.label(text="Incompatible with this armature type")
        
        col = layout.column()
        col.prop(satproperties, 'symmetry_offset')
        col.prop(satproperties, 'symmetry_upperarm_rotation_fix')

        if preferences.show_info:
            box = layout.box()
            box.label(text="Meant for armature reproportioning", icon='INFO')
            box.label(text="Allows for symmetry while keeping", icon='INFO')
            box.label(text="corrected roll values")
        
class SAT_PT_weightarmature(bpy.types.Panel): #Weight Armature panel
    bl_label = "Weight Armature"
    bl_parent_id = 'SAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw (self, context):
        satinfo = bpy.context.scene.satinfo
        preferences = get_user_preferences()
        layout = self.layout

        row = layout.row()
        row.operator('sat.weightarmature_create', text='Generate')
        row.operator('sat.weightarmature_delete', text='Delete')

        if preferences.show_info:
            box = layout.box()
            box.label(text="Meant for weight creation", icon='INFO')
            box.label(text="Allows more spread out", icon='INFO')
            box.label(text="vertex weights, requiring")
            box.label(text="less tweaking overall")

class SAT_PT_rigifyretarget(bpy.types.Panel): #Rigify Retargetting panel
    bl_label = "Rigify Retarget"
    bl_idname = 'SAT_PT_rigifyretarget'
    bl_parent_id = 'SAT_PT_mainpanel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw (self, context):
        satproperties = bpy.context.scene.satproperties
        satinfo = bpy.context.scene.satinfo
        preferences = get_user_preferences()
        layout = self.layout

        if bpy.context.preferences.addons.get('rigify'):
            row = layout.row()
            row.operator('sat.rigifyretarget_create', text='Generate')
            row.operator('sat.rigifyretarget_delete', text='Delete')

            col = layout.column()

            if not satinfo.animation_armature:
                col.prop(satproperties, 'target_object')
                col.label(text="Used to check for facial expressions")

            if satproperties.target_armature:
                if satinfo.animation_armature:
                    if satinfo.animation_armature_setup:
                        if bpy.context.object.name != satproperties.target_armature.name + '.anim':
                            col.operator('sat.rigifyretarget_generate', text="Generate rig", icon='OUTLINER_DATA_ARMATURE')
                            if satproperties.target_object:
                                col.label(text="Reposition facial drivers correctly", icon='INFO')
                                col.label(text="and edit bone parameters to your need")
                            else:
                                col.label(text="Edit bone parameters to your need", icon='INFO')

                        else:
                            col.operator('sat.rigifyretarget_link', text="Link to generated armature", icon='OUTLINER_DATA_ARMATURE')

                    else:
                        col.prop(satproperties, 'retarget_constraints')

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

class SAT_PT_rigifyretargetexport(bpy.types.Panel):
    bl_label = "Bake/Export"
    bl_parent_id = 'SAT_PT_rigifyretarget'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        satproperties = bpy.context.scene.satproperties


        col.label(text="Action bake:")
        row = layout.row()
        row.operator('sat.rigifyretarget_bake_single', text='Single', icon='ACTION')
        row.operator('sat.rigifyretarget_bake_all', text='All', icon='ACTION')
        col = layout.column()
        col.prop(satproperties, 'bake_helper_bones')
        if not satproperties.retarget_constraints:
            col.label(text="Retarget constraints are disabled...")

        col = layout.column()

        #If Blender Source Tools is enabled
        if bpy.context.preferences.addons.get('io_scene_valvesource'):
            col.label(text="Export: (Only for Source 1)")
            col.operator('sat.rigifyretarget_export_all', text="Export All", icon='ACTION')
            if satproperties.retarget_constraints == True:
                col = layout.column()
                col.label(text="Retarget constraints are enabled...")
        else:
            col.label(text="Blender Source Tools is not installed", icon='CANCEL')
            col.label(text="Please install if you want to use this feature")