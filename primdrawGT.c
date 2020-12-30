/*  primdrawG.c, by Schnappy, 12-2020
    
    - Draw a gouraud shaded, UV textured mesh exported by the blender <= 2.79b plugin io_export_psx_tmesh.py
    
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
#include "coridor.c"

#define VMODE       0
#define HAS_TEX       0

#define SCREENXRES 320
#define SCREENYRES 240

#define CENTERX		SCREENXRES/2
#define CENTERY		SCREENYRES/2

#define OTLEN	    2048	    // Maximum number of OT entries
#define PRIMBUFFLEN	1024 * sizeof(POLY_GT3)	    // Maximum number of POLY_GT3 primitives

// Display and draw environments, double buffered
DISPENV disp[2];
DRAWENV draw[2];

u_long	    ot[2][OTLEN];   		        // Ordering table (contains addresses to primitives)
char	primbuff[2][PRIMBUFFLEN] = {0};	// Primitive list // That's our prim buffer

//~ int		    primcnt=0;			            // Primitive counter

char * nextpri = primbuff[0];			            // Primitive counter

char		    db	= 0;                        // Current buffer counter

short vs;
//~ RECT	ClearRect	={0,0,320,240};

//~ extern unsigned long _binary_TIM_bousai_tim_start[];
//~ extern unsigned long _binary_TIM_bousai_tim_end[];
//~ extern unsigned long _binary_TIM_bousai_tim_length;

//~ TIM_IMAGE bousai;

//~ static int frame = 0;

// Prototypes
void init(void);
void display(void);
void LoadTexture(u_long * tim, TIM_IMAGE * tparam);

void init(){
    // Reset the GPU before doing anything and the controller
	PadInit(0);
	ResetGraph(0);
	
	// Initialize and setup the GTE
	InitGeom();
	SetGeomOffset(CENTERX, CENTERY);        // x, y offset
	SetGeomScreen(CENTERX*2);                 // Distance between eye and screen  
	
    	// Set the display and draw environments
	SetDefDispEnv(&disp[0], 0, 0         , SCREENXRES, SCREENYRES);
	SetDefDispEnv(&disp[1], 0, SCREENYRES, SCREENXRES, SCREENYRES);
    
	SetDefDrawEnv(&draw[0], 0, SCREENYRES, SCREENXRES, SCREENYRES);
	SetDefDrawEnv(&draw[1], 0, 0, SCREENXRES, SCREENYRES);
    
    if (VMODE)
    {
        SetVideoMode(MODE_PAL);
        disp[0].screen.y += 8;
        disp[1].screen.y += 8;
    }
	
    setRGB0(&draw[0], 80, 80, 255);
    setRGB0(&draw[1], 80, 80, 255);

    draw[0].isbg = 1;
    draw[1].isbg = 1;

    PutDispEnv(&disp[db]);
	PutDrawEnv(&draw[db]);
		
	// Init font system
	FntLoad(960, 0);
	FntOpen(16, 16, 196, 64, 0, 256);
	
    }

void display(void){
    
    DrawSync(0);
    vs = VSync(0);

    PutDispEnv(&disp[db]);
    PutDrawEnv(&draw[db]);

    SetDispMask(1);
    
    DrawOTag(ot[db] + OTLEN - 1);
    
    db = !db;

    nextpri = primbuff[db];
    
        
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
	
    POLY_GT3 *poly = {0};                           // pointer to a POLY_G4 

    
	SVECTOR	Rotate={ 0 };					// Rotation coordinates
	VECTOR	Trans={ 0, 0, CENTERX*2, 0 };		// Translation coordinates
                                            // Scaling coordinates
	VECTOR	Scale={ ONE, ONE, ONE, 0 };     // ONE == 4096
	MATRIX	Matrix={0};						// Matrix data for the GTE
	
    // Texture window
    
    DR_MODE * dr_mode;                        // Pointer to dr_mode prim
    
    RECT tws = {0, 0, 32, 32};            // Texture window coordinates : x, y, w, h
                
	init();
    
    for (int k = 0; k < sizeof(meshes)/sizeof(TMESH *); k++){
        LoadTexture(meshes[k]->tim_data, meshes[k]->tim);
    }
    
	// Main loop
	while (1) {
    //~ while ((VSync(-1) - frame) < 1){
	
		// Read pad status
		PadStatus = PadRead(0);
		
		if (AutoRotate == 0) {
		
			if (PadStatus & PADL1) Trans.vz -= 4;
			if (PadStatus & PADR1) Trans.vz += 4;
			if (PadStatus & PADL2) Rotate.vz -= 8;
			if (PadStatus & PADR2) Rotate.vz += 8;

			if (PadStatus & PADLup)		Rotate.vx -= 8;
			if (PadStatus & PADLdown)	Rotate.vx += 8;
			if (PadStatus & PADLleft)	Rotate.vy -= 14;
			if (PadStatus & PADLright)	Rotate.vy += 14;
			
			if (PadStatus & PADRup)		Trans.vy -= 2;
			if (PadStatus & PADRdown)	Trans.vy += 2;
			if (PadStatus & PADRleft)	Trans.vx -= 2;
			if (PadStatus & PADRright)	Trans.vx += 2;
					
			if (PadStatus & PADselect) {
				Rotate.vx = Rotate.vy = Rotate.vz = 0;
				Scale.vx = Scale.vy = Scale.vz = ONE;
				Trans.vx = Trans.vy = 0;
				Trans.vz = CENTERX;
			}
			
		}
		
		if (PadStatus & PADstart) {
			if (TPressed == 0) {
				AutoRotate = (AutoRotate + 1) & 1;
				Rotate.vx = Rotate.vy = Rotate.vz = 0;
				Scale.vx = Scale.vy = Scale.vz = ONE;
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
		ClearOTagR(ot[db], OTLEN);
        
		// Convert and set the matrixes
		RotMatrix(&Rotate, &Matrix);
		TransMatrix(&Matrix, &Trans);
		ScaleMatrix(&Matrix, &Scale);
		
		SetRotMatrix(&Matrix);
		SetTransMatrix(&Matrix);
		
		for (int k = 0; k < sizeof(meshes)/sizeof(TMESH *); k++){
        
            // Render the sample vector model
            t=0;
            
            // modelCube is a TMESH, len member == # vertices, but here it's # of triangle... So, for each tri * 3 vertices ...
            for (i = 0; i < (meshes[0]->tmesh->len * 3); i += 3) {               
                
                poly = (POLY_GT3 *)nextpri;
                
                // Initialize the primitive and set its color values
                
                SetPolyGT3(poly);
                
                setRGB0(poly, meshes[k]->tmesh->c[i].r  , meshes[k]->tmesh->c[i].g  , meshes[k]->tmesh->c[i].b);
                setRGB1(poly, meshes[k]->tmesh->c[i+1].r, meshes[k]->tmesh->c[i+1].g, meshes[k]->tmesh->c[i+1].b);
                setRGB2(poly, meshes[k]->tmesh->c[i+2].r, meshes[k]->tmesh->c[i+2].g, meshes[k]->tmesh->c[i+2].b);
                
                ((POLY_GT3 *)poly)->tpage = getTPage(meshes[k]->tim->mode&0x3, 0,
                                                     meshes[k]->tim->prect->x,
                                                     meshes[k]->tim->prect->y
                                                    );
                // The TIMs are loaded in vram vertically on the same TPAGE; eg. Tim1 640,0, Tim1 640, 128
                // We then add tim_image.prect.y to the y coord of the uvs to use the correct texture.
                 
                setUV3(poly, meshes[k]->tmesh->u[i].vx  , meshes[k]->tmesh->u[i].vy   + meshes[k]->tim->prect->y,
                             meshes[k]->tmesh->u[i+1].vx, meshes[k]->tmesh->u[i+1].vy + meshes[k]->tim->prect->y,
                             meshes[k]->tmesh->u[i+2].vx, meshes[k]->tmesh->u[i+2].vy + meshes[k]->tim->prect->y);
                             
                // Rotate, translate, and project the vectors and output the results into a primitive

                OTz  = RotTransPers(&meshes[k]->tmesh->v[meshes[k]->index[t]]  , (long*)&poly->x0, &p, &Flag);
                OTz += RotTransPers(&meshes[k]->tmesh->v[meshes[k]->index[t+1]], (long*)&poly->x1, &p, &Flag);
                OTz += RotTransPers(&meshes[k]->tmesh->v[meshes[k]->index[t+2]], (long*)&poly->x2, &p, &Flag);
                
                
                // Using RotTransPers3 is a bit faster (-31ms/frame), but you loose precision for Z-ordering
                //~ OTz = RotTransPers3(
                        //~ &meshes[k]->tmesh->v[meshes[k]->index[t]],  
                        //~ &meshes[k]->tmesh->v[meshes[k]->index[t+1]],
                        //~ &meshes[k]->tmesh->v[meshes[k]->index[t+2]],
                        //~ (long*)&poly->x0, (long*)&poly->x1, (long*)&poly->x2,
                        //~ &p,
                        //~ &Flag
                        //~ );
                
                // Sort the primitive into the OT
                OTz /= 3;
                if ((OTz > 0) && (OTz < OTLEN))
                    AddPrim(&ot[db][OTz-2], poly);
                
                nextpri += sizeof(POLY_GT3);
                
                t+=3;
                
            }
        }
        
        //~ dr_mode = (DR_MODE *)nextpri;
        
        //~ setDrawMode(dr_mode,1,0, getTPage(tim_cube.mode&0x3, 0,
                                          //~ tim_cube.prect->x,
                                          //~ tim_cube.prect->y), &tws);  //set texture window
    
        //~ AddPrim(&ot[db], dr_mode);
        
        //~ nextpri += sizeof(DR_MODE);
        
        	// Render the banner (FntPrint is always on top because it is not part of the OT)
		//~ #if HI_RES
		//~ FntPrint("\n\n");
		//~ #endif
		//~ FntPrint("\n\nGOURAUD SHADED TMESH EXAMPLE\n");
		//~ FntPrint("SCHNAPPY, 2020 \n");
		//~ FntPrint("BASED ON PRIMDRAW BY LAMEGUY64, 2014 \n");
		FntPrint("# tris :%d \n", sizeof(ot[db])/sizeof(POLY_GT3));
		FntPrint("Vsync :%d \n", vs);	
		FntPrint("%d ", sizeof(meshes)/sizeof(TMESH *));	
		FntPrint("%d ", meshes[0]->tim->prect->y);	
        
        FntFlush(-1);
		
		display();

        //~ frame = VSync(-1);

	}
    return 0;
}
