//Creation and liberatio
// 1 matrix
void create1matrix(short int *** m, int l, int h);
void free1matrix(short int *** m, int h);
// 3 matrices
void create3matrices(DonneesImageRGB* picture, short int *** red, short int *** green, short int *** blue);
void free3matrices(short int *** red, short int *** green, short int *** blue, int h);

//Save Image
//Color
void saveImage(DonneesImageRGB ** image, short int ** red, short int ** green, short int ** blue, int l, int h);
//from MatImage
void saveImageMI(DonneesImageRGB ** image, MatImage * mi);
//NB
void saveImageNB(DonneesImageRGB ** image, short int ** grey, int l, int h);
//NB from MatImage
void saveImageMINB(DonneesImageRGB ** image, MatImage * mi);

//Change Image
//Color
void changeImageRGB(DonneesImageRGB ** image, short int ** red, short int **green, short int ** blue);
//NB
void changeImageNB(DonneesImageRGB ** image, short int ** grey);

//Duplicate
//image
void duplicateImage(short int ** r1, short int ** g1, short int ** b1, short int ** r2, short int ** g2, short int ** b2, int l, int h);
//matrix
void duplicateMatrice(short int ** m1, short int ** m2, int l, int h);

//Shades of grey
void shadesOfGrey(short int *** grey, short int ** red, short int ** green, short int ** blue, int l, int h);

/* MatImage */
//creation
void createMatImage(MatImage ** matImage, short int ** red, short int ** green, short int ** blue, int l, int h, chaine nameBMP);
//creation from Image
void createMatImageFromImage(MatImage ** matImage, DonneesImageRGB * image, chaine nameBMP);

//setting
//Color
void modifyMatricesColorMatImage(MatImage ** Image, short int ** red, short int ** green, short int ** blue);
//NB
void modifyMatricesNBMatImage(MatImage ** Image, short int ** grey);

//liberation
void freeMatImage(MatImage ** matImage);

