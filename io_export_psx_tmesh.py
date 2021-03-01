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
import unicodedata
from math import radians

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
        import bmesh
        from math import degrees, floor, cos, sin
        from mathutils import Vector
        
        def triangulate_object(obj): # Stolen from here : https://blender.stackexchange.com/questions/45698/triangulate-mesh-in-python/45722#45722
            me = obj.data
            # Get a BMesh representation
            bm = bmesh.new()
            bm.from_mesh(me)
            bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method=0, ngon_method=0)
            # Finish up, write the bmesh back to the mesh
            bm.to_mesh(me)
            bm.free()
            # ~ return bm
        
        def CleanName(strName):
            name = strName.replace(' ','_')
            name = name.replace('.','_')
            name = unicodedata.normalize('NFKD',name).encode('ASCII', 'ignore').decode()
            return name
            
        # Leave edit mode to avoid errors
        bpy.ops.object.mode_set(mode='OBJECT')

        # triangulate objects of type mesh 
        if self.exp_Triangulate:
            for o in range(len(bpy.data.objects)):
                if bpy.data.objects[o].type == 'MESH':
                    triangulate_object(bpy.data.objects[o])
                    
                # ~ obj = bpy.data.objects[bpy.data.objects[o].name]
                
                # ~ tm = obj.to_mesh(bpy.context.scene, False, 'PREVIEW')

                # ~ work_meshes.append(tm)
                        
        scale = self.exp_Scale
        
        # get working directory path
        filepath = bpy.data.filepath
        folder = os.path.dirname(bpy.path.abspath(filepath))
        dirpath = os.path.join(folder, "TIM")
        
        camAngles = []
        
        # if using precalculated BG, render and export them to ./TIM/
        if self.exp_Precalc:
            
            # create folder if !exist
            os.makedirs(dirpath, exist_ok = 1)
            
            # file format config
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.image_settings.quality = 100
            bpy.context.scene.render.image_settings.compression = 0
            bpy.context.scene.render.image_settings.color_depth = '8'
            
            # get current cam
            cam = bpy.context.scene.camera
            
            # store cam location and rot for restoration later
            # ~ originLoc = cam.location
            # ~ originRot = cam.rotation_euler 
            
            for o in bpy.data.objects:
                
                if o.type == 'CAMERA' and o.name.startswith("camPath"):
                    
                    # set cam as active - could be useful if multiple cam are present
                    bpy.context.scene.camera = o
                    
                    # set cam Rot/Loc to empty rot/loc 
                    # ~ cam.location = o.location 
                    # ~ cam.rotation_euler = o.rotation_euler
                    
                    # apply 90degrees rotation on local X axis, as EMPTYs are pointing to -Z (bottom of the screen) by default
                    # ~ cam.rotation_euler.rotate_axis('X', radians(90))
                    
                    # render and save image
                    bpy.ops.render.render()
                    bpy.data.images["Render Result"].save_render(folder + os.sep + "TIM" + os.sep + "bg_" + CleanName(o.name) + "." + str(bpy.context.scene.render.image_settings.file_format).lower())
                    camAngles.append(o)
        
                    
            # set cam back to original pos/rot
            # ~ cam.location = originLoc
            # ~ cam.rotation_euler = originRot
                    
        f = open(os.path.normpath(self.filepath),"w+")
        
        # write BODY struct def
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
                
        # VERTEX ANIM struct
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
                
        # PRIM struc
        f.write("typedef struct {\n" +
                "\tVECTOR order;\n" +
                "\tint    code; // Same as POL3/POL4 codes : Code (F3 = 1, FT3 = 2, G3 = 3, GT3 = 4) Code (F4 = 5, FT4 = 6, G4 = 7, GT4 = 8)\n" +
                "\t} PRIM;\n\n")
        
        # MESH struct
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
        
        # CAM POSITION struct
        f.write("typedef struct {\n" +
                "\tVECTOR  pos;\n" +
                "\tSVECTOR rot;\n" + 
                "\t} CAMPOS;\n\n" +
                "\n// Blender cam ~= PSX cam with these settings : NTSC - 320x240, PAL 320x256, pixel ratio 1:1, cam focal length : perspective 90° ( 16 mm ))\n\n")
        
        # CAM ANGLE
        f.write("typedef struct {\n" +
                "\tCAMPOS    * campos;\n" +
                "\tTIM_IMAGE * BGtim;\n" +
                "\tunsigned long * tim_data;\n" +
                "\t} CAMANGLE;\n\n")
                
        # CAM PATH struct
        f.write("typedef struct {\n" +
                "\tshort len, cursor, pos;\n" +
                "\tVECTOR points[];\n" +
                "\t} CAMPATH;\n\n")

        camPathPoints = []
        defaultCam = 'NULL'
        
        first_mesh = CleanName(bpy.data.meshes[0].name)

        # set camera position and rotation in the scene
        for o in range(len(bpy.data.objects)):
            if bpy.data.objects[o].type == 'CAMERA' and bpy.data.objects[o].data.get('isDefault'):
                defaultCam = bpy.data.objects[o].name
            if bpy.data.objects[o].type == 'CAMERA':
                f.write("CAMPOS camPos_" + CleanName(bpy.data.objects[o].name) + " = {\n" +
                "\t{" + str(round(-bpy.data.objects[o].location.x * scale)) + "," + str(round(bpy.data.objects[o].location.z * scale)) + "," +str(round(-bpy.data.objects[o].location.y * scale)) + "},\n" +
                "\t{" + str(round(-(degrees(bpy.data.objects[o].rotation_euler.x)-90)/360 * 4096)) + "," + str(round(degrees(bpy.data.objects[o].rotation_euler.z)/360 * 4096)) + "," + str(round(-(degrees(bpy.data.objects[o].rotation_euler.y))/360 * 4096)) + "}\n" +
                "};\n\n")
                
        # find camStart and camEnd empties for camera trajectory
            if bpy.data.objects[o].type == 'CAMERA' :
                if bpy.data.objects[o].name.startswith("camPath") and not bpy.data.objects[o].data.get('isDefault'):
                    camPathPoints.append(bpy.data.objects[o].name)
        
        if camPathPoints:
            
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
            f.write("CAMPATH camPath = {\n" +
                            "\t0,\n" +
                            "\t0,\n" +
                            "\t0\n"  +
                            "};\n\n")        
        # Lights : max 3 sunlamp, no space coords
        
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
                ## intensity
                energy   = int(bpy.data.lamps[l].energy * 4096)
                
                # Euler based
                
                # get a direction vector from world matrix
                lightdir = bpy.data.objects[bpy.data.lamps[l].name].matrix_world * Vector((0,0,-1,0))
                
                
                f.write( 
                    "\t" + str(int(lightdir.x * energy)) + "," + 
                    "\t" + str(int(-lightdir.z * energy)) + "," +
                    "\t" + str(int(lightdir.y * energy))  
                    )
                    
                if l != len(bpy.data.lamps) - 1:
                    f.write(",\n")
                
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

            f.write(
                "\t" + LCM[0] + "," + LCM[3] + "," + LCM[6] + ",\n" +
                "\t" + LCM[1] + "," + LCM[4] + "," + LCM[7] + ",\n" +
                "\t" + LCM[2] + "," + LCM[5] + "," + LCM[8] + "\n" )
            f.write("\t};\n\n")
                
        actorPtr = first_mesh
        levelPtr = first_mesh
        propPtr = first_mesh
        
        for m in bpy.data.meshes:
 
            # Write vertices vectors
            
            # AABB : Store vertices coordinates by axis
            Xvals = []
            Yvals = []
            Zvals = []
 
            # remove '.' from mesh name
            cleanName = CleanName(m.name)
            # ~ cleanName = m.name.replace('.','_')
            # ~ cleanName = unicodedata.normalize('NFKD',cleanName).encode('ASCII', 'ignore').decode()
 
            f.write("SVECTOR "+"model"+cleanName+"_mesh[] = {\n")
            for i in range(len(m.vertices)):
                v = m.vertices[i].co
                
                # AABB : append vertices coords by axis
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
                            if self.exp_Precalc and m.get('isBG'):
                                f.write("\t255, 255, 0, 0") # Clamp values to 0-255 to avoid tpage overflow
                            else:
                                f.write("\t"+str(max(0, min( round(ux) , 255 )))+","+str(max(0, min(round(tex_height - uy) , 255 )))+", 0, 0") # Clamp values to 0-255 to avoid tpage overflow
                            if i != len(uv_layer) - 1:
                                f.write(",")
                            f.write("\n")
                        f.write("};\n\n")
                        
                        # save uv tex if needed - still have to convert them to tim...
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
                        f.write("\t80,80,80,0")  # Let's add a bit more relief with a shade of grey
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
            
            # get custom properties isRigidBody, isPrism, isAnim
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
            
            if m.get('isActor'):
                actorPtr = cleanName
            
            if m.get('isLevel'):
                levelPtr = cleanName
            
            if m.get('isProp'):
                propPtr = cleanName
            
            # write vertex anim if isAnim != 0 # https://stackoverflow.com/questions/9138637/vertex-animation-exporter-for-blender
            if m.get("isAnim") is not None and m["isAnim"] != 0:
                
                #write vertex pos
                
                o = bpy.data.objects[m.name]

                # ~ frame_start = bpy.context.scene.frame_start
                frame_start = int(bpy.data.actions[m.name].frame_range[0])
                # ~ frame_end = bpy.context.scene.frame_end
                frame_end = int(bpy.data.actions[m.name].frame_range[1])
                
                nFrame = frame_end - frame_start
                
                # ~ f.write("int "+"model"+cleanName+"_anim_nframes = " + str(nFrame) + ";\n")
                # ~ f.write("int "+"model"+cleanName+"_anim_nvert = {" + str(len(nm.vertices)) + "};")
                # ~ f.write("SVECTOR "+"model"+cleanName+"_anim_data[") 
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
                            # ~ f.write("{\n")
                            f.write("\t\t//Frame %d\n" % i)
                        f.write("\t\t{ " + str(round(nm.vertices[v].co.x*scale)) + "," + str(round(-nm.vertices[v].co.z*scale)) + "," + str(round(nm.vertices[v].co.y*scale)) + " }")
                        if c != len(nm.vertices) * (nFrame) * 3 - 3:
                            f.write(",\n")
                        if v == len(nm.vertices) - 1:
                            f.write("\n")
                        c += 3;
                    # ~ if i != (frame_end - frame_start):
                            # ~ f.write(",")
                    tmp_meshes.append(nm)
                        # ~ tmp_meshes.remove(nm)
                f.write("\n\t}\n};\n")
                
                for nm in tmp_meshes:
                    bpy.data.meshes.remove(nm)
                
                # ~ c = 0

                # ~ tmp_meshes_n = []

                # ~ for i in range(frame_start - 1, frame_end):
                    
                    
                    
                    # ~ bpy.context.scene.frame_set(i)
                    # ~ bpy.context.scene.update()

                    # ~ nm_n = o.to_mesh(bpy.context.scene, True, 'PREVIEW')
                    
                    # ~ if i == 0 :
                        # ~ f.write("\t{\n")
    
                    # ~ for v in range(len(nm_n.vertices)):
                        
                        # ~ poly = m.polygons[v]
                        
                        # ~ if v == 0:
                            # ~ f.write("\t\t//Frame %d\n" % i)
                        # ~ f.write("\t\t{ " + str(round(-poly.normal.x * 4096)) + "," + str(round(poly.normal.z  * 4096)) + "," + str(round(-poly.normal.y * 4096) ) + ",0 }")
                                                
                        # ~ if c != len(nm_n.vertices) * (nFrame + 1) * 3 - 3:
                            # ~ f.write(",\n")
                        # ~ if v == len(nm_n.vertices) - 1:
                            # ~ f.write("\n")
                        # ~ c += 3;
                    
                    # ~ tmp_meshes_n.append(nm_n)
                # ~ f.write("\t\n}\n};\n")
        
                
                # ~ for nm_n in tmp_meshes_n:
                    # ~ bpy.data.meshes.remove(nm_n)
            
                
            #Stuff # ~ bpy.data.objects[bpy.data.meshes[0].name].active_shape_key.value : access shape_key
            
            #write object matrix, rot and pos vectors
            f.write("MATRIX model"+cleanName+"_matrix = {0};\n" +
                    "VECTOR model"+cleanName+"_pos    = {"+ str(round(bpy.data.objects[m.name].location.x * scale)) + "," + str(round(-bpy.data.objects[m.name].location.z * scale)) + "," + str(round(bpy.data.objects[m.name].location.y * scale)) + ", 0};\n" +
                    "SVECTOR model"+cleanName+"_rot   = {"+ str(round(degrees(bpy.data.objects[m.name].rotation_euler.x)/360 * 4096)) + "," + str(round(degrees(bpy.data.objects[m.name].rotation_euler.z)/360 * 4096)) + "," + str(round(degrees(bpy.data.objects[m.name].rotation_euler.y)/360 * 4096)) + "};\n" +
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
            
            # write texture binary name and declare TIM_IMAGE
            # by default, load the file from the TIM folder
            # ~ if len(m.uv_textures) != 0:
            if len(m.uv_textures) != None:
                for t in range(len(m.uv_textures)): 
                    if m.uv_textures[0].data[0].image != None:
                        tex_name = texture_image.name
                        prefix   = str.partition(tex_name, ".")[0].replace('-','_')
                        prefix   = CleanName(prefix)
                        
                        f.write("extern unsigned long "+"_binary_TIM_" + prefix + "_tim_start[];\n")
                        f.write("extern unsigned long "+"_binary_TIM_" + prefix + "_tim_end[];\n")
                        f.write("extern unsigned long "+"_binary_TIM_" + prefix + "_tim_length;\n\n")
                        f.write("TIM_IMAGE tim_" + prefix + ";\n\n")
                
            f.write("MESH mesh"+cleanName+" = {\n")
            f.write("\t&model"+ cleanName +",\n")
            f.write("\tmodel" + cleanName + "_index,\n")
            
            if len(m.uv_textures) != None:
                for t in range(len(m.uv_textures)):
                    if m.uv_textures[0].data[0].image != None:
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
            # ~ cleanName = bpy.data.meshes[k].name.replace('.','_')
            # ~ cleanName = unicodedata.normalize('NFKD',cleanName).encode('ASCII', 'ignore').decode() 
            f.write("\t&mesh" + cleanName)
            if k != len(bpy.data.meshes) - 1:
                f.write(",\n")
        f.write("\n}; \n")

        # nothing in camAngles, use default camera
        if not camAngles:
            f.write("CAMANGLE camAngle_" + CleanName(defaultCam) + " = {\n" +
                    "\t&camPos_" + CleanName(defaultCam) + ",\n" +
                    "\t0,\n" + 
                    "\t0\n" + 
                    "};\n\n")
        
        # cam angles is populated
        for o in camAngles:
            prefix = CleanName(o.name)
            
            # include Tim data 
            f.write("extern unsigned long "+"_binary_TIM_bg_" + prefix + "_tim_start[];\n")
            f.write("extern unsigned long "+"_binary_TIM_bg_" + prefix + "_tim_end[];\n")
            f.write("extern unsigned long "+"_binary_TIM_bg_" + prefix + "_tim_length;\n\n")
            
            # write corresponding TIM_IMAGE struct 
            f.write("TIM_IMAGE tim_bg_" + prefix + ";\n\n")
            
            # write corresponding CamAngle struct
            f.write("CAMANGLE camAngle_" + prefix + " = {\n" +
                    "\t&camPos_" + prefix + ",\n" +
                    "\t&tim_bg_" + prefix + ",\n" +
                    "\t_binary_TIM_bg_" + prefix + "_tim_start\n" +
                    "};\n\n")
            
        # write cam angles array for loops
        f.write("CAMANGLE * camAngles[" + str(len(camAngles)) + "] = {\n")
        for o in camAngles:
            prefix = CleanName(o.name)     
            f.write("\t&camAngle_" + prefix + ",\n")
        f.write("};\n\n")
        

        f.write("MESH * actorPtr = &mesh" + actorPtr + ";\n")
        f.write("MESH * levelPtr = &mesh" + levelPtr + ";\n")
        f.write("MESH * propPtr  = &mesh" + propPtr + ";\n\n")
        
        # ~ if self.exp_Precalc:
        f.write("CAMANGLE * camPtr =  &camAngle_" + CleanName(defaultCam) + ";\n\n")
        # ~ else :
            # ~ f.write("CAMPOS * camPtr =  &camPos_" + CleanName(defaultCam) + ";\n\n")
        
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
