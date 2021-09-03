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
#include <stdbool.h>
#include <math.h>

//STRUCTURE Histogram

//Histogram

//Create ni
void initializeNi(int *** ni){
	int ** n = * ni;
	n = (int **)malloc(sizeof(int *)*256);
	for(int i = 0; i < 256; i++){
		n[i] = (int*)malloc(sizeof(int)*2);
		n[i][0] = i;
		n[i][1] = 0;
	}
	*ni = n;
}

//Free ni
void freeNi(int *** ni){
	int ** n = * ni;
	for(int i = 0; i < 256; i++){
		free(n[i]);
	}
	free(n);
	n = NULL;
	*ni = n;
}

//Creation of histogram
void createHistogram(Histogram ** histo){
	Histogram * h = *histo;
	h = (Histogram *)malloc(sizeof(Histogram));
	initializeNi(&(h->ni));
	h->histogram = NULL;
	strcpy(h->nameBMP,"");
	h->nimax = 0;
	h->nimin = 0;
	h->N = 0;
	*histo = h;
}

//Compute histogram
void computeHistogram(Histogram ** histo, MatImage * mi, int c){
	Histogram * h = *histo;
	int i, j, k;
	int sum = 0;
	i = j = k = 0;
	
	for(i = 0 ; i < (mi->h) ; i++){
		for(j = 0 ; j < (mi->l) ; j++){
			//count the number of pixel
			(h->N)++;
			//count the number of pixel for a certain level of grey
			h->ni[mi->grey[i][j]][1] = h->ni[mi->grey[i][j]][1] + 1;
		}
	}

	h->nimax = 0;
	h->nimin = h->N;
	
	for(k = 0; k < 256; k++){
		//find the minimal and maximal number of pixels for a level of grey
		if(c == 1) {
			sum = sum + h->ni[k][1];
			h->ni[k][1] = sum;
		}
		if(h->nimax < h->ni[k][1]) h->nimax = h->ni[k][1];
		if(h->nimin > h->ni[k][1]) h->nimin = h->ni[k][1];
	}

	//Create the image
	drawHistogram(&(h->histogram),h);

	//Name .bmp
	if(c == 0){
		strcpy(h->nameBMP, "histogram ");
	}
	else if (c == 1){
		strcpy(h->nameBMP, "chistogram ");
	}
	strcat(h->nameBMP,mi->nameBMP);
	
	*histo = h;
}

//Draw an histogram in a picture
void drawHistogram(DonneesImageRGB ** image, Histogram * histo){
	DonneesImageRGB * im = * image;
	short int ** hred = NULL;
	short int ** hgreen = NULL;
	short int ** hblue = NULL;

	//Creation of matrices
	create1matrix(&hred,512,512);
	create1matrix(&hgreen,512,512);
	create1matrix(&hblue,512,512);
	
	for(int i = 0; i < 512; i++){
		for(int j = 0; j < 512; j++){
			// White background with red and black outlines
			hred[i][j] = 255;
			hgreen[i][j] = 255;
			hblue[i][j] = 255;

			// Red
			if(i == 0 || j == 0 || i == 511 || j == 511){
				hred[i][j] = 255;
				hgreen[i][j] = 0;
				hblue[i][j] = 0;
			}

			// Black
			if(i == 1 || j == 1 || i == 510 || j == 510){
				hred[i][j] = 0;
				hgreen[i][j] = 0;
				hblue[i][j] = 0;
			}
		}
	}

	double * bar = (double *)malloc(sizeof(double *)*256);
	
	for(int k = 0; k < 256; k++){
		bar[k] = (double)((512./(histo->nimax-histo->nimin))*(histo->ni[k][1]-histo->nimin));
		//Blue histogram
		for(int i = 0; i < 512; i++){
			for(int j = 0; j < 512; j++){
				if(j == 2*k || j == 2*k+1){
					if(i <= bar[k]){
						hred[i][j] = 0;
						hgreen[i][j] = 0;
						hblue[i][j] = 255;
					}
				}
			}
		}				
	}

	free(bar);

	//Creation of the picture
	if(im == NULL)
	saveImage(&im,hred,hgreen,hblue,512,512);

	//Liberation of matrices
	free1matrix(&hred,512);
	free1matrix(&hgreen,512);
	free1matrix(&hblue,512);
	
	*image = im;
}

//Liberation of histogram
void freeHistogram(Histogram ** histo){
	Histogram * h = *histo;
	freeNi(&(h->ni));
	free(h->ni);
	libereDonneesImageRGB(&(h->histogram));
	free(h);
	h = NULL;
	*histo = h;
}

//create MatImage Histograms
void setHistogramsInMI(MatImage ** matImage){
	MatImage * mi = *matImage;
	computeHistogram(&(mi->histo),mi,0);
	computeHistogram(&(mi->chisto),mi,1);
	*matImage = mi;
}

//Compute entropy
void computeEntropy(double * entropy, Histogram * h){
	int i = 0;
	double ent = 0;
	double pi = 0;
	
	for(i = 0; i < 256; i++){
		pi = (double)(((double)(h->ni[i][1]))/((double)(h->N)));
		pi = (pi*log(pi));
		if(pi < - 0.00001)
			ent = (double)(- pi + ent);
	}
	
	*entropy = ent;
}

//Print elements of image
//Print Histogram
void printHistogram(Histogram * histo){
	printf("Histogram created in %s\n",histo->nameBMP);
	ecrisBMPRGB_Dans(histo->histogram,histo->nameBMP);
}

//Print the entropy
void printEntropy(MatImage * mi){
	printf("Entropy : %lf\n", mi->entropy);
}
