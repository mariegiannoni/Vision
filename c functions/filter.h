//Image in shades of grey
void shadesOfGrey(short int *** grey, short int ** red, short int ** green, short int ** blue, int l, int h);
//Negative image
void negativeImage(int h, int l, short int *** red, short int *** green, short int *** blue);
//Manual Threshold
void manualThreshold(int h, int l, short int ***red, short int ***green, short int ***blue, short int threshold);
//Manual Threshold NB
void manualThresholdNB(int h, int l, short int ***grey, short int threshold);
//exchange two elements
void exchange(short int * tab, int i, int j);
//sorting in ascendant way
void ascendingSort(short int * tab, short int dim);
//Compute median of a matrix nxnx
void computeMedian(short int ** g, short int * median, int i, int j, short int dim);
//Compute the median filter of size nxn
void medianFilterNxN(short int *** new, short int ** old, int l, int h, short int dim);
//compute median filter of size nxn for a MatImage
void medianFilterMINxN(MatImage ** picture, short int dim);
//compute the mean of a matrix nxn
void computeMean(short int ** grey, short int *mean, int i, int j, short int dim);
//average filter of size nxn
void averageFilterNxN(short int *** new, short int ** old, int l, int h, short int dim);
//average filter of size nxn for a MatImage
void averageFilterMINxN(MatImage ** picture, short int dim);
//compute the gaussian coefficient double dimension
double gaussian(int x, int y, double sigma);
//compute the gaussian approximation for a matrix nxn (weighted sum)
void computeGaussian(short int ** grey, short int *gauss, int i, int j, short int dim);
//gaussian filter of size nxn
void gaussianFilterNxN(short int *** new, short int ** grey, int l, int h, short int dim);
//gaussian filter of size nxn for a MatImage
void gaussianFilterMINxN(MatImage ** picture, short int dim);
//compute dilatation of a matrix of size nxn
void computeDilatation(short int ** grey, short int *dil, int i, int j, short int dim);
//dilatation filter of size nxn
void dilatationFilterNxN(short int *** new, short int ** grey, int l, int h, short int dim);
//dilatation filter of size nxn for a MatImage
void dilatationFilterMINxN(MatImage ** picture, short int dim);
//compute erosion of a matrix of size nxn
void computeErosion(short int ** grey, short int *ero, int i, int j, short int dim);
//erosion filter of size nxn
void erosionFilterNxN(short int *** new, short int ** grey, int l, int h, short int dim);
//erosion filter of size nxn for a MatImage
void erosionFilterMINxN(MatImage ** picture, short int dim);
//opening filter : erosion - dilatation
void openingFilterMINxN(MatImage ** picture, short int dim);
//closing filter : dilatation - erosion
void closingFilterMINxN(MatImage ** picture, short int dim);
//Roberts filter for MatImage
void robertsFilter(short int *** gradient, short int ** grey, int l, int h, int norm);
//Roberts filter
void robertsFilterMI(MatImage ** picture, int norm);
//Prewitt filter
void prewittFilter(short int *** gradient, short int *** direction, short int ** grey, int l, int h);
//Prewitt filter for MatImage
void prewittFilterMI(MatImage ** picture);
//Sobel filter
void sobelFilter(short int *** gradient, short int *** direction, short int ** grey, int l, int h);
//Sobel filter for MatImage
void sobelFilterMI(MatImage ** picture);
//Laplacian filter
void laplacianFilter(short int *** laplacian, short int ** grey, int l, int h, short int dim);
//Laplacian filter for MatImage
void laplacianFilterMI(MatImage ** picture, short int dim);

//Create a MatImage with shade of grey
void shadeOfGreyMI(MatImage ** picture);
//Gaussian filter 3x3 on MatImage
void gaussianFilter3x3MI(MatImage ** picture, short int dim);
//Gaussian filter 5x5 on MatImage
void gaussianFilter5x5MI(MatImage ** picture, short int dim);
//Create a MatImage with contrast stretching
void contrastStretching(MatImage ** mat);
//Median filter RGB
void computeMedianRGB(short int ** red, short int ** green, short int ** blue, int * row, int * column, int i, int j, short int dim);
void medianFilterRGB(short int *** red, short int *** green, short int *** blue, short int ** r, short int ** g, short int ** b, int l, int h, short int dim);
void medianFilterRGBMI(MatImage ** picture, short int dim);
//Entropy maximization
short int entropyMaximization(MatImage * pict);
//Automatic threshold by entropy maximization
void automaticThresholdingEntropyMaximization(MatImage ** picture);
//Interclass variance maximization
short int interclassVarianceMaximization(MatImage * pict);
//Automatic threshold with interclass variance maximization
void automaticThresholdingInterclassVarianceMaximization(MatImage ** picture);
