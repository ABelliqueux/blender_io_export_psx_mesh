
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
 /*		   PSX screen coordinate system 
 *
 *                           Z+
 *                          /
 *                         /
 *                        +------X+
 *                       /|
 *                      / |
 *                     /  Y+
 *                   eye		*/

#include <sys/types.h>
#include <libgte.h>
#include <libgpu.h>
#include <libetc.h>
#include <stdio.h>

// Sample vector model
#include "cube.c"

#define HI_RES		0		// 0: 320x240, 1: 640x480
#define VMODE       1
#define OT_LENGTH	2048	// Maximum number of OT entries
#define MAX_PRIMS	1024	// Maximum number of POLY_GT3 primitives

// Center screen coordinates
#define SCREENXRES 320
#define SCREENYRES 240

#define CENTERX		SCREENXRES/2
#define CENTERY		SCREENYRES/2

// Display and draw environments
DISPENV disp;
DRAWENV draw;

u_long	ot[2][OT_LENGTH];		// Ordering table (contains addresses to primitives)
POLY_GT3	primbuff[2][MAX_PRIMS];	// Primitive list // That's our prim buffer
int		primcnt=0;			    // Primitive counter
int		db	= 0;                // Current buffer counter

RECT	ClearRect	={0,0,320,240};

//~ extern unsigned long _binary_TIM_bousai_tim_start[];
//~ extern unsigned long _binary_TIM_bousai_tim_end[];
//~ extern unsigned long _binary_TIM_bousai_tim_length;

//~ TIM_IMAGE bousai;


// Prototypes
void init();
void LoadTexture(u_long * tim, TIM_IMAGE * tparam);

void init(){
    // Reset the GPU before doing anything and the controller
	PadInit(0);
	ResetGraph(0);
	
	
	// Initialize and setup the GTE
	InitGeom();
	SetGeomOffset(CENTERX, CENTERY);        // x, y offset
	SetGeomScreen(CENTERX);                 // Distance between eye and screen  
	
    
	// Set the display and draw environments
	SetDefDispEnv(&disp, 0, 0, SCREENXRES, SCREENYRES);
	SetDefDrawEnv(&draw, 0, SCREENYRES, SCREENXRES, SCREENYRES);
    
    if (VMODE)
    {
        SetVideoMode(MODE_PAL);
        disp.screen.y += 8;
        }
	
	// Set the new display/drawing environments
	VSync(0);
	
    PutDispEnv(&disp);
	PutDrawEnv(&draw);
	
    ClearImage(&ClearRect, 0, 0, 127);          // Clear FB
	
	// Init font system
	FntLoad(960, 0);
	FntOpen(16, 16, 196, 64, 0, 256);
	
    }
    
void LoadTexture(u_long * tim, TIM_IMAGE * tparam){     // This part is from Lameguy64's tutorial series : lameguy64.net/svn/pstutorials/chapter1/3-textures.html login/pw: annoyingmous
		OpenTIM(tim);                                   // Open the tim binary data, feed it the address of the data in memory
		ReadTIM(tparam);                                // This read the header of the TIM data and sets the corresponding members of the TIM_IMAGE structure
		
        LoadImage(tparam->prect, tparam->paddr);        // Transfer the data from memory to VRAM at position prect.x, prect.y
		DrawSync(0);                                    // Wait for the drawing to end
		
		if (tparam->mode & 0x8){ // check 4th bit       // If 4th bit == 1, TIM has a CLUT
			LoadImage(tparam->crect, tparam->caddr);    // Load it to VRAM at position crect.x, crect.y
			DrawSync(0);                                // Wait for drawing to end
	}

}

int main() {
		
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
	
    
    draw.tw.w = 32; 
    draw.tw.h = 32; 

    
	init();
    
	LoadTexture(_binary_TIM_cube_tim_start, &tim_cube);
	// Main loop
	while (1) {
	
		// Render the banner (FntPrint is always on top because it is not part of the OT)
		//~ #if HI_RES
		//~ FntPrint("\n\n");
		//~ #endif
		//~ FntPrint("\n\nGOURAUD SHADED TMESH EXAMPLE\n");
		//~ FntPrint("SCHNAPPY, 2020 \n");
		//~ FntPrint("BASED ON PRIMDRAW BY LAMEGUY64, 2014 \n");
		
		
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
			SetPolyGT3(&primbuff[db][primcnt]);
			setRGB0(&primbuff[db][primcnt], modelCube.c[i].r, modelCube.c[i].g, modelCube.c[i].b);
			setRGB1(&primbuff[db][primcnt], modelCube.c[i+1].r, modelCube.c[i+1].g, modelCube.c[i+1].b);
			setRGB2(&primbuff[db][primcnt], modelCube.c[i+2].r, modelCube.c[i+2].g, modelCube.c[i+2].b);
			
            ((POLY_GT3 *)&primbuff[db][primcnt])->tpage = getTPage(tim_cube.mode&0x3, 0,
                                                                   tim_cube.prect->x,
                                                                   tim_cube.prect->y);

            setUV3(&primbuff[db][primcnt], modelCube.u[i].vx, modelCube.u[i].vy,
                                           modelCube.u[i+1].vx, modelCube.u[i+1].vy,
                                           modelCube.u[i+2].vx, modelCube.u[i+2].vy);
                                           
            //~ FntPrint("%d %d %d %d %d %d\n", modelCube.u[i].vx, modelCube.u[i].vy,
                                           //~ modelCube.u[i+1].vx, modelCube.u[i+1].vy,
                                           //~ modelCube.u[i+2].vx, modelCube.u[i+2].vy);
            // Rotate, translate, and project the vectors and output the results into a primitive

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
        
		//~ t=0;
        //~ // modelCube is a TMESH, len member == # vertices, but here it's # of triangle... So, for each tri * 3 vertices ...
		//~ for (i = 0; i < (modelPlan.len*3); i += 3) {               
			
			//~ // Initialize the primitive and set its color values
			//~ SetPolyG3(&primbuff[db][primcnt]);
			//~ setRGB0(&primbuff[db][primcnt], modelPlan.c[i].r, modelPlan.c[i].g, modelPlan.c[i].b);
			//~ setRGB1(&primbuff[db][primcnt], modelPlan.c[i+1].r, modelPlan.c[i+1].g, modelPlan.c[i+1].b);
			//~ setRGB2(&primbuff[db][primcnt], modelPlan.c[i+2].r, modelPlan.c[i+2].g, modelPlan.c[i+2].b);
			
            //~ // Rotate, translate, and project the vectors and output the results into a primitive

            //~ OTz = RotTransPers(&modelPlan_mesh[modelPlan_index[t]], (long*)&primbuff[db][primcnt].x0, &p, &Flag);
            
			//~ OTz += RotTransPers(&modelPlan_mesh[modelPlan_index[t+1]], (long*)&primbuff[db][primcnt].x1, &p, &Flag);
			//~ OTz += RotTransPers(&modelPlan_mesh[modelPlan_index[t+2]], (long*)&primbuff[db][primcnt].x2, &p, &Flag);
			
			//~ // Sort the primitive into the OT
			//~ OTz /= 3;
			//~ if ((OTz > 0) && (OTz < OT_LENGTH))
				//~ AddPrim(&ot[db][OTz-2], &primbuff[db][primcnt]);
			
			//~ primcnt++;
			//~ t+=3;
			
		//~ }
		
		
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
    return 0;
}
