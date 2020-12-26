import os
import bpy
 
bl_info = {
    "name":         "PSX mesh",
    "author":       "TheDukeOfZill",
    "blender":      (2,6,9),
    "version":      (0,0,1),
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
            for i in range(len(m.polygons)):
                colors = m.vertex_colors["Col"].data
                f.write("\t"+str(int(colors[i*3].color.r*255))+","+str(int(colors[i*3].color.g*255))+","+str(int(colors[i*3].color.b*255))+", 0")
                if i != len(m.polygons) - 1:
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
