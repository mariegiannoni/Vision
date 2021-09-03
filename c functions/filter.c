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

//FILTERS

//Contrast stretching
void contrastStretching(MatImage ** mat){
	MatImage *mi = *mat;
	short int expdyn = 0;
	int i = 0;
	int j = 0;
	//expdyn = ai+b with a = (255-0)/(ngmax-ngmin) and b = (0*ngmax-255*ngmin)/(ngmax-ngmin)
	//ngmax - ngmin
	int delta = mi->histo->nimax - mi->histo->nimin;
	double a = (double)(255/delta);
	double b = (double)((-255*mi->histo->nimin)/delta);

	for(i = 0 ; i < (mi->h) ; i++){
		for(j = 0 ; j < (mi->l) ; j++){
			//expdyn = 255*(mi->grey[i][j]-mi->histo->nimin)/(mi->histo->nimax - mi->histo->nimin);
			expdyn = (short int)(a*(mi->grey[i][j])+b);
			mi->red[i][j] = expdyn;
			mi->green[i][j] = expdyn;
			mi->blue[i][j] = expdyn;
		}
	}

	*mat = mi;
}

//shades of grey
void shadesOfGrey(short int *** grey, short int ** red, short int ** green, short int ** blue, int l, int h){
	int i = 0;
	int j = 0;
	short int ** g = *grey;

	for(i=0;i<h;i++){
		for(j=0;j<l;j++){
			*(*(g+i)+j)=(*(*(red+i)+j))*0.2125+(*(*(green+i)+j))*0.7154+(*(*(blue+i)+j))*0.0721;
		}
	}
	*grey = g;
}

//Negative image
void negativeImage(int h, int l, short int *** red, short int *** green, short int *** blue){
	int i,j;
	short int ** r = *red;
	short int ** v = *green;
	short int ** b = *blue;
	short int r1,b1,v1;
	for(i=0;i<h;i++){
		for(j=0;j<l;j++){
			r1 = r[i][j];
			b1 = b[i][j];
			v1 = v[i][j];
			r[i][j]=255-r1;
			v[i][j]=255-v1;
			b[i][j]=255-b1;
		}
	}
	*red = r;
	*blue = b;
	*green = v;
}

//Manual Threshold
void manualThreshold(int h, int l, short int ***red, short int ***green, short int ***blue, short int threshold)
{
    int i,j;
	short int ** r = *red;
	short int ** v = *green;
	short int ** b = *blue;
    for(i=0;i<h;i++)
    {
        for(j=0;j<l;j++)
        {
            if(threshold >= r[i][j])
            {
                r[i][j]=0;
                v[i][j]=0;
                b[i][j]=0;
            }
            else
            {
				r[i][j]=255;
                v[i][j]=255;
                b[i][j]=255;
            }
        }
    }
    *red = r;
	*blue = b;
	*green = v;
}

//Manual Threshold NB
void manualThresholdNB(int h, int l, short int ***grey, short int threshold){
    int i,j;
	short int ** g = *grey;

    for(i = 0; i < h; i++)
    {
        for(j = 0; j < l; j++)
        {
            if(g[i][j] > threshold)
            {
                g[i][j] = 255;
            }
            else
            {
				g[i][j] = 0;
            }
        }
    }
    *grey = g;
}

//Median Filter 3x3 and 5x5
//Sorting functions
//exchange two elements
void exchange(short int * tab, int i, int j){
	short int tab1;
	tab1=tab[i];
	tab[i]=tab[j];
	tab[j]=tab1;
}

//sorting in ascendant way
void ascendingSort(short int * tab, short int dim){
	int notfinished = 1;
	short int i = 0;
	while(notfinished == 1){
		notfinished = 0;
		for(i = 0; i < dim; i++){
			if(tab[i+1]<tab[i]){
				exchange(tab, i, i+1);
				notfinished = 1;
			}
		}
	}
}

//Median Filter nxn
//Calculation of the median for nxn values
void computeMedian(short int ** grey, short int * median, int i, int j, short int dim){
	short int * tab = (short int *)malloc(sizeof(short int)*dim*dim);
	short int k, l, m;
	k = l = m = 0;
	for(k = (int)(i - ((dim - 1)/2)); k < (int)(i + ((dim - 1)/2)) +1 ; k++){
		for(l = (int)(j - ((dim - 1)/2)); l < (int)(j + ((dim - 1)/2))+1 ; l++){
			tab[m] = grey[k][l];
			m++;
		}
	}
	//we put all the dimxdim pixel in a tab and sort them in ascending way
	ascendingSort(tab,dim*dim);
	//the retrieve the central element of the tab
	*median=tab[(int)((dim*dim-1)/2)];
}

//Median Filter NxN
void medianFilterNxN(short int *** new, short int ** grey, int l, int h, short int dim){
	int i,j;
	int p = dim/2;
	short int median;
	short int ** n = *new;
	for(i=p;i<h-p;i++){
		for(j=p;j<l-p;j++){
			//we compute the median for the central pixel i,j of a matrix dimxdim
			computeMedian(grey, &median, i, j, dim);
			n[i][j] = median;
		}
	}
	*new = n;
}

//Median Filter MI NxN
void medianFilterMINxN(MatImage ** picture, short int dim){
	MatImage * pict = *picture;
	//intermediate matrix for the change
	short int ** intermediate = NULL;
	create1matrix(&intermediate, pict->l, pict->h);
	//compute median filter
	medianFilterNxN(&(intermediate), pict->grey, pict->l, pict->h, dim);
	//we change the matrix and the picture
	duplicateMatrice(pict->grey, intermediate, pict->l, pict->h);
	changeImageNB(&(pict->image), pict->grey);
	free1matrix(&intermediate, pict->h);
	*picture = pict;
}


//Mean Filter NxN
//Calculation of the mean for nxn values
void computeMean(short int ** grey, short int *mean, int i, int j, short int dim){
	short int sum = 0;
	int k, l;
	for(k = (int)(i - ((dim - 1)/2)); k < (int)(i + ((dim - 1)/2)) +1 ; k++){
		for(l = (int)(j - ((dim - 1)/2)); l < (int)(j + ((dim - 1)/2))+1 ; l++){
			sum = sum + *(*(grey+k)+l);
		}
	}
	//we do the average of the elements in a matrix
	sum = sum/(dim*dim);
	*mean=sum;
}

//average filter
void averageFilterNxN(short int *** new, short int ** grey, int l, int h, short int dim){
	int i, j;
	short int mean;
	short int ** n = *new;
	int p = dim/2;
	for(i=p;i<h-p;i++){
		for(j=p;j<l-p;j++){
			//the central element is equal to the average of the matrix of size dimxdim centralized on it
			computeMean(grey, &mean, i, j, dim);
			n[i][j] = mean;
		}
	}
	*new = n;
}

//average filter MI
void averageFilterMINxN(MatImage ** picture, short int dim){
	MatImage * pict = *picture;
	//intermediate matrix for the change
	short int ** intermediate = NULL;
	create1matrix(&intermediate, pict->l, pict->h);
	//compute average filter
	averageFilterNxN(&(intermediate), pict->grey, pict->l, pict->h, dim);
	//we change the matrix and the picture
	duplicateMatrice(pict->grey, intermediate, pict->l, pict->h);
	changeImageNB(&(pict->image), pict->grey);
	free1matrix(&intermediate, pict->h);
	*picture = pict;
}

double gaussian(int x, int y, double sigma){
	double sigma_2 = sigma*sigma;
	double x_2 = x*x;
	double y_2 = y*y;

	double gxy = 1./(sqrt(2*M_PI)*sigma_2);

	gxy = gxy*exp((-(x_2+y_2)/sigma_2));

	return gxy;
}

//gaussian filter nxn
//compute the gaussian coefficient and applied them
void computeGaussian(short int ** grey, short int *gauss, int i, int j, short int dim){
	short int wsum = 0;
	short int sum = 0;
	double coeff = 0;
	short int  p = dim/2.;

	int k, l;
	for(k = (int)(i - ((dim - 1)/2)); k < (int)(i + ((dim - 1)/2)) +1 ; k++){
		for(l = (int)(j - ((dim - 1)/2)); l < (int)(j + ((dim - 1)/2))+1 ; l++){
			// coeff = ((dim²-1)/4)²x((dim-1)/(dim+1))^((k-p)²+(l-p)²) + 0.5 (approximation of the gaussian)
			coeff = (double)((((double)(dim*dim)-1)/4.)*(((double)dim*dim-1)/4.)*pow((double)(dim-1)/(dim+1),(double)((k-p)*(k-p)+(l-p)*(l-p)))+0.5);
			//I force the little element to 1 in order them to not be null when they are non null
			if(coeff < 1 && coeff != 0) coeff = 1;
			//weighted sum of coeff
			wsum = wsum + coeff;
			//sum of the elements multiplied per their coeff
			sum = sum + coeff*grey[k][l];
		}
	}
	//we devide the sum per the weighted sum
	sum = sum/wsum;
	*gauss=sum;
}

//Gaussian Filter with a dim n
void gaussianFilterNxN(short int *** new, short int ** grey, int l, int h, short int dim){
	int i, j;
	short int gauss;
	short int ** n = *new;
	int p = dim/2;
	for(i=p;i<h-p;i++){
		for(j=p;j<l-p;j++){
			//compute the central element with an gaussian approximation of a matrix dimxdim
			computeGaussian(grey, &gauss, i, j, dim);
			n[i][j] = gauss;
		}
	}
	*new = n;
}

//gaussian filter MI
void gaussianFilterMINxN(MatImage ** picture, short int dim){
	MatImage * pict = *picture;
	//intermediate matrix for the change
	short int ** intermediate = NULL;
	create1matrix(&intermediate, pict->l, pict->h);
	//compute gaussian filter
	gaussianFilterNxN(&(intermediate), pict->grey, pict->l, pict->h, dim);
	//we change the matrix and the picture
	duplicateMatrice(pict->grey, intermediate, pict->l, pict->h);
	changeImageNB(&(pict->image), pict->grey);
	free1matrix(&intermediate, pict->h);
	*picture = pict;
}

//dilatation filter
//compute dilatation
void computeDilatation(short int ** grey, short int *dil, int i, int j, short int dim){
	short int sup = 0;

	int k, l;
	for(k = (int)(i - ((dim - 1)/2)); k < (int)(i + ((dim - 1)/2)) +1 ; k++){
		for(l = (int)(j - ((dim - 1)/2)); l < (int)(j + ((dim - 1)/2))+1 ; l++){
			if(grey[k][l] > sup) sup = grey[k][l];
		}
	}
	*dil=sup;
}

//dilatation for nxn window
void dilatationFilterNxN(short int *** new, short int ** grey, int l, int h, short int dim){
	int i, j;
	short int dil;
	short int ** n = *new;
	int p = dim/2;
	for(i = p; i < h-p; i++){
		for(j = p; j < l-p; j++){
			//compute the central pixel i,j of a matrix of size dimxdim
			computeDilatation(grey, &dil, i, j, dim);
			n[i][j] = dil;
		}
	}
	*new = n;
}

//dilatation filter MI
void dilatationFilterMINxN(MatImage ** picture, short int dim){
	MatImage * pict = *picture;
	//intermediate matrix for the change
	short int ** intermediate = NULL;
	//compute dilatation filter
	dilatationFilterNxN(&(intermediate), pict->grey, pict->l, pict->h, dim);
	//we change the matrix and the picture
	duplicateMatrice(pict->grey, intermediate, pict->l, pict->h);
	changeImageNB(&(pict->image), pict->grey);
	free1matrix(&intermediate, pict->h);
	*picture = pict;
}

//erosion filter
//compute erosion
void computeErosion(short int ** grey, short int *ero, int i, int j, short int dim){
	short int inf = 255;
	int k, l;
	for(k = (int)(i - ((dim - 1)/2)); k < (int)(i + ((dim - 1)/2)) +1 ; k++){
		for(l = (int)(j - ((dim - 1)/2)); l < (int)(j + ((dim - 1)/2))+1 ; l++){
			//we retrieve the inf of the matrix dimxdim
			if(grey[k][l] < inf) inf = grey[k][l];
		}
	}
	*ero=inf;
}

//erosionfor nxn window
void erosionFilterNxN(short int *** new, short int ** grey, int l, int h, short int dim){
	int i, j;
	short int ero;
	short int ** n = *new;
	int p = dim/2;
	for(i=p;i<h-p;i++){
		for(j=p;j<l-p;j++){
			//we compute the erosion for a i,j pixel with the elements around
			computeErosion(grey, &ero, i, j, dim);
			n[i][j] = ero;
		}
	}
	*new = n;
}

//dilatation filter MI
void erosionFilterMINxN(MatImage ** picture, short int dim){
	MatImage * pict = *picture;
	//intermediate matrix for the change
	short int ** intermediate = NULL;
	create1matrix(&intermediate, pict->l, pict->h);
	//compute erosion filter
	erosionFilterNxN(&(intermediate), pict->grey, pict->l, pict->h, dim);
	//we change the matrix and the picture
	duplicateMatrice(pict->grey, intermediate, pict->l, pict->h);
	changeImageNB(&(pict->image), pict->grey);
	free1matrix(&intermediate, pict->h);
	*picture = pict;
}

//Opening for MatImage - Erosion followed by a dilatation
void openingFilterMINxN(MatImage ** picture, short int dim){
	erosionFilterMINxN(picture,dim);
	dilatationFilterMINxN(picture,dim);
}

//Opening for MatImage - dilatation followed by an erosion
void closingFilterMINxN(MatImage ** picture, short int dim){
	dilatationFilterMINxN(picture,dim);
	erosionFilterMINxN(picture,dim);
}

//Roberts
void robertsFilter(short int *** gradient, short int ** grey, int l, int h, int norm){
	//Original image in shades of grey :
	short int ** image = grey;

	//compute image Gx (horizontal gradient)
	// Gx = I(i,j+1) - I(i,j)
	double x = 0;

	//compute image Gy (vertical gradient)
	// Gy = I(i+1,j) - I(i,j)
	double y = 0;

	//compute gradient norme
	// G = sqrt(Gx*Gx + Gy*Gy) (norm 2) or max(abs(Gx),abs(Gy)) (norme infini, sup) or abs(Gx)+abs(Gy) (norm 1)
	// G = arctan(Gy/Gx) (direction)
	short int ** g = *gradient;
	double xyg = 0;

	for(int i = 0; i < h-1; i++){
		for(int j = 0; j < l-1; j++){
			//Compute horizontal gradient
			x = image[i][j+1] - image[i][j];

			//Compute vertical gradient
			y = image[i+1][j] - image[i][j];

			//Computation of different values
			if(norm == 1){ //abs(Gx) + abx(Gy)
				xyg = abs(x) + abs(y);
			}
			else if (norm == 2){ //sqrt(Gx²+Gy²)
				xyg = sqrt(x*x+y*y);
			}
			else if (norm == 0){ //max(abs(Gx),abs(Gy))
				x > y ? xyg = abs(x) : abs(y);
			}
			else if (norm == 4){ //atan(y/x)
				xyg = (255./2)*atan((double)((y/x)/M_PI) + 1);
			}

			if(g[i][j] < 0) g[i][j] = 0;
			if(g[i][j] > 255) g[i][j] = 255;
			g[i][j] = (short int)xyg;
		}
	}

	*gradient = g;
}

//roberts for a matimage
void robertsFilterMI(MatImage ** picture, int norm){
	MatImage * pict = *picture;
	//intermediate 1 and 2 matrix for the change
	short int ** intermediate = NULL;
	create1matrix(&intermediate, pict->l, pict->h);
	//compute prewitt filter
	robertsFilter(&(intermediate), pict->grey, pict->l, pict->h,norm);
	//we change the matrix and the picture
	duplicateMatrice(pict->grey, intermediate, pict->l, pict->h);
	changeImageNB(&(pict->image), pict->grey);
	free1matrix(&intermediate, pict->h);
	*picture = pict;
}

//Prewitt
void prewittFilter(short int *** gradient, short int *** direction, short int ** grey, int l, int h){
	//Original image in shades of grey :
	short int ** image = grey;

	//compute image Gx (horizontal gradient)
	//		|-1  0 +1|
	// Gx = |-1  0 +1| * I
	//		|-1  0 +1|
	short int mx[3][3] = {{-1, 0, 1},
						  {-1, 0, 1},
						  {-1, 0, 1}};
	double x = 0;

	//compute image Gy (vertical gradient)
	//		|-1 -1 -1|
	// Gy = | 0  0  0| * I
	//		|+1 +1 +1|
	short int my[3][3] = {{-1, -1, -1},
						  {0, 0, 0},
						  {1, 1, 1}};
	double y = 0;

	//compute gradient norme
	// G = sqrt(Gx*Gx + Gy*Gy)
	short int ** g = *gradient;
	double xyg = 0;

	//Direction of the gradient
	// D = arctan(Gy/Gx)
	// ]-pi/2;pi/2[
	short int ** d = *direction;
	double xyd = 0;

	for(int i = 1; i < h-1; i++){
		for(int j = 1; j < l-1; j++){
			//Compute horizontal gradient
			x = mx[0][0]*image[i-1][j-1] + mx[0][1]*image[i][j-1] + mx[0][2]*image[i+1][j-1]
			  + mx[1][0]*image[i-1][j] + mx[1][1]*image[i][j] + mx[1][2]*image[i+1][j]
			  + mx[2][0]*image[i-1][j+1] + mx[2][1]*image[i][j+1] + mx[2][2]*image[i+1][j+1];

			//Compute vertical gradient
			y = my[0][0]*image[i-1][j-1] + my[0][1]*image[i][j-1] + my[0][2]*image[i+1][j-1]
			  + my[1][0]*image[i-1][j] + my[1][1]*image[i][j] + my[1][2]*image[i+1][j]
			  + my[2][0]*image[i-1][j+1] + my[2][1]*image[i][j+1] + my[2][2]*image[i+1][j+1];

			//Computation of different values
			xyg = sqrt(x*x+y*y);
			xyd = (255./2)*atan((double)((y/x)/M_PI) + 1); // I multiply per 100 because I will put it after in a short int, so I need an integer

			if(g[i][j] < 0) g[i][j] = 0;
			if(g[i][j] > 255) g[i][j] = 255;
			g[i][j] = (short int)xyg;
			d[i][j] = (short int)xyd;
		}
	}

	*gradient = g;
	*direction = d;
}

//prewitt for a matimage
void prewittFilterMI(MatImage ** picture){
	MatImage * pict = *picture;
	//intermediate 1 and 2 matrix for the change
	short int ** intermediate1 = NULL;
	short int ** intermediate2 = NULL;
	create1matrix(&intermediate1, pict->l, pict->h);
	create1matrix(&intermediate2, pict->l, pict->h);
	//compute prewitt filter
	prewittFilter(&(intermediate1),&(intermediate2), pict->grey, pict->l, pict->h);
	//we change the matrix and the picture
	duplicateMatrice(pict->grey, intermediate1, pict->l, pict->h);
	changeImageNB(&(pict->image), pict->grey);
	free1matrix(&intermediate1, pict->h);
	free1matrix(&intermediate2, pict->h);
	*picture = pict;
}

//Sobel
void sobelFilter(short int *** gradient, short int *** direction, short int ** grey, int l, int h){
	//Original image in shades of grey :
	short int ** image = grey;

	//compute image Gx (horizontal gradient)
	//		|-1  0 +1|
	// Gx = |-2  0 +2| * I
	//		|-1  0 +1|
	short int mx[3][3] = {{-1, 0, 1},
						  {-2, 0, 2},
						  {-1, 0, 1}};
	double x = 0;

	//compute image Gy (vertical gradient)
	//		|-1 -2 -1|
	// Gy = | 0  0  0| * I
	//		|+1 +2 +1|
	short int my[3][3] = {{-1, -2, -1},
						  {0, 0, 0},
						  {1, 2, 1}};
	double y = 0;

	//compute gradient norme
	// G = sqrt(Gx*Gx + Gy*Gy)
	short int ** g = *gradient;
	double xyg = 0;

	//Direction of the gradient
	// D = arctan(Gy/Gx)
	// ]-pi/2;pi/2[
	short int ** d = *direction;
	double xyd = 0;

	for(int i = 1; i < h-1; i++){
		for(int j = 1; j < l-1; j++){
			//Compute horizontal gradient
			x = mx[0][0]*image[i-1][j-1] + mx[0][1]*image[i][j-1] + mx[0][2]*image[i+1][j-1]
			  + mx[1][0]*image[i-1][j] + mx[1][1]*image[i][j] + mx[1][2]*image[i+1][j]
			  + mx[2][0]*image[i-1][j+1] + mx[2][1]*image[i][j+1] + mx[2][2]*image[i+1][j+1];

			//Compute vertical gradient
			y = my[0][0]*image[i-1][j-1] + my[0][1]*image[i][j-1] + my[0][2]*image[i+1][j-1]
			  + my[1][0]*image[i-1][j] + my[1][1]*image[i][j] + my[1][2]*image[i+1][j]
			  + my[2][0]*image[i-1][j+1] + my[2][1]*image[i][j+1] + my[2][2]*image[i+1][j+1];

			//Computation of different values
			xyg = sqrt(x*x+y*y);
			xyd = (255./2)*atan((double)((y/x)/M_PI) + 1); // I multiply per 100 because I will put it after in a short int, so I need an integer

			if(g[i][j] < 0) g[i][j] = 0;
			if(g[i][j] > 255) g[i][j] = 255;
			g[i][j] = (short int)xyg;
			d[i][j] = (short int)xyd;
		}
	}

	*gradient = g;
	*direction = d;
}

//sobel for a matimage
void sobelFilterMI(MatImage ** picture){
	MatImage * pict = *picture;
	//intermediate 1 and 2 matrix for the change
	short int ** intermediate1 = NULL;
	short int ** intermediate2 = NULL;
	create1matrix(&intermediate1, pict->l, pict->h);
	create1matrix(&intermediate2, pict->l, pict->h);
	//compute sobel filter
	sobelFilter(&(intermediate1),&(intermediate2), pict->grey, pict->l, pict->h);
	//we change the matrix and the picture
	duplicateMatrice(pict->grey, intermediate1, pict->l, pict->h);
	changeImageNB(&(pict->image), pict->grey);
	free1matrix(&intermediate1, pict->h);
	free1matrix(&intermediate2, pict->h);
	*picture = pict;
}

//Laplacian filter
void laplacianFilter(short int *** laplacian, short int ** grey, int l, int h, short int dim){
	//Original image in shades of grey :
	short int ** image = grey;

	short int ** m = NULL;
	create1matrix(&m,3,3);

	//compute coefficient - 4
	//	   |0  -1 0|
	// L = |-1 4 -1| * I
	//	   |0  -1 0|
	if(dim == 4){
		m[0][0] = 0;
		m[0][1] = -1;
		m[0][2] = 0;
		m[1][0] = -1;
		m[1][1] = 4;
		m[1][2] = -1;
		m[2][0] = 0;
		m[2][1] = -1;
		m[2][2] = 0;
	}

	//compute coefficient - 8
	//	   |-1 -1 -1|
	// L = |-1  8 -1| * I
	//	   |-1 -1 -1|
	else if(dim == 8){
		m[0][0] = -1;
		m[0][1] = -1;
		m[0][2] = -1;
		m[1][0] = -1;
		m[1][1] = 8;
		m[1][2] = -1;
		m[2][0] = -1;
		m[2][1] = -1;
		m[2][2] = -1;
	}

	double x = 0;
	short int ** lapla = *laplacian;

	for(int i = 1; i < h-1; i++){
		for(int j = 1; j < l-1; j++){
			//Compute horizontal gradient
			x = m[0][0]*image[i-1][j-1] + m[0][1]*image[i][j-1] + m[0][2]*image[i+1][j-1]
			  + m[1][0]*image[i-1][j] + m[1][1]*image[i][j] + m[1][2]*image[i+1][j]
			  + m[2][0]*image[i-1][j+1] + m[2][1]*image[i][j+1] + m[2][2]*image[i+1][j+1];

			//if(g[i][j] < 0) g[i][j] = 0;
			//if(g[i][j] > 255) g[i][j] = 255;
			lapla[i][j] = (short int)x;
		}
	}

	free1matrix(&m,3);
	*laplacian = lapla;
}

//laplacian for a matimage
void laplacianFilterMI(MatImage ** picture, short int dim){
	MatImage * pict = *picture;
	//intermediate 1 and 2 matrix for the change
	short int ** intermediate = NULL;
	create1matrix(&intermediate, pict->l, pict->h);
	//compute laplacian filter
	laplacianFilter(&(intermediate), pict->grey, pict->l, pict->h, dim);
	//we change the matrix and the picture
	duplicateMatrice(pict->grey, intermediate, pict->l, pict->h);
	changeImageNB(&(pict->image), pict->grey);
	free1matrix(&intermediate, pict->h);
	*picture = pict;
}

//Shade of grey of a MatImage
void shadeOfGreyMI(MatImage ** picture){
	MatImage * pict = *picture;
	shadesOfGrey(&(pict->grey),pict->red,pict->green,pict->blue,pict->h,pict->l);
	changeImageNB(&(pict->image), pict->grey);
	*picture = pict;
}

//compute median RGB
void computeMedianRGB(short int ** red, short int ** green, short int ** blue, int * row, int * column, int i, int j, short int dim){
	int p = (dim-1)/2;

	double distTot = 0;
	double minDistTot = 9999999999;
	int minDistK = 0;
	int minDistL = 0;

	for(int k = i - p; k < i + p + 1; k++){
		for(int l = j - p; l < j + p + 1; l++){
			distTot = 0;
			for(int n = i - p; n < i + p + 1; n++){
				for(int m = j - p; m < j + p + 1; m++){
					distTot = distTot
							  + (red[n][m] - red[k][l])*(red[n][m] - red[k][l])
						      + (green[n][m] - green[k][l])*(green[n][m] - green[k][l])
							  + (blue[n][m] - blue[k][l])*(blue[n][m] - blue[k][l]);
					}
			}
			if(minDistTot > distTot){
				minDistTot = distTot;
				minDistK = k;
				minDistL = l;
			}
		}
	}
	*row = minDistK;
	*column = minDistL;
}

//Median filter RGB
void medianFilterRGB(short int *** red, short int *** green, short int *** blue, short int ** r, short int ** g, short int ** b, int l, int h, short int dim){
	int p = (dim-1)/2;
	int column = 0;
	int row = 0;

	short int ** newr = *red;
	short int ** newg = *green;
	short int ** newb = *blue;

	for(int i = p; i < h - p; i++){
		for(int j = p; j < l - p; j++){
			computeMedianRGB(r, g, b, &row, &column, i, j, dim);
			newr[i][j] = r[row][column];
			newg[i][j] = g[row][column];
			newb[i][j] = b[row][column];
		}
	}

	*red = newr;
	*green = newg;
	*blue = newb;
}

//Median filter RGB for MI
void medianFilterRGBMI(MatImage ** picture, short int dim){
	MatImage * pict = *picture;

	//intermediate 1 and 2 matrix for the change
	short int ** intermediate1 = NULL;
	short int ** intermediate2 = NULL;
	short int ** intermediate3 = NULL;
	create3matrices(pict->image, &intermediate1, &intermediate2, &intermediate3);

	//compute laplacian filter
	medianFilterRGB(&(intermediate1), &(intermediate2), &(intermediate3), pict->red, pict->green, pict->blue, pict->l, pict->h, dim);

	//we change the matrix and the picture
	duplicateImage(pict->red, pict->green, pict->blue, intermediate1, intermediate2, intermediate3, pict->l, pict->h);
	changeImageRGB(&(pict->image), pict->red, pict->green, pict->blue);

	free3matrices(&intermediate1, &intermediate2, &intermediate3, pict->h);

	*picture = pict;
}


short int entropyMaximization(MatImage * pict){
	//Threshold
	short int threshold = 0;
	short int maxThreshold = 0;

	//Sum
	double sumMin = 0;
	double sumMax = 0;

	//entropy
	double entropy = 0;
	double maxEntropy = 0;

	//Probability
	double pi = 0;

	for(threshold = 0; threshold < 256; threshold ++){
		for(int k = 0; k < 256; k++){
			if(k <= threshold){ // we sum from 0 to the threshold the product of the probability of gray level i with the log of the probability
				pi = (double)(((double)(pict->histo->ni[k][1]))/((double)(pict->histo->N)));
				pi = pi*log(pi);
				if(pi < - 0.00001)
					sumMin = sumMin + pi;
			}
			else { // we sum from the threshold + 1 to 255
				pi = (double)(((double)(pict->histo->ni[k][1]))/((double)(pict->histo->N)));
				pi = pi*log(pi);
				if(pi < - 0.00001)
					sumMax = sumMax + pi;
			}
		}

		// we apply the formula
		entropy = - (1./pict->chisto->ni[threshold][1])*sumMin;
		entropy = entropy - (1./(pict->histo->N - pict->chisto->ni[threshold][1]))*sumMax;
		entropy = entropy + log(pict->chisto->ni[threshold][1]*((double)(pict->histo->N - pict->chisto->ni[threshold][1])));

		//we retrieve the threshold for the maximal value of entropy
		if(maxEntropy < entropy){
			maxEntropy = entropy;
			maxThreshold = threshold;
		}

		sumMax = 0;
		sumMin = 0;
	}
	return maxThreshold;
}

//Automatic thresholding by entropy maximization
void automaticThresholdingEntropyMaximization(MatImage ** picture){
	MatImage * pict = *picture;

	//Threshold
	short int threshold = entropyMaximization(pict);

	//We do a manual thresholdhing on the picture using the threshold retrieved here
	manualThresholdNB(pict->h,pict->l,&(pict->grey),threshold);

	//we change the matrix and the picture
	changeImageNB(&(pict->image), pict->grey);

	*picture = pict;
}

short int interclassVarianceMaximization(MatImage * pict){
	//Threshold
	short int threshold = 0;
	short int maxThreshold = 0;

	//Sum
	int sumMin = 0;
	int sumMax = 0;

	//proportion of pixel under and above the threshold
	int numberMin = 0;
	int numberMax = 0;

	//Variance
	double variance = 0;
	double varianceMax = 0;

	//Probability
	double pmin = 0;
	double pmax = 0;

	//Mean
	double mean = 0;
	double meanMax = 0;
	double meanMin = 0;

	for(threshold = 0; threshold < 256; threshold ++){
		for(int k = 0; k < 256; k++){
			if(k <= threshold){ // we sum from 0 to the threshold the value of pixel
				numberMin = numberMin + pict->histo->ni[k][1];
				sumMin = sumMin + pict->histo->ni[k][1]*k;
			}
			else { // we sum from the threshold + 1 to 255
				numberMax = numberMax + pict->histo->ni[k][1];
				sumMax = sumMax + pict->histo->ni[k][1]*k;
			}
		}

		//Mean
		if(numberMax != 0) meanMax = (double)(sumMax/numberMax);

		if(numberMin != 0) meanMin = (double)(sumMin/numberMin);

		sumMax = sumMin + sumMax;
		if(numberMax != 0) mean = (double)(sumMax/pict->histo->N);

		// we apply the formula
		meanMin = mean - meanMin;
		meanMax = mean - meanMax;

		pmin = (double)((double)numberMin/(double)pict->histo->N);
		pmax = (double)((double)numberMax/(double)pict->histo->N);

		variance = pmin*meanMin*meanMin+pmax*meanMax*meanMax;

		//we retrieve the threshold for the maximal value of entropy
		if(varianceMax < variance){
			varianceMax = variance;
			maxThreshold = threshold;
		}

		numberMax = 0;
		numberMin = 0;
		sumMax = 0;
		sumMin = 0;
	}

	return maxThreshold;
}

//Automatic thresholding by maximization of interclass variance
void automaticThresholdingInterclassVarianceMaximization(MatImage ** picture){
	MatImage * pict = *picture;

	//Threshold
	short int threshold = interclassVarianceMaximization(pict);
	//We do a manual thresholdhing on the picture using the threshold retrieved here
	manualThresholdNB(pict->h,pict->l,&(pict->grey),threshold);

	//we change the matrix and the picture
	changeImageNB(&(pict->image), pict->grey);

	*picture = pict;
}
