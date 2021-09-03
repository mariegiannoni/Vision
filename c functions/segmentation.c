#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "OutilsLib.h"
#include "BMPLib.h"
#include "ErreurLib.h"
#include "ESLib.h"
#include "structure.h"
#include "basic.h"
#include "histo.h"
#include "segmentation.h"
#include "filter.h"
#include "hsv.h"
#include "measure.h"
#include <stdbool.h>
#include <math.h>

//We initialize with zero

void initializeZero(short int *** m, int l, int h){
	int i, j;
	i = j = 0;
	short int ** matrix = *m;

	for(i = 0 ; i < h ; i++){
		for(j = 0 ; j < l ; j++){
			matrix[i][j] = 0;
		}
	}

	*m = matrix;
}


void initialize255(short int *** m, int l, int h){
	int i, j;
	i = j = 0;
	short int ** matrix = *m;

	for(i = 0 ; i < h ; i++){
		for(j = 0 ; j < l ; j++){
			matrix[i][j] = 255;
		}
	}

	*m = matrix;
}

//We initialize a matrix with only minus 1 inside to do comparision in a easier way

void initializeMinus1(short int *** m, int l, int h){
	int i, j;
	i = j = 0;
	short int ** matrix = *m;

	for(i = 0 ; i < h ; i++){
		for(j = 0 ; j < l ; j++){
			matrix[i][j] = -1;
		}
	}

	*m = matrix;
}

//EROSION
void erosionPoints(short int *** new, short int ** image, int ** points, int nbPt, short int etiq, int window, int l, int h){
	short int ** n = *new;
	int neighbour = 0;
	short int background = 0;
	for(int k = 0; k < nbPt; k ++){
		if(image[points[k][1]][points[k][0]] == etiq){
			neighbour = 0;
			for(int row = points[k][1]-1; row < points[k][1]+2; row ++){
				for(int column = points[k][0]-1; column < points[k][0]+2; column ++){
					//We check that we still are in the limit of the image
					if((row >= 0 && row < l) && (column >= 0 && column < h)){
						if(window == 8){ //V8
							if(image[row][column] != etiq){
								neighbour++;
								background = image[row][column];
							}
						}
						else { //V4
							if(row == points[k][1] || column == points[k][0]){
								if(image[row][column] != etiq){
									neighbour++;
									background = image[row][column];
								}
							}
						}
					}
				}
			}
			if(neighbour > 0){
				n[points[k][1]][points[k][0]] = background;
			}
		}
	}
	*new = n;
}

void erosionEtiq(short int *** new, short int ** image, short int etiq, int window, int lmin, int lmax, int hmin, int hmax, int l, int h){
	short int ** n = *new;
	int neighbour = 0;
	short int background = 0;
	for(int i = hmin; i < hmax; i ++){
		for(int j = lmin; j < lmax; j++){
			if(image[i][j] == etiq){
				neighbour = 0;
				for(int row = i-1; row < i+2; row ++){
					for(int column = j-1; column < j+2; column ++){
						//We check that we still are in the limit of the image
						if((row >= 0 && row < l) && (column >= 0 && column < h)){
							if(window == 8){ //V8
								if(image[row][column] != etiq){
									neighbour++;
									background = image[row][column];
								}
							}
							else { //V4
								if(row == i || column == j){
									if(image[row][column] != etiq){
										neighbour++;
										background = image[row][column];
									}
								}
							}
						}
					}
				}
				if(neighbour > 0){
					n[i][j] = background;
				}
			}
		}
	}
	*new = n;
}

//Dilation
void dilatationPoints(short int *** new, short int ** image,  int ** points, int nbPt, short int etiq, int distance, int window, int l, int h){
	short int ** n = *new;
	for(int k = 0; k < nbPt; k ++){
		if(image[points[k][1]][points[k][0]] == etiq){
			for(int row = points[k][1]-1; row < points[k][1]+2; row ++){
				for(int column = points[k][0]-1; column < points[k][0]+2; column ++){
					//We check that we still are in the limit of the image
					if((row >= 0 && row < l) && (column >= 0 && column < h)){
						if(window == 8){ //V8
							n[row][column]  = etiq;
						}
						else { //V4
							if(row == points[k][1] || column == points[k][0]){
								n[row][column] = etiq;
							}
						}
					}
				}
			}
		}
	}
	*new = n;
}

void dilatationEtiq(short int *** new, short int ** image, short int etiq, int distance, int window, int lmin, int lmax, int hmin, int hmax, int l, int h){
	short int ** n = *new;
	for(int i = hmin; i < hmax; i ++){
		for(int j = lmin; j < lmax; j++){
			if(image[i][j] == etiq){
				for(int row = i-distance; row < i+distance+1; row ++){
					for(int column = j-distance; column < j+distance+1; column ++){
						//We check that we still are in the limit of the image
						if((row >= 0 && row < l) && (column >= 0 && column < h)){
							if(window == 8){ //V8
								n[row][column] = etiq;
							}
							else { //V4
								if(row == i || column == j){
									n[row][column] = etiq;
								}
							}
						}
					}
				}
			}
		}
	}
	*new = n;
}

//We color the background around a shape
void colorBackground(short int *** new, short int ** image, int ** points, int nbPt, short int etiq, short int background, int lmin, int lmax, int hmin, int hmax, int l, int h){
	short int ** n = *new;

	for(int i = 0; i < h; i ++){
		for(int j = 0; j < lmin; j++){
			n[i][j] = background;
		}
		for(int j = lmax; j < l; j++){
			n[i][j] = background;
		}
	}

	for(int j = lmin; j < lmax; j ++){
		for(int i = 0; i < hmin; i++){
			n[i][j] = background;
		}
		for(int i = hmax; i < h; i++){
			n[i][j] = background;
		}
	}

	for(int k = 0; k < nbPt; k ++){
		if(image[points[k][1]][points[k][0]] == etiq){
			// 1 : i - 1
			if((points[k][1] - 1 >= lmin && points[k][1] - 1 < lmax + 1) && (points[k][0] >= hmin && points[k][0] < hmax + 1) && image[points[k][1]-1][points[k][0]] != etiq){
				// we colore from i - 1 to 0, avoiding not background color
				for(int i = points[k][1] - 1; i > hmin - 1; i--){
					if(image[i][points[k][0]] != etiq){
						n[i][points[k][0]] = background;
					}
				}
			}
			// 2 : i + 1
			if((points[k][1] + 1 >= lmin && points[k][1] + 1 < lmax + 1) && (points[k][0] >= hmin && points[k][0] < hmax + 1) && image[points[k][1]+1][points[k][0]] != etiq){
				// we colore from i + 1 to 0, avoiding not background color
				for(int i = points[k][1] + 1; i < hmax + 1; i++){
					if(image[i][points[k][0]] != etiq){
						n[i][points[k][0]] = background;
					}
				}
			}
			// 3 : j - 1
			if((points[k][1] >= lmin && points[k][1] < lmax + 1) && (points[k][0] - 1 >= hmin && points[k][0] - 1 < hmax + 1) && image[points[k][1]][points[k][0]-1] != etiq){
				// we colore from j - 1 to 0, avoiding not background color
				for(int j = points[k][0] - 1; j > lmin - 1; j--){
					if(image[points[k][1]][j] != etiq){
						n[points[k][1]][j] = background;
					}
				}
			}
			// 4 : j + 1
			if((points[k][1] >= lmin && points[k][1] < lmax + 1) && (points[k][0] + 1 >= hmin && points[k][0] + 1 < hmax + 1) && image[points[k][1]][points[k][0]+1] != etiq){
				// we colore from j + 1 to 0, avoiding not background color
				for(int j = points[k][0] + 1; j < lmax + 1; j++){
					if(image[points[k][1]][j] != etiq){
						n[points[k][1]][j] = background;
					}
				}
			}
			n[points[k][1]][points[k][0]] = 127;
		}
	}
	*new = n;
}

//We use a threshold to decide if the element is a part of the region or not.
//This threshold is the maximal difference between the grey level of the region
//and the grey level of the candidate

int isCompatible(short int region, short int candidate, short int simThreshold){
	int compatible = 0;
	if(abs(candidate - region) < simThreshold){
		compatible = 1;
	}
	return compatible;
}

void conditionalDilatation(short int *** new, short int ** image, int i, int j, short int etiq, short int color, int window, int l, int h, int threshold){
	short int ** n = *new;
	if(image[i][j] == color){
		//printf("%d %d\n", i, j);
		for(int row = i-1; row < i+2; row ++){
			for(int column = j-1; column < j+2; column ++){
				//We check that we still are in the limit of the image
				if((row != i && column != j) && (row >= 0 && row < l) && (column >= 0 && column < h)){
					if(n[row][column] != etiq && isCompatible(image[i][j], image[row][column], threshold) == 1){
						if(window == 8){ //V8
							n[row][column] = etiq;
							conditionalDilatation(&n, image, row, column, etiq, color, window, l, h, threshold);
							//printf("%d %d %hd %hd\n", row, column, image[row][column], n[row][column]);
							//getchar();
						}
						else { //V4
							if(row == i || column == j){
								n[row][column] = etiq;
								conditionalDilatation(&n, image, row, column, etiq, color, window, l, h, threshold);
							}
						}
					}
				}
			}
		}
	}
	*new = n;
}

void regionGrowing(short int *** new, short int ** image, short int color, int lmin, int lmax, int hmin, int hmax, int l, int h, int threshold, int window, int mod, int *nbEtiq){
	short int ** n = *new;
	short int etiq = 0;
	short int min, mini, minj;
	short int maxEtiq = 0;
	min = mini = minj = 255;
	short int background;

	if(color < 127){
		initialize255(&n, l, h);
		background = 255;
	}
	else{
		initializeZero(&n, l, h);
		background = 0;
	}

	for(int i = hmin; i < hmax; i++){
		for(int j = lmin; j < lmax; j++){
			if(image[i][j] == color && n[i][j] == background){ // We find an element of the region that is not etiquetted yet
				if(etiq > maxEtiq){
					maxEtiq = etiq;
				}
				for(int row = i-1; row < i+2; row ++){
					for(int column = j-1; column < j+2; column ++){
						//We check that we still are in the limit of the image
						if((row >= 0 && row < l) && (column >= 0 && column < h)){
							if(n[row][column] != background){
								if(window == 8){
									if(mod == 0 || mod == 1){
										if(min >= n[row][column]){
											min = n[row][column];
											mini = row;
											minj = column;
										}
									}
								}
								else {
									if(row == i || column == j){
										if(mod == 0 || mod == 1){
											if(min >= n[row][column]){
												min = n[row][column];
												mini = row;
												minj = column;
											}
										}
									}
								}
							}
						}
					}
				}

				if(mod == 0 || mod == 1){ // incrementation - 1 - 2 - 3 - ...
					if(min != 255 && etiq != 254) etiq = min;
					else etiq ++;
					min = 255;
				}
				else {
					etiq = (etiq + 20)%256;
				}

				n[i][j] = etiq;

				//We do a dilatation
				conditionalDilatation(&n, image, i, j, etiq, color, window, lmax, hmax, threshold);
			}
		}
	}

	*nbEtiq = maxEtiq;
	*new = n;
}

//Region Growing Process to find a certain region
void regionGrowingProcess(short int *** objectEtiq, short int *** object, short int ** image, short int color, short int etiq, short int threshold, int window, int lmin, int lmax, int hmin, int hmax, int l, int h){
	short int ** ob = *object;
	short int ** obE = *objectEtiq;

	for(int i = hmin; i < hmax; i++){
		for(int j = lmin; j < lmax; j++){
			if(isCompatible(color, image[i][j], threshold) == 1){
				for(int row = i-1; row < i+2; row ++){
					for(int column = j-1; column < j+2; column ++){
						//We check that we still are in the limit of the image
						if((row >= 0 && row < l-1) && (column >= 0 && column < h-1)){
							//We look for the neighbour
							if(window == 8){ //V8
								if(isCompatible(color, image[row][column], threshold) == 1){
									ob[row][column] = image[row][column];
									obE[row][column] = etiq;
								}
								else {
									if(color >= 0 && color <= 127){
										ob[row][column] = 255;

									}
									else {
										ob[row][column] = 0;
									}

									if(etiq >= 0 && etiq <= 127){
										obE[row][column] = 255;

									}
									else {
										obE[row][column] = 0;
									}
								}
							}
							else { //V4
								if(row == i || column == j){
									if(isCompatible(color, image[row][column], threshold) == 1){
										ob[row][column] = image[row][column];
										obE[row][column] = etiq;
									}
									else {
										if(color >= 0 && color <= 127){
											ob[row][column] = 255;
										}
										else {
											ob[row][column] = 0;
										}

										if(etiq >= 0 && etiq <= 127){
											obE[row][column] = 255;
										}
										else {
											obE[row][column] = 0;
										}
									}
								}
							}
						}
					}
				}
			}
			else {
				if(color >= 0 && color <= 127){
					ob[i][j] = 255;
				}
				else {
					ob[i][j] = 0;
				}

				if(etiq >= 0 && etiq <= 127){
					obE[i][j] = 255;
				}
				else {
					obE[i][j] = 0;
				}
			}
		}
	}

	*object = ob;
	*objectEtiq = obE;
}

//WATERSHED
void watershed(short int *** new, short int ** grey, int l, int h, int window, int distance){
	short int ** n = *new;
	initializeMinus1(&n,l,h);
	short int min, mini, minj;
	min = mini = minj = 255;
	int k, i, j, row, column;
	k = i = j = row = column = 0;

	for (k = 0; k < 256; k++){
		for(i = 0; i < h; i++){
			for(j = 0; j < l; j++){
				if(grey[i][j] == k){
				//I will check if this pixel is :
				//- pool (local minimum - it can be the only minimum or one of the minimum)
				//- not a pool

					if(window == 8){
						//V8
						//I look in every direction

						for(row = i-1; row < i+2; row++){
							for(column = j-1; column < j+2; column ++){
								// I check that my pixel has a minimum value
								if((row >= 0 && row < l) && (column >= 0 && column < h)){ // I check that I am still in the picture
									if(min >= grey[row][column]){
										min = grey[row][column];
										mini = row;
										minj = column;
									}
								}
							}
						}

						n[i][j] = min;
						min = 255;
					}
					else if(window == 4){
						//V4
						// I look in only four directions

						for(row = i-1; row < i+2; row++){
							for(column = j-1; column < j+2; column ++){
								// I check that my pixel has a minimum value
								if((row >= 0 && row < l) && (column >= 0 && column < h)){ // I check that I am still in the picture
									if(min >= grey[row][column]){
										min = grey[row][column];
										mini = row;
										minj = column;
									}
								}
							}
						}

						n[i][j] = min;
						min = 255;
					}
				}
			}
		}
		for(int i = 0; i < h; i++){
			for(int j = 0; j < l; j++){
				if(n[i][j] == k){
					//dilatation here according to the distance distance
					if(window == 8){
						//V8
						//I look in every direction

						for(row = i-distance; row < i+distance; row++){
							for(column = j-distance; column < j+distance; column ++){
								if((row >= 0 && row < l) && (column >= 0 && column < h)){ // I check that I am still in the picture
									if(grey[row][column] >= k){
										n[row][column] = k;
									}
								}
							}
						}
					}
					else if(window == 4){
						//V4
						// I look in only four directions

						for(row = i-distance; row < i+distance; row++){
							for(column = j-distance; column < j+distance; column ++){
								// I check that my pixel has a minimum value
								if((row >= 0 && row < l) && (column >= 0 && column < h)){ // I check that I am still in the picture
									if(grey[row][column] >= k){
										n[row][column] = k;
									}
								}
							}
						}
					}
				}
			}
		}
	*new = n;
	}
}

void watershedMI(MatImage ** picture, int window, int distance){
	MatImage * pict = *picture;
	//intermediate 1 and 2 matrix for the change
	short int ** intermediate = NULL;
	create1matrix(&intermediate, pict->l, pict->h);
	//compute laplacian filter
	watershed(&(intermediate), pict->grey, pict->l, pict->h, window, distance);
	//we change the matrix and the picture
	duplicateMatrice(pict->grey, intermediate, pict->l, pict->h);
	changeImageNB(&(pict->image), pict->grey);
	free1matrix(&intermediate, pict->h);
	*picture = pict;
}

//Fonction retournant un entier (0 si noir, 1 si blanc ou 2 si blanc et noir) définissant la valeur d'un carré
int calculCarreNB(int x1, int y1, int x2, int y2, short int ** gris){
	int n;
	int i=y1;
	if(*(*(gris+y1)+x1)==255){
		n=1;
	}
	else{
		n=0;
	}
	while(i<y2&&n!=2){
		int j=x1;
		while(j<x2&&n!=2){
			if(*(*(gris+i)+j)!=*(*(gris+y1)+x1)){
				n=2;
			}
			j++;
		}
		i++;
	}
	return n;
}

//Fonction  qui crée un arbre binaire dont la racine est un noeud à partir d'une matrice
void creeArbreNB(noeudBinaire ** racine, int x0, int y0, int x1, int y1, int l, int h, int val, short int ** gris){
	noeudBinaire *r = *racine;
	r=(noeudBinaire*)malloc(sizeof(noeudBinaire));
	r->x0 = x0;
	r->y0 = y0;
	r->x1 = x1;
	r->y1 = y1;
	r->l = l;
	r->h = h;
	r->val = val;
	int t[6];
	int v;
	if(val==2 && x0<x1 && y0<y1 && x0>=0 && y0 >=0){
		//n1
		t[0]=x0;
		t[1]=y0;
		t[2]=x0+l/2-1;
		t[3]=y0+h/2-1;
		t[4]=l/2;
		t[5]=h/2;
		v=calculCarreNB(t[0],t[1],t[2],t[3],gris);
		creeArbreNB(&(r->n1),t[0],t[1],t[2],t[3],t[4],t[5],v,gris);
		//n2
		t[0]=x0+l/2;
		t[1]=y0;
		t[2]=x1;
		t[3]=y0+h/2-1;
		t[4]=l/2;
		t[5]=h/2;
		v=calculCarreNB(t[0],t[1],t[2],t[3],gris);
		creeArbreNB(&(r->n2),t[0],t[1],t[2],t[3],t[4],t[5],v,gris);
		//n3
		t[0]=x0;
		t[1]=y0+h/2;
		t[2]=x0+l/2-1;
		t[3]=y1;
		t[4]=l/2;
		t[5]=h/2;
		v=calculCarreNB(t[0],t[1],t[2],t[3],gris);
		creeArbreNB(&(r->n3),t[0],t[1],t[2],t[3],t[4],t[5],v,gris);
		//n4
		t[0]=x0+l/2;
		t[1]=y0+l/2;
		t[2]=x1;
		t[3]=y1;
		t[4]=l/2;
		t[5]=h/2;
		v=calculCarreNB(t[0],t[1],t[2],t[3],gris);
		creeArbreNB(&(r->n4),t[0],t[1],t[2],t[3],t[4],t[5],v,gris);
	}else{
		r->n1 = r->n2 = r->n3 = r->n4 = NULL;
	}
	*racine=r;
}

//Fonction qui étiquette les feuilles d'un arbre selon la valeur du noeud (-1 si 2 de 0 à i[256] sinon)
void etiquetteFeuilleNB(noeudBinaire ** racine, int *i){
	*i=*i+20;
	*i=*i%256;
	if((*racine)->val==2){
		(*racine)->etiquette=-1;
		etiquetteFeuilleNB(&((*racine)->n1),i);
		etiquetteFeuilleNB(&((*racine)->n2),i);
		etiquetteFeuilleNB(&((*racine)->n3),i);
		etiquetteFeuilleNB(&((*racine)->n4),i);
	}
	else{
		(*racine)->etiquette=*i;
	}
}

//Si etiq est faux
//Fonction qui remplit la matrice de 255 ou de 0 selon la valeur du noeud (0 : 0, 1 : 255)
void colorieMatrice(noeudBinaire * racine, short int *** gris){
	short int **g;
	g=*gris;
	int i,j;
		if(racine->val==1){
			for(i=racine->y0;i<racine->y0 + racine->h;i++){
				for(j=racine->x0;j<racine->x0 + racine->l;j++){
					*(*(g+i)+j)=255;
				}
			}
		}
		else if(racine->val==0){
			for(i=racine->y0;i<racine->y0 + racine->h;i++){
				for(j=racine->x0;j<racine->x0 + racine->l;j++){
					*(*(g+i)+j)=0;
				}
			}
		}
		else{
			colorieMatrice(racine->n1,&g);
			colorieMatrice(racine->n2,&g);
			colorieMatrice(racine->n3,&g);
			colorieMatrice(racine->n4,&g);
		}
	*gris=g;
}

//Si etiq est vrai
//Fonction qui remplit la matrice avec les valeurs des étiquettes
void colorieMatriceEtiquette(noeudBinaire * racine, short int *** gris){
	short int **g;
	g=*gris;
	int i,j;
	if(racine->val==2){
		colorieMatriceEtiquette(racine->n1,&g);
		colorieMatriceEtiquette(racine->n2,&g);
		colorieMatriceEtiquette(racine->n3,&g);
		colorieMatriceEtiquette(racine->n4,&g);
	}
	else{
		for(i=racine->y0;i<racine->y0 + racine->h;i++){
			for(j=racine->x0;j<racine->x0 + racine->l;j++){
				*(*(g+i)+j)=racine->etiquette;
			}
		}
	}
	*gris=g;
}

//Fonction qui crée une matrice à partir d'un arbre : elle appelle colorieMatrice ou colorieMatriceEtiquette selon la valeur d'etiq (si 0 : colorieMatrice, si 1 : colorieMatriceEtiquette)
void creeMatriceArbreNB(noeudBinaire *racine, short int *** gris, int etiq){
	short int ** g;
	g=(short int**)malloc(sizeof(short int *)*(racine->l));
	for(int i=0;i<racine->l;i++){
		g[i]=(short int*)malloc(sizeof(short int)*(racine->h));
	}
	if(etiq == 1){
		colorieMatriceEtiquette(racine,&g);
	}
	else{
		colorieMatrice(racine,&g);
	}
	*gris = g;
}

//Fonction qui libère un arbre
void libereArbreNB(noeudBinaire ** racine){
	if(*racine != NULL){
		libereArbreNB(&((*racine)->n1));
		libereArbreNB(&((*racine)->n2));
		libereArbreNB(&((*racine)->n3));
		libereArbreNB(&((*racine)->n4));
		free(*racine);
	}
}

//Recomposition image binaire avec étiquette
//Racine représente la racine de l'arbre pour parcourir l'ensemble de l'arbre, trouve est le noeudBinaire voisin, x0,y0,x1,y1 sont les coordonées de la racine dont on cherche les voisins
void chercheVoisin(noeudBinaire ** racine1, int x0, int y0, int x1, int y1, int etiq, int val){
	noeudBinaire * racine = *racine1;
	if(racine->val != 2){
		if(racine->etiquette != etiq && racine->val == val){
			//En effet, on ne veut pas reconsidérer un voisin déjà modifié ou qui a provoqué lui-même une modification chez la racine dont on cherche les voisins
			//Voisin de droite
			if(racine->x0 == x1 +1 && racine->y0 <= y1 && racine->y0 >= y0){
				racine->etiquette = etiq;
			}
			//Voisin de gauche
			else if(racine->x1 == x0 -1 && racine->y0 <= y1 && racine->y0 >= y0){
				racine->etiquette = etiq;
			}
			//Voisin du dessous
			else if(racine->y1 == y0 -1 && racine->x0 <= x1 && racine->x0 >= x0){
				racine->etiquette = etiq;
			}
			//Voisin du dessus
			else if(racine->y0 == y1 +1 && racine->x0 <= x1 && racine->x0 >= x0){
				racine->etiquette = etiq;
			}
		}
	}else{
	//On continue de chercher un voisin
		chercheVoisin(&(racine->n1),x0,y0,x1,y1,etiq,val);
		chercheVoisin(&(racine->n2),x0,y0,x1,y1,etiq,val);
		chercheVoisin(&(racine->n3),x0,y0,x1,y1,etiq,val);
		chercheVoisin(&(racine->n4),x0,y0,x1,y1,etiq,val);
	}
	*racine1 = racine;
}

void fusionNB(noeudBinaire ** fusion, noeudBinaire ** racine){
	noeudBinaire * f = *fusion;
	noeudBinaire * r = *racine;
	if(f != NULL){
		if(f->val == 2){
			fusionNB(&(f->n4),&r);
			fusionNB(&(f->n3),&r);
			fusionNB(&(f->n2),&r);
			fusionNB(&(f->n1),&r);
		}else{
			chercheVoisin(&r,f->x0,f->y0,f->x1,f->y1,f->etiquette,f->val);
		}
	}
}

