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

int main(void)
{
	//Image
	DonneesImageRGB *image=NULL;
	image = lisBMPRGB("test.bmp");
	DonneesImageRGB *image2=NULL;
	image2 = lisBMPRGB("test.bmp");

	//MatImage
	MatImage * mi = NULL;
	createMatImageFromImage(&mi,image,"testPolyMI.bmp");
	MatImage * mi2 = NULL;
	createMatImageFromImage(&mi2,image2,"testPolyMI3.bmp");
	Shape * shape = NULL;
	manualThresholdNB(mi2->h, mi2->l, &(mi2->grey), 127);
	manualThresholdNB(mi->h, mi->l, &(mi->grey), 127);
	shapePoint(&shape, mi2->grey, mi2->grey, 0, mi2->l, mi2->h);
	geometricalCircularity(&shape);
	convexHullGraham(&shape, shape->edges, shape->nbPtE, mi2->l);
	shadesOfGrey(&(mi2->red), mi->red, mi->green, mi->blue, mi->l, mi->h);
	shadesOfGrey(&(mi2->green), mi->red, mi->green, mi->blue, mi->l, mi->h);
	shadesOfGrey(&(mi2->blue), mi->red, mi->green, mi->blue, mi->l, mi->h);
		
	printPoints(shape->hull, shape->nbPtH, mi2->red, mi2->green, mi2->blue, mi->l, mi->h, 255, 0, 0);
	changeImageRGB(&(mi2->image), mi2->red, mi2->green, mi2->blue);
	if(mi2->image !=NULL)
	ecrisBMPRGB_Dans(mi2->image,"testHull.bmp");

	/*printPoints(shape->edges, shape->nbPtE, mi2->red, mi2->green, mi2->blue, mi->l, mi->h, 255, 0, 0);
	changeImageRGB(&(mi2->image), mi2->red, mi2->green, mi2->blue);
	if(mi2->image !=NULL)
	ecrisBMPRGB_Dans(mi2->image,"testEdges.bmp");*/

	regionGrowingProcess(&(mi->red), &(mi->blue), mi->grey, 0, 127, 0.5, 8, 0, mi->l, 0, mi->h, mi->l, mi->h);
	changeImageNB(&(mi->image), mi->red);
	if(mi->image !=NULL)
	ecrisBMPRGB_Dans(mi->image,"RegionGrowingTest1.bmp");
	changeImageNB(&(mi->image), mi->blue);
	if(mi->image !=NULL)
	ecrisBMPRGB_Dans(mi->image,"RegionGrowingTest2.bmp");

	symmetryMeasure(&(shape), mi->grey, mi->l, mi->h);
	/*
	printf("1\n");
	int nb = 0;
	regionGrowing(&(mi->red), mi2->grey, 0, shape->bb[0][0], shape->bb[1][0], shape->bb[2][1], shape->bb[1][1], mi->l, mi->h, 1, 8, 0, &nb);
	changeImageNB(&(mi->image), mi->red);
	if(mi->image !=NULL)
	ecrisBMPRGB_Dans(mi->image,"RegionGrowingTest3.bmp");
	printf("nb = %d\n", nb);

	printf("2\n");
	regionGrowing(&(mi->green), mi2->grey, 0, shape->bb[0][0], shape->bb[1][0], shape->bb[2][1], shape->bb[1][1], mi->l, mi->h, 1, 8, 1, &nb);
	changeImageNB(&(mi->image), mi->green);
	if(mi->image !=NULL)
	ecrisBMPRGB_Dans(mi->image,"RegionGrowingTest4.bmp");
	printf("nb = %d\n", nb);
	
	printf("3\n");
	regionGrowing(&(mi->blue), mi2->grey, 0, shape->bb[0][0], shape->bb[1][0], shape->bb[2][1], shape->bb[1][1], mi->l, mi->h, 1, 8, 2, &nb);
	changeImageNB(&(mi->image), mi->blue);
	if(mi->image !=NULL)
	ecrisBMPRGB_Dans(mi->image,"RegionGrowingTest5.bmp");
	printf("nb = %d\n", nb);
	*/
	connectivity(&shape, mi2->grey, mi2->l, mi2->h, 1, 8);
	
	/*dilatationPoints(&(mi->grey), mi2->grey, shape->points, shape->nbPt, 0, 5, 4, 0, mi2->l, 0, mi2->h, mi2->l, mi2->h);
	changeImageNB(&(mi2->image), mi->grey);
	if(mi2->image !=NULL)
	ecrisBMPRGB_Dans(mi2->image,"testPolyDilatation4.bmp");*/
	/*dilatationPoints(&(mi->grey), mi2->grey, shape->edges, shape->nbPtE, 0, 5, 4, 0, mi2->l, 0, mi2->h, mi2->l, mi2->h);
	changeImageNB(&(mi2->image), mi->grey);
	if(mi2->image !=NULL)
	ecrisBMPRGB_Dans(mi2->image,"testPolyDilatation4.bmp");*/
	//computeMaxFeretDiameter(&shape);


	//dilatation(&(mi->grey),mi2->grey, 255, 0, mi->l, mi->h);
	//changeImageNB(&(mi->image), mi2->grey);
	//ecrisBMPRGB_Dans(mi2->image,"testNew.bmp");
	/*ecrisBMPRGB_Dans(mi->image,mi->nameBMP);
	setHistogramsInMI(&mi);
	printHistogram(mi->histo);
	printHistogram(mi->chisto);*/

	//Median
	/*regionGrowingMI(&mi, 40, 4, 1);
	chaine str;
	strcpy(str, "etiq region growing ");
	strcat(str,mi->nameBMP);
	ecrisBMPRGB_Dans(mi->image,str);*/
	
	freeShape(&shape);
	libereDonneesImageRGB(&image);
	libereDonneesImageRGB(&image2);
	freeMatImage(&mi);
	freeMatImage(&mi2);
	return 0;
}
