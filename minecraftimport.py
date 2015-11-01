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
import urllib.request
from math import pi
import operator
import ast


from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

dbg = False

bl_info = {
    "name": "Minecraft mejiggest (*.mcmo)",
    "description": "This addon allows you to import minecraft worls and mob motions",
    "author": "Aat Karelse",
    "version": (0, 2, 1),
    "blender": (2, 6, 3),
    #"api": ???,
    "location": "File > Import > minecraft stuff",
    "warning": "Alpha",
    # "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/Scripts/Import-Export/WarCraft_MDL",
    # "tracker_url": "http://projects.blender.org/tracker/index.php?func=detail&aid=29552",
    "category": "Import-Export"}

    

# This class initiates and starts the state machine and uses the gathered data
# to construct the model in Blender.
class DataImporter:

    def createMeshFromData(self, material, origin, verts, faces):
        # Create mesh and object
        me = bpy.data.meshes.new(str(material)+'Mesh')
        ob = bpy.data.objects.new(str(material), me)

        ob.show_name = True
        
        mat = bpy.data.materials.new("PKHG")

        if material == 9:
            mat.diffuse_color = (0,0,1)
            mat.alpha = 0.5
            mat.use_transparency = True
            mat.transparency_method = 'RAYTRACE'
        elif material == 1:
            mat.diffuse_color = (0.7,0.7,0.7)
        elif material == 3:
            mat.diffuse_color = (0.9,0.7,0.6)
        elif material == 7:
            mat.diffuse_color = (0.2,0.2,0.2)
        elif material in [11, 10]:
            mat.diffuse_color = (0.9,0.2,0.2)
            mat.emit = 5
        elif material in [13]:
            mat.diffuse_color = (0.5,0.5,0.5)
        elif material == 15:
            mat.diffuse_color = (0.6,0.5,0.4)
        elif material == 16:
            mat.diffuse_color = (0.4,0.4,0.4)
        elif material == 17 or material == 5:
            mat.diffuse_color = (0.5,0.3,0.1)
        elif material == 18 or material == 2 or material == 111 or material == 31:
            mat.diffuse_color = (0,0.8,0)
        elif material == 12 or material == 24 :
            mat.diffuse_color = (1,0.8,0.7)
        elif material == 49:
            mat.diffuse_color = (0,0,0.2)
        elif material in [44, 82]:
            mat.diffuse_color = (0.8,0.8,0.8)
        elif material == 79:
            mat.diffuse_color = (0.4,0.4,1)
        elif material in [89, 50, 124, 91, 51, 62] :
            mat.diffuse_color = (0.9,0.9,0.2)
            mat.emit = 5
        elif material == 138:
            mat.diffuse_color = (0.5,0.5,0.8)
        elif material in [155, 171, 156]:
            mat.diffuse_color = (1,1,1)
        elif material == 159:
            mat.diffuse_color = (1,0.8,0.8)
        else:
            mat.diffuse_color = (0,0,0)

        ob.active_material = mat
        # Link object to scene and make active
        scn = bpy.context.scene
        scn.objects.link(ob)
        
     
        # Create mesh from given verts, faces.
        me.from_pydata(verts, [], faces)

        # Update mesh with new data
        me.update()    
        return ob

    def run(self, filepath, context):
        start_time = time.time()
        
        origin = open(filepath, 'r')

        total = ast.literal_eval(origin.read())
        
        indexi = 0

        
        vertices = total['vertices']
        faces = total['faces']
        entitys = total['allhistory']
        total = None

        extralist = {}

        for mat in vertices:

            self.createMeshFromData(mat, (0,0,0), vertices[mat], faces[mat] )
            faces[mat] = None
            vertices[mat] = None

       
        

        for value in entitys:
            
            aentity = entitys[value]
            
            firstloc = aentity['positions'][0]['pos']
            # bpy.ops.mesh.primitive_uv_sphere_add(size=0.5, location=firstloc)
            # bpy.ops.mesh.primitive_cube_add(location=firstloc)
            bpy.ops.mesh.primitive_monkey_add(location=firstloc)
            ob = bpy.context.object
            ob.rotation_mode = 'XYZ'
            # ob.rotation_euler = ((pi * 90 / 180), 0,0 )
            ob.scale = (0.5,0.5,0.5)

            mat = bpy.data.materials.new("PKHG")

            mobtype = aentity['type']
            if mobtype == '50':
                ob.name = "creeper"
                mat.diffuse_color = (0.0,1.0,0.0)
            elif mobtype == '51':
                ob.name = "skeleton"
                mat.diffuse_color = (1.0,1.0,1.0)
            elif mobtype == '52':
                ob.name = "spider"
                mat.diffuse_color = (0.2,0.1,0.1)
            elif mobtype == '54':
                ob.name = "zombol"
                mat.diffuse_color = (0.0,0.3,0.0)
            elif mobtype == '55':
                ob.name = "slime"
                mat.diffuse_color = (0.5,1,0.5)
            elif mobtype == '58':
                ob.name = "enderman"
                mat.diffuse_color = (0.5,0.0,0.5)
            elif mobtype == '90':
                ob.name = "pig"
                mat.diffuse_color = (0.5,0.4,0.4)
            elif mobtype == '65':
                ob.name = "bat"
                mat.diffuse_color = (1,0.5,0.2)
            elif mobtype == '91':
                ob.name = "sheep"
                mat.diffuse_color = (1,1,1)
            elif mobtype == '92':
                ob.name = "cow"
                mat.diffuse_color = (1,0.2,0.1)
            elif mobtype == '94':
                ob.name = "squid"
                mat.diffuse_color = (0.2,0.2,1)
            
            elif mobtype == '101':
                ob.name = "rabbit"
                mat.diffuse_color = (0.5,0.1,0.05)
            elif len(mobtype) > 10:
                mobtype = mobtype.replace('-','')
                request = urllib.request.urlopen('https://sessionserver.mojang.com/session/minecraft/profile/' + mobtype)
                data = request.read().decode("utf8")
                time.sleep( 1 )
                
                if len(data) > 10:
                    data = json.loads(data)
                    ob.name = "player: " + data['name']
                else:
                   
                    ob.name = "player: unknown"
                mat.diffuse_color = (1,0.6,0.4)
            else:
                mat.diffuse_color = (0.0,0.0,0.0)
                ob.name = str(mobtype)

            ob.active_material = mat

            for posses in aentity['positions'][1:]:
                frame_num = int((posses['time'] / 20) * 25)
                bpy.context.scene.frame_set(frame_num)
                ob.location =  (posses['pos'][0], posses['pos'][2], posses['pos'][1])
                
                ob.rotation_euler = ((pi * 90 / 180), 0,(pi * (posses['yawpichhead'][0]-90) / 180) )
                ob.hide = not bool(posses['alive'])
                ob.hide_render = not bool(posses['alive'])
                bpy.ops.anim.keyframe_insert(type='Location',confirm_success=False)
                bpy.ops.anim.keyframe_insert(type='Rotation',confirm_success=False)
                ob.keyframe_insert("hide")
                ob.keyframe_insert("hide_render")


        print("Script finished after {} seconds".format(time.time() - start_time))
        return {'FINISHED'}

# This is the import operator.
class MineCraftImport(bpy.types.Operator, ImportHelper):
    '''Import form minecraft netrecorder some format (.mcmo)'''
    bl_idname = "something.minecraft"
    bl_label = "MineCraft EntityPaths"
    # mc ep
    
    filename_ext = ".mcmo"
    
    filter_glob = StringProperty(
            default="*.mcmo",
            options={'HIDDEN'}
            )
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        di = DataImporter()
        return di.run(self.filepath, context)

def menu_func_export(self, context):
    self.layout.operator(MineCraftImport.bl_idname, text="Mcmo import (.mcmo)")

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