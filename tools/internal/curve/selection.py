############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################
import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, FloatProperty, IntProperty

def select_spline(spline, deselect=False):
	state = not deselect
	for bezier_points in spline.bezier_points:
		bezier_points.select_left_handle = state
		bezier_points.select_control_point = state
		bezier_points.select_right_handle = state



class Curve_OT_Select_By_Length(Operator):
	bl_idname = 'curve.select_by_length'
	bl_label = 'Select By Length'
	bl_options = {'REGISTER', 'UNDO'}

	by: EnumProperty(name = 'By', default='GREATER',
		items=[('GREATER', 'Greater then', ''),('LESS', 'LESS than', ''),('EQUAL', 'Equal to', '')])
	length: FloatProperty(unit='LENGTH', default=1.0, min=0)
	tolerans: FloatProperty(unit='LENGTH', default=0.01, min=0)

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode == 'EDIT_CURVE'
		return False
	
	def check_lenght(self, obj):
		for spline in obj.data.splines:
			length = spline.calc_length()
			if self.by == 'GREATER':
				if length > self.length:
					select_spline(spline)
				else:
					select_spline(spline, deselect=True)
			
			elif self.by == 'LESS':
				if length < self.length:
					select_spline(spline)
				else:
					select_spline(spline, deselect=True)
			
			elif self.by == 'EQUAL':
				if self.length - self.tolerans < length <= self.length + self.tolerans:
					select_spline(spline)
				else:
					select_spline(spline, deselect=True)

	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'by')
		layout.prop(self, 'length')
		if self.by == 'EQUAL':
			layout.prop(self, 'tolerans')

	def execute(self, ctx):
		for obj in ctx.selected_objects:
			if obj.type == 'CURVE':
				self.check_lenght(obj)
		return{'FINISHED'}



class Curve_OT_Select_By_Segment_Count(Operator):
	bl_idname = 'curve.select_by_segment_count'
	bl_label = 'Select By Segment Count'
	bl_options = {'REGISTER', 'UNDO'}

	by: EnumProperty(name = 'By', default='GREATER',
		items=[('GREATER', 'Greater then', ''),('LESS', 'LESS than', ''),('EQUAL', 'Equal to', '')])
	count: IntProperty(name="Count", min= 2, default=3)
	tolerans: IntProperty(default=0, min=1)

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode == 'EDIT_CURVE'
		return False
	
	def check_count(self, obj):
		for spline in obj.data.splines:
			count = len(spline.bezier_points)
			if self.by == 'GREATER':
				if count > self.count:
					select_spline(spline)
				else:
					select_spline(spline, deselect=True)
			
			elif self.by == 'LESS':
				if count < self.count:
					select_spline(spline)
				else:
					select_spline(spline, deselect=True)
			
			elif self.by == 'EQUAL':
				if self.count - self.tolerans < count < self.count + self.tolerans:
					select_spline(spline)
				else:
					select_spline(spline, deselect=True)

	def draw(self, ctx):
		layout = self.layout
		layout.prop(self, 'by')
		layout.prop(self, 'count')
		if self.by == 'EQUAL':
			layout.prop(self, 'tolerans')

	def execute(self, ctx):
		for obj in ctx.selected_objects:
			if obj.type == 'CURVE':
				self.check_count(obj)
		return{'FINISHED'}


# class Curve_OT_Select_By_Close(Operator):
# 	bl_idname = 'curve.select_by_close'
# 	bl_label = 'Select By Close/Open'
# 	bl_options = {'REGISTER', 'UNDO'}

# 	closed: EnumProperty(name = 'By', default='OPEN',
# 		items=[('CLOSE', 'if Close', ''),('OPEN', 'if Open', ''))

# 	@classmethod
# 	def poll(self, ctx):
# 		if ctx.area.type == 'VIEW_3D':
# 			if len(ctx.scene.objects) > 0:
# 				if ctx.object != None:
# 					return ctx.mode == 'EDIT_CURVE'
# 		return False
	
# 	def check_count(self, obj):
# 		for spline in obj.data.splines:
# 			count = len(spline.bezier_points)
# 			if self.closed:


# 				select_spline(spline)
# 			else:
# 				select_spline(spline, deselect=True)


# 	def draw(self, ctx):
# 		layout = self.layout
# 		layout.prop(self, 'by')
# 		layout.prop(self, 'count')
# 		if self.by == 'EQUAL':
# 			layout.prop(self, 'tolerans')

# 	def execute(self, ctx):
# 		for obj in ctx.selected_objects:
# 			if obj.type == 'CURVE':
# 				self.check_count(obj)
# 		return{'FINISHED'}


def selection_menu(self, ctx):
	layout = self.layout
	layout.separator()
	layout.operator('curve.select_by_length')
	layout.operator('curve.select_by_segment_count')



classes = [Curve_OT_Select_By_Length, Curve_OT_Select_By_Segment_Count]

def register_selection():
	[bpy.utils.register_class(c) for c in classes]
	bpy.types.VIEW3D_MT_select_edit_curve.append(selection_menu)

def unregister_selection():
	bpy.types.VIEW3D_MT_select_edit_curve.remove(selection_menu)
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_selection()