typedef char chaine[100];

//Data of Histogram
typedef struct Histogram {
	DonneesImageRGB * histogram; //picture of the histogram
	int ** ni; //pixel number of grey level
	int N; //total number pixel
	int nimax; //maximal value of grey level
	int nimin; //minimal value of grey level
	chaine nameBMP; //name of the .bmp
}Histogram;

//Data structure with all the information about a picture
typedef struct MatImage {
	DonneesImageRGB * image;
	short int ** red, **blue, **green, **grey;
	int l, h;
	double entropy; //entropy of the picture
	Histogram * histo; //histogram of the picture
	Histogram * chisto; //cumulative histogram
	chaine nameBMP; //name of the .bmp
}MatImage;

//Shape
typedef struct Shape {
	//Data
	short int etiq;
	double meanColor;
	double standardDeviation;
	//Points of the shape
	int nbPt; //also the area
	int ** points;
	//Points of the edges
	int nbPtE; //also the full perimeter
	int ** edges;
	int perimeter; //the perimeter without the pixel that has only one neighbour which is not from the shape
	int perimeterCrofton;
	//Bounding Box
	int ** bb;
	int vertical;
	int horizontal;
	double elongation;
	//maximal and minimal Féret diameter and convex hull
	int nbPtH;
	int ** hull;
	double maxFeretDiameter;
	double minFeretDiameter;
	//Circularity
	double geometrical;
	double radial;
	//Symmetry - Blaschke
	double minkowski;
	double blaschke;
	//Connectivity
	int connect;
	int nbConnectedComponent;
	int nbHoles;
}Shape;

// Quad tree
typedef struct noeudBinaire{
	int val; //0 si noir, 1 si blanc, 2 si ni noir ni blanc
	struct noeudBinaire *n1, *n2, *n3, *n4;
	//Largeur et hauteur de l'image
	int l,h;
	//Coordonées des coins
	int x0,y0,x1,y1;
	//Numéro d'étiquette : de 0 à i[256] si val = 0 ou 1 ou -1 si val = 2
	int etiquette;
}noeudBinaire;
