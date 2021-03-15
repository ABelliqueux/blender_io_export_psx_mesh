# bpy. app. debug = True 
 
bl_info = {
    "name":         "PSX TMesh exporter",
    "author":       "Schnappy, TheDukeOfZill",
    "blender":      (2,7,9),
    "version":      (0,0,2),
    "location":     "File > Import-Export",
    "description":  "Export psx data format",
    "category":     "Import-Export"
}

import os

import bpy

import bmesh

import unicodedata

from math import radians, degrees, floor, cos, sin 

from mathutils import Vector

from collections import defaultdict

from bpy.props import (CollectionProperty,
                       StringProperty,
                       BoolProperty,
                       EnumProperty,
                       FloatProperty
                       )

from bpy_extras.io_utils import (ExportHelper,
                                 axis_conversion
                                 )
 
class ExportMyFormat(bpy.types.Operator, ExportHelper):

    bl_idname       = "export_psx.c";

    bl_label        = "PSX compatible scene exporter";

    bl_options      = {'PRESET'};

    filename_ext    = ".c";
    
    exp_Triangulate = BoolProperty(

        name="Triangulate meshes ( Destructive ! )",

        description="Triangulate meshes (destructive ! Do not use your original file)",

        default=False,
    )
    
    exp_Scale = FloatProperty(

        name="Scale",

        description="Scale of exported mesh.",

        min=1, max=1000,

        default=65,

        )
    
    exp_Precalc = BoolProperty(

        name="Use precalculated BGs",

        description="Set the BGs UV to black",

        default=False,
    )
    
    def execute(self, context):

        def triangulate_object(obj): 
            
            # Triangulate an object's mesh
            # Source : https://blender.stackexchange.com/questions/45698/triangulate-mesh-in-python/45722#45722
            
            me = obj.data
            
            # Get a BMesh representation
            bm = bmesh.new()
            
            bm.from_mesh(me)
            
            bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method=0, ngon_method=0)
            
            # Finish up, write the bmesh back to the mesh
            bm.to_mesh(me)
            
            bm.free()
        
        def CleanName(strName):
            
            # Removes specials characters, dots ans space from string
            
            name = strName.replace(' ','_')
            
            name = name.replace('.','_')
            
            name = unicodedata.normalize('NFKD',name).encode('ASCII', 'ignore').decode()
            
            return name

        def isInPlane(plane, obj):
    
            # Checks  if 'obj' has its coordinates contained between the plane's coordinate.
            # If 'obj' is partly contained, returns which side (S, W, N, E) it's overlapping.
            # If 'obj' is not contained in 'plane', returns 0.
            
            if (   
                 (LvlPlanes[plane]['x1'] < LvlObjects[obj]['x1'] and LvlPlanes[plane]['x2'] > LvlObjects[obj]['x2']) and
                 (LvlPlanes[plane]['y1'] < LvlObjects[obj]['y1'] and LvlPlanes[plane]['y2'] > LvlObjects[obj]['y2']) 
               ):
                
                return 1
                
            # Overlap on the West side of the plane
            if ( 
                 ( LvlPlanes[plane]['x1'] > LvlObjects[obj]['x1'] and LvlPlanes[plane]['x1'] < LvlObjects[obj]['x2'] ) and 
                 ( LvlPlanes[plane]['y1'] < LvlObjects[obj]['y1'] and LvlPlanes[plane]['y2'] > LvlObjects[obj]['y2'] ) 
               ):
                
                return 4
            
            # Overlap on the East side of the plane
            if ( 
                 ( LvlPlanes[plane]['x2'] < LvlObjects[obj]['x2'] and LvlPlanes[plane]['x2'] > LvlObjects[obj]['x1'] ) and 
                 ( LvlPlanes[plane]['y1'] < LvlObjects[obj]['y1'] and LvlPlanes[plane]['y2'] > LvlObjects[obj]['y2'] ) 
               ):
                
                return 6
                
            # Overlap on the North side of the plane
            if ( 
                 ( LvlPlanes[plane]['y2'] < LvlObjects[obj]['y2'] and LvlPlanes[plane]['y2'] > LvlObjects[obj]['y1'] ) and 
                 ( LvlPlanes[plane]['x1'] < LvlObjects[obj]['x1'] and LvlPlanes[plane]['x2'] > LvlObjects[obj]['x2'] )  
               ): 

                return 8
            
            # Overlap on the South side of the plane
            if ( 
                 ( LvlPlanes[plane]['y1'] > LvlObjects[obj]['y1'] and LvlPlanes[plane]['y1'] < LvlObjects[obj]['y2'] ) and 
                 ( LvlPlanes[plane]['x1'] < LvlObjects[obj]['x1'] and LvlPlanes[plane]['x2'] > LvlObjects[obj]['x2'] )
               ):
                
                return 2

            else:
                
                return 0
            
        def getSepLine(plane, side):
            
            # Construct the line used for BSP generation from 'plane' 's coordinates, on specified side (S, W, N, E)
            # Returns an array of 3 values
            
            if side == 'S':
                
                return [ LvlPlanes[plane]['x1'], LvlPlanes[plane]['y1'], LvlPlanes[plane]['x2'], LvlPlanes[plane]['y1'] ]
                
            if side == 'N':
                
                return [ LvlPlanes[plane]['x1'], LvlPlanes[plane]['y2'], LvlPlanes[plane]['x2'], LvlPlanes[plane]['y2'] ]
                        
            if side == 'W':
                
                return [ LvlPlanes[plane]['x1'], LvlPlanes[plane]['y1'], LvlPlanes[plane]['x1'], LvlPlanes[plane]['y2'] ]
                
            if side == 'E':
                
                return [ LvlPlanes[plane]['x2'], LvlPlanes[plane]['y1'], LvlPlanes[plane]['x2'], LvlPlanes[plane]['y2'] ]

        def checkLine(lineX1, lineY1 ,lineX2 ,lineY2, objX1, objY1, objX2, objY2):

            # Returns wether object spanning from objXY1 to objXY2 is Back, Front, Same or Intersecting the line 
            # defined by points (lineXY1, lineXY2)
                
            val1 = ( objX1 - lineX1 ) * ( lineY2-lineY1 ) - ( objY1 - lineY1 ) * ( lineX2 - lineX1 )
            
            # rounding to avoid false positives
            
            val1 = round(val1, 4)
            
            val2 = ( objX2 - lineX1 ) * ( lineY2-lineY1 ) - ( objY2 - lineY1 ) * ( lineX2 - lineX1 )
            
            val2 = round(val2, 4)
            
            if ( (val1 > 0) and (val2 > 0) ):
                
                return "front"
                
            elif ( (val1 < 0) and (val2 < 0) ):
                
                return "back"
                
            elif ( (val1 == 0) and (val2 == 0) ):
                
                return "connected"
                
            elif ( 
                    ( (val1>0) and (val2==0) ) or 
                    ( (val1==0) and (val2>0) ) 
                 ):
                
                return "front"
                
            elif ( 
                    ( (val1<0) and (val2==0) ) or 
                    ( (val1==0) and (val2<0) ) 
                 ):
                
                return "back"
                
            elif ( 
                   ( (val1<0) and (val2>0) ) or
                   ( (val1>0) and (val2<0) ) 
                 ):
                
                return "intersect"

        # Leave edit mode to avoid errors

        bpy.ops.object.mode_set(mode='OBJECT')

        # If set, triangulate objects of type mesh 

        if self.exp_Triangulate:

            for o in range(len(bpy.data.objects)):

                if bpy.data.objects[o].type == 'MESH':

                    triangulate_object(bpy.data.objects[o])
                    
        # Set Scale 
        
        scale = self.exp_Scale
        
        # Get working directory path
        
        filepath = bpy.data.filepath
        
        folder = os.path.dirname(bpy.path.abspath(filepath))
        
        dirpath = os.path.join(folder, "TIM")
        
    ### Export pre-calculated backgrounds 
        
        camAngles = []
        
        defaultCam = 'NULL'

        # If using precalculated BG, render and export them to ./TIM/
        
        if self.exp_Precalc:
            
            # Create folder if it doesn't exist
            
            os.makedirs(dirpath, exist_ok = 1)
            
            # Set file format config
            
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.image_settings.quality = 100
            bpy.context.scene.render.image_settings.compression = 0
            bpy.context.scene.render.image_settings.color_depth = '8'
            
            # Get active cam
            
            cam = bpy.context.scene.camera
            
            # Find default cam, and cameras in camPath
            
            for o in bpy.data.objects:

                if o.type == 'CAMERA' and o.data.get('isDefault'):

                    defaultCam = o.name
                    
                if o.type == 'CAMERA' and o.name.startswith("camPath"):
                    
                    # Set camera as active

                    bpy.context.scene.camera = o
                    
                    # Render and save image
                    
                    bpy.ops.render.render()
                    
                    bpy.data.images["Render Result"].save_render(folder + os.sep + "TIM" + os.sep + "bg_" + CleanName(o.name) + "." + str(bpy.context.scene.render.image_settings.file_format).lower())
                    
                    # Add camera object to camAngles
                    
                    camAngles.append(o)
        
        
### Start writing output file
        
        # Open file
        
        f = open(os.path.normpath(self.filepath),"w+")
        
    ## Add C structures definitions
        
        # BODY
        
        f.write("typedef struct {\n" +
                "\tVECTOR  gForce;\n" +
                "\tVECTOR  position;\n" +
                "\tSVECTOR velocity;\n" +
                "\tint     mass;\n" +
                "\tint     invMass;\n" +
                "\tVECTOR  min; \n" +
                "\tVECTOR  max; \n" +
                "\tint     restitution; \n" +
                "\t} BODY;\n\n")
        
        # VANIM
        
        f.write("typedef struct { \n" +
                "\tint nframes;    // number of frames e.g   20\n" +
                "\tint nvert;      // number of vertices e.g 21\n" +
                "\tint cursor;     // anim cursor\n" +
                "\tint lerpCursor; // anim cursor\n" +
                "\tint dir;        // playback direction (1 or -1)\n" +
                "\tint interpolate; // use lerp to interpolate keyframes\n" +
                "\tSVECTOR data[]; // vertex pos as SVECTORs e.g 20 * 21 SVECTORS\n" +
                # ~ "\tSVECTOR normals[]; // vertex pos as SVECTORs e.g 20 * 21 SVECTORS\n" +
                "\t} VANIM;\n\n")
                
        # PRIM
        
        f.write("typedef struct {\n" +
                "\tVECTOR order;\n" +
                "\tint    code; // Same as POL3/POL4 codes : Code (F3 = 1, FT3 = 2, G3 = 3, GT3 = 4) Code (F4 = 5, FT4 = 6, G4 = 7, GT4 = 8)\n" +
                "\t} PRIM;\n\n")
        
        # MESH
        
        f.write("typedef struct {  \n"+
                "\tTMESH   *    tmesh;\n" +
                "\tPRIM    *    index;\n" +
                "\tTIM_IMAGE *  tim;  \n" + 
                "\tunsigned long * tim_data;\n"+
                "\tMATRIX  *    mat;\n" + 
                "\tVECTOR  *    pos;\n" + 
                "\tSVECTOR *    rot;\n" +
                "\tshort   *    isRigidBody;\n" +
                "\tshort   *    isStaticBody;\n" +
                "\tshort   *    isPrism;\n" +
                "\tshort   *    isAnim;\n" +
                "\tshort   *    isActor;\n" +
                "\tshort   *    isLevel;\n" +
                "\tshort   *    isBG;\n" +
                "\tlong    *    p;\n" + 
                "\tlong    *    OTz;\n" + 
                "\tBODY    *    body;\n" + 
                "\tVANIM   *    anim;\n" + 
                "\t} MESH;\n\n")
        
        # CAMPOS
        
        f.write("typedef struct {\n" +
                "\tVECTOR  pos;\n" +
                "\tSVECTOR rot;\n" + 
                "\t} CAMPOS;\n\n" +
                "\n// Blender cam ~= PSX cam with these settings : NTSC - 320x240, PAL 320x256, pixel ratio 1:1, cam focal length : perspective 90° ( 16 mm ))\n\n")
        
        # CAMANGLE
        
        f.write("typedef struct {\n" +
                "\tCAMPOS    * campos;\n" +
                "\tTIM_IMAGE * BGtim;\n" +
                "\tunsigned long * tim_data;\n" +
                "\t} CAMANGLE;\n\n")
                
        # CAMPATH
        
        f.write("typedef struct {\n" +
                "\tshort len, cursor, pos;\n" +
                "\tVECTOR points[];\n" +
                "\t} CAMPATH;\n\n")

        # PARENTNODE
        
        f.write("typedef struct {\n" +
                "\tint index;\n" +
                "\tMESH * siblings[];\n" +
                "\t} PARENTNODE ;\n\n")
    
        # CHILDNODE

        f.write("typedef struct {\n" +
                "\tint index;\n" +
                "\tMESH * children[];\n" + 
                "\t} CHILDNODE ;\n\n")
        
        # NODE

        f.write("typedef struct {\n" +
                "\tMESH * curPlane;\n" +
                "\tPARENTNODE * siblings;\n" + 
                "\tCHILDNODE * objects;\n" + 
                "\t} NODE;\n\n")

    ## Camera setup

        # List of points defining the camera path

        camPathPoints = []

        # Define first mesh. Will be used as default if no properties are found in meshes
        
        first_mesh = CleanName(bpy.data.meshes[0].name)

        # Set camera position and rotation in the scene
        
        for o in range(len(bpy.data.objects)):
            if bpy.data.objects[o].type == 'CAMERA' and bpy.data.objects[o].data.get('isDefault'):
                defaultCam = bpy.data.objects[o].name
            if bpy.data.objects[o].type == 'CAMERA':
                f.write("CAMPOS camPos_" + CleanName(bpy.data.objects[o].name) + " = {\n" +
                "\t{" + str(round(-bpy.data.objects[o].location.x * scale)) + "," + str(round(bpy.data.objects[o].location.z * scale)) + "," +str(round(-bpy.data.objects[o].location.y * scale)) + "},\n" +
                "\t{" + str(round(-(degrees(bpy.data.objects[o].rotation_euler.x)-90)/360 * 4096)) + "," + str(round(degrees(bpy.data.objects[o].rotation_euler.z)/360 * 4096)) + "," + str(round(-(degrees(bpy.data.objects[o].rotation_euler.y))/360 * 4096)) + "}\n" +
                "};\n\n")
                
        # Find camera path points and append them to camPathPoints[]
        
            if bpy.data.objects[o].type == 'CAMERA' :
                if bpy.data.objects[o].name.startswith("camPath") and not bpy.data.objects[o].data.get('isDefault'):
                    camPathPoints.append(bpy.data.objects[o].name)
        
        # Write the CAMPATH structure
        
        if camPathPoints:
            
            # Populate with points found above
            
            # ~ camPathPoints = list(reversed(camPathPoints))
            
            for p in range(len(camPathPoints)):
                if p == 0:
                    f.write("CAMPATH camPath = {\n" +
                            "\t" + str(len(camPathPoints)) + ",\n" +
                            "\t0,\n" +
                            "\t0,\n" +
                            "\t{\n")
                f.write("\t\t{" + str(round(-bpy.data.objects[camPathPoints[p]].location.x * scale)) + "," + str(round(bpy.data.objects[camPathPoints[p]].location.z * scale)) + "," +str(round(-bpy.data.objects[camPathPoints[p]].location.y * scale)) + "}")
                if p != len(camPathPoints) - 1:
                    f.write(",\n")  
            f.write("\n\t}\n};\n\n")
        
        else:
            
            # If no camera path points are found, use default
            
            f.write("CAMPATH camPath = {\n" +
                            "\t0,\n" +
                            "\t0,\n" +
                            "\t0\n"  +
                            "};\n\n")        
        
    ## Lighting setup 
    
        # Light sources will be similar to Blender's sunlamp
        # A maximum of 3 light sources will be used
        
        # LLM : Local Light Matrix   
          
        if len(bpy.data.lamps) is not None:
            
            # ~ f.write( "static MATRIX lgtmat = {\n" +
                     # ~ "\t 4096, 4096, 4096,\n" +
                     # ~ "\t -4096, 4096, 4096,\n" +
                     # ~ "\t -4096, 4096, -4096\n" +
                     # ~ "};\n")
                     
            cnt = 0
            pad = 3 - len(bpy.data.lamps)
            
            f.write( "static MATRIX lgtmat = {\n")
            
            for l in range(len(bpy.data.lamps)):

                # Lightsource energy
                
                energy   = int(bpy.data.lamps[l].energy * 4096)
                
                # Get lightsource's world orientation
                
                lightdir = bpy.data.objects[bpy.data.lamps[l].name].matrix_world * Vector((0,0,-1,0))
                
                f.write( 
                    "\t" + str(int(lightdir.x * energy)) + "," + 
                    "\t" + str(int(-lightdir.z * energy)) + "," +
                    "\t" + str(int(lightdir.y * energy))  
                    )
                    
                if l != len(bpy.data.lamps) - 1:
                    f.write(",\n")
                
                # If less than 3 light sources exist in blender, fill the matrix with 0s.                
                
                if pad:
                    f.write(",\n")
                    while cnt < pad:
                        f.write("\t0,0,0")
                        if cnt != pad:
                            f.write(",\n")
                        cnt += 1
            
            f.write("\n\t};\n\n")
        
            # LCM : Local Color Matrix
            
            f.write( "static MATRIX cmat = {\n")
            
            LCM = []
            for l in bpy.data.lamps:
                LCM.append(str(int(l.color.r * 4096) if l.color.r else 0))
                LCM.append(str(int(l.color.g * 4096) if l.color.g else 0))
                LCM.append(str(int(l.color.b * 4096) if l.color.b else 0))
            
            if len(LCM) < 9:
                while len(LCM) < 9:
                    LCM.append('0')

            # Write LC matrix

            f.write(
                "\t" + LCM[0] + "," + LCM[3] + "," + LCM[6] + ",\n" +
                "\t" + LCM[1] + "," + LCM[4] + "," + LCM[7] + ",\n" +
                "\t" + LCM[2] + "," + LCM[5] + "," + LCM[8] + "\n" )
            f.write("\t};\n\n")
    
    ## Meshes 
    
        actorPtr = first_mesh
        levelPtr = first_mesh
        propPtr = first_mesh
        nodePtr = first_mesh
        
        timList = []
        
        for m in bpy.data.meshes:
 
            # Store vertices coordinates by axis to find max/min coordinates
            
            Xvals = []
            Yvals = []
            Zvals = []
 
            cleanName = CleanName(m.name)

            # Write vertices vectors
 
            f.write("SVECTOR "+"model"+cleanName+"_mesh[] = {\n")

            for i in range(len(m.vertices)):
                
                v = m.vertices[i].co
                
                # Append vertex coords to lists
                
                Xvals.append(v.x)
                Yvals.append(v.y)
                Zvals.append(-v.z)
                
                f.write("\t{"+str(round(v.x*scale))+","+str(round(-v.z*scale)) + "," + str(round(v.y*scale)) +"}")
                
                if i != len(m.vertices) - 1:
                    f.write(",")
                f.write("\n")
            f.write("};\n\n")
            
            # Write normals vectors
 
            f.write("SVECTOR "+"model"+cleanName+"_normal[] = {\n")
            for i in range(len(m.vertices)):
                poly = m.vertices[i]
                f.write("\t"+str(round(-poly.normal.x * 4096))+","+str(round(poly.normal.z  * 4096))+","+str(round(-poly.normal.y  * 4096))+",0")
                if i != len(m.vertices) - 1:
                    f.write(",")
                f.write("\n")
            f.write("};\n\n")
 
            # Write UVs vectors if a texture exists
            
            # get name of texture image https://docs.blender.org/api/2.79b/bpy.types.Image.html#bpy.types.Image
            # bpy.context.active_object.data.uv_textures.active.data[0].image.name
            # bpy.context.active_object.data.uv_textures.active.data[0].image.filepath
            # bpy.context.active_object.data.uv_textures.active.data[0].image.filepath_from_user()
            #
            # get image size x, y
            # print(bpy.data.meshes[0].uv_textures[0].data[0].image.size[0]) # x
            # print(bpy.data.meshes[0].uv_textures[0].data[0].image.size[1]) # y
            
                
            if len(m.uv_textures) != None:
 
                for t in range(len(m.uv_textures)):
 
                    if m.uv_textures[t].data[0].image != None:
 
                        f.write("SVECTOR "+"model"+cleanName+"_uv[] = {\n")
 
                        texture_image = m.uv_textures[t].data[0].image
 
                        tex_width = texture_image.size[0]
 
                        tex_height = texture_image.size[1]
 
                        uv_layer = m.uv_layers[0].data
 
                        for i in range(len(uv_layer)):
 
                            u = uv_layer[i].uv
 
                            ux = u.x * tex_width
 
                            uy = u.y * tex_height
 
                            # ~ if self.exp_Precalc and m.get('isBG'):
                                # ~ f.write("\t255, 255, 0, 0") # Clamp values to 0-255 to avoid tpage overflow
                            # ~ else:
 
                            f.write("\t"+str(max(0, min( round(ux) , 255 )))+","+str(max(0, min(round(tex_height - uy) , 255 )))+", 0, 0") # Clamp values to 0-255 to avoid tpage overflow
 
                            if i != len(uv_layer) - 1:
 
                                f.write(",")
 
                            f.write("\n")
 
                        f.write("};\n\n")
                        
                        # Save UV texture to a file in ./TIM
                        # It will have to be converted to a tim file

                        if texture_image.filepath == '':

                            os.makedirs(dirpath, exist_ok = 1)

                            texture_image.filepath_raw = folder + os.sep + "TIM" + os.sep + CleanName(texture_image.name) + "." + texture_image.file_format

                        texture_image.save()
                        
            # Write vertex colors vectors
 
            f.write("CVECTOR "+"model"+cleanName+"_color[] = {\n")
             
            # If vertex colors exist, use them
            
            if len(m.vertex_colors) != 0:           
            
                colors = m.vertex_colors[0].data
            
                for i in range(len(colors)):
            
                    f.write("\t"+str(int(colors[i].color.r*255))+","+str(int(colors[i].color.g*255))+","+str(int(colors[i].color.b*255))+", 0")
            
                    if i != len(colors) - 1:
            
                        f.write(",")
            
                    f.write("\n")
            
            # If no vertex colors, default to 2 whites, 1 grey
            
            else:                                  
            
                for i in range(len(m.polygons) * 3):
            
                    if i % 3 == 0:
            
                        f.write("\t80,80,80,0")
            
                    else:
            
                        f.write("\t128,128,128,0")
            
                    if i != (len(m.polygons) * 3) - 1:
            
                        f.write(",")
            
                    f.write("\n")
            
            f.write("};\n\n")
            
            # Write polygons index + type
            
            f.write("PRIM "+"model"+cleanName+"_index[] = {\n")
            
            for i in range(len(m.polygons)):
            
                poly = m.polygons[i]
            
                f.write("\t"+str(poly.vertices[0])+","+str(poly.vertices[1])+","+str(poly.vertices[2]))
                
                if len(poly.vertices) > 3:
            
                    f.write("," + str(poly.vertices[3]) + ",8")
            
                else:
            
                    f.write(",0,4")
                
                if i != len(m.polygons) - 1:
            
                    f.write(",")
            
                f.write("\n")
            
            f.write("};\n\n")
            
            # Get object's custom properties
            
            chkProp = {
                'isAnim':0,
                'isRigidBody':0,
                'isStaticBody':0,
                'isPrism':0,
                'isActor':0,
                'isLevel':0,
                'isBG':0,
                'mass': 1,
                'restitution': 0,
                'lerp': 0
            }
            
            for prop in chkProp:
                if m.get(prop) is not None:
                    chkProp[prop] = m[prop]
            
            # put isBG back to 0 if using precalculated BGs
            if not self.exp_Precalc:
                chkProp['isBG'] = 0;
            
            if m.get('isActor'):
                actorPtr = cleanName
            
            if m.get('isLevel'):
                levelPtr = cleanName
            
            if m.get('isProp'):
                propPtr = cleanName
            
            if m.get('isLevel'):
                nodePtr = cleanName
    
    ## Vertex animation
                
            # write vertex anim if isAnim != 0 
            # Source : https://stackoverflow.com/questions/9138637/vertex-animation-exporter-for-blender
            
            if m.get("isAnim") is not None and m["isAnim"] != 0:
                
                # Write vertex pos
                
                o = bpy.data.objects[m.name]

                # ~ frame_start = bpy.context.scene.frame_start
                
                frame_start = int(bpy.data.actions[m.name].frame_range[0])
                
                # ~ frame_end = bpy.context.scene.frame_end
                
                frame_end = int(bpy.data.actions[m.name].frame_range[1])
                
                nFrame = frame_end - frame_start
                
                c = 0;
                
                tmp_meshes = []
                
                for i in range(frame_start, frame_end):
                    
                    bpy.context.scene.frame_set(i)
                    
                    bpy.context.scene.update()

                    nm = o.to_mesh(bpy.context.scene, True, 'PREVIEW')
                                        
                    if i == 0 :
                    
                        f.write("VANIM model"+cleanName+"_anim = {\n" +
                                "\t" + str(nFrame) + ",\n" +
                                "\t" + str(len(nm.vertices)) + ",\n" + 
                                "\t0,\n" + 
                                "\t0,\n" + 
                                "\t1,\n" + 
                                "\t" + str(chkProp['lerp']) + ",\n" + 
                                "\t{\n"
                                )
                    
                    for v in range(len(nm.vertices)):
                    
                        if v == 0:

                            f.write("\t\t//Frame %d\n" % i)

                        f.write("\t\t{ " + str(round(nm.vertices[v].co.x*scale)) + "," + str(round(-nm.vertices[v].co.z*scale)) + "," + str(round(nm.vertices[v].co.y*scale)) + " }")

                        if c != len(nm.vertices) * (nFrame) * 3 - 3:

                            f.write(",\n")

                        if v == len(nm.vertices) - 1:

                            f.write("\n")

                        c += 3;

                    tmp_meshes.append(nm)

                f.write("\n\t}\n};\n")

                # Remove meshe's working copies
                
                for nm in tmp_meshes:

                    bpy.data.meshes.remove(nm)
                
            # bpy.data.objects[bpy.data.meshes[0].name].active_shape_key.value : access shape_key
            
    ## Mesh world transform setup
            
            # Write object matrix, rot and pos vectors
            
            f.write("MATRIX model"+cleanName+"_matrix = {0};\n" +
                    "VECTOR model"+cleanName+"_pos    = {"+ str(round(bpy.data.objects[m.name].location.x * scale)) + "," + str(round(-bpy.data.objects[m.name].location.z * scale)) + "," + str(round(bpy.data.objects[m.name].location.y * scale)) + ", 0};\n" +
                    "SVECTOR model"+cleanName+"_rot   = {"+ str(round(degrees(bpy.data.objects[m.name].rotation_euler.x)/360 * 4096)) + "," + str(round(degrees(-bpy.data.objects[m.name].rotation_euler.z)/360 * 4096)) + "," + str(round(degrees(bpy.data.objects[m.name].rotation_euler.y)/360 * 4096)) + "};\n" +
                    "short model"+cleanName+"_isRigidBody = " + str(int(chkProp['isRigidBody'])) + ";\n" +
                    "short model"+cleanName+"_isStaticBody = " + str(int(chkProp['isStaticBody'])) + ";\n" +
                    "short model"+cleanName+"_isPrism = " + str(int(chkProp['isPrism'])) + ";\n" +
                    "short model"+cleanName+"_isAnim = " + str(int(chkProp['isAnim'])) + ";\n" +
                    "short model"+cleanName+"_isActor = " + str(int(chkProp['isActor'])) + ";\n" +
                    "short model"+cleanName+"_isLevel = " + str(int(chkProp['isLevel'])) + ";\n" +
                    "short model"+cleanName+"_isBG = " + str(int(chkProp['isBG'])) + ";\n" +
                    "long model"+cleanName+"_p = 0;\n" +
                    "long model"+cleanName+"_OTz = 0;\n" +
                    "BODY model"+cleanName+"_body = {\n" +
                    "\t{0, 0, 0, 0},\n" +
                    "\t" + str(round(bpy.data.objects[m.name].location.x * scale)) + "," + str(round(-bpy.data.objects[m.name].location.z * scale)) + "," + str(round(bpy.data.objects[m.name].location.y * scale)) + ", 0,\n" +
                    "\t"+ str(round(degrees(bpy.data.objects[m.name].rotation_euler.x)/360 * 4096)) + "," + str(round(degrees(-bpy.data.objects[m.name].rotation_euler.z)/360 * 4096)) + "," + str(round(degrees(bpy.data.objects[m.name].rotation_euler.y)/360 * 4096)) + ", 0,\n" +
                    "\t" + str(int(chkProp['mass'])) + ",\n" +
                    "\tONE/" + str(int(chkProp['mass'])) + ",\n" +
                    # write min and max values of AABBs on each axis
                    "\t" + str(round(min(Xvals) * scale)) + "," + str(round(min(Zvals) * scale)) + "," + str(round(min(Yvals) * scale)) + ", 0,\n" +
                    "\t" + str(round(max(Xvals) * scale)) + "," + str(round(max(Zvals) * scale)) + "," + str(round(max(Yvals) * scale)) + ", 0,\n" +
                    "\t" + str(int(chkProp['restitution'])) + "\n" + 
                    "\t};\n\n")
 
            # Write TMESH struct
            
            f.write("TMESH "+"model"+cleanName+" = {\n")
            
            f.write("\t"+"model"+cleanName+"_mesh,  \n")
            
            f.write("\t"+"model"+cleanName+"_normal,\n")
            
            if len(m.uv_textures) != None:
            
                for t in range(len(m.uv_textures)):
            
                    if m.uv_textures[0].data[0].image != None:
            
                        f.write("\t"+"model"+cleanName+"_uv,\n")
            
                    else:
            
                        f.write("\t0,\n")
            else:
            
                f.write("\t0,\n")
            
            f.write("\t"+"model"+cleanName+"_color, \n")
            
            # According to libgte.h, TMESH.len should be # of vertices. Meh...
            
            f.write("\t"+str(len(m.polygons))+"\n")
            
            f.write("};\n\n")
            
            # Write texture binary name and declare TIM_IMAGE
            # By default, loads the file from the ./TIM folder
            
            if len(m.uv_textures) != None:

                for t in range(len(m.uv_textures)): 

                    if m.uv_textures[0].data[0].image != None:
                        
                        tex_name = texture_image.name

                        prefix   = str.partition(tex_name, ".")[0].replace('-','_')

                        prefix   = CleanName(prefix)

                        # Add Tex name to list if it's not in there already

                        if prefix in timList:

                            break

                        else:
                            
                            f.write("extern unsigned long "+"_binary_TIM_" + prefix + "_tim_start[];\n")

                            f.write("extern unsigned long "+"_binary_TIM_" + prefix + "_tim_end[];\n")

                            f.write("extern unsigned long "+"_binary_TIM_" + prefix + "_tim_length;\n\n")

                            f.write("TIM_IMAGE tim_" + prefix + ";\n\n")
                            
                            timList.append(prefix)

            f.write("MESH mesh"+cleanName+" = {\n")
            
            f.write("\t&model"+ cleanName +",\n")
            
            f.write("\tmodel" + cleanName + "_index,\n")
            
            

            if len(m.uv_textures) != None:
            
                for t in range(len(m.uv_textures)):
            
                    if m.uv_textures[0].data[0].image != None:
            
                        tex_name = texture_image.name

                        prefix   = str.partition(tex_name, ".")[0].replace('-','_')

                        prefix   = CleanName(prefix)
                        
                        f.write("\t&tim_"+ prefix + ",\n")
                   
                        f.write("\t_binary_TIM_" + prefix + "_tim_start,\n")
                   
                    else:
                   
                        f.write("\t0,\n" +
                   
                                "\t0,\n")     
            else:
                
                f.write("\t0,\n" +
                
                        "\t0,\n")     
                
            f.write("\t&model"+cleanName+"_matrix,\n" +
                    "\t&model"+cleanName+"_pos,\n" +
                    "\t&model"+cleanName+"_rot,\n" +
                    "\t&model"+cleanName+"_isRigidBody,\n" +
                    "\t&model"+cleanName+"_isStaticBody,\n" +
                    "\t&model"+cleanName+"_isPrism,\n" +
                    "\t&model"+cleanName+"_isAnim,\n" +
                    "\t&model"+cleanName+"_isActor,\n" +
                    "\t&model"+cleanName+"_isLevel,\n" +
                    "\t&model"+cleanName+"_isBG,\n" +
                    "\t&model"+cleanName+"_p,\n" +
                    "\t&model"+cleanName+"_OTz,\n" +
                    "\t&model"+cleanName+"_body")
                    
            if m.get("isAnim") is not None and m["isAnim"] != 0:
                    
                    f.write(",\n\t&model"+cleanName+"_anim\n")
            else:
                    
                    f.write("\n")
                    
            f.write("};\n\n")

        f.write("MESH * meshes[" + str(len(bpy.data.meshes)) + "] = {\n")

        for k in range(len(bpy.data.meshes)):

            cleanName = CleanName(bpy.data.meshes[k].name)

            f.write("\t&mesh" + cleanName)

            if k != len(bpy.data.meshes) - 1:

                f.write(",\n")

        f.write("\n}; \n")

        # If camAngles is empty, use default camera, and do not include pre-calculated backgrounds

        if not camAngles:

            f.write("CAMANGLE camAngle_" + CleanName(defaultCam) + " = {\n" +
                    "\t&camPos_" + CleanName(defaultCam) + ",\n" +
                    "\t0,\n" + 
                    "\t0\n" + 
                    "};\n\n")
        
        # If camAngles is populated, use backgrounds and camera angles
        
        for o in camAngles:
        
            prefix = CleanName(o.name)
            
            # Include Tim data 
            
            f.write("extern unsigned long "+"_binary_TIM_bg_" + prefix + "_tim_start[];\n")
            
            f.write("extern unsigned long "+"_binary_TIM_bg_" + prefix + "_tim_end[];\n")
            
            f.write("extern unsigned long "+"_binary_TIM_bg_" + prefix + "_tim_length;\n\n")
            
            # Write corresponding TIM_IMAGE struct 
            
            f.write("TIM_IMAGE tim_bg_" + prefix + ";\n\n")
            
            # Write corresponding CamAngle struct
            
            f.write("CAMANGLE camAngle_" + prefix + " = {\n" +
                    "\t&camPos_" + prefix + ",\n" +
                    "\t&tim_bg_" + prefix + ",\n" +
                    "\t_binary_TIM_bg_" + prefix + "_tim_start\n" +
                    "};\n\n")
            
        # Write camera angles in an array for loops
        
        f.write("CAMANGLE * camAngles[" + str(len(camAngles)) + "] = {\n")
        
        for o in camAngles:
        
            prefix = CleanName(o.name)     
        
            f.write("\t&camAngle_" + prefix + ",\n")
        
        f.write("};\n\n")
        

        f.write("MESH * actorPtr = &mesh" + actorPtr + ";\n")
        
        f.write("MESH * levelPtr = &mesh" + levelPtr + ";\n")
        
        f.write("MESH * propPtr  = &mesh" + propPtr + ";\n\n")
        
        f.write("CAMANGLE * camPtr =  &camAngle_" + CleanName(defaultCam) + ";\n\n")

        
    ## Spatial Partitioning
    
        # ToDo :
        # Auto-detect which plane the actor is on and set that as curNode
    
        # Planes in the level ( define by 'isLevel' data property for now )

        LvlPlanes = {}

        # Objects in the level

        LvlObjects = {}

        # Link objects to their respective plane

        PlanesObjects = defaultdict(dict)

        # Store XY1, XY2 values

        Xvalues = []

        Yvalues = []

        # Find planes and objects bounding boxes
        
        # Planes first
        
        for o in bpy.data.objects:
        
            # Only loop through meshes
        
            if o.type == 'MESH':
        
                # Get Level planes coordinates
        
                if o.data.get('isLevel'):
                   
                    # World matrix is used to convert local to global coordinates
                    
                    mw = o.matrix_world
                   
                    for v in bpy.data.objects[o.name].data.vertices:
                   
                        # Convert local to global coords
                        
                        Xvalues.append( (mw * v.co).x )
                   
                        Yvalues.append( (mw * v.co).y )
                   
                    LvlPlanes[o.name] = {'x1' : min(Xvalues),
                                         'y1' : min(Yvalues),
                                         'x2' : max(Xvalues),
                                         'y2' : max(Yvalues)}
                                         
                    # Clear X/Y lists for next iteration
                    
                    Xvalues = []
                   
                    Yvalues = []
                
                # For each object not a plane and not actor, get its coordinates
                
                if not o.data.get('isLevel') and not o.data.get('isActor') :
                    
                    # World matrix is used to convert local to global coordinates
                    
                    mw = o.matrix_world
                    
                    for v in bpy.data.objects[o.name].data.vertices:
                    
                        # Convert local to global coords
                    
                        Xvalues.append( (mw * v.co).x )
                    
                        Yvalues.append( (mw * v.co).y )
                    
                    LvlObjects[o.name] = {'x1' : min(Xvalues),
                                          'y1' : min(Yvalues),
                                          'x2' : max(Xvalues),
                                          'y2' : max(Yvalues)}

                    # Clear X/Y lists for next iteration

                    Xvalues = []

                    Yvalues = []

        
        # Sides of the plane to check

        checkSides = [ 
                       ['N','S'], 
                       ['S','N'], 
                       ['W','E'], 
                       ['E','W'] 
                     ]


        # Generate a dict : 
        
        # ~ { 
        # ~     'S' : [] 
        # ~     'N' : [] list of planes connected to this plane, and side they're on
        # ~     'W' : [] 
        # ~     'E' : []
        # ~     'objects' : [] list of objects on this plane
        # ~     ''
        # ~ }

        for p in LvlPlanes:
            
            # Find objects on plane
            
            for o in LvlObjects:
                
                # If object is above plane ..
                
                if isInPlane(p, o) == 1:
                
                    # .. add this object to the plane's list
                
                    if 'objects' in PlanesObjects[p]:
                
                        PlanesObjects[p]['objects'].append(o)
                
                    else:
                
                        PlanesObjects[p] = { 'objects' : [o] }
            
            # Find surrounding planes
            
            for op in LvlPlanes:
                
                # Loop on other planes
                
                if op is not p:
                    
                    # Check each side
                    
                    for s in checkSides:
                    
                        # If connected ('connected') plane exists...
                    
                        if checkLine(
                    
                            getSepLine(p, s[0])[0],
                            getSepLine(p, s[0])[1],
                            getSepLine(p, s[0])[2],
                            getSepLine(p, s[0])[3],
                            
                            getSepLine(op, s[1])[0],
                            getSepLine(op, s[1])[1],
                            getSepLine(op, s[1])[2],
                            getSepLine(op, s[1])[3]
                    
                             ) == 'connected':
                            
                            # ... add it to the list
                            
                            if 'siblings' not in PlanesObjects[p]:
                                
                                PlanesObjects[p]['siblings'] = {}
                            
                            # If more than one plane is connected on the same side of the plane, 
                            # add it to the corresponding list    
                            
                            if s[0] in PlanesObjects[p]['siblings']:
                            
                                PlanesObjects[p]['siblings'][s[0]].append(op)
                            
                            else:
                            
                                PlanesObjects[p]['siblings'][s[0]] = [op]
               
            pName = CleanName(p)
            
            # Write PARENTNODE structure
            
            f.write("PARENTNODE node" + pName + "_siblings = {\n" + 
                    "\t" + str(len(PlanesObjects[p]['siblings'])) + ",\n" +
                    "\t{\n")
            
            for side in PlanesObjects[p]['siblings']:
                
                for sibling in PlanesObjects[p]['siblings'][side]:
            
                    f.write("\t\t&mesh" + CleanName(sibling) + ",\n")
                    
            f.write("\t}\n" +
                    "};\n\n")
            
            # Write CHILDNODE structure
            
            ## TODO : if objects is not none 
            
            f.write("CHILDNODE node" + pName + "_objects = {\n" + 
                    "\t" + str(len(PlanesObjects[p]['objects'])) + ",\n" +
                    "\t{\n")
            
            for obj in PlanesObjects[p]['objects']:
                
                f.write( "\t\t&mesh" + CleanName(obj) + ",\n" )
                    
            f.write("\t}\n" +
                    "};\n\n")
                    
            
            # Write NODE structure
                    
            f.write( "NODE node" + pName + " = {\n" +
                     "\t&mesh" + pName + ",\n" +
                     "\t&node" + pName + "_siblings,\n" +
                     "\t&node" + pName + "_objects\n" +
                     "};\n\n" )
       
       
                     # ~ "\t{\n")
            
            # ~ for side in PlanesObjects[p]['siblings']:
                
                # ~ for sibling in PlanesObjects[p]['siblings'][side]:
                    
                    # ~ f.write( "\t\t&node" + CleanName(sibling) + ",\n" )
                
            # ~ f.write( "\t},\n" + 
                     # ~ "\t{\n" )
            
            # ~ for obj in PlanesObjects[p]['objects']:
                
                # ~ f.write( "\t\t&mesh" + CleanName(obj) + ",\n" )
            
            
            # ~ f.write( "\t}\n" + 
                     # ~ "};\n\n")

        f.write("NODE * curNode =  &node" + nodePtr + ";\n\n")

        # Set default camera back in Blender
        
        if defaultCam != 'NULL':
        
            bpy.context.scene.camera = bpy.data.objects[defaultCam]

        f.close()
        
        return {'FINISHED'};
 
def menu_func(self, context):
    
    self.layout.operator(ExportMyFormat.bl_idname, text="PSX Format(.c)");
 
def register():
    
    bpy.utils.register_module(__name__);
    
    bpy.types.INFO_MT_file_export.append(menu_func);
    
def unregister():
    
    bpy.utils.unregister_module(__name__);
    
    bpy.types.INFO_MT_file_export.remove(menu_func);
 
if __name__ == "__main__":
    
    register()
