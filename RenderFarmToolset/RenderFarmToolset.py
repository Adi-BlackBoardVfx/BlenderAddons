bl_info = {
	"name": "Render farm toolset",
	"author": "Adi Samsonoff",
	"version": (1, 0),
	"blender": (2, 80, 0),
	"location": "Render properties",
	"description": "Prepares blend file for render farm upload(mainly path debugging)",
	"warning": "",
	"wiki_url": "",
	"category": "Render",
}

import bpy
import os, shutil
from bpy.path import abspath, relpath, basename

class RenderFarmToolset(bpy.types.Panel):
	bl_label = "Render farm toolset"
	bl_idname = "RENDER_PT_RenderFarmToolset"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "render"
	bl_options = {'DEFAULT_CLOSED'}
	
	bpy.types.Scene.RemapPath = bpy.props.StringProperty (
		name="Remap Path", 
		subtype='FILE_PATH',)

	def draw(self, context):
		layout = self.layout
		scene = context.scene

		row = layout.row()
		row.prop(scene, "RemapPath")
		row = layout.row()
		row.operator("scene.debug_paths")
		row.enabled= False
		if os.path.exists(abspath(scene.RemapPath)):
			if ".." in scene.RemapPath:
				row = layout.row()
				row.label(text="Path should be absolute", icon='ERROR')
			else:
				row.enabled= True
		else:
			row = layout.row()
			row.label(text="Invalid path", icon='ERROR')


class DebugPaths(bpy.types.Operator):
	bl_idname = "scene.debug_paths"
	bl_label = "Remap Images"
	bl_description = "Remap all image paths relative to given path, ignore missing files"
	bl_options = {'UNDO'}
	
	def execute(self, context):
		#find missing files and eliminate filepath to ignore them
		MissingFiles= []
		for img in bpy.data.images:
			path = abspath(img.filepath)
			if not os.path.exists(path):
				MissingFiles.append( (img,img.filepath) )
				img.filepath = ""

		#remapping operation
		bpy.ops.file.pack_all()
		print("*packed all")
		bpy.ops.file.unpack_all(method='USE_LOCAL')
		print("*un-packed all")
		TexturesDir = os.path.join( os.path.dirname(abspath(bpy.data.filepath)) , "textures" )
		if os.path.exists(TexturesDir):
			shutil.rmtree(TexturesDir)
			print("*packed images removed")
		else:
			print("*no textures folder was found")
		bpy.ops.file.find_missing_files(find_all=True, directory=bpy.context.scene.RemapPath)
		print("*images remapped")
		bpy.ops.file.make_paths_relative()
		print("*paths made relative")

		#refill filepath for ignore images
		print("*ignored images:")
		for i in MissingFiles:
			print (i[0].name)
			i[0].filepath = i[1]

		return {'FINISHED'}



classes = (
	RenderFarmToolset,
	DebugPaths
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()