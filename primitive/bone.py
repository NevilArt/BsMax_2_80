############################################################################
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation,either version 3 of the License,or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not,see <https://www.gnu.org/licenses/>.
############################################################################

import bpy
from primitive.primitive import CreatePrimitive,PrimitiveGeometryClass
from bsmax.actions import delete_objects
from bsmax.math import get_axis_constraint

class Armature(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Armature"
		self.finishon = 0 # infinit
		self.owner = None
		self.data = None
		self.bones = []
	def reset(self):
		self.__init__()
	def create(self, ctx):
		bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))
		self.owner = ctx.active_object
		self.data = self.owner.data
	def update(self, ctx):
		pass
	def abort(self):
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		edit_bones = self.data.edit_bones
		if len(edit_bones) > 0:
			edit_bones.remove(edit_bones[-1])
		for i in range(len(edit_bones) - 1):
			# TODO find a better way to replace with this ugly code
			bpy.ops.armature.select_all(action='DESELECT')
			edit_bones.active = edit_bones[i]
			edit_bones[i + 1].select = True
			bpy.ops.armature.parent_set(type='CONNECTED')
			
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
		if len(self.data.bones) == 0:
			delete_objects([self.owner])
		self.reset()

class Create_OT_Bone(CreatePrimitive):
	bl_idname="create.bone"
	bl_label="Bone"
	subclass = Armature()
	lastclick = 1
	startpoint = None

	def create(self, ctx, clickpoint):
		self.usedkeys += ['LEFT_SHIFT', 'RIGHT_SHIFT', 'BACK_SPACE']
		self.requestkey = ['BACK_SPACE']
		self.subclass.create(ctx)
		self.startpoint = clickpoint.view
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		edit_bones = self.subclass.data.edit_bones 
		for bone in edit_bones:
			edit_bones.remove(bone)

	def update(self, ctx, clickcount, dimantion):
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		edit_bones = self.subclass.data.edit_bones

		if self.shift:
			if len(edit_bones) > 0:
				dimantion.view = get_axis_constraint(edit_bones[-1].head, dimantion.view)

		if len(edit_bones) > 0:
			edit_bones[-1].tail = dimantion.view
		if clickcount != self.lastclick:
			newbone = edit_bones.new('Bone')
			if len(edit_bones) == 1:
				newbone.head = self.startpoint
			else:
				newbone.head = edit_bones[-2].tail
			newbone.tail = dimantion.view
			self.lastclick = clickcount

	def event(self, event, value):
		if event == 'BACK_SPACE':
			if value == 'RELEASE':
				bpy.ops.object.mode_set(mode='EDIT', toggle=False)
				edit_bones = self.subclass.data.edit_bones
				if len(edit_bones) > 1:
					edit_bones.remove(edit_bones[-1])
	def finish(self):
		pass

def register_bone():
	bpy.utils.register_class(Create_OT_Bone)

def unregister_bone():
	bpy.utils.unregister_class(Create_OT_Bone)