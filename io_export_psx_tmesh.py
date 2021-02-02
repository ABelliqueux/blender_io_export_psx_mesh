import os
import bpy
 
bl_info = {
    "name":         "PSX TMesh exporter",
    "author":       "Schnappy, TheDukeOfZill",
    "blender":      (2,7,9),
    "version":      (0,0,2),
    "location":     "File > Import-Export",
    "description":  "Export psx data format",
    "category":     "Import-Export"
}
        
import bpy
from bpy_extras.io_utils import ExportHelper
 
class ExportMyFormat(bpy.types.Operator, ExportHelper):
    bl_idname       = "export_psx.c";
    bl_label        = "PSX compatible format exporter";
    bl_options      = {'PRESET'};
    filename_ext    = ".c";
    
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
        
        # Leave edit mode to avoid errors
        bpy.ops.object.mode_set(mode='OBJECT')

        # triangulate objects of type mesh 
        for m in range(len(bpy.data.objects)):
            if bpy.data.objects[m].type == 'MESH':
                triangulate_object(bpy.data.objects[m])
        
        scale = 65
        f = open(os.path.normpath(self.filepath),"w+")
        
        # write BODY struct def
        f.write("typedef struct {\n" +
                "\tVECTOR  position;\n" +
                "\tSVECTOR velocity;\n" +
                "\tint     mass;\n" +
                "\tVECTOR  min; \n" +
                "\tVECTOR  max; \n" +
                "\t} BODY;\n\n")
        # VERTEX ANIM struct
        f.write("typedef struct { \n" +
                "\tint nframes;    // number of frames e.g   20\n" +
                "\tint nvert;      // number of vertices e.g 21\n" +
                "\tSVECTOR data[]; // vertex pos as SVECTORs e.g 20 * 21 SVECTORS\n" +
                "\t} VANIM;\n\n")
                
        # MESH struct
        f.write("typedef struct {  \n"+
                "\tTMESH   *    tmesh;\n" +
                "\tint     *    index;\n" +
                "\tTIM_IMAGE *  tim;  \n" + 
                "\tu_long  *    tim_data;\n"+
                "\tMATRIX  *    mat;\n" + 
                "\tVECTOR  *    pos;\n" + 
                "\tSVECTOR *    rot;\n" +
                "\tshort   *    isRigidBody;\n" +
                "\tshort   *    isPrism;\n" +
                "\tshort   *    isAnim;\n" +
                "\tlong    *    p;\n" + 
                "\tBODY    *     body;\n" + 
                "\tVANIM    *     anim;\n" + 
                "\t} MESH;\n\n")
        
        # CAM POSITION struct
        f.write("typedef struct {\n" +
                "\tVECTOR  pos;\n" +
                "\tSVECTOR rot;\n" + 
                "\t} CAMPOS;\n\n" +
                "\n// Blender cam ~= PSX cam with these settings : TV NTSC 4:3, Cam focal length : 100° ( 13.43 mm ))\n")
        # CAM PATH struct
        f.write("typedef struct {\n" +
                "\tshort len, cursor;\n" +
                "\tVECTOR points[];\n" +
                "\t} CAMPATH;\n\n")

        camPathPoints = []

        # set camera position and rotation in the scene
        for o in range(len(bpy.data.objects)):
            if bpy.data.objects[o].type == 'CAMERA':
                f.write("CAMPOS camStartPos = {\n" +
                "\t{" + str(round(-bpy.data.objects[o].location.x * scale)) + "," + str(round(bpy.data.objects[o].location.z * scale)) + "," +str(round(-bpy.data.objects[o].location.y * scale)) + "},\n" +
                "\t{" + str(round(-(degrees(bpy.data.objects[o].rotation_euler.x)-90)/360 * 4096)) + "," + str(round(degrees(bpy.data.objects[o].rotation_euler.z)/360 * 4096)) + "," + str(round(-(degrees(bpy.data.objects[o].rotation_euler.y))/360 * 4096)) + "},\n" +
                "};\n\n")

        # find camStart and camEnd empties for camera trajectory
            if bpy.data.objects[o].type == 'EMPTY' :
                if bpy.data.objects[o].name.startswith("camPath"):
                    camPathPoints.append(bpy.data.objects[o].name)
        
        if camPathPoints:
            
            # ~ camPathPoints = list(reversed(camPathPoints))
            
            for p in range(len(camPathPoints)):
                if p == 0:
                    f.write("CAMPATH camPath = {\n" +
                            "\t" + str(len(camPathPoints)) + ",\n" +
                            "\t0,\n" +
                            "\t{\n")
                f.write("\t\t{" + str(round(-bpy.data.objects[camPathPoints[p]].location.x * scale)) + "," + str(round(bpy.data.objects[camPathPoints[p]].location.z * scale)) + "," +str(round(-bpy.data.objects[camPathPoints[p]].location.y * scale)) + "}")
                if p != len(camPathPoints) - 1:
                    f.write(",\n")  
            f.write("\n\t}\n};\n\n")
                
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
                    while cnt < pad:
                        f.write("\t0,0,0")
                        if cnt != 1:
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
                
            
        for m in bpy.data.meshes:
 
            # Write vertices vectors
            
            # AABB : Store vertices coordinates by axis
            Xvals = []
            Yvals = []
            Zvals = []
 
            # remove '.' from mesh name
            cleanName = m.name.replace('.','_')

 
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
                if i != len(m.polygons) - 1:
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
            if len(m.uv_textures) != 0:
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
                            f.write("\t"+str(max(0, min( round(ux) , 255 )))+","+str(max(0, min(round(tex_height - uy) , 255 )))+", 0, 0") # Clamp values to 0-255 to avoid tpage overflow
                            if i != len(uv_layer) - 1:
                                f.write(",")
                            f.write("\n")
                        f.write("};\n\n")
             
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
            
            # Write polygons index
            f.write("int "+"model"+cleanName+"_index[] = {\n")
            for i in range(len(m.polygons)):
                poly = m.polygons[i]
                f.write("\t"+str(poly.vertices[0])+","+str(poly.vertices[1])+","+str(poly.vertices[2]))
                if i != len(m.polygons) - 1:
                    f.write(",")
                f.write("\n")
            f.write("};\n\n")
            
            # get custom properties isRigidBody, isPrism, isAnim
            chkProp = {
                'isAnim':0,
                'isRigidBody':0,
                'isPrism':0,
                'mass':1000
            }
            
            for prop in chkProp:
                if m.get(prop) is not None:
                    chkProp[prop] = m[prop]
            
            # write vertex anim if isAnim != 0 # https://stackoverflow.com/questions/9138637/vertex-animation-exporter-for-blender
            if m.get("isAnim") is not None and m["isAnim"] != 0:
                
                #write vertex pos
                o = bpy.data.objects[m.name]

                frame_start = bpy.context.scene.frame_start
                frame_end = bpy.context.scene.frame_end
                
                nFrame = frame_end - frame_start
                
                # ~ f.write("int "+"model"+cleanName+"_anim_nframes = " + str(nFrame) + ";\n")
                # ~ f.write("int "+"model"+cleanName+"_anim_nvert = {" + str(len(nm.vertices)) + "};")
                # ~ f.write("SVECTOR "+"model"+cleanName+"_anim_data[") 
                c = 0;
                
                tmp_meshes = []
                
                for i in range(frame_start - 1, frame_end):
                    
                    bpy.context.scene.frame_set(i)
                    bpy.context.scene.update()

                    nm = o.to_mesh(bpy.context.scene, True, 'PREVIEW')
                    
                    # ~ f.write(str(len(nm.vertices)))
                    if i == 0 :
                        f.write("VANIM modelCylindre_anim = {\n" +
                                "\t" + str(nFrame) + ",\n" +
                                "\t" + str(len(nm.vertices)) + ",\n" + 
                                "\t{\n"
                                )
                    for v in range(len(nm.vertices)):
                        if v == 0:
                            # ~ f.write("{\n")
                            f.write("\t\t//Frame %d\n" % i)
                        f.write("\t\t{ " + str(round(nm.vertices[v].co.x*scale)) + "," + str(round(-nm.vertices[v].co.z*scale)) + "," + str(round(nm.vertices[v].co.y*scale)) + " }")
                        if c != len(nm.vertices) * (nFrame + 1) * 3 - 3:
                            f.write(",\n")
                        if v == len(nm.vertices) - 1:
                            f.write("\n")
                        c += 3;
                    # ~ if i != (frame_end - frame_start):
                            # ~ f.write(",")
                    tmp_meshes.append(nm)
                        # ~ tmp_meshes.remove(nm)
                
                f.write("\n\t}\n};\n\n")
                
                for nm in tmp_meshes:
                    # ~ f.write(str(nm))
                    bpy.data.meshes.remove(nm)
            
                
            #Stuff # ~ bpy.data.objects[bpy.data.meshes[0].name].active_shape_key.value : access shape_key
            
            #write object matrix, rot and pos vectors
            f.write("MATRIX model"+cleanName+"_matrix = {0};\n" +
                    "VECTOR model"+cleanName+"_pos    = {"+ str(round(bpy.data.objects[m.name].location.x * scale)) + "," + str(round(-bpy.data.objects[m.name].location.z * scale)) + "," + str(round(bpy.data.objects[m.name].location.y * scale)) + ", 0};\n" +
                    "SVECTOR model"+cleanName+"_rot   = {"+ str(round(degrees(bpy.data.objects[m.name].rotation_euler.x)/360 * 4096)) + "," + str(round(degrees(-bpy.data.objects[m.name].rotation_euler.z)/360 * 4096)) + "," + str(round(degrees(bpy.data.objects[m.name].rotation_euler.y)/360 * 4096)) + "};\n" +
                    "short model"+cleanName+"_isRigidBody =" + str(int(chkProp['isRigidBody'])) + ";\n" +
                    "short model"+cleanName+"_isPrism =" + str(int(chkProp['isPrism'])) + ";\n" +
                    "short model"+cleanName+"_isAnim =" + str(int(chkProp['isAnim'])) + ";\n" +
                    "long model"+cleanName+"_p = 0;\n" +
                    "BODY model"+cleanName+"_body = {\n" +
                    "\t" + str(round(bpy.data.objects[m.name].location.x * scale)) + "," + str(round(-bpy.data.objects[m.name].location.z * scale)) + "," + str(round(bpy.data.objects[m.name].location.y * scale)) + ", 0,\n" +
                    "\t"+ str(round(degrees(bpy.data.objects[m.name].rotation_euler.x)/360 * 4096)) + "," + str(round(degrees(-bpy.data.objects[m.name].rotation_euler.z)/360 * 4096)) + "," + str(round(degrees(bpy.data.objects[m.name].rotation_euler.y)/360 * 4096)) + ", 0,\n" +
                    "\t" + str(int(chkProp['mass'])) + ",\n" +
                    # write min and max values of AABBs on each axis
                    "\t" + str(round(min(Xvals) * scale)) + "," + str(round(min(Zvals) * scale)) + "," + str(round(min(Yvals) * scale)) + ", 0,\n" +
                    "\t" + str(round(max(Xvals) * scale)) + "," + str(round(max(Zvals) * scale)) + "," + str(round(max(Yvals) * scale)) + ", 0,\n" +
                    "\t};\n\n")
 
            # Write TMESH struct
            f.write("TMESH "+"model"+cleanName+" = {\n")
            f.write("\t"+"model"+cleanName+"_mesh,  \n")
            f.write("\t"+"model"+cleanName+"_normal,\n")
            
            if len(m.uv_textures) != 0:
                for t in range(len(m.uv_textures)):
                    if m.uv_textures[0].data[0].image != None:
                        f.write("\t"+"model"+cleanName+"_uv,\n")
            else:
                f.write("\t0,\n")
            
            f.write("\t"+"model"+cleanName+"_color, \n")
            
            # According to libgte.h, TMESH.len should be # of vertices. Meh...
            f.write("\t"+str(len(m.polygons))+"\n")
            f.write("};\n\n")
            
            # write texture binary name and declare TIM_IMAGE
            # by default, load the file from the TIM folder
            # ~ if len(m.uv_textures) != 0:
            if len(m.uv_textures) != 0:
                for t in range(len(m.uv_textures)): 
                    if m.uv_textures[0].data[0].image != None:
                        tex_name = texture_image.name
                        prefix   = str.partition(tex_name, ".")[0].replace('-','_')
                        f.write("extern unsigned long "+"_binary_TIM_" + prefix + "_tim_start[];\n")
                        f.write("extern unsigned long "+"_binary_TIM_" + prefix + "_tim_end[];\n")
                        f.write("extern unsigned long "+"_binary_TIM_" + prefix + "_tim_length;\n\n")
                        f.write("TIM_IMAGE tim_" + prefix + ";\n\n")
                
            f.write("MESH mesh"+cleanName+" = {\n")
            f.write("\t&model"+ cleanName +",\n")
            f.write("\tmodel" + cleanName + "_index,\n")
            
            if len(m.uv_textures) != 0:
                for t in range(len(m.uv_textures)):
                    if m.uv_textures[0].data[0].image != None:
                        f.write("\t&tim_"+ prefix + ",\n")
                        f.write("\t_binary_TIM_" + prefix + "_tim_start,\n") 
            else:
                f.write("\t0,\n" +
                        "\t0,\n")            
            f.write("\t&model"+cleanName+"_matrix,\n" +
                    "\t&model"+cleanName+"_pos,\n" +
                    "\t&model"+cleanName+"_rot,\n" +
                    "\t&model"+cleanName+"_isRigidBody,\n" +
                    "\t&model"+cleanName+"_isPrism,\n" +
                    "\t&model"+cleanName+"_isAnim,\n" +
                    "\t&model"+cleanName+"_p,\n" +
                    "\t&model"+cleanName+"_body")
            if m.get("isAnim") is not None and m["isAnim"] != 0:
                    f.write(",\n\t&model"+cleanName+"_anim\n")
            else:
                    f.write("\n")
                    
            f.write("};\n\n")

        f.write("MESH * meshes[" + str(len(bpy.data.meshes)) + "] = {\n")
        for k in range(len(bpy.data.meshes)): 
            f.write("\t&mesh" + bpy.data.meshes[k].name.replace('.','_'))
            if k != len(bpy.data.meshes) - 1:
                f.write(",\n")
        f.write("\n}; \n")
        
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
