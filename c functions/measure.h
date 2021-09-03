void create1matrixInt(int *** m, int l, int h);
void free1matrixInt(int *** m, int h);
void freeShape(Shape ** shape);
void exchangeInt2(int ** tab, int i, int j);
void ascendingSortInt2(int** tab, int dim);
void shapePoint(Shape ** shape, short int ** image, short int ** originalImage, short int etiq, int l, int h);
void vector(int * y, int * x, int x1, int y1, int x2, int y2);
double norm(int x, int y);
double scalarProduct(int x1, int y1, int x2, int y2);
double angle(int x1, int y1, int x2, int y2, int rad);
double distance(int x1, int y1, int x2, int y2);
int orientation(int x1, int y1, int x2, int y2, int x3, int y3);
void exchangeInt(int** tab, int i, int j);
void ascendingSortInt(int ** tab, int dim1);
void convexHullGraham(Shape ** shape, int ** points, int nbPt, int l );
void printPoints(int ** points, int nbPt, short int ** red, short int ** green, short int ** blue, int l, int h, short int r, short int g, short int b);
void geometricalCircularity(Shape ** shape);
void symmetryMeasure(Shape ** shape, short int ** image, int l, int h);
void connectivity(Shape ** shape, short int ** image, int l, int h, int threshold, int window);