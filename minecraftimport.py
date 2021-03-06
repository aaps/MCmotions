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
# import urllib.request
import math 
import operator
import ast
try:
    import _pickle as pickle
except:
    import pickle
import os
import base64
import zlib

# from materials import *



from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

dbg = False

bl_info = {
    "name": "Minecraft motions import (*.mcmo)",
    "description": "This addon allows you to import minecraft worlds and mob motions",
    "author": "Aat Karelse",
    "version": (0, 4, 0),
    "blender": (2, 6, 3),
    #"api": ???,
    "location": "File > Import > minecraft stuff",
    "warning": "Alpha",
    "wiki_url": "https://github.com/aaps/MCmotions",
    # "tracker_url": "http://projects.blender.org/tracker/index.php?func=detail&aid=29552",
    "category": "Import-Export"}

    

# This class initiates and starts the state machine and uses the gathered data
# to construct the model in Blender.
class DataImporter:
         

    def createMeshFromData(self, material, origin, verts, faces):
        # Create mesh and object
        
        mat = bpy.data.materials.new('TexMat')



        if material in self.materials:
            themat = self.materials
        else:
            themat = {material:{'name': 'Unknown - ' + str(material), 'color': (0, 0, 0), 'alpha':0, 'emittance':0 ,'textures':[]}}

        # print(themat[material])
        if 'textures' in themat[material] and len(themat[material]['textures']) > 0:

            for texpath in themat[material]['textures']:
                mtex = mat.texture_slots.add()
                mtex.texture = self.textures[texpath]

        # print('ok' + )
        me = bpy.data.meshes.new(themat[material]['name']+' Mesh')
        ob = bpy.data.objects.new(themat[material]['name'], me)
        ob.location = origin
        if len(themat[material]) >= 2:
            mat.diffuse_color = themat[material]['color']
        if len(themat[material]) >= 3 and themat[material]['alpha'] != 0:
            mat.alpha = themat[material]['alpha']
            mat.use_transparency = True
            mat.transparency_method = 'RAYTRACE'
        if len(themat[material]) >= 4 and themat[material]['emittance'] != 0:
            mat.emit = themat[material]['emittance']


        ob.show_name = True
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
        
        handle = open(filepath, 'rb')

        total =  pickle.loads(zlib.decompress(handle.read()))
        
        indexi = 0
        
        vertices = total['vertices']
        faces = total['faces']
        entitys = total['allhistory']
        origins = total['origins']
        self.materials = total['materials']
        self.textures = total['textures']

        

        total = None

        extralist = {}

        self.tempdir = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'textures' 
        try:
            os.makedirs(self.tempdir)
        except Exception:
            print('some dir error should be ok !')

        
        filelist = [ f for f in os.listdir(self.tempdir) ]
        for f in filelist:
            try:
                os.remove(f)
            except Exception:
                print('file removal trouble no biggy')

            
        if self.textures:
            for texture in self.textures:
                fileh = open(self.tempdir + os.sep + texture + ".png", "wb")
                fileh.write(base64.b64decode(self.textures[texture]))


        temp = {}
        for material in self.materials:
            

            if 'textures' in self.materials[material] and len(self.materials[material]['textures']) > 0:
                
                for texpath in self.materials[material]['textures']:
                    
                    img = bpy.data.images.load(self.tempdir + os.sep + texpath + '.png')
                    
                    cTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
                    cTex.image = img
                    temp[texpath] = cTex
        self.textures = temp
        print(self.textures)
                    
                


        for mat in vertices:



            if mat in vertices and mat in faces and mat in origins:
                self.createMeshFromData(mat, origins[mat], vertices[mat], faces[mat] )
                faces[mat] = None
                vertices[mat] = None
            else:
                print(str(mat) + 'not in faces, vertices or origins !')


        for value in entitys:
            
            aentity = entitys[value]
            if len( aentity['positions']) > 0:
                firstloc = aentity['positions'][0]['pos']
                firstloc = firstloc[0], firstloc[1]+2,firstloc[2]
                headloc = firstloc[0],firstloc[1]+1, firstloc[2]

                bpy.ops.mesh.primitive_cube_add(location=headloc)
                
                head = bpy.context.object
                head.rotation_mode = 'XYZ'
                head.scale = (0.25, 0.25, 0.25)

                bpy.ops.mesh.primitive_cube_add(location=firstloc)

                ob = bpy.context.object
                ob.rotation_mode = 'XYZ'
                ob.scale = (0.25, 0.75, 0.25)
                
                mat = bpy.data.materials.new("PKHG")

                mobtype = aentity['type']
                if mobtype == '50':
                    ob.name = "creeper"
                    mat.diffuse_color = (0.0, 1.0, 0.0)
                elif mobtype == '51':
                    ob.name = "skeleton"
                    mat.diffuse_color = (1.0, 1.0, 1.0)
                elif mobtype == '52':
                    ob.name = "spider"
                    mat.diffuse_color = (0.2, 0.1, 0.1)
                elif mobtype == '54':
                    ob.name = "zombol"
                    mat.diffuse_color = (0.0, 0.3, 0.0)
                elif mobtype == '55':
                    ob.name = "slime"
                    mat.diffuse_color = (0.5, 1, 0.5)
                elif mobtype == '58':
                    ob.name = "enderman"
                    mat.diffuse_color = (0.5, 0.0, 0.5)
                elif mobtype == '90':
                    ob.name = "pig"
                    mat.diffuse_color = (0.5, 0.4, 0.4)
                elif mobtype == '65':
                    ob.name = "bat"
                    mat.diffuse_color = (1, 0.5, 0.2)
                elif mobtype == '91':
                    ob.name = "sheep"
                    mat.diffuse_color = (1, 1, 1)
                elif mobtype == '92':
                    ob.name = "cow"
                    mat.diffuse_color = (1, 0.2, 0.1)
                elif mobtype == '94':
                    ob.name = "squid"
                    mat.diffuse_color = (0.2, 0.2, 1)
                
                elif mobtype == '101':
                    ob.name = "rabbit"
                    mat.diffuse_color = (0.5, 0.1, 0.05)
                elif len(mobtype) > 10 or mobtype == 'player':
                    if mobtype == 'player':
                        ob.name = "player: RECORDER"
                    
                        mat.diffuse_color = (1, 0, 0)
                    else:
                        if 'type' in aentity:
                            ob.name = "player: " + aentity['type']
                        else:
                            ob.name = "player: unknown"
                        mat.diffuse_color = (1, 0.6, 0.4)

                else:
                    mat.diffuse_color = (0.0, 0.0, 0.0)
                    ob.name = str(mobtype)

                ob.active_material = mat

                bpy.ops.object.select_all(action='DESELECT')
                ob.select = True
                head.select = True
                
                put_on_layers = lambda x: tuple((i in x) for i in range(20))

                bpy.context.scene.objects.active = ob
                bpy.ops.object.parent_set()

                maincam = bpy.data.cameras.new("Camera")
                maincam.clip_start = 1
                maincam.clip_end = 5000
                cam_ob = bpy.data.objects.new("Camera", maincam)
                cam_ob.rotation_euler = (0, math.radians(180), 0)

                selfycam = bpy.data.cameras.new("Camera")
                selfycam.clip_start = 1
                selfycam.clip_end = 5000
                selfy_cam_ob = bpy.data.objects.new("Camera", selfycam)
                selfy_cam_ob.rotation_euler = (0, 0, 0)
                selfy_cam_ob.location = (0, 0, 25)
                
                selfy_cam_ob.layers[:] = put_on_layers({2})
                cam_ob.layers[:] = put_on_layers({2})
                ob.layers[:] = put_on_layers({2})
                head.layers[:] = put_on_layers({2})
                
                selfy_cam_ob.parent = head
                cam_ob.parent = head
                bpy.context.scene.objects.link(cam_ob)
                bpy.context.scene.objects.link(selfy_cam_ob)

                for posses in aentity['positions'][1:]:
                    frame_num = int((posses['time'] / 20) * 25)
                    bpy.context.scene.frame_set(frame_num)
                    ob.location = (posses['pos'][0], posses['pos'][2], posses['pos'][1]+0.75)
                    yaw = posses['yawpichhead'][1]

                    head.rotation_euler = (math.radians(posses['yawpichhead'][1]), 0, 0)
                    ob.rotation_euler = (math.radians(90), 0, math.radians(posses['yawpichhead'][0]) )
                    ob.hide = not bool(posses['alive'])
                    ob.hide_render = not bool(posses['alive'])

                    ob.keyframe_insert("hide")
                    ob.keyframe_insert("hide_render")
                    ob.keyframe_insert(data_path="location")
                    ob.keyframe_insert(data_path="rotation_euler")

                if ob.animation_data:
                    for fc in ob.animation_data.action.fcurves:
                        fc.extrapolation = 'LINEAR'
                        for kp in fc.keyframe_points:
                            kp.interpolation = 'LINEAR'

        print("Script finished after {} seconds".format(time.time() - start_time))
        return {'FINISHED'}

# This is the import operator.
class MineCraftImport(bpy.types.Operator, ImportHelper):
    '''Import form minecraft netrecorder some format (.mcmo)'''
    bl_idname = "minecraft.importminecraftdump"
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

def menu_func_import(self, context):
    self.layout.operator(MineCraftImport.bl_idname, text="Mcmo import (.mcmo)")

def register():
    bpy.utils.register_class(MineCraftImport)
    bpy.types.INFO_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(MineCraftImport)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()

    bpy.ops.something.minecraft('INVOKE_DEFAULT')