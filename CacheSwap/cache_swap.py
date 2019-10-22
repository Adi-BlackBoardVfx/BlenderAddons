bl_info = {
	"name": "cache swap (.abc/.pc2/.mdd)",
	"author": "Adi Samsonoff",
	"version": (1, 0),
	"blender": (2, 80, 0),
	"location": "View3Dn",
	"description": "updates cache modifier: swaps existing cache file with new one",
	"warning": "",
	"wiki_url": "",
	"category": "Mesh",
}

import bpy
import os
from bpy.path import abspath, relpath, basename

class CacheSwapPanel(bpy.types.Panel):
	bl_label = "Cache Swap"
	bl_idname = "OBJECT_PT_CahceSwap"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "Cache Swap"
	bl_context = "objectmode"

	bpy.types.Scene.NewCachePath = bpy.props.StringProperty (
		name="New Cache File", 
		subtype='FILE_PATH',)
	
	def draw(self, context):
		layout = self.layout
		obj = context.object
		scene = context.scene

		row = layout.row()
		row.label(text="Active object: " + obj.name, icon='OBJECT_DATA')
		
		IdentifyCache = self.IdentifyCache(obj)
		row = layout.row()
		row.label(text=IdentifyCache["text"], icon=IdentifyCache["icon"])

		if IdentifyCache["CurrentCacheFile"]:
			layout.separator()
		
			box = layout.box()
			box.label(text="New Cache File")
			box.prop(scene, "NewCachePath", text="")
			if basename(scene.NewCachePath) == IdentifyCache["CurrentCacheFile"]["name"]:
				box.label(text="Attention: Same cache file name as current, are you sure you want to re-upload?", translate=True, icon='ERROR')

			row = layout.row()
			row.operator("scene.upload_and_swap", icon='ARROW_LEFTRIGHT').CurrentCacheFile = IdentifyCache["CurrentCacheFile"]["mod_name"] + '___' + IdentifyCache["CurrentCacheFile"]["format"]


	
	
	def IdentifyCache(self, obj):
		CacheFound = []
		IdentifyCache = {
			"text":None,
			"icon":None, 
			"CurrentCacheFile": None  }
			
		if len(obj.modifiers) > 0:
			for mod in obj.modifiers:
				if mod.type == "MESH_CACHE" or mod.type == "MESH_SEQUENCE_CACHE":
					CacheFound.append(mod.name)
		
		if len(CacheFound) == 0:
			IdentifyCache["text"] = "No cache modifiers found"
			IdentifyCache["icon"] ='CANCEL'
		elif len(CacheFound) > 1:
			IdentifyCache["text"] = "More than one cache modifier found"
			IdentifyCache["icon"] ='ERROR' 
		else:
			CurrentCacheFile = self.CurrentCacheFile(obj, CacheFound[0])
			IdentifyCache["text"] = "Currect Cache: %s" %( CurrentCacheFile["name"] )
			IdentifyCache["icon"] ='FILE_CACHE'
			IdentifyCache["CurrentCacheFile"] = CurrentCacheFile

		return IdentifyCache

	def CurrentCacheFile(self, obj, mod_name):
		CacheFile = {"format":None, "name":None, "mod_name":mod_name}
		mod = obj.modifiers[mod_name]
		
		if mod.type == "MESH_SEQUENCE_CACHE":
			CacheFile["format"] = 'ABC'
			CacheFile["name"] = mod.cache_file.name
		
		elif mod.type == "MESH_CACHE":
			CacheFile["format"] = mod.cache_format
			CacheFile["name"] = basename(mod.filepath)

		return CacheFile




class UploadAndSwap(bpy.types.Operator):
	bl_idname = "scene.upload_and_swap"
	bl_label = "Upload And Swap"
	bl_description = "Upload new cache file & swap all objects with the same current cache to the new one"
	bl_options = {'UNDO'}

	CurrentCacheFile : bpy.props.StringProperty()
	
	def execute(self, context):
		ModifierName= self.CurrentCacheFile.rsplit("___")[0]
		Format= self.CurrentCacheFile.rsplit("___")[1]
		
		if os.path.exists( abspath(context.scene.NewCachePath) ):
			if Format == "ABC":
				self.AlembicSwap(ModifierName)
			else:
				self.MddPc2Swap(ModifierName)
		else:
			self.report({'ERROR'}, 'Path does not exist')

		return {'FINISHED'}

	def AlembicSwap(self, ModifierName):
		NewCachePath = bpy.context.scene.NewCachePath
		
		#upload new cache
		bpy.ops.cachefile.open(filepath= NewCachePath) 
		NewCache = bpy.data.cache_files.get(basename(NewCachePath))
		#just in case there's been a missmatch because of a previously loaded cache file with the same name...
		if abspath(NewCache.filepath) != abspath(NewCachePath):
			for CF in bpy.data.cache_files:
				if CF.name.contains( basename(NewCachePath) ) and abspath(CF.filepath) == abspath(NewCachePath):
					NewCache = CF
		
		#look for objects with same current cache
		CurrentCache = bpy.context.active_object.modifiers[ModifierName].cache_file
		for obj in bpy.context.scene.objects:
			if len(obj.modifiers)>0:
				for mod in obj.modifiers:
					if mod.type == "MESH_SEQUENCE_CACHE":
						if mod.cache_file == CurrentCache:
							#swap cache
							mod.cache_file = NewCache
							self.report({'INFO'}, 'Cache succesfully changed :)')


	def MddPc2Swap(self, ModifierName):
		#get new cache
		NewCachePath = bpy.context.scene.NewCachePath
		if NewCachePath.upper().endswith('MDD') or NewCachePath.upper().endswith('PC2'):
			NewCacheFormat = NewCachePath.upper()[-3:]
			#look for objects with same current cache
			CurrentCache = bpy.context.active_object.modifiers[ModifierName].filepath
			for obj in bpy.context.scene.objects:
				if len(obj.modifiers)>0:
					for mod in obj.modifiers:
						if mod.type == "MESH_CACHE":
							if mod.filepath == CurrentCache:
								#swap cache
								mod.cache_format = NewCacheFormat
								mod.filepath = NewCachePath
								self.report({'INFO'}, 'Cache succesfully changed :)')

		else:
			self.report({'ERROR'}, 'Mesh Cache modifier accepts only .MDD/.PC2')
		
		

classes = (
	CacheSwapPanel,
	UploadAndSwap
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()