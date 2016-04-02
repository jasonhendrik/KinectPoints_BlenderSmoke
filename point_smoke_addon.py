# Credits 2015
# Jason Hendrik -> jsnhendrik@gmail.com  

# This script was developed for motion graphics production workflow in Blender
# Recording point cloud data files from the kinect and turning them into Particles, 
# Smoke Emittors, Etc... This script will import the frames into the meshData of an object.
# moving the timeline will replace the data with each frame.


# VERSION 0.11 

import bpy; 
from bpy import *; 
import bmesh;


frameCount = 398


bpy.ops.object.delete(use_global=False )

# prepare a scene
scn = bpy.context.scene
scn.frame_start = 0
scn.frame_end = frameCount
primera = 1


def ImportOneFrame(FolderPath,primera,increment):

    # create obj and add to scene
    me = bpy.data.meshes.new('points'+ str(increment)) 
    ob = bpy.data.objects.new('frame'+ str(increment), me) 
    
    ob.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(ob)   

    # for currentFrame in range(1):
    file = FolderPath
    mydata = {} 
    vertexdata = []
    facedata = []
    counter=0
    c= 0
    
    # Vertex  (some credits missing here)
    for line in file.readlines():
        
        mydata[c] = line.split(',');
        
        rX = float(mydata[c][1])-50; 
        rY = float(mydata[c][2])-100;
        rZ = float(mydata[c][3])-650;
        
        nextVertex = rX/10,rZ/10,-rY/10
        vertexdata.append(nextVertex);
        
        c=c+1
       
    for i in range(0, c-55):
        
        mydata[counter] = line.split(',');
        
        ap = counter
        bp = counter+1
        cp = counter+54
        dp = counter+55
        
        if (float(mydata[ap][1]) > 0 and float(mydata[bp][1]) > 0 and float(mydata[cp][1]) > 0) or (float(mydata[ap][2]) > 0 and float(mydata[bp][2]) > 0 and float(mydata[cp][3]) > 0) or (float(mydata[ap][3]) and float(mydata[bp][3]) > 0 and float(mydata[cp][3])):
            nextFace = bp,cp,ap
            facedata.append(nextFace);
        if (float(mydata[dp][1]) > 0 and float(mydata[bp][1]) > 0 and float(mydata[cp][1]) > 0) or (float(mydata[dp][2]) > 0 and float(mydata[bp][2]) > 0 and float(mydata[cp][3]) > 0) or (float(mydata[dp][3]) and float(mydata[bp][3]) > 0 and float(mydata[cp][3])):
            nextFace =dp,cp,bp
            facedata.append(nextFace);
        
        counter=counter+1
    
    bpy.context.scene.frame_set(increment)
    
    if primera == 1:
        me.from_pydata(vertexdata,[], facedata)
        me.update(calc_edges=True)          
        primera = 0
    else:
        
        ob.keyframe_insert(data_path="hide_render", frame=increment) 
        bpy.ops.anim.keyframe_insert(type='shape', confirm_success=True)
        c = 0;
        f= 0;
        for vert in ob.data.vertices:
            vert.keyframe_insert("co", frame=increment-1)
            
            nX = float(mydata[c][1])-50; 
            nY = float(mydata[c][2])-100;
            nZ = float(mydata[c][3])-650;      
            
            pVertex = nX/10,nZ/10,-nY/10
            if float(mydata[c][1]) > 0 and float(mydata[c][2]) > 0 and float(mydata[c][3]) > 0:
                vert.co = pVertex
            else:
                vert.co = vert.co
            
            vert.keyframe_insert("co", frame=increment)
            
            c = c+1
     
    #file.close()
                  
    # animate
    ob.hide = True
    ob.hide_render = True   
    ob.keyframe_insert(data_path="hide", frame=0) 
    ob.keyframe_insert(data_path="hide_render", frame=0)     
    ob.hide = False 
    ob.hide_render = False   
    ob.keyframe_insert(data_path="hide", frame=increment)
    ob.keyframe_insert(data_path="hide_render", frame=increment)    
    ob.hide = True
    ob.hide_render = True    
    ob.keyframe_insert(data_path="hide", frame=increment+1) 
    ob.keyframe_insert(data_path="hide_render", frame=increment+1)        
   
    #move timeline to keyframe
    bpy.context.scene.frame_current = increment      
   
    #select one object
    bpy.ops.object.select_all(action='DESELECT')
    myobject = bpy.data.objects['frame'+str(increment)]    
    myobject.select = True
    bpy.context.scene.objects.active = myobject
       
    #begin material
    
    mat = bpy.data.materials.new('PointCloud')     
    mat = bpy.data.materials[-1]
    obj = bpy.context.active_object       
    obj.active_material = mat   
    mat.type = 'HALO'
    mat.alpha = 0
        
    bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
   
    #output to console   
    print("Imported frame " + str(increment))
    
    #select one object
    bpy.ops.object.select_all(action='DESELECT')
    myobject = bpy.data.objects['frame'+ str(increment)]    
    myobject.select = False    
    


#MAIN PROGRAM

for increment in range (frameCount):   
    #Replace this folder-path with the folder containing your kinect recordings from "OFKinectRecorder" or Similar Process
    FolderPath = open('/Users/jasonhendrik/Google Drive/personal_projects/smoke_tests/data/guitar/'+ 'frame' + str(increment) +'.txt','r')    
    ImportOneFrame(FolderPath, primera, increment);    

#create placeholder object
bpy.ops.mesh.primitive_cube_add(radius=0, view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.context.object.name = "animation"

#Add Smoke Particles (for Viewing Too)
bpy.ops.object.particle_system_add()
bpy.data.particles["ParticleSettings"].name = "smoke_emittors"

bpy.data.particles["smoke_emittors"].count = (100000)
bpy.data.particles["smoke_emittors"].frame_start = scn.frame_start
bpy.data.particles["smoke_emittors"].frame_end =  scn.frame_end 
bpy.data.particles["smoke_emittors"].lifetime = 4
bpy.data.particles["smoke_emittors"].emit_from = 'VERT'


def mesh_update(scene):
       
       
    #needs to only update mesh named "animation"
    # even when not selected...
    # issues here need afix
    
    
    bpy.data.objects['animation'].data = bpy.data.meshes.get("points%i" % scene.frame_current)  
    #bpy.context.object.data = bpy.data.meshes.get("points%i" % scene.frame_current)    
    
    

bpy.app.handlers.frame_change_pre.append(mesh_update)
    
