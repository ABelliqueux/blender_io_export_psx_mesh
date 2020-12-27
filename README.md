# blender_io_export_psx_mesh

Blender <= 2.79c plugin to export a PSX mesh to a C file.

Specifically, it generates a C file containing :

  * an array of SVECTOR containing the vertices coordinates
  * an array of SVECTOR containing the normals
  * an array of CVECTOR containg the color of each vertex
  * an array of int that describe the relation between the tri meshes
  * a TMESH struct to ease access to those arrays

From `libgte.h`  :

```c
typedef struct {
        SVECTOR         *v;                     /*shared vertices*/
        SVECTOR         *n;                     /*shared normals*/
        SVECTOR         *u;                     /*shared texture addresses*/
        CVECTOR         *c;                     /*shared colors*/
        u_long          len;                    /*mesh length(=#vertex)*/
} TMESH;

```

# Install

Put the `io_export_psx_mesh.py` file in the addons folder of blender 2.79 :

On Linux, that's :

`~/.config/blender/2.79/scripts/addons`

# Steps to load your mesh 

  1. You must first triangulate your mesh (manually or via the modifier).
    
  2. When your model is ready, you can then vertex paint it. If you don't, the vertices colors will default to white.
  
  * If you modify your geometry *after* vertex painting, the plugin will faile to export the mesh. This is because the vertex color data is set to 0 each time you modify your geometry.
  
  3. Get the example code by Lameguy64 from [here](http://psx.arthus.net/code/primdraw.7z)

  4. Edit the `primdraw.c` file 
  
  * lines 29 and 30 to reflect the number of tris you want to be able to draw 
  
```c
#define OT_LENGTH	2048	// Maximum number of OT entries
#define MAX_PRIMS	1024	// Maximum number of POLY_FT3 primitives
```
seem to be safe values.
  
  
  
  * to reflect the values in your exported .c file :

For example, if you export the start cube after vertex painting and triangulation :

lines 190 to 199 of the original file :

```c
		for (i=0; i<vec.len; i++) { 
			
			// Initialize the primitive and set its color values
			SetPolyF3(&myPrims[ActivePage][myPrimNum]);
			setRGB0(&myPrims[ActivePage][myPrimNum], vec_color[i].r, vec_color[i].g, vec_color[i].b);
			
			// Rotate, translate, and project the vectors and output the results into a primitive
			OTz = RotTransPers(&vec_mesh[t], (long*)&myPrims[ActivePage][myPrimNum].x0, &p, &Flag);
			OTz += RotTransPers(&vec_mesh[t+1], (long*)&myPrims[ActivePage][myPrimNum].x1, &p, &Flag);
			OTz += RotTransPers(&vec_mesh[t+2], (long*)&myPrims[ActivePage][myPrimNum].x2, &p, &Flag);
```

become :

```c
		for (i=0; i<modelCube.len; i++) {
			
			// Initialize the primitive and set its color values
			SetPolyF3(&myPrims[ActivePage][myPrimNum]);
			setRGB0(&myPrims[ActivePage][myPrimNum], modelCube_color[i].r, modelCube_color[i].g, modelCube_color[i].b);
			
			// Rotate, translate, and project the vectors and output the results into a primitive
            OTz = RotTransPers(&modelCube_mesh[modelCube_index[t]], (long*)&myPrims[ActivePage][myPrimNum].x0, &p, &Flag);
			OTz += RotTransPers(&modelCube_mesh[modelCube_index[t+1]], (long*)&myPrims[ActivePage][myPrimNum].x1, &p, &Flag);
			OTz += RotTransPers(&modelCube_mesh[modelCube_index[t+2]], (long*)&myPrims[ActivePage][myPrimNum].x2, &p, &Flag);

```

# Credits

Author of the code example is [Lameguy64](https://github.com/Lameguy64)
Original author of the plugin is TheDukeOfZill, 04-2014

Original post : http://www.psxdev.net/forum/viewtopic.php?f=64&t=537&sid=f5d30dcfdef34bc9f4d644033ba93a98
