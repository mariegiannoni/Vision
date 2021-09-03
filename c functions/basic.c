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

//Creation of one matrix
void create1matrix(short int *** m, int l, int h){
	int i, j;
	i = j = 0;
	short int ** matrix = *m;

	matrix = (short int**)malloc(sizeof(short int *)*h);
	for(i = 0 ; i < h ; i++)
		matrix[i] = (short int*)malloc(sizeof(short int)*l);

	for(i = 0 ; i < h ; i++){
		for(j = 0 ; j < l ; j++){
			matrix[i][j] = 0;
		}
	}

	*m = matrix;
}

//Liberation of one matrix
void free1matrix(short int *** m, int h){
	short int **matrix = NULL;
	int i = 0;
	matrix = *m;

	for(i = 0 ; i < h ; i++){
		free(*(matrix+i));
		*(matrix+i) = NULL;
	}

	free(matrix);
	matrix = NULL;

	*m = matrix;
}

//Creation of three matrices
void create3matrices(DonneesImageRGB* picture, short int *** red, short int *** green, short int *** blue){
	int i,j,k;
	k=0;
	short int ** r, ** g, ** b;

	r = (short int**)malloc(sizeof(short int *)*picture->hauteurImage);
	g = (short int**)malloc(sizeof(short int *)*picture->hauteurImage);
	b = (short int**)malloc(sizeof(short int *)*picture->hauteurImage);
	for(i = 0 ; i < picture->hauteurImage ; i++){
		r[i] = (short int*)malloc(sizeof(short int)*picture->largeurImage);
		g[i] = (short int*)malloc(sizeof(short int)*picture->largeurImage);
		b[i] = (short int*)malloc(sizeof(short int)*picture->largeurImage);
	}

	for(i = 0 ; i < (picture->hauteurImage) ; i++){
		for(j = 0 ; j < (picture->largeurImage) ; j++){
			*(*(b+i)+j) = *(picture->donneesRGB+k);
			k++;
			*(*(g+i)+j) = *(picture->donneesRGB+k);
			k++;
			*(*(r+i)+j) = *(picture->donneesRGB+k);
			k++;
		}
	}

	*red = r;
	*green = g;
	*blue = b;
}

//Liberation of three matrices
void free3matrices(short int *** red, short int *** green, short int *** blue, int h){
	short int **r, **g, **b;
	r = *red;
	g = *green;
	b = *blue;
	int i = 0;

	for(i = 0 ; i < h ; i++){
		free(*(r+i));
		free(*(g+i));
		free(*(b+i));
		*(r+i) = NULL;
		*(g+i) = NULL;
		*(b+i) = NULL;
	}

	free(r);
	free(g);
	free(b);
	r=NULL;
	g=NULL;
	b=NULL;

	*red=r;
	*blue=b;
	*green=g;
}

//Save Image
void saveImage(DonneesImageRGB ** image, short int ** red, short int ** green, short int ** blue, int l, int h){
	DonneesImageRGB * im = *image;
	int i, j, k;
	k = 0;

	im = (DonneesImageRGB*)malloc(sizeof(DonneesImageRGB));
	im->donneesRGB = (unsigned char *)malloc(sizeof(unsigned char)*3*l*h);
	im->largeurImage = l;
	im->hauteurImage = h;

	for(i = 0 ; i < h ; i++){
		for( j = 0 ; j < l ; j++){
			*((im->donneesRGB)+k) = blue[i][j];
			k++;
			*((im->donneesRGB)+k) = green[i][j];
			k++;
			*((im->donneesRGB)+k) = red[i][j];
			k++;
		}
	}

	*image = im;
}

//Save Image Mat Image
void saveImageMI(DonneesImageRGB ** image, MatImage * mi){
	DonneesImageRGB * im = *image;
	int i, j, k;
	k = 0;

	im = (DonneesImageRGB*)malloc(sizeof(DonneesImageRGB));
	im->donneesRGB = (unsigned char *)malloc(sizeof(unsigned char)*3*mi->l*mi->h);
	im->largeurImage = mi->l;
	im->hauteurImage = mi->h;

	for(i = 0 ; i < mi->h ; i++){
		for( j = 0 ; j < mi->l ; j++){
			printf("AVANT %u %u %u\n", *((im->donneesRGB)+k), *((im->donneesRGB)+k)+1,*((im->donneesRGB)+k)+2);
			*((im->donneesRGB)+k) = *(*(mi->blue+i)+j);
			k++;
			*((im->donneesRGB)+k) = *(*(mi->green+i)+j);
			k++;
			*((im->donneesRGB)+k) = *(*(mi->red+i)+j);
			k++;
			printf("APRES %u %u %u\n", *((im->donneesRGB)+k-2), *((im->donneesRGB)+k)-1,*((im->donneesRGB)+k));
		}
	}

	*image = im;
}

//Save Image NB
void saveImageNB(DonneesImageRGB ** image, short int ** grey, int l, int h){
	DonneesImageRGB * im = *image;
	int i, j, k;
	k=0;

	im = (DonneesImageRGB*)malloc(sizeof(DonneesImageRGB));
	im->donneesRGB = (unsigned char *)malloc(sizeof(unsigned char)*3*l*h);
	im->largeurImage = l;
	im->hauteurImage = h;

	for(i = 0 ; i < h ; i++){
		for( j = 0 ; j < l ; j++){
			*((im->donneesRGB)+k) = *(*(grey+i)+j);
			k++;
			*((im->donneesRGB)+k) = *(*(grey+i)+j);
			k++;
			*((im->donneesRGB)+k) = *(*(grey+i)+j);
			k++;
		}
	}

	*image = im;
}

//Save Image NB MatImage
void saveImageNBMI(DonneesImageRGB ** image, MatImage * mi){
	DonneesImageRGB * im = *image;
	int i, j, k;
	k=0;

	im = (DonneesImageRGB*)malloc(sizeof(DonneesImageRGB));
	im->donneesRGB = (unsigned char *)malloc(sizeof(unsigned char)*3*mi->l*mi->h);
	im->largeurImage = mi->l;
	im->hauteurImage = mi->h;

	for(i = 0 ; i < mi->h ; i++){
		for( j = 0 ; j < mi->l ; j++){
			*((im->donneesRGB)+k) = *(*(mi->grey+i)+j);
			k++;
			*((im->donneesRGB)+k) = *(*(mi->grey+i)+j);
			k++;
			*((im->donneesRGB)+k) = *(*(mi->grey+i)+j);
			k++;
		}
	}

	*image = im;
}

//Change image
void changeImageRGB(DonneesImageRGB ** image, short int ** red, short int **green, short int ** blue){
	DonneesImageRGB * im = *image;
	int  k = 0;
	for(int i = 0 ; i < im->hauteurImage ; i++){
		for(int j = 0 ; j < im->largeurImage ; j++){
			*((im->donneesRGB)+k) = *(*(blue+i)+j);
			k++;
			*((im->donneesRGB)+k) = *(*(green+i)+j);
			k++;
			*((im->donneesRGB)+k) = *(*(red+i)+j);
			k++;
		}
	}
	*image = im;
}

//Change image NB
void changeImageNB(DonneesImageRGB ** image, short int ** grey){
	DonneesImageRGB * im = *image;
	int k = 0;
	for(int i = 0 ; i < im->hauteurImage ; i++){
		for(int j = 0 ; j < im->largeurImage ; j++){
			*((im->donneesRGB)+k) = *(*(grey+i)+j);
			k++;
			*((im->donneesRGB)+k) = *(*(grey+i)+j);
			k++;
			*((im->donneesRGB)+k) = *(*(grey+i)+j);
			k++;
		}
	}
	*image = im;
}

//Duplicate image
void duplicateImage(short int ** r1, short int ** g1, short int ** b1, short int ** r2, short int ** g2, short int ** b2, int l, int h){
	int i, j;
	for(i = 0 ; i < h ; i++){
		for(j = 0 ; j < l ; j++){
			r1[i][j] = r2[i][j];
			g1[i][j] = g2[i][j];
			b1[i][j] = b2[i][j];
		}
	}
}

//Duplicate one matrix
void duplicateMatrice(short int ** m1, short int ** m2, int l, int h){
	int i, j;
	for(i = 0 ; i < h ; i++){
		for(j = 0 ; j < l ; j++){
			m1[i][j] = m2[i][j];
		}
	}
}

//create MatImage
void createMatImage(MatImage ** matImage, short int ** red, short int ** green, short int ** blue, int l, int h, chaine nameBMP){
	MatImage * mi = *matImage;
	mi = (MatImage *)malloc(sizeof(MatImage));

	//Dimensions
	mi->l = l;
	mi->h = h;

	//Matrices - color
	create1matrix(&(mi->red),l,h);
	duplicateMatrice(mi->red, red, l, h);
	create1matrix(&(mi->blue),l,h);
	duplicateMatrice(mi->blue, blue, l, h);
	create1matrix(&(mi->green),l,h);
	duplicateMatrice(mi->green, green, l, h);

	//Matrix - grey
	create1matrix(&(mi->grey),l,h);
	shadesOfGrey(&(mi->grey), red, green, blue, l, h);

	//DonneesImageRGB
	saveImage(&(mi->image),red, green, blue, l, h);

	//Histograms
	createHistogram(&(mi->histo));
	createHistogram(&(mi->chisto));

	//Name
	strcpy(mi->nameBMP,nameBMP);
	
	*matImage = mi;
}

//Create MatImage from image
void createMatImageFromImage(MatImage ** matImage, DonneesImageRGB * image, chaine nameBMP){
	MatImage * mi = *matImage;
	mi = (MatImage *)malloc(sizeof(MatImage));

	//Dimensions
	mi->l = image->largeurImage;
	mi->h = image->hauteurImage;

	//Create image
	short int ** red, ** blue, ** green;
	create3matrices(image, &red, &green, &blue);
	
	//Matrices - color
	create1matrix(&(mi->red),mi->l,mi->h);
	duplicateMatrice(mi->red, red, mi->l, mi->h);
	create1matrix(&(mi->blue),mi->l,mi->h);
	duplicateMatrice(mi->blue, blue, mi->l, mi->h);
	create1matrix(&(mi->green),mi->l,mi->h);
	duplicateMatrice(mi->green, green, mi->l, mi->h);

	//Matrix - grey
	create1matrix(&(mi->grey),mi->l,mi->h);
	shadesOfGrey(&(mi->grey), red, green, blue, mi->l, mi->h);

	//DonneesImageRGB
	saveImage(&(mi->image),red, green, blue, mi->l, mi->h);

	//Histograms
	createHistogram(&(mi->histo));
	createHistogram(&(mi->chisto));

	//Name
	strcpy(mi->nameBMP,nameBMP);

	//Free matrices
	free3matrices(&red, &green, &blue, mi->h);
	
	*matImage = mi;
}

//modifying matrices of MatImage
//Colored image
void modifyMatricesColorMatImage(MatImage ** matImage, short int ** red, short int ** green, short int ** blue){
	MatImage * mi = *matImage;
	duplicateImage(mi->red, mi->green, mi->blue, red, green, blue, mi->l, mi->h);
	shadesOfGrey(&(mi->grey), mi->red, mi->green, mi->blue, mi->l, mi->h);
	*matImage = mi;
}

//Grey image
void modifyMatricesNBMatImage(MatImage ** matImage, short int ** grey){
	MatImage * mi = *matImage;
	duplicateMatrice(mi->grey, grey,mi->l,mi->h);
	*matImage = mi;
}

//Liberation of MatImage
void freeMatImage(MatImage ** matImage){
	MatImage * mi = *matImage;
	if(mi != NULL){
		if(mi->red != NULL && mi->green != NULL && mi->blue != NULL)
		free3matrices(&(mi->red), &(mi->green), &(mi->blue), mi->h);

		if(mi->grey != NULL)
		free1matrix(&(mi->grey),mi->h);
		
		if(mi->image != NULL )
		libereDonneesImageRGB(&(mi->image));
		
		if(mi->histo != NULL)
		freeHistogram(&(mi->histo));
		
		if(mi->chisto != NULL)
		freeHistogram(&(mi->chisto));

		free(mi);
		mi = NULL;
	}
	*matImage = mi;
}
