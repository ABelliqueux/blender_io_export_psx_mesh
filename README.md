# blender_io_export_psx_mesh

Blender <= 2.79c plugin to export a PSX mesh to an array in a C file.

# Install

Put the `io_export_psx_mesh.py` file in the addons folder of blender 2.79 :

On Linux, that's :

`~/.config/blender/2.79/scripts/addons`

# Steps to load your mesh 

Your mesh must be vertex colored for the plugin to work, and triangulated before export (Use & apply a triangulate modifier)

Get the example by Lameguy64 from [here](http://psx.arthus.net/code/primdraw.7z)

Edit the file to reflect the values in your exported .c file :

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
