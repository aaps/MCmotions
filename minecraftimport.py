# Copyright (c) 2011 Thomas Glamsch
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

import bpy
import string
import pdb
import time
import json
from math import pi

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

dbg = False

bl_info = {
    "name": "Minecraft mejiggest (*.json)",
    "description": "This addon allows you to import WarCraft MDL model files (.mdl).",
    "author": "Thomas 'CruzR' Glamsch",
    "version": (0, 2, 1),
    "blender": (2, 6, 3),
    #"api": ???,
    "location": "File > Import > minecraft stuff",
    "warning": "Currently only the vertices and faces are imported, work in progress.",
    # "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/Scripts/Import-Export/WarCraft_MDL",
    # "tracker_url": "http://projects.blender.org/tracker/index.php?func=detail&aid=29552",
    "category": "Import-Export"}

    

# This class initiates and starts the state machine and uses the gathered data
# to construct the model in Blender.
class DataImporter:

    
    def run(self, filepath, context):
        start_time = time.time()
        
        origin = open(filepath, 'r')

        total = json.loads(origin.read())

        for key, value in total.items():
            firstloc = value['positions'][0]['pos']
            bpy.ops.mesh.primitive_cube_add(location=firstloc)
            ob = bpy.context.object

            mat = bpy.data.materials.new("PKHG")

            mobtype = int(value['type'])
            if mobtype == 50:
                ob.name = "creeper"
                mat.diffuse_color = (0.0,1.0,0.0)
            elif mobtype == 51:
                ob.name = "skeleton"
                mat.diffuse_color = (1.0,1.0,1.0)
            elif mobtype == 52:
                ob.name = "spider"
                mat.diffuse_color = (0.2,0.1,0.1)
            elif mobtype == 54:
                ob.name = "zombol"
                mat.diffuse_color = (0.0,0.3,0.0)
            elif mobtype == 90:
                ob.name = "pig"
                mat.diffuse_color = (0.5,0.4,0.4)
            elif mobtype == 65:
                ob.name = "bat"
                mat.diffuse_color = (1,0.5,0.2)
            elif mobtype == 58:
                ob.name = "enderman"
                mat.diffuse_color = (0.5,0.0,0.5)
            else:
                mat.diffuse_color = (0.0,0.0,0.0)

            ob.active_material = mat
            frame_num = 0
            for posses in value['positions'][1:]:
                bpy.context.scene.frame_set(frame_num)
                ob.location =  (posses['pos'][0], posses['pos'][2], posses['pos'][1])
                ob.rotation_mode = 'XYZ'
                ob.rotation_euler = (0, 0,(pi * posses['yawpichhead'][0] / 180) )
                ob.hide = not bool(posses['alive'])
                ob.hide_render = not bool(posses['alive'])
                bpy.ops.anim.keyframe_insert(type='Location')
                bpy.ops.anim.keyframe_insert(type='Rotation')
                ob.keyframe_insert("hide")
                ob.keyframe_insert("hide_render")


                
                frame_num = posses['time'] * 24


        print("Script finished after {} seconds".format(time.time() - start_time))
        return {'FINISHED'}

# This is the import operator.
class MineCraftImport(bpy.types.Operator, ImportHelper):
    '''Import form minecraft netrecorder some format (.json)'''
    bl_idname = "something.minecraft"
    bl_label = "MineCraft EntityPaths"
    # mc ep
    
    filename_ext = ".json"
    
    filter_glob = StringProperty(
            default="*.json",
            options={'HIDDEN'}
            )
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        di = DataImporter()
        return di.run(self.filepath, context)

def menu_func_export(self, context):
    self.layout.operator(MineCraftImport.bl_idname, text="MineCraft EntityPaths (.json)")

def register():
    bpy.utils.register_class(MineCraftImport)
    bpy.types.INFO_MT_file_import.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(MineCraftImport)
    bpy.types.INFO_MT_file_import.remove(menu_func_export)

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.something.minecraft('INVOKE_DEFAULT')