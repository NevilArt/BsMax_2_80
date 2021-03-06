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
from bsmax.operator import PickOperator

class Object_OT_Attach(PickOperator):
	bl_idname = "object.attach"
	bl_label = "Attach"
	
	filters = ['AUTO']

	@classmethod
	def poll(self, ctx):
		if ctx.area.type == 'VIEW_3D':
			if len(ctx.scene.objects) > 0:
				if ctx.object != None:
					return ctx.mode == 'OBJECT'
		return False
	
	def convert(self, ctx, obj):
		obj.select_set(True)
		ctx.view_layer.objects.active = obj
		
		""" collaps modifiers """
		for modifier in obj.modifiers:
			bpy.ops.object.modifier_apply(modifier=modifier.name)

		# """ set the target mode """
		# bpy.ops.object.convert(target="MESH")


	def picked(self, ctx, source, subsource, target, subtarget):
		bpy.ops.object.select_all(action='DESELECT')
		self.convert(ctx, target)
		
		for s in source:
			s.select_set(True)
			ctx.view_layer.objects.active = s
			
			""" clear primitive data """
			if s.type in {'MESH','CURVE'}:
				s.data.primitivedata.classname = ""
		
		target.select_set(state = True)
		bpy.ops.object.join()
		bpy.ops.ed.undo_push()
		bpy.ops.object.attach('INVOKE_DEFAULT')
		self.report({'OPERATOR'},'bpy.ops.object.attach()')



class Object_TO_Delete_Plus(Operator):
	""" Delete Plus """
	bl_idname = "object.delete_plus"
	bl_label = "Delete Plus"
	bl_options = {'REGISTER', 'UNDO'}
	
	@classmethod
	def poll(self, ctx):
		return ctx.mode == 'OBJECT'
	
	def execute(self,ctx):
		for obj in ctx.selected_objects:
			for child in obj.children:
				matrix_world = child.matrix_world.copy()
				child.parent = None
				child.matrix_world = matrix_world
		bpy.ops.object.delete({"selected_objects": ctx.selected_objects})
		return{"FINISHED"}


classes = [Object_OT_Attach, Object_TO_Delete_Plus]

def register_attach():
	[bpy.utils.register_class(c) for c in classes]

def unregister_attach():
	[bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
	register_attach()