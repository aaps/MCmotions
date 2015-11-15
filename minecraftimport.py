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
import math 
import operator
import ast


from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

dbg = False

bl_info = {
    "name": "Minecraft mejiggest (*.mcmo)",
    "description": "This addon allows you to import minecraft worls and mob motions",
    "author": "Aat Karelse",
    "version": (0, 3, 0),
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

    def createRightStandardColor(self, material):
        mat = bpy.data.materials.new("PKHG")
        if material[1] == 0:
            color = (1,1,1)
        elif material[1] == 1:
            color = (1, 0.54902, 0)
        elif material[1] == 2:
            color = (0.6, 0.196078, 0.8)
        elif material[1] == 3:
            color = (0.690196, 0.878431, 0.901961)
        elif material[1] == 4:
            color = (1,1,0)
        elif material[1] == 5:
            color = (0.196078, 0.803922, 0.196078)
        elif material[1] == 6:
            color = (1, 0.411765, 0.705882)
        elif material[1] == 7:
            color = (0.411765, 0.411765, 0.411765)
        elif material[1] == 8:
            color = (0.745098, 0.745098, 0.745098)
        elif material[1] == 9:
            color = (0, 0.545098, 0.545098)
        elif material[1] == 10:
            color = (0.627451, 0.12549, 0.941176)
        elif material[1] == 11:
            color = (0, 0, 0.803922)
        elif material[1] == 12:
            color = (0.545098, 0.270588, 0.0745098)
        elif material[1] == 13:
            color = (0, 0.392157, 0)
        elif material[1] == 14:
            color = (1,0,0)
        elif material[1] == 15:
            color = (0,0,0)
        return color


    def createRightStoneSlabColor(self, material):
        mat = bpy.data.materials.new("PKHG")
        if material[1] in [0,8]:
            color = (0.662745, 0.662745, 0.662745)
        elif material[1] in [1,9]:
            color = (1, 0.980392, 0.803922)
        elif material[1] in [2,10]:
            color = (0.803922, 0.521569, 0.247059)
        elif material[1] in [3,11]:
            color = (0.517647, 0.517647, 0.517647)
        elif material[1] in [4,12]:
            color = (0.545098, 0, 0)
        elif material[1] in [5,13]:
            color = (0.562745, 0.562745, 0.562745)
        elif material[1] in [6,14]:
            color = (0.545098, 0, 0)
        elif material[1] in [7,15]:
            color = (1,1,1)
        else:
            color = (0,0,0)
        return color

    def createRightWoodeSlabColor(self, material):
        mat = bpy.data.materials.new("PKHG")
        if material[1] in [0,6]:
            color = (0.933333, 0.909804, 0.666667)
        elif material[1] in [1,7]:
            color = (0.803922 ,0.521569, 0.247059)
        elif material[1] in [2,8]:
            color = (0.980392, 0.980392, 0.823529)
        elif material[1] in [3,9]:
            color = (1, 0.627451, 0.478431)
        elif material[1] in [4,10]:
            color = (1, 0.388235, 0.278431)
        elif material[1] in [5,11]:
            color = (0.545098, 0.270588, 0.0745098)
        else:
            color = (0,0,0)
        return color

    def createRightSaplingColor(self, material):
        mat = bpy.data.materials.new("PKHG")
        if material[1] == 0:
            color = (0.486275, 0.988235, 0)
        elif material[1] == 1:
            color = (0.419608, 0.556863, 0.137255)
        elif material[1] == 2:
            color = (0.486275, 0.988235, 0)
        elif material[1] == 3:
            color = (0, 0.392157, 0)
        elif material[1] == 4:
            color = (0.603922, 0.803922, 0.196078)
        elif material[1] == 5:
            color = (0.133333, 0.545098, 0.133333)
        else:
            color = (0,0,0)
        return color

    # def createRightFlowerColor(self, material):
    #     mat = bpy.data.materials.new("PKHG")
    #     if material[1] == 0:
    #         color = (1,1,1)
    #     elif material[1] == 1:
    #         color = (1, 0.54902, 0)
    #     elif material[1] == 2:
    #         color = (0.6, 0.196078, 0.8)
    #     elif material[1] == 3:
    #         color = (0.690196, 0.878431, 0.901961)
    #     elif material[1] == 4:
    #         color = (1,1,0)
    #     elif material[1] == 5:
    #         color = (0.196078, 0.803922, 0.196078)
    #     elif material[1] == 6:
    #         color = (1, 0.411765, 0.705882)
    #     elif material[1] == 7:
    #         color = (0.411765, 0.411765, 0.411765)
    #     elif material[1] == 8:
    #         color = (0.745098, 0.745098, 0.745098)
    #     elif material[1] == 9:
    #         color = (0, 0.545098, 0.545098)
    #     elif material[1] == 10:
    #         color = (0.627451, 0.12549, 0.941176)
    #     elif material[1] == 11:
    #         color = (0, 0, 0.803922)
    #     elif material[1] == 12:
    #         color = (0.545098, 0.270588, 0.0745098)
    #     elif material[1] == 13:
    #         color = (0, 0.392157, 0)
    #     elif material[1] == 14:
    #         color = (1,0,0)
    #     elif material[1] == 15:
    #         color = (0,0,0)
    #     return color
         
         
         

    def createMeshFromData(self, material, origin, verts, faces):
        # Create mesh and object
        me = bpy.data.meshes.new(str(material)+'Mesh')
        ob = bpy.data.objects.new(str(material), me)

        ob.show_name = True
        
        mat = bpy.data.materials.new("PKHG")
        # print(material)
        if material[0] == 9:
            mat.diffuse_color = (0,0,1)
            mat.alpha = 0.5
            mat.use_transparency = True
            mat.transparency_method = 'RAYTRACE'
        elif material[0] == 1:
            mat.diffuse_color = (0.7,0.7,0.7)
        elif material[0] == 3:
            mat.diffuse_color = (0.9,0.7,0.6)
        elif material[0] == 6:  
            mat.diffuse_color = self.createRightSaplingColor(material)
        elif material[0] == 7:
            mat.diffuse_color = (0.2,0.2,0.2)
        elif material[0] in [11, 10]:
            mat.diffuse_color = (0.9,0.2,0.2)
            mat.emit = 5
        elif material[0] in [13]:
            mat.diffuse_color = (0.5,0.5,0.5)
        elif material[0] == 15:
            mat.diffuse_color = (0.6,0.5,0.4)
        elif material[0] == 16:
            mat.diffuse_color = (0.4,0.4,0.4)
        elif material[0] in [5, 125, 126]:
            mat.diffuse_color = self.createRightWoodeSlabColor(material)
            
        elif material[0] in [18,2,111, 31]:
            mat.diffuse_color = (0,0.8,0)
        elif material[0] in [12,24] :
            mat.diffuse_color = (1,0.8,0.7)
        elif material[0] == 49:
            mat.diffuse_color = (0,0,0.2)
        elif material[0] in [44, 43]:
            mat.diffuse_color = self.createRightStoneSlabColor(material)
            # mat.diffuse_color = (0.8,0.8,0.8)
        elif material[0] in [80, 78]:
            mat.diffuse_color = (1,1,1)
        elif material[0] == 79:
            mat.diffuse_color = (0.4,0.4,1)
            mat.alpha = 0.2
            mat.use_transparency = True
            mat.transparency_method = 'RAYTRACE'
        elif material[0] in [89, 50, 124, 91, 51, 62] :
            mat.diffuse_color = (0.9,0.9,0.2)
            mat.emit = 5
        elif material[0] == 119:
            mat.diffuse_color = (0.627451, 0.12549, 0.941176)
        elif material[0] == 138:
            mat.diffuse_color = (0.6,0.6,1)
            mat.emit = 5
        elif material[0] == 144:
            mat.diffuse_color = (0.745098, 0.745098, 0.745098)
        elif material[0] in [152]:
            mat.diffuse_color = (1,0,0)
        elif material[0] in [155, 156]:
            mat.diffuse_color = (1,1,1)
        elif material[0] in [174]:
            mat.diffuse_color = (0.7,0.7,1)
        elif material[0] in [171, 35, 159]:
            mat.diffuse_color = self.createRightStandardColor(material)
        elif material[0] in [95, 160]:
            mat.diffuse_color = self.createRightStandardColor(material)
            mat.alpha = 0.5
            mat.use_transparency = True
            mat.transparency_method = 'RAYTRACE'

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
            if len( aentity['positions']) > 0:
                firstloc = aentity['positions'][0]['pos']
                firstloc = firstloc[0], firstloc[1]+2,firstloc[2]
                headloc = firstloc[0],firstloc[1]+1, firstloc[2]

                bpy.ops.mesh.primitive_cube_add(location=headloc)
                
                head = bpy.context.object
                head.rotation_mode = 'XYZ'
                head.scale = (0.25,0.25,0.25)



                bpy.ops.mesh.primitive_cube_add(location=firstloc)

                
                ob = bpy.context.object
                ob.rotation_mode = 'XYZ'
                ob.scale = (0.25,0.75,0.25)
                


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
                elif len(mobtype) > 10 or mobtype == 'player':
                    if mobtype == 'player':
                        ob.name = "player: RECORDER"
                    

                        mat.diffuse_color = (1,0,0)
                    else:
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
                cam_ob.rotation_euler = (0, math.radians(180),  0)

                selfycam = bpy.data.cameras.new("Camera")
                selfycam.clip_start = 1
                selfycam.clip_end = 5000
                selfy_cam_ob = bpy.data.objects.new("Camera", selfycam)
                selfy_cam_ob.rotation_euler = (0, 0,  0)
                selfy_cam_ob.location = (0,0,25)
                
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

                    head.rotation_euler = (math.radians(posses['yawpichhead'][1]),0,0)
                    ob.rotation_euler = (math.radians(90), 0, math.radians(posses['yawpichhead'][0]) )
                    ob.hide = not bool(posses['alive'])
                    ob.hide_render = not bool(posses['alive'])

                    
                    ob.keyframe_insert("hide")
                    ob.keyframe_insert("hide_render")
                    ob.keyframe_insert(data_path="location")
                    ob.keyframe_insert(data_path="rotation_euler")

                for fc in ob.animation_data.action.fcurves:
                    fc.extrapolation = 'LINEAR'
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'LINEAR'



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