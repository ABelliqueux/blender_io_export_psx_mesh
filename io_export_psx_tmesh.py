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
        scale = 20
        f = open(os.path.normpath(self.filepath),"w+")
        for m in bpy.data.meshes:
 
            f.write("SVECTOR "+"model"+m.name+"_mesh[] = {\n")
            for i in range(len(m.vertices)):
                v = m.vertices[i].co
                f.write("\t{"+str(v.x*scale)+","+str(v.y*scale)+","+str(v.z*scale)+"}")
                if i != len(m.vertices) - 1:
                    f.write(",")
                f.write("\n")
            f.write("};\n\n")
 
            f.write("SVECTOR "+"model"+m.name+"_normal[] = {\n")
            for i in range(len(m.polygons)):
                poly = m.polygons[i]
                f.write("\t"+str(poly.normal.x)+","+str(poly.normal.y)+","+str(poly.normal.z)+",0")
                if i != len(m.polygons) - 1:
                    f.write(",")
                f.write("\n")
            f.write("};\n\n")
 
            f.write("CVECTOR "+"model"+m.name+"_color[] = {\n")
            
            # If vertex colors exist, use them
            if len(m.vertex_colors) != 0:           
                colors = m.vertex_colors["Col"].data
                for i in range(len(colors)):
                    f.write("\t"+str(int(colors[i].color.r*255))+","+str(int(colors[i].color.g*255))+","+str(int(colors[i].color.b*255))+", 0")
                    if i != len(colors) - 1:
                        f.write(",")
                    f.write("\n")
            # If no vertex colors, default to 2 whites, 1 grey
            else:                                  
                for i in range(len(m.polygons) * 3):
                    if i % 3 == 0:
                        f.write("\t200,200,200,0")  # Let's add a bit more relief with a shade of grey
                    else:
                        f.write("\t255,255,255,0")
                    if i != (len(m.polygons) * 3) - 1:
                        f.write(",")
                    f.write("\n")
            f.write("};\n\n")
 
            f.write("int "+"model"+m.name+"_index[] = {\n")
            for i in range(len(m.polygons)):
                poly = m.polygons[i]
                f.write("\t"+str(poly.vertices[0])+","+str(poly.vertices[1])+","+str(poly.vertices[2]))
                if i != len(m.polygons) - 1:
                    f.write(",")
                f.write("\n")
            f.write("};\n\n")
 
            
            f.write("TMESH "+"model"+m.name+" = {\n")
            f.write("\t"+"model"+m.name+"_mesh,\n")
            f.write("\t"+"model"+m.name+"_normal,\n")
            f.write("\t0,\n")
            f.write("\t"+"model"+m.name+"_color,\n")
            # According to libgte.h, TMESH.len should be # of vertices. Meh...
            f.write("\t"+str(len(m.polygons))+"\n")
            f.write("};\n")
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
