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
        from math import degrees
        
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
        
        scale = 200
        f = open(os.path.normpath(self.filepath),"w+")
        
        # write typedef struct
        f.write("typedef struct {  \n"+
                "\tTMESH   *    tmesh;\n" +
                "\tint     *    index;\n" +
                "\tTIM_IMAGE *  tim;  \n" + 
                "\tu_long  *    tim_data;\n"+
                "\tMATRIX  *    mat;\n" + 
                "\tVECTOR  *    pos;\n" + 
                "\tSVECTOR *    rot;\n" +
                "\tshort   *    isPrism;\n" +
                "\tlong    *    p;\n" + 
                "\t} MESH;\n\n")
        
        for m in bpy.data.meshes:
 
            # Write vertices vectors
 
            f.write("SVECTOR "+"model"+m.name+"_mesh[] = {\n")
            for i in range(len(m.vertices)):
                v = m.vertices[i].co
                f.write("\t{"+str(v.x*scale)+","+str(v.y*scale)+","+str(v.z*scale)+"}")
                if i != len(m.vertices) - 1:
                    f.write(",")
                f.write("\n")
            f.write("};\n\n")
            
            # Write normals vectors
 
            f.write("SVECTOR "+"model"+m.name+"_normal[] = {\n")
            for i in range(len(m.polygons)):
                poly = m.polygons[i]
                f.write("\t"+str(poly.normal.x)+","+str(poly.normal.y)+","+str(poly.normal.z)+",0")
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
                        f.write("SVECTOR "+"model"+m.name+"_uv[] = {\n")
                        texture_image = m.uv_textures[t].data[0].image
                        tex_width = texture_image.size[0]
                        tex_height = texture_image.size[1]
                        uv_layer = m.uv_layers[0].data
                        for i in range(len(uv_layer)):
                            u = uv_layer[i].uv
                            ux = u.x * tex_width
                            uy = u.y * tex_height
                            f.write("\t"+str(ux)+","+str(tex_height - uy)+", 0, 0")
                            if i != len(uv_layer) - 1:
                                f.write(",")
                            f.write("\n")
                        f.write("};\n\n")
             
            # Write vertex colors vectors
 
            f.write("CVECTOR "+"model"+m.name+"_color[] = {\n") 
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
            f.write("int "+"model"+m.name+"_index[] = {\n")
            for i in range(len(m.polygons)):
                poly = m.polygons[i]
                f.write("\t"+str(poly.vertices[0])+","+str(poly.vertices[1])+","+str(poly.vertices[2]))
                if i != len(m.polygons) - 1:
                    f.write(",")
                f.write("\n")
            f.write("};\n\n")
 
            #write object matrix, rot and pos vectors
            f.write("MATRIX model"+m.name+"_matrix = {0};\n" +
                    "VECTOR model"+m.name+"_pos    = {"+ str(bpy.data.objects[m.name].location.x * 100) + "," + str(bpy.data.objects[m.name].location.y * 100) + "," + str(bpy.data.objects[m.name].location.z * 100) + ", 0};\n" +
                    "SVECTOR model"+m.name+"_rot   = {"+ str(degrees(bpy.data.objects[m.name].rotation_euler.x)/360 * 4096) + "," + str(degrees(bpy.data.objects[m.name].rotation_euler.y)/360 * 4096) + "," + str(degrees(bpy.data.objects[m.name].rotation_euler.z)/360 * 4096) + "};\n" +
                    "short model"+m.name+"_isPrism = 0;\n" +
                    "long model"+m.name+"_p = 0;\n" +
                    "\n")
 
            # Write TMESH struct
            f.write("TMESH "+"model"+m.name+" = {\n")
            f.write("\t"+"model"+m.name+"_mesh,  \n")
            f.write("\t"+"model"+m.name+"_normal,\n")
            
            if len(m.uv_textures) != 0:
                for t in range(len(m.uv_textures)):
                    if m.uv_textures[0].data[0].image != None:
                        f.write("\t"+"model"+m.name+"_uv,\n")
            else:
                f.write("\t0,\n")
            
            f.write("\t"+"model"+m.name+"_color, \n")
            
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
                
            f.write("MESH mesh"+m.name+" = {\n")
            f.write("\t&model"+ m.name +",\n")
            f.write("\tmodel" + m.name + "_index,\n")
            
            if len(m.uv_textures) != 0:
                for t in range(len(m.uv_textures)):
                    if m.uv_textures[0].data[0].image != None:
                        f.write("\t&tim_"+ prefix + ",\n")
                        f.write("\t_binary_TIM_" + prefix + "_tim_start,\n") 
            else:
                f.write("\t0,\n" +
                        "\t0,\n")            
            f.write("\t&model"+m.name+"_matrix,\n" +
                    "\t&model"+m.name+"_pos,\n" +
                    "\t&model"+m.name+"_rot,\n" +
                    "\t&model"+m.name+"_isPrism,\n" +
                    "\t&model"+m.name+"_p\n")
                    
                    
            f.write("};\n\n")

        f.write("MESH * meshes[" + str(len(bpy.data.meshes)) + "] = {\n")
        for k in range(len(bpy.data.meshes)): 
            f.write("\t&mesh" + bpy.data.meshes[k].name)
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
