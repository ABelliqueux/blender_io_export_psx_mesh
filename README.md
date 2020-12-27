![Pic or it didn't happen](primdrawG.jpg)

# blender_io_export_psx_tmesh

Blender <= 2.79c plugin to export a gouraud shaded PSX mesh to a C file.

Specifically, it generates a C file containing :

  * an array of SVECTOR containing the vertices coordinates
  * an array of SVECTOR containing the normals
  * an array of CVECTOR containing the color of each vertex
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

# Install the plugin

Put the `io_export_psx_tmesh.py` file in the addons folder of blender 2.79 :

On Linux, that's :

`~/.config/blender/2.79/scripts/addons`

# Steps to load your mesh 

  1. You must first triangulate your mesh (manually or via the modifier).
    
  2. When your model is ready, you can then vertex paint it. If you don't, the vertices colors will default to white.
  
  * If you modify your geometry *after* vertex painting, the plugin will faile to export the mesh. This is because the vertex color data is set to 0 each time you modify your geometry.

  3. If needed, edit the `primdraw.c` file , lines 29 and 30,  to reflect the number of tris you want to be able to draw ( ~750 in NTSC, ~910 in PAL )
  
```c
#define OT_LENGTH	2048	// Maximum number of OT entries
#define MAX_PRIMS	1024	// Maximum number of POLY_GT3 primitives, should be equal to at least your # of tris * 3 
```
seem to be safe values.

# Compiling

The provided `Makefile`  uses the [Nugget+PsyQ setup](https://github.com/ABelliqueux/nolibgs_hello_worlds#setting-up-the-sdk--modern-gcc--psyq-aka-nuggetpsyq).

Create a folder in `(...)/pcsx-redux/src/mips/`, put the `Makefile`, `cube.c` and `primdrawG.c` in it, then in a terminal, just type `make` to build the ps-exe.

# Credits

Based on the [code](https://pastebin.com/suU9DigB) provided by TheDukeOfZill, 04-2014, on http://www.psxdev.net/forum/viewtopic.php?f=64&t=537#p4088

PSX code based on [example](http://psx.arthus.net/code/primdraw.7z) by [Lameguy64](https://github.com/Lameguy64)
