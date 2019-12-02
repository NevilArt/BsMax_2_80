import bpy
from primitive.primitive import CreatePrimitive, PrimitiveGeometryClass
from bsmax.actions import delete_objects

def GetBoxMesh(width, length, height, wsegs, lsegs, hsegs):
	verts, edges, faces = [], [], []
	# Control the input values
	if wsegs < 1: wsegs = 1
	if lsegs < 1: lsegs = 1
	if hsegs < 1: hsegs = 1

	w = width / wsegs
	l = length / lsegs
	h = height / hsegs
	hw, hl = width / 2, length / 2
	# Create vertexes
	for he in (0.0, height):
		for i in range(wsegs + 1):
			for j in range(lsegs + 1):
				x = w * i - hw
				y = l * j - hl
				z = he
				verts.append((x, y, z))
	for i in range(1,hsegs):
		for j in range(lsegs + 1):
			x = -hw
			y = l * j - hl
			z = h * i
			verts.append((x, y, z))
		for j in range(1, wsegs + 1):
			x = w * j - hw
			y = length - hl
			z = h * i
			verts.append((x, y, z))
		for j in range(lsegs - 1, -1, -1):
			x = width - hw
			y = l * j - hl
			z = h * i
			verts.append((x , y, z))
		for j in range(wsegs - 1, 0, -1):
			x = w * j - hw
			y = -hl 
			z = h * i
			verts.append((x, y, z))
	# Create faces
	# fill plates
	for k in range(2):
		f = k * (wsegs + 1) * (lsegs + 1)
		for i in range(wsegs):
			for j in range(lsegs):
				a = j + (lsegs + 1) * i + f
				b = a + 1
				c = b + lsegs + 1
				d = c - 1
				if k == 0:
					faces.append((a, b, c, d))
				else:
					faces.append((d, c, b, a))
	# fill center
	f = ((lsegs + 1) * 2) * (wsegs + 1)
	l = (wsegs + lsegs) * 2
	for i in range(hsegs - 2):
		for j in range(l):
			a = f + i * l + j   
			if j < l - 1:
				b = a + 1
				c = b + l
				d = c - 1
			else:
				b = f + i * l
				c = f + (i + 1) * l
				d = a + l
			faces.append((d, c, b, a))

	f2 = f + l * (hsegs - 2) # last line first vertext
	if hsegs > 1:
		# silde lowr line 1
		for i in range(lsegs):
			a = i
			b = a + 1
			c = f + i + 1
			d = f + i
			faces.append((d, c, b, a))
		# silde lowr line 2
		fl, fu = lsegs, f + lsegs
		for i in range(wsegs):
			a = fl + i * (lsegs + 1)
			b = a + lsegs + 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))
		# silde lowr line 3
		fl = (wsegs + 1) * (lsegs + 1) - 1
		fu = f + wsegs + lsegs
		for i in range(lsegs):
			a = fl - i
			b = a - 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))
		# silde lowr line  4
		fl = (lsegs + 1) * wsegs
		fu = (wsegs + 1) * (lsegs + 1) * 2 + (lsegs + 1) * 2 + (wsegs - 2)
		for i in range(wsegs):
			a = fl - i * (lsegs + 1)
			b = a - (lsegs + 1)
			if i < wsegs - 1:
				c = fu + i + 1
			else:
				c = f
			d = fu + i
			faces.append((d, c, b, a))
		# silde Uper line 1
		fl = (wsegs + 1) * ((hsegs + lsegs - 1) * 2) + (lsegs - 1) * ((hsegs - 2) * 2)
		fu = (wsegs + 1) * (lsegs + 1)
		for i in range(lsegs):
			a = fl + i
			b = a + 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))
		# silde Uper line 2
		fl += lsegs
		fu += lsegs
		for i in range(wsegs):
			a = fl + i
			b = a + 1
			c = fu + (i + 1) * (lsegs + 1)
			d = fu + i * (lsegs + 1)
			faces.append((d, c, b, a))
		# silde Upper line 3
		fl += wsegs
		fu = ((wsegs + 1) * (lsegs + 1) * 2) - 1
		for i in range(lsegs):
			a = fl + i
			b = a + 1
			c = fu - (i + 1)
			d = fu - i
			faces.append((d, c, b, a))
		# silde lowr line  4
		fl += lsegs
		fu -= lsegs
		for i in range(wsegs):
			a = fl + i
			if i < wsegs - 1:
				b = a + 1
				c = fu - (i + 1) * (lsegs + 1)
			else:
				b = (wsegs + 1) * ((hsegs + lsegs - 1) * 2) + (lsegs - 1) * ((hsegs - 2) * 2)
				c = (wsegs + 1) * (lsegs + 1)
			d = fu - i * (lsegs + 1)
			faces.append((d, c, b, a))
	else:
		# silde lowr line 1
		fu = (wsegs + 1) * (lsegs + 1)
		for i in range(lsegs):
			a = i
			b = a + 1
			c = fu + i + 1
			d = fu + i
			faces.append((d, c, b, a))
		# silde lowr line 2
		fl = lsegs
		fu += lsegs
		for i in range(wsegs):
			a = fl + i * (lsegs + 1)
			b = a + lsegs + 1
			c = fu + (i + 1) * (lsegs + 1)
			d = fu + i * (lsegs + 1)
			faces.append((d, c, b, a))
		# silde lowr line 3
		fl = (wsegs + 1) * (lsegs + 1) - 1
		fu = ((wsegs + 1) * (lsegs + 1) * 2) - 1
		for i in range(lsegs):
			a = fl - i
			b = a - 1
			c = fu - (i + 1)
			d = fu - i
			faces.append((d, c, b, a))
		# silde lowr line  4
		fl = (lsegs + 1) * wsegs
		fu -= lsegs
		for i in range(wsegs):
			a = fl - i * (lsegs + 1)
			b = a - (lsegs + 1)
			if i < wsegs - 1:
				c = fu - (i + 1) * (lsegs + 1)
			else:
				c = (wsegs + 1) * (lsegs + 1)
			d = fu - i * (lsegs + 1)
			faces.append((d, c, b, a))
	return verts, edges, faces

class Box(PrimitiveGeometryClass):
	def __init__(self):
		self.classname = "Box"
		self.finishon = 3
		self.owner = None
		self.data = None
	def reset(self):
		self.__init__()
	def create(self, ctx):
		mesh = GetBoxMesh(0, 0, 0, 1, 1, 1)
		self.create_mesh(ctx, mesh, self.classname)
		pd = self.data.primitivedata
		pd.classname = self.classname
		pd.wsegs, pd.lsegs, pd.hsegs = 1, 1, 1
	def update(self):
		pd = self.data.primitivedata
		mesh = GetBoxMesh(pd.width, pd.length, pd.height,
					pd.wsegs, pd.lsegs, pd.hsegs)
		self.update_mesh(mesh)
	def abort(self):
		delete_objects([self.owner])

class BsMax_OT_CreateBox(CreatePrimitive):
	bl_idname = "bsmax.createbox"
	bl_label = "Box (Create)"
	subclass = Box()

	def create(self, ctx, clickpoint):
		self.subclass.create(ctx)
		owner = self.subclass.owner
		self.params = owner.data.primitivedata
		owner.location = clickpoint.view
		owner.rotation_euler = clickpoint.orient
	def update(self, clickcount, dimantion):
		if clickcount == 1:
			self.params.width = dimantion.width
			self.params.length = dimantion.length
			self.subclass.owner.location = dimantion.center
		elif clickcount == 2:
			self.params.height = dimantion.height
		if clickcount > 0:
			self.subclass.update()
	def finish(self):
		pass

def box_cls(register):
	c = BsMax_OT_CreateBox
	if register: bpy.utils.register_class(c)
	else: bpy.utils.unregister_class(c)

if __name__ == '__main__':
	box_cls(True)

__all__ = ["box_cls", "Box"]