/*  primdrawG.c, by Schnappy, 12-2020
    
    - Draw a gouraud shaded, UV textured mesh exported by the blender <= 2.79b plugin io_export_psx_tmesh.py
    
    * added depth cueing use with fog farcolor
    * switched to double buffer
    * switched to vsync callback for pad input
    
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

// Precalculated sin/cos values
#include "psin.c"
#include "pcos.c"

// Sample model
#include "coridor.c"

#define VMODE       0                           // 0: NTSC, 1: PAL

#define SCREENXRES 320
#define SCREENYRES 240

#define CENTERX		SCREENXRES/2
#define CENTERY		SCREENYRES/2

#define OTLEN	    2048	                    // Maximum number of OT entries
#define PRIMBUFFLEN	1024 * sizeof(POLY_GT3)	    // Maximum number of POLY_GT3 primitives

// Display and draw environments, double buffered
DISPENV disp[2];
DRAWENV draw[2];

u_long	    ot[2][OTLEN]  = {0};   		        // Ordering table (contains addresses to primitives)
char	primbuff[2][PRIMBUFFLEN] = {0};	        // Primitive list // That's our prim buffer

char * nextpri = primbuff[0];			        // Primitive counter

char		    db	= 0;                        // Current buffer counter

short vs;

int		PadStatus;

typedef struct{
    int x, xv;                                  // x: current value += vx : new value 
    int y, yv;
    int z, zv;
    int pan, panv;                              // horizontal rotation
    int tilt, tiltv;                            // vertical rotation
    int rol;                                    // lateral rotation

    VECTOR pos;                                 // camera current pos vector
    SVECTOR rot;                                // camera current rot vector

    MATRIX mat;
} CAMERA;

CAMERA camera = {0};

// Prototypes
void init(void);
void display(void);
void applyCamera(CAMERA * cam);
void applyOrbCam(MESH * mesh);
void LoadTexture(u_long * tim, TIM_IMAGE * tparam);
void callback(void);

int main() {
		
	int		i;
	
	long	t, p, OTz, Flag;                        // t == vertex count, p == depth cueing interpolation value, OTz ==  value to create Z-ordered OT, Flag == see LibOver47.pdf, p.143
	
    POLY_GT3 * poly;                                // pointer to a POLY_GT3 

    MATRIX  PolyMatrix = {0};                       // global transformation matrix
    
    CVECTOR outCol, outCol1, outCol2 = {0,0,0,0};   // Holds vertices colors with depth cueing applied
    
	init();

    VSyncCallback(callback);                        // pad is read on vsync callback
    
    SetFarColor(20, 20, 40);                        // vertices colors are mixed with farcolor depending on p value
    SetFogNearFar(1200, 3000,SCREENXRES);           // fog distance thresholds 
    
    for (int k = 0; k < sizeof(meshes)/sizeof(TMESH *); k++){
        LoadTexture(meshes[k]->tim_data, meshes[k]->tim);       
    }

    // Set Camera starting pos and rot
    
    camera.xv = -ONE * -89;
    camera.yv = -ONE * 59;
    camera.zv = -ONE * 133;

    camera.tiltv = 232 ;
    camera.panv = -336;

    applyCamera(&camera);

	// Main loop
	while (1) {
        
        
        // Local Transform
        
        meshes[2]->rot->vy -= 28;   // rotate small cube
        meshes[1]->rot->vy += 28;   // rotate blue monolith thingy
        
        
        //World Translations
        
        meshes[1]->pos->vz = meshes[1]->pos->vz + (pcos[VSync(-1)%1024]/768 ); // move blue monolith thingy
        meshes[1]->pos->vx = meshes[1]->pos->vx + (psin[VSync(-1)%1024]/768 );        
        
        // Camera setup 
        
        camera.pos.vx = -(camera.x/ONE);
        camera.pos.vy = -(camera.y/ONE);
        camera.pos.vz = -(camera.z/ONE);
        
        camera.rot.vx = camera.tilt;
        camera.rot.vy = -camera.pan;
        
        applyCamera(&camera);
        
		// Clear the current OT
		ClearOTagR(ot[db], OTLEN);
		
		for (int k = 0; k < sizeof(meshes)/sizeof(meshes[0]); k++){
        
            // Render the sample vector model
            t=0;
            
            // modelCube is a TMESH, len member == # vertices, but here it's # of triangle... So, for each tri * 3 vertices ...
            for (i = 0; i < (meshes[k]->tmesh->len * 3); i += 3) {               
                
                poly = (POLY_GT3 *)nextpri;
                
                
                
                RotMatrix(meshes[k]->rot, meshes[k]->mat);                  // Apply mesh rotation to matrix 

                TransMatrix(meshes[k]->mat, meshes[k]->pos);                // Apply mesh translation to matrix 
                
                CompMatrixLV(&camera.mat, meshes[k]->mat, &PolyMatrix);     // Make a composite matrix from cam matrix + meshes matrices
                
                SetRotMatrix(&PolyMatrix);                                   // Set rotation matrix
                
                SetTransMatrix(&PolyMatrix);                                 // Set Transmatrix matrix

                // Draw meshes

                SetPolyGT3(poly);
                
                DpqColor3(&meshes[k]->tmesh->c[i],&meshes[k]->tmesh->c[i+1],&meshes[k]->tmesh->c[i+2], *meshes[k]->p,
                          &outCol,&outCol1,&outCol2 
                        );              
                        
                setRGB0(poly, outCol.r, outCol.g  , outCol.b);
                setRGB1(poly, outCol1.r, outCol1.g, outCol1.b);
                setRGB2(poly, outCol2.r, outCol2.g, outCol2.b);
                                

                // WIP : Trying to use the draw area as a texture to create pseudo refraction effect
                if (*meshes[k]->isPrism){ 
                    ((POLY_GT3 *)poly)->tpage = getTPage(meshes[k]->tim->mode&0x3, 0,
                                                         0,                                 
                                                         320
                    );
                    setUV3(poly, 32, 32,
                                 32, 220,
                                 220,220);
                } else {
                    
                    ((POLY_GT3 *)poly)->tpage = getTPage(meshes[k]->tim->mode&0x3, 0,
                                                     meshes[k]->tim->prect->x,
                                                     meshes[k]->tim->prect->y
                    );
                }
                    
                     setUV3(poly, meshes[k]->tmesh->u[i].vx  , meshes[k]->tmesh->u[i].vy   + meshes[k]->tim->prect->y,
                                  meshes[k]->tmesh->u[i+1].vx, meshes[k]->tmesh->u[i+1].vy + meshes[k]->tim->prect->y,
                                  meshes[k]->tmesh->u[i+2].vx, meshes[k]->tmesh->u[i+2].vy + meshes[k]->tim->prect->y);
                //~ }
                
                // Rotate, translate, and project the vectors and output the results into a primitive

                OTz  = RotTransPers(&meshes[k]->tmesh->v[meshes[k]->index[t]]  , (long*)&poly->x0, meshes[k]->p, &Flag);                
                OTz += RotTransPers(&meshes[k]->tmesh->v[meshes[k]->index[t+1]], (long*)&poly->x1, meshes[k]->p, &Flag);
                OTz += RotTransPers(&meshes[k]->tmesh->v[meshes[k]->index[t+2]], (long*)&poly->x2, meshes[k]->p, &Flag);                
                
                // Using RotTransPers3 is a bit faster (-31ms/frame), but you loose precision for Z-ordering
                //~ OTz = RotTransPers3(
                        //~ &meshes[k]->tmesh->v[meshes[k]->index[t]],  
                        //~ &meshes[k]->tmesh->v[meshes[k]->index[t+1]],
                        //~ &meshes[k]->tmesh->v[meshes[k]->index[t+2]],
                        //~ (long*)&poly->x0, (long*)&poly->x1, (long*)&poly->x2,
                        //~ meshes[k]->p,
                        //~ &Flag
                        //~ );
                
                // Sort the primitive into the OT
                OTz /= 3;
                if ((OTz > 0) && (OTz < OTLEN) && (*meshes[k]->p < 3588)){
                    AddPrim(&ot[db][OTz-2], poly);
                }
                nextpri += sizeof(POLY_GT3);
                
                t+=3;
            }
        }
                
		//~ FntPrint("BASED ON PRIMDRAW BY LAMEGUY64, 2014 \n");
		FntPrint("#Tris :%d \n", sizeof(ot[db])/sizeof(POLY_GT3));
		FntPrint("Vsync :%d \n", VSync(0));	
		FntPrint("#Meshes %d\n", sizeof(meshes)/sizeof(TMESH *));	
		FntPrint("Cam pos : %d, %d, %d\n", camera.pos.vx, camera.pos.vy, camera.pos.vz);	
		FntPrint("Cam or : %d, %d", camera.tilt, camera.pan);	
        
        FntPrint("\np:%d", *meshes[0]->p);
        FntPrint("\n%d %d", meshes[1]->pos->vx, meshes[1]->pos->vz);
        FntPrint("\n%d %d", *meshes[0]->isPrism, *meshes[1]->isPrism);
        
        FntFlush(-1);
		
		display();

	}
    return 0;
}

void init(){
    // Reset the GPU before doing anything and the controller
	PadInit(0);
	ResetGraph(0);
	
	// Initialize and setup the GTE
	InitGeom();
	SetGeomOffset(CENTERX, CENTERY);        // x, y offset
	SetGeomScreen(CENTERX);                 // Distance between eye and screen  
	
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
	
    setRGB0(&draw[0], 0, 0, 0);
    setRGB0(&draw[1], 0, 0, 0);

    draw[0].isbg = 1;
    draw[1].isbg = 1;

    PutDispEnv(&disp[db]);
	PutDrawEnv(&draw[db]);
		
	// Init font system
	FntLoad(960, 0);
	FntOpen(16, 16, 196, 96, 0, 512);
	
    }

void display(void){
    
    DrawSync(0);
    vs = VSync(-1);

    PutDispEnv(&disp[db]);
    PutDrawEnv(&draw[db]);

    SetDispMask(1);
    
    DrawOTag(ot[db] + OTLEN - 1);
    
    db = !db;

    nextpri = primbuff[db];
    
        
    }

void applyCamera(CAMERA * cam){
    VECTOR vec;                                         // Vector that holds the output values of the following instructions

    RotMatrix(&cam->rot, &cam->mat);                    // Convert rotation angle in psx units (360° == 4096) to rotation matrix)
    
    ApplyMatrixLV(&cam->mat, &cam->pos, &vec);          // Multiply matrix by vector pos and output to vec

    TransMatrix(&cam->mat, &vec);                       // Apply transform vector
    
    SetRotMatrix(&cam->mat);                            // Set Rotation matrix
    SetTransMatrix(&cam->mat);                          // Set Transform matrix
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

void callback(void){
    
    PadStatus = PadRead(0);
	
	// Camera panning
	if (PadStatus & PADLup)		camera.tiltv += 8;
	if (PadStatus & PADLdown)	camera.tiltv -= 8;  
	if (PadStatus & PADLleft)	camera.panv -= 12;
	if (PadStatus & PADLright)	camera.panv += 12;
	
	// Camera movement
	if (PadStatus & PADRup) {
        camera.zv += (ccos(camera.pan) * ccos(camera.tilt)) / 1024;     // pan = horizontal motion, tilt = vertical.  cos(pan) returns value in rang -ONE,ONE on the horiz. axis. -4096-0 = left, 0-4096 = right
		camera.xv += (csin(camera.pan) * ccos(camera.tilt)) / 1024;     
        camera.yv += (csin(camera.tilt) * ccos(camera.tilt)) / 1024;
	}

	if (PadStatus & PADRdown) {
        camera.zv -= (ccos(camera.pan) * ccos(camera.tilt)) / 1024;     // pan = horizontal motion, tilt = vertical.  cos(pan) returns value in rang -ONE,ONE on the horiz. axis. -4096-0 = left, 0-4096 = right
		camera.xv -= (csin(camera.pan) * ccos(camera.tilt)) / 1024;     
        camera.yv -= (csin(camera.tilt) * ccos(camera.tilt)) / 1024;
	}
	
	if (PadStatus & PADRleft) {
		camera.zv += (csin(camera.pan)*2);
		camera.xv -= (ccos(camera.pan)*2);
	}

	if (PadStatus & PADRright) {
		camera.zv -= (csin(camera.pan)*2);
		camera.xv += (ccos(camera.pan)*2);
	}
	
	if (PadStatus & PADR1)	camera.yv -= ONE*1;
	if (PadStatus & PADR2)	camera.yv += ONE*1;
	
	// Reset
	if (PadStatus & PADselect) {
		camera.x = camera.y = camera.z = 0;
		camera.pan = camera.tilt = camera.rol = 0;
		camera.panv = camera.tiltv = 0;
		camera.xv = 0;
		camera.yv = 0;
		camera.zv = -150;
	}
	
	camera.x += camera.xv;
	camera.y += camera.yv;
	camera.z += camera.zv;
	camera.pan += camera.panv;
	camera.tilt += camera.tiltv;
	
	camera.xv    = 0;
	camera.yv    = 0;
	camera.zv    = 0;
	camera.panv  = 0;
	camera.tiltv = 0;
	
    
    }
