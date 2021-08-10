import bpy
from . import addon_updater_ops

@addon_updater_ops.make_annotations
class SAT_preferences(bpy.types.AddonPreferences):
	"""Valve Armature Toolkit updater preferences"""
	bl_idname = __package__

	#Updater preferences
	auto_check_update = bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=True,
		)
	updater_intrval_months = bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0
		)
	updater_intrval_days = bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=2,
		min=0,
		max=31
		)
	updater_intrval_hours = bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23
		)
	updater_intrval_minutes = bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59
		)

	#Addon preferences
	show_info = bpy.props.BoolProperty(
		name="Show operator information",
		description="If to show description of what each operator is made for",
		default=True,
	)

	def draw(self, context):
		layout = self.layout
		settings = addon_updater_ops.get_user_preferences(context)

		layout.prop(settings, "show_info")

		#Addon panel
		addon_updater_ops.update_settings_ui(self, context)
