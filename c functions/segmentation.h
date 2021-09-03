//Initialize matrix
void initializeZero(short int *** m, int l, int h);
void initialize255(short int *** m, int l, int h);
void initializeMinus1(short int *** m, int l, int h);
//dilatation
void dilatationPoints(short int *** new, short int ** image,  int ** points, int nbPt, short int etiq, int distance, int window, int l, int h);
void dilatationEtiq(short int *** new, short int ** image, short int etiq, int distance, int window, int lmin, int lmax, int hmin, int hmax, int l, int h);
//erosion
void erosionPoints(short int *** new, short int ** image, int ** points, int nbPt, short int etiq, int window, int l, int h);
void erosionEtiq(short int *** new, short int ** image, short int etiq, int window, int lmin, int lmax, int hmin, int hmax, int l, int h);
//Background colored
void colorBackground(short int *** new, short int ** image, int ** points, int nbPt, short int etiq, short int background, int lmin, int lmax, int hmin, int hmax, int l, int h);
//Region growing
int isCompatible(short int region, short int candidate, short int simThreshold);
void regionGrowingProcess(short int *** objectEtiq, short int *** object, short int ** image, short int color, short int etiq, short int threshold, int window, int lmin, int lmax, int hmin, int hmax, int l, int h);
void conditionalDilatation(short int *** new, short int ** image, int i, int j, short int etiq, short int color,int window, int l, int h, int threshold);
void regionGrowing(short int *** new, short int ** image, short int color, int lmin, int lmax, int hmin, int hmax, int l, int h, int threshold, int window, int mod, int *nbEtiq);
//Watershed
void watershed(short int *** new, short int ** grey, int l, int h, int window, int distance);
void watershedMI(MatImage ** picture, int window, int distance);

//Quad tree
//Fonction retournant un entier (0 si noir, 1 si blanc ou 2 si blanc et noir) définissant la valeur d'un carré
int calculCarreNB(int x1, int y1, int x2, int y2, short int ** gris);
//Fonction  qui crée un arbre binaire dont la racine est un noeud à partir d'une matrice
void creeArbreNB(noeudBinaire ** racine, int x0, int y0, int x1, int y1, int l, int h, int val, short int ** gris);
//Fonction qui étiquette les feuilles d'un arbre selon la valeur du noeud (-1 si 2 de 0 à i[256] sinon)
void etiquetteFeuilleNB(noeudBinaire ** racine, int *i);
//Si etiq est faux
//Fonction qui remplit la matrice de 255 ou de 0 selon la valeur du noeud (0 : 0, 1 : 255)
void colorieMatrice(noeudBinaire * racine, short int *** gris);
//Si etiq est vrai
//Fonction qui remplit la matrice avec les valeurs des étiquettes
void colorieMatriceEtiquette(noeudBinaire * racine, short int *** gris);
//Fonction qui crée une matrice à partir d'un arbre : elle appelle colorieMatrice ou colorieMatriceEtiquette selon la valeur d'etiq (si 0 : colorieMatrice, si 1 : colorieMatriceEtiquette)
void creeMatriceArbreNB(noeudBinaire *racine, short int *** gris, int etiq);
//Fonction qui libère un arbre
void libereArbreNB(noeudBinaire ** racine);
//Recomposition image binaire avec étiquette
//Racine représente la racine de l'arbre pour parcourir l'ensemble de l'arbre, trouve est le noeudBinaire voisin, x0,y0,x1,y1 sont les coordonées de la racine dont on cherche les voisins
void chercheVoisin(noeudBinaire ** racine1, int x0, int y0, int x1, int y1, int etiq, int val);
// Fusionne les régions qui partage la même couleur en leur attribuant la même étiquette
void fusionNB(noeudBinaire ** fusion, noeudBinaire ** racine);
