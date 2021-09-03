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
void create1matrixInt(int *** m, int l, int h){
	int i, j;
	i = j = 0;
	int ** matrix = *m;

	matrix = (int**)malloc(sizeof(int *)*h);
	for(i = 0 ; i < h ; i++)
		matrix[i] = (int*)malloc(sizeof(int)*l);

	for(i = 0 ; i < h ; i++){
		for(j = 0 ; j < l ; j++){
			matrix[i][j] = 0;
		}
	}

	*m = matrix;
}

//Liberation of one matrix
void free1matrixInt(int *** m, int h){
	int ** matrix = NULL;
	int i = 0;
	matrix = *m;

	if(matrix != NULL){
		for(i = 0 ; i < h ; i++){
		if(matrix[i] != NULL)
		free(*(matrix+i));
		*(matrix+i) = NULL;
	}

	free(matrix);
	matrix = NULL;
	}

	*m = matrix;
}

void freeShape(Shape ** shape){
	Shape * s = *shape;
	if(s != NULL){
		if(s->points != NULL && s->nbPt != 0){
			free1matrixInt(&(s->points), s->nbPt);
			s->points = NULL;
		}
		if(s->edges != NULL && s->nbPtE != 0){
			free1matrixInt(&(s->edges), s->nbPtE);
			s->edges = NULL;
		}
		if(s->hull != NULL && s->nbPtH != 0){
			free1matrixInt(&(s->hull), s->nbPtH);
			s->hull = NULL;
		}
		if(s->bb != NULL){
			free1matrixInt(&(s->bb), 4);
			s->bb = NULL;
		}
		free(s);
		s = NULL;
	}
	*shape = s;
}

void exchangeInt2(int ** tab, int i, int j){
	int tab0;
	int tab1;

	tab0 = tab[i][0];
	tab1 = tab[i][1];

	tab[i][0] = tab[j][0];
	tab[i][1] = tab[j][1];

	tab[j][0] = tab0;
	tab[j][1] = tab1;
}

//sorting in ascendant way
void ascendingSortInt2(int** tab, int dim){
	int notfinished = 1;
	int i = 0;
	while(notfinished == 1){
		notfinished = 0;
		for(i = 0; i < dim-1; i++){
			if(tab[i+1][0] > tab[i][0]){
				exchangeInt(tab, i, i+1);
				notfinished = 1;
			}
			/*else if(tab[i+1][0] == tab[i][0]){
				if(tab[i+1][1] < tab[i][1]){
					exchangeInt(tab, i, i+1);
					notfinished = 1;
				}
			}*/
		}
	}
}


//Find point of a shape
void shapePoint(Shape ** shape, short int ** image, short int ** originalImage, short int etiq, int l, int h){
	//Creation of shape
	Shape * s = *shape;
	s = (Shape*)malloc(sizeof(Shape));
	s->etiq = etiq;

	//Initialization
	s->perimeterCrofton = 0;
	//maximal and minimal Féret diameter and convex hull
	s->nbPtH = 0;
	s->hull = NULL;
	s->maxFeretDiameter = 0;
	s->minFeretDiameter = 0;
	//Circularity
	s->geometrical = 0;
	s->radial = 0;
	//Symmetry - Blaschke
	s->minkowski = 0;
	s->blaschke = 0;
	//Connectivity
	s->connect = 0;
	s->nbConnectedComponent = 0;
	s->nbHoles = 0;

	//Declaration
	int maxX = 0;
	int minX = 99999999;
	int maxY = 0;
	int minY = 99999999;
	int counter1 = 0;
	int counter2 = 0;
	int counter3 = 0;
	double mean = 0;

	//We retrieve the number of points and the min and max on y and x axis
	for(int i = 0; i < h; i ++){
		for(int j = 0; j < l; j ++){
			if(image[i][j] == etiq){ // If we find an element of the shape
				if(i < minY) minY = i;
				if(j < minX) minX = j;
				if(i > maxY) maxY = i;
				if(j > maxX) maxX = j;
				counter1 ++;

				//We sum the color
				mean = mean + originalImage[i][j];

				int neighbour = 0;
				for(int n = i-1 ; n < i+2; n++){
					for(int m = j-1 ; m < j+2; m++){
						if((n >= 0 && n < h) && (m >=0 && m < l)){
							if(image[n][m] != etiq)
								neighbour ++;
						}
						else {
							neighbour ++;
						}
					}
				}

				if(neighbour > 0)
					counter2 ++;
				if(neighbour > 1)
					counter3++;

				neighbour = 0;
			}
		}
	}
	mean = mean/counter1;
	s->meanColor = mean;
	s->perimeter = counter3;

	//Creation of the tab of points
	s->nbPt = counter1; //also the area
	create1matrixInt(&(s->points), 2, counter1);

	//Creation of the edges
	s->nbPtE = counter2;
	create1matrixInt(&(s->edges), 2, counter2);

	//Diminution of approximation on the perimeter
	counter3 = counter2 + counter3;
	s->perimeter = (int)counter3/2;

	//Creation of the bounding box
	create1matrixInt(&(s->bb), 2, 4);
	//Upper on the left
	s->bb[0][0] = minX;
	s->bb[0][1] = maxY;

	//Upper on the right
	s->bb[1][0] = maxX;
	s->bb[1][1] = maxY;

	//Lower on the left
	s->bb[2][0] = minX;
	s->bb[2][1] = minY;

	//Lower on the right
	s->bb[3][0] = maxX;
	s->bb[3][1] = minY;

	s->vertical = maxY - minY;
	s->horizontal = maxX - minX;
	if(s->vertical > s->horizontal)
		s->elongation = (double)(s->horizontal/s->vertical);
	else
		s->elongation = (double)(s->vertical/s->horizontal);

	int nb = 0;
	double stD = 0;
	int k = 0;
	for(int i = 0; i < h; i ++){
		for(int j = 0; j < l; j ++){
			if(image[i][j] == etiq){ // If we find an element of the shape
				s->points[k][0] = j; //x
				s->points[k][1] = i; //y

				if(k < counter1)
					k++;

				//We compute the standard deviation
				stD = stD + (double)(((double)(originalImage[i][j]-mean))*((double)(originalImage[i][j]-mean)));
				int neighbour = 0;
				//We look if at least one neighbour is of a different colour

				for(int n = i-1 ; n < i+2; n++){
					for(int m = j-1 ; m < j+2; m++){
						if((n >= 0 && n < h) && (m >=0 && m < l)){
							if(image[n][m] != etiq)
								neighbour ++;
						}
						else {
							neighbour ++;
						}
					}
				}

				if(neighbour > 0) {
					s->edges[nb][0] = j; //x
					s->edges[nb][1] = i; //y
					if(nb < counter2)
						nb++;

				}
				neighbour = 0;
			}
		}
	}

	ascendingSortInt2(s->edges, s->nbPtE);
	ascendingSortInt2(s->points, s->nbPt);

	stD = stD/counter1;
	s->standardDeviation = sqrt(stD);

	*shape = s;
}

//Vector
void vector(int * y, int * x, int x1, int y1, int x2, int y2){
	*x = x2 - x1;
	*y = y2 - y1;
}

//Norm
double norm(int x, int y){
	return sqrt((double)(x*x + y*y));
}

//Scalar Product
double scalarProduct(int x1, int y1, int x2, int y2){
	return x1*x2 + y1*y2;
}

//Angle in degree
double angle(int x1, int y1, int x2, int y2, int rad){
	if(rad == 1){
		return (double)acos(scalarProduct(x1, y1, x2, y2)/(norm(x1, y1)*norm(x2, y2)));
	}
	else {
		return (180/M_PI)*acos(scalarProduct(x1, y1, x2, y2)/(norm(x1, y1)*norm(x2, y2)));
	}
}

//Distance
double distance(int x1, int y1, int x2, int y2){
	return (double)sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1));
}

// Orientation of three points // colinear if == 0, turn to the left if > 0, turn to the right if < 0
int orientation(int x1, int y1, int x2, int y2, int x3, int y3){
    return (double)((double)((y2 - y1) * (x3 - x1)) - (double)((x2 - x1) * (y3 - y1)));
}

//Sorting functions
//exchange two elements
void exchangeInt(int ** tab, int i, int j){
	int tab0;
	int tab1;
	int tab2;

	tab0 = tab[i][0];
	tab1 = tab[i][1];
	tab2 = tab[i][2];

	tab[i][0] = tab[j][0];
	tab[i][1] = tab[j][1];
	tab[i][2] = tab[j][2];

	tab[j][0] = tab0;
	tab[j][1] = tab1;
	tab[j][2] = tab2;
}

//sorting in ascendant way
void ascendingSortInt(int** tab, int dim){
	int notfinished = 1;
	int i = 0;
	while(notfinished == 1){
		notfinished = 0;
		for(i = 1; i < dim-1; i++){
			if(tab[i+1][1] < tab[i][1]){
				exchangeInt(tab, i, i+1);
				notfinished = 1;
			}
			else if(tab[i+1][1] == tab[i][1]){
				if(tab[i+1][2] > tab[i][2]){
					exchangeInt(tab, i, i+1);
					notfinished = 1;
				}
			}
		}
	}
}

//Convex Hull of a shape
void convexHullGraham(Shape ** shape, int ** points, int nbPt, int l ){
	Shape * s = *shape;
	//Find the bottom-most point
	int minY = 99999;
	int minX = 99999;
	int rankMin = 0;

	for(int k = 0; k < nbPt; k++){
		if(points[k][1] <= minX){ //y
			minX = points[k][1];
			rankMin = k;
			minY = points[k][0];
			if(points[k][0] < minY){ //x
				minY = points[0][1];
				rankMin = k;
			}
		}
	}

	//This point is the first point of the convex hull
	//It is the first point of the convex hull
	int ** intermediate1 = NULL;
	create1matrixInt(&(intermediate1), 3, nbPt);

	intermediate1[0][0] = rankMin; //rank
	intermediate1[0][1] = 0; //angle
	intermediate1[0][2] = 0; //distance

	//Pt necessary for the angle's computation
	int vector_x1 = 0;
	int vector_y1 = 0;

	int vector_x2 = 0;
	int vector_y2 = 0;

	int axis_x = l-1;
	int axis_y = minY;
	double angl = 0;

	//Now we compute all the angle between an horizontal axis and all the other point
	for(int k = 0; k < nbPt; k++){
		if(k < rankMin){
			intermediate1[k+1][0] = k;

			//We compute the two vector
			vector(&vector_x1, &vector_y1, points[rankMin][0], points[rankMin][1], points[k+1][0], points[k+1][1]);
			vector(&vector_x2, &vector_y2, points[rankMin][0], points[rankMin][1], axis_x, axis_y);

			//We compute the angle between them
			angl = angle(vector_x1, vector_y1, vector_x2, vector_y2, 0) + 0.5;

			if(isnan(angl)){ //nan
				intermediate1[k+1][1] = 0;
			}
			else {
				intermediate1[k+1][1] =  (int)angl;
			}

			//We compute the distance
			intermediate1[k+1][2] = (int)(distance(points[rankMin][0], points[rankMin][1], points[k+1][0], points[k+1][1]) + 0.5);

		}
		else if(k > rankMin){
			intermediate1[k][0] = k;

			//We compute the two vector
			vector(&vector_x1, &vector_y1, points[rankMin][0], points[rankMin][1], points[k][0], points[k][1]);
			vector(&vector_x2, &vector_y2, points[rankMin][0], points[rankMin][1], axis_x, axis_y);

			//We compute the angle between them
			angl = angle(vector_x1, vector_y1, vector_x2, vector_y2, 0) + 0.5;

			if(isnan(angl)){ //nan
				intermediate1[k][1] = 0;
			}
			else {
				intermediate1[k][1] =  (int)angl;
			}

			//We compute the distance
			intermediate1[k][2] = (int)(distance(points[rankMin][0], points[rankMin][1], points[k][0], points[k][1]) + 0.5);

		}
	}

	ascendingSortInt(intermediate1, nbPt);

	//We remove the element k when angle of k and k+1 is the same (colinear)
	int size = 0;
	for(int k = 1; k < nbPt; k++){
		while(k < nbPt - 1 && intermediate1[k][1] == intermediate1[k+1][1]){
			intermediate1[k+1][2] = -1; //We put -1 in the last case to say that we don't keep this element
			k ++;
		}
		size ++; //we count the number of element in the next step
	}

	if(size < 3){ //If we don't have enough point, we stop the computation
		free1matrixInt(&intermediate1, nbPt);
		s->hull = NULL;
		s->nbPtH = 0;
		return;
	}

	int ** intermediate2 = NULL;
	create1matrixInt(&intermediate2, 1, size);
	intermediate2[0][0] = intermediate1[0][0];
	int i = 1;

	//We will remove the -1 marked point
	for(int k = 1; k < nbPt; k++){
		while(k < nbPt - 1 && intermediate1[k][2] == -1)
			k++;
		intermediate2[i][0] = intermediate1[k][0]; //we add the element without -1 in the new tab
		if(i < size - 1)
			i++;
	}

	int ** intermediate3 = NULL;
	create1matrixInt(&intermediate3, 1, size);

	//1
	intermediate3[0][0] = intermediate2[0][0];
	//2
	intermediate3[1][0] = intermediate2[1][0];

	int size2 = 2; //size of the real convex hull
	int n = 2;

	for(int k = 2; k < size; k++){
		vector_x1 = points[intermediate3[n-2][0]][0];
		vector_y1 = points[intermediate3[n-2][0]][1];
		vector_x2 = points[intermediate3[n-1][0]][0];
		vector_y2 = points[intermediate3[n-1][0]][1];
		//We remove element when the angle formy by it and two previous one
		while(k < size - 1 && orientation(vector_x1, vector_y1, vector_x2, vector_y2, points[intermediate2[k][0]][0], points[intermediate2[k][0]][1]) == 0){
			k++;
		}
		intermediate3[n][0] = intermediate2[k][0];
		n++;
		size2 ++;
	}

	if(size2 < 3){ //If we don't have enough point, we stop the computation
		free1matrixInt(&intermediate1, nbPt);
		free1matrixInt(&intermediate2, size);
		free1matrixInt(&intermediate3, size);
		s->hull = NULL;
		s->nbPtH = 0;
		return;
	}

	i = 0;
	//We conserve only the element with a +1 in the hull
	create1matrixInt(&(s->hull), 2, size2);
	s->nbPtH = size2;

	i = 0;
	for(int k = 0; k < size2; k++){
		s->hull[k][0] = points[intermediate3[k][0]][0];
		s->hull[k][1] = points[intermediate3[k][0]][1];
	}

	free1matrixInt(&intermediate1, nbPt);
	free1matrixInt(&intermediate2, size);

	*shape = s;
}

//Draw  points on a picture
void printPoints(int ** points, int nbPt, short int ** red, short int ** green, short int ** blue, int l, int h, short int r, short int g, short int b){
	if(nbPt == 0 || points == NULL) return;
	r = 127;
	g = 127;
	b = 127;
	for(int i = 0; i < nbPt; i++){
		for(int n = points[i][1]-1; n < points[i][1]+2; n++){
			for(int m = points[i][0]-1; m < points[i][0]+2; m++){
				if(i < 20){
					red[n][m] = r;
					green[n][m] = g;
					blue[n][m] = b;
					r = r + 10;
				}
				else {
					r = 255;
					g = 0;
					b = 0;
					if(n >= 0 && n < h && m >= 0 && m < l && red[n][m] != 127){
						red[n][m] = r;
						green[n][m] = g;
						blue[n][m] = b;
					}
				}
			}
		}
	}
}


//Geometrical circularity
void geometricalCircularity(Shape ** shape){
	Shape * s = *shape;

	s->geometrical = (double)((double)(4*M_PI*s->nbPt)/(double)(s->perimeter*s->perimeter));

	*shape = s;
}

//Symmetry measure - Blaschke
void symmetryMeasure(Shape ** shape, short int ** image, int l, int h){
	Shape * s = *shape;

	//We need two pictures
	short int ** x = NULL;
	short int ** xMinus = NULL;
	create1matrix(&x, l, h);
	create1matrix(&xMinus, l, h);

	if(s->etiq < 127){
		initialize255(&xMinus, l, h);
		initialize255(&x, l, h);
	}

	//We devide the place to work in order to stay beyond the borders
	int div = l*h/((s->bb[0][0]-s->bb[1][0])*(s->bb[2][1]-s->bb[1][1]));

	//We resize x
	for(int i = 0; i < h/div; i++){
		for(int j = 0; j < l/div; j++){
			x[i+((h-h/div))/2][j+((l-l/div)/2)]= image[div*i][div*j];
		}
	}

	//We create the shape of x
	Shape * xShape = NULL;
	shapePoint(&xShape, x, x, s->etiq, l, h);

	//We draw xMinus
	for(int i = xShape->bb[2][1]; i < xShape->bb[1][1]; i++){
		for(int j = xShape->bb[0][0]; j < xShape->bb[1][0]; j++){
			xMinus[i][j] = x[xShape->bb[1][1]+xShape->bb[2][1]-i][xShape->bb[1][0]+xShape->bb[0][0]-j];
		}
	}

	//We create the shape of x minus
	Shape * xMinusShape = NULL;
	shapePoint(&xMinusShape, xMinus, xMinus, s->etiq, l, h);

	//For all the point of the Edge of the shape X
	for(int k = 0; k < xShape->nbPtE; k++){
		//We draw the shape x minus
		for(int i = 0; i < xMinusShape->bb[1][1] - xMinusShape->bb[2][1]; i++){
			for(int j = 0; j < xMinusShape->bb[1][0] - xMinusShape->bb[0][0]; j++){
				if(xMinus[xMinusShape->points[0][1]+i][xMinusShape->points[0][0]+j] == xMinusShape->etiq)
				x[i + xShape->edges[k][1]][j + xShape->edges[k][0]] = xMinus[xMinusShape->points[0][1]+i][xMinusShape->points[0][0]+j];
			}
		}
	}

	//We count the sum of X and X-
	int counter  = 0;
	for(int i = 0; i < h; i++){
		for(int j = 0; j < l; j++){
			if(x[i][j] == xShape->etiq){
				counter ++;
			}
		}
	}

	//We devide this sum by 2
	s->minkowski = (double)(counter* div * div /2.);
	s->blaschke = (double)((double)s->nbPt/s->minkowski);

	//We free the shape
	if(xMinusShape != NULL)
	freeShape(&xMinusShape);
	if(xShape != NULL)
	freeShape(&xShape);
	if(x != NULL)
	free1matrix(&x, h);
	if(xMinus != NULL)
	free1matrix(&xMinus, h);

	*shape = s;
}

//Connectivity measure
void connectivity(Shape ** shape, short int ** image, int l, int h, int threshold, int window){
	Shape * s = *shape;;
	short int ** new = NULL;
	short int ** object = NULL;
	int nbCC = 0;
	int nbH = 0;
	create1matrix(&new, l, h);
	create1matrix(&object, l, h);

	// First : we label the connected components and retrieve the last label, which is the number of labels
	regionGrowing(&new, image, s->etiq, s->bb[0][0], s->bb[1][0], s->bb[2][1], s->bb[1][1], l, h, threshold, window, 0, &nbCC);
	s->nbConnectedComponent = nbCC;

	//Second : We threshold the image for safety
	manualThresholdNB(h, l, &new, nbCC+1);

	//Third : We reverse the color
	negativeImage(h, l, &new, &new, &new);

	//Fourth : we label the holes and the background
	regionGrowing(&object, new, 0, s->bb[0][0]-10, s->bb[1][0]+10, s->bb[2][1]-10, s->bb[1][1]+10, l, h, threshold, window, 0, &nbH);

	//Fifth : we remove the background
	nbH--;
	s->nbHoles = nbH;

	//Sixth : we compute the connectivity using the number of holes and connected components
	s->connect = nbCC - nbH;

	// Now we check in all the connected component if there is a
	free1matrix(&new, h);
	free1matrix(&object, h);
	*shape = s;
}

