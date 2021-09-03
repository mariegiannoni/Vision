/* Histogram */

//ni
//Creation
void initializeNi(int *** ni);
//Liberation
void freeNi(int *** ni);

//NormalHistogram
//Creation
void createHistogram(Histogram ** histo);
//Compute Histogram of a picture
void computeHistogram(Histogram ** histo, MatImage * mi, int c);
//Create picture representing Hisotgram
void drawHistogram(DonneesImageRGB ** image, Histogram * histo);
//Liberation
void freeHistogram(Histogram ** histo);

//setting of the histograms in MatImage
void setHistogramsInMI(MatImage ** matImage);

//Entropy
void computeEntropy(double * entropy, Histogram * h);

//Print
//Histogram
void printHistogram(Histogram * histo);
//Entropy
void printEntropy(MatImage * mi);
