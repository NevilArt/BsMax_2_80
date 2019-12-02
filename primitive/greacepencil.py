import bpy
from mathutils import Vector
from bpy.props import EnumProperty
from primitive.primitive import CreatePrimitive
from bsmax.actions import delete_objects

class GreacePencil:
	def __init__(self):
		self.finishon = 2
		self.owner = None
	def reset(self):
		self.__init__()
	def create(self, ctx, gpencil_type):
		bpy.ops.object.gpencil_add(location=(0,0,0),type=gpencil_type)
		self.owner = ctx.active_object
		self.data = self.owner.data
	def update(self):
		pass
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateGreacePencil(CreatePrimitive):
	bl_idname="bsmax.creategreacepencil"
	bl_label="GreacePencil (Create)"
	subclass = GreacePencil()

	gpencil_type: EnumProperty(name='Type',default='EMPTY',
		items =[('EMPTY','Blank',''),('STROKE','Stroke',''),('MONKEY','Monkey','')])

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx, self.gpencil_type)
		owner = self.subclass.owner
		owner.location = clickpoint.view		
		owner.rotation_euler = clickpoint.orient + Vector((-1.5708,0,0))

	def update(self, clickcount, dimantion):
		if clickcount == 1:
			owner = self.subclass.owner
			owner.location = dimantion.center
			r = dimantion.radius/2
			owner.scale = (r,r,r)

	def finish(self):
		pass

def greacepencil_cls(register):
	c = BsMax_OT_CreateGreacePencil
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	greacepencil_cls(True)

__all__ = ["greacepencil_cls"]