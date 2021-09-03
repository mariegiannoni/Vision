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

//RGB intot HSV conversion
//Compute min
void computeMin(short int m1, short int m2, short int * min){
	short int m = *min;
	if(m1 >= m2)
		m = m2;
	else
		m = m1;
	*min = m;
}

//Compute max
void computeMax(short int m1, short int m2, short int * max){
	short int m = *max;
	if(m1 >= m2)
		m = m1;
	else
		m = m2;
	*max = m;
}

//Compute min of 3 elements
void computeMin3(short int m1, short int m2, short int m3, short int * min){
	short int m = *min;
	computeMin(m1,m2,&m);
	computeMin(m,m3,&m);
	*min = m;
}

//Compute max of 3 elements
void computeMax3(short int m1, short int m2, short int m3, short int * max){
	short int m = *max;
	computeMax(m1,m2,&m);
	computeMax(m,m3,&m);
	*max = m;
}

//Compute the hue of HSV
void computeH(short int ** red, short int ** green, short int ** blue, short int *** h, int length, int heigth){
	short int **hue = * h;

	double intermediate = 0;
	
	short int max, min, m;
	max = min = m = 0;
	
	for(int i = 0; i < heigth; i++)
	{
		for(int j = 0;j < length; j++)
		{
			computeMax3(red[i][j], green[i][j], blue[i][j], &max);
			computeMin3(red[i][j], green[i][j], blue[i][j], &min);
			
			m=max-min;
			
			if(m >= 0)
			{
				if(m == 0)
				{
					intermediate = -11;
				}
				else if(max == *(*(red+i)+j))
				{
					intermediate = (*(*(green+i)+j) - *(*(blue+i)+j));
					intermediate = (1./m) * intermediate;
					intermediate = fmod(intermediate, 6);
					intermediate = 60 * intermediate;
				}
				else if(max == *(*(green+i)+j))
				{
					intermediate = (*(*(blue+i)+j) - *(*(red+i)+j));
					intermediate = intermediate * (1/m);
					intermediate = intermediate + 2;
					intermediate = 60 * intermediate;
				}
				else if(max == *(*(blue+i)+j))
				{
					intermediate = (*(*(red+i)+j) - *(*(green+i)+j));
					intermediate = intermediate * (1/m);
					intermediate = intermediate + 4;
					intermediate = 60 * intermediate;
				}
				intermediate = intermediate + 0.5;
				*(*(hue+i)+j) = (short int)intermediate;
			}
		}
	}
	*h = hue;
}

//Compute the saturation of HSV
void computeS(short int ** red, short int ** green, short int ** blue, short int *** sat, int length, int heigth){
	short int **s = * sat;

	short int max, min;
	max = min = 0;
	long intermediate = 0;
	
	for(int i = 0; i < heigth; i++)
	{
		for(int j = 0 ; j < length; j++)
		{
			computeMax3((*(*(red+i)+j)), (*(*(green+i)+j)), (*(*(blue+i)+j)), &max);
			computeMin3((*(*(red+i)+j)), (*(*(green+i)+j)), (*(*(blue+i)+j)), &min);
			
			if(max == 0){
				 intermediate = 0;
			}else{
				intermediate = max-min;
				intermediate = (100./max)*(intermediate+0.5);
			}
			
			intermediate = intermediate;
			*(*(s+i)+j) = (short int) intermediate;
		}
	}

	*sat = s;
}

//Compute the value of HSV
void computeV(short int ** red, short int ** green, short int ** blue, short int *** val, int length, int heigth){
	short int **v = * val;
	long intermediate = 0;
	for(int i = 0; i < heigth; i++)
	{
		for(int j = 0 ; j < length; j++)
		{
			computeMax3((*(*(red+i)+j)), (*(*(green+i)+j)), (*(*(blue+i)+j)), &((*(*(v+i)+j))));
			intermediate = (*(*(v+i)+j));
			intermediate = (100./255) * (intermediate + 0.5);
			(*(*(v+i)+j)) = (short int)intermediate;
		}
	}
	*val = v;
}

//Convert RGB in HSV
void fromRGBtoHSV(MatImage ** picture){
	MatImage * pict = *picture;
	computeH(pict->red, pict->green, pict->blue, &(pict->red), pict->l, pict->h);
	computeS(pict->red, pict->green, pict->blue, &(pict->green), pict->l, pict->h);
	computeV(pict->red, pict->green, pict->blue, &(pict->blue), pict->l, pict->h);
	*picture = pict;
}
