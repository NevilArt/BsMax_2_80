import bpy
from bpy.types import Operator
from bpy.props import EnumProperty
from primitive.primitive import CreatePrimitive
from bsmax.actions import delete_objects

class Empty:
	def __init__(self):
		self.finishon = 2
		self.owner = None
	def reset(self):
		self.__init__()
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateEmpty(CreatePrimitive):
	bl_idname="bsmax.createempty"
	bl_label="Empty (Create)"
	subclass = Empty()

	empty_type: EnumProperty(name='Type',default='PLAIN_AXES',
		items =[('PLAIN_AXES','Point axis',''),('ARROWS','Arrows',''),
				('SINGLE_ARROW','Single Arrow',''),('CIRCLE','Circle',''),
				('CUBE','Cube',''),('SPHERE','Sphere',''),
				('CONE','Cone',''),('IMAGE','Image','')])
	depth: EnumProperty(name='Depth',default='DEFAULT',
		items =[('DEFAULT','Default',''),('FRONT','Front',''),('BACK','Back','')])

	def create(self, ctx, clickpoint):
		bpy.ops.object.empty_add(type=self.empty_type,location=clickpoint.view)
		self.subclass.owner = ctx.active_object
		self.subclass.owner.rotation_euler = clickpoint.orient
		if self.empty_type == "IMAGE":
			self.subclass.owner.empty_image_depth = self.depth

	def update(self, clickcount, dimantion):
		if clickcount == 1:
			self.subclass.owner.empty_display_size = dimantion.radius
	def finish(self):
		pass

class BsMax_OT_CreateImage(Operator):
	bl_idname="bsmax.createimage"
	bl_label="Image (Create)"
	bl_options={"UNDO"}
	image_type: EnumProperty(name='Type',default='REFERENCE',
		items =[('REFERENCE','Reference',''),('BACKGROUND','Background','')])
	@classmethod
	def poll(self, ctx):
		return ctx.area.type == 'VIEW_3D'
	def execute(self, ctx):
		if self.image_type == "REFERENCE":
			bpy.ops.bsmax.createempty('INVOKE_DEFAULT',empty_type="IMAGE",depth="DEFAULT")
		else:
			bpy.ops.bsmax.createempty('INVOKE_DEFAULT',empty_type="IMAGE",depth="BACK")
		return {'FINISHED'}

def empty_cls(register):
	classes = [BsMax_OT_CreateEmpty, BsMax_OT_CreateImage]
	for c in classes:
		if register: bpy.utils.register_class(c)
		else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	empty_cls(True)

__all__ = ["empty_cls"]