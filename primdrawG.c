
/*  primdrawG.c, by Schnappy, 12-2020
    
    - Draw a gouraud shaded mesh exported as a TMESH by the blender <= 2.79b plugin io_export_psx_tmesh.py
    
    based on primdraw.c by Lameguy64 (http://www.psxdev.net/forum/viewtopic.php?f=64&t=537)
	2014 Meido-Tek Productions.
	
	Demonstrates:
		- Using a primitive OT to draw triangles without libgs.
		- Using the GTE to rotate, translate, and project 3D primitives.
	
	Controls:
		Start							- Toggle interactive/non-interactive mode.
		Select							- Reset object's position and angles.
		L1/L2							- Move object closer/farther.
		L2/R2							- Rotate object (XY).
		Up/Down/Left/Right				- Rotate object (XZ/YZ).
		Triangle/Cross/Square/Circle	- Move object up/down/left/right.
		
*/

#include <sys/types.h>
#include <libgte.h>
#include <libgpu.h>
#include <libetc.h>
#include <stdio.h>

// Sample vector model
#include "cube.c"

#define HI_RES		0		// 0: 320x240, 1: 640x480

#define OT_LENGTH	3072	// Maximum number of OT entries
#define MAX_PRIMS	2048	// Maximum number of POLY_GT3 primitives

// Center screen coordinates
#if HI_RES
#define CENTERX		320
#define CENTERY		240
#else
#define CENTERX		160
#define CENTERY		120
#endif

// Display and draw environments
DISPENV disp;
DRAWENV draw;

u_long	ot[2][OT_LENGTH];		// Ordering table (contains addresses to primitives)
POLY_G3	primbuff[2][MAX_PRIMS];	// Primitive list // That's our prim buffer
int		primcnt=0;			// Primitive counter


// Prototypes
int main();


int main() {
	
	int		db	= 0; // That's db	
	#if HI_RES == 0
	RECT	ClearRect	={0,0,320,240};
	#else
	RECT	ClearRect	={0,0,640,480};
	#endif
	
	
	int		i;
	int		PadStatus;
	int		TPressed=0;
	int		AutoRotate=1;
	
	long	t, p, OTz, Flag;                // t == vertex count, p == depth cueing interpolation value, OTz ==  value to create Z-ordered OT, Flag == see LibOver47.pdf, p.143
	
	SVECTOR	Rotate={ 0 };					// Rotation coordinates
	VECTOR	Trans={ 0, 0, CENTERX, 0 };		// Translation coordinates
	
	// Scaling coordinates
	VECTOR	Scale={ ONE*(1+HI_RES), ONE*(1+HI_RES), ONE*(1+HI_RES), 0 }; // ONE == 4096, is * 2 if HI_RES == 1
	
	MATRIX	Matrix={0};						// Matrix data for the GTE
	
	
	// Reset the GPU before doing anything and the controller
	PadInit(0);
	ResetGraph(0);
	
	
	// Initialize and setup the GTE
	InitGeom();
	SetGeomOffset(CENTERX, CENTERY);        // x, y offset
	SetGeomScreen(CENTERX);                 // Distance between eye and screen  
	
	
	// Init font system
	FntLoad(960, 0);
	FntOpen(0, 0, 640, 480, 0, 512);
	
	
	// Set the display and draw environments
	#if HI_RES == 0                             // 320x240
	SetDefDispEnv(&disp, 0, 0, 320, 240);
	SetDefDrawEnv(&draw, 0, 240, 320, 240);
	#else                                       // 640x480
	SetDefDispEnv(&disp, 0, 0, 640, 480);
	SetDefDrawEnv(&draw, 0, 0, 640, 480);	
	#endif
	
	
	// Set the new display/drawing environments
	VSync(0);
	PutDispEnv(&disp);
	PutDrawEnv(&draw);
	ClearImage(&ClearRect, 0, 0, 127);          // Clear FB
	
	
	// Main loop
	while (1) {
	
		// Render the banner (FntPrint is always on top because it is not part of the OT)
		#if HI_RES
		FntPrint("\n\n");
		#endif
		FntPrint("\n\nGOURAUD SHADED TMESH EXAMPLE\n");
		FntPrint("SCHNAPPY, 2020 \n");
		FntPrint("BASED ON PRIMDRAW BY LAMEGUY64, 2014 \n");
		
		
		// Read pad status
		PadStatus = PadRead(0);
		
		if (AutoRotate == 0) {
		
			if (PadStatus & PADL1) Trans.vz -= 4;
			if (PadStatus & PADR1) Trans.vz += 4;
			if (PadStatus & PADL2) Rotate.vz -= 8;
			if (PadStatus & PADR2) Rotate.vz += 8;

			if (PadStatus & PADLup)		Rotate.vx -= 8;
			if (PadStatus & PADLdown)	Rotate.vx += 8;
			if (PadStatus & PADLleft)	Rotate.vy -= 8;
			if (PadStatus & PADLright)	Rotate.vy += 8;
			
			if (PadStatus & PADRup)		Trans.vy -= 2;
			if (PadStatus & PADRdown)	Trans.vy += 2;
			if (PadStatus & PADRleft)	Trans.vx -= 2;
			if (PadStatus & PADRright)	Trans.vx += 2;
					
			if (PadStatus & PADselect) {
				Rotate.vx = Rotate.vy = Rotate.vz = 0;
				Scale.vx = Scale.vy = Scale.vz = ONE*(1+HI_RES);
				Trans.vx = Trans.vy = 0;
				Trans.vz = CENTERX;
			}
			
		}
		
		if (PadStatus & PADstart) {
			if (TPressed == 0) {
				AutoRotate = (AutoRotate + 1) & 1;
				Rotate.vx = Rotate.vy = Rotate.vz = 0;
				Scale.vx = Scale.vy = Scale.vz = ONE*(1+HI_RES);
				Trans.vx = Trans.vy = 0;
				Trans.vz = CENTERX;
			}
			TPressed = 1;
		} else {
			TPressed = 0;
		}

		if (AutoRotate) {
			Rotate.vy += 8;	// Pan
			Rotate.vx += 8;	// Tilt
			//~ Rotate.vz += 8;	// Roll
		}
		
		
		// Clear the current OT
		ClearOTagR(&ot[db][0], OT_LENGTH);
		primcnt = 0;
		
		
		// Convert and set the matrixes
		RotMatrix(&Rotate, &Matrix);
		TransMatrix(&Matrix, &Trans);
		ScaleMatrix(&Matrix, &Scale);
		
		SetRotMatrix(&Matrix);
		SetTransMatrix(&Matrix);
		
		
		// Render the sample vector model
		t=0;
        // modelCube is a TMESH, len member == # vertices, but here it's # of triangle... So, for each tri * 3 vertices ...
		for (i = 0; i < (modelCube.len*3); i += 3) {               
			
			// Initialize the primitive and set its color values
			SetPolyG3(&primbuff[db][primcnt]);
			setRGB0(&primbuff[db][primcnt], modelCube_color[i].r, modelCube_color[i].g, modelCube_color[i].b);
			setRGB1(&primbuff[db][primcnt], modelCube_color[i+1].r, modelCube_color[i+1].g, modelCube_color[i+1].b);
			setRGB2(&primbuff[db][primcnt], modelCube_color[i+2].r, modelCube_color[i+2].g, modelCube_color[i+2].b);
			// Rotate, translate, and project the vectors and output the results into a primitive
			// RotTransPers(*vertex coordinate vector, *screen coordinates, *p (see line 69), * flag)
            OTz = RotTransPers(&modelCube_mesh[modelCube_index[t]], (long*)&primbuff[db][primcnt].x0, &p, &Flag);
            
			OTz += RotTransPers(&modelCube_mesh[modelCube_index[t+1]], (long*)&primbuff[db][primcnt].x1, &p, &Flag);
			OTz += RotTransPers(&modelCube_mesh[modelCube_index[t+2]], (long*)&primbuff[db][primcnt].x2, &p, &Flag);
			
			// Sort the primitive into the OT
			OTz /= 3;
			if ((OTz > 0) && (OTz < OT_LENGTH))
				AddPrim(&ot[db][OTz-2], &primbuff[db][primcnt]);
			
			primcnt++;
			t+=3;
			
		}
		
		
		// Prepare to switch buffers
		#if HI_RES == 0
		SetDefDispEnv(&disp, 0, 240*db, 320, 240);
		SetDefDrawEnv(&draw, 0, 240*(1-db), 320, 240);
		#endif
		

		// Wait for all drawing to finish
		DrawSync(0);
		
		// Clear the current buffer before rendering the next frame
		#if HI_RES == 0
		ClearRect.y = 240*db;
		#endif
		ClearImage(&ClearRect, 0, 0, 127);
		
		// Begin rendering the next frame
		DrawOTag(&ot[db][OT_LENGTH-1]);
		FntFlush(0);
		
		
		// Wait for VSync and then switch buffers
		VSync(0);
		#if HI_RES == 0
		PutDispEnv(&disp);
		PutDrawEnv(&draw);
		#endif
		SetDispMask(1);
		
		
		// Toggle buffer index
		#if HI_RES == 0
		db = !db;
		#endif
		
	}
	
}
