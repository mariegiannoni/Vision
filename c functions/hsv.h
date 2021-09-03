//RGB intot HSV conversion
//Compute min
void computeMin(short int m1, short int m2, short int * min);
//Compute max
void computeMax(short int m1, short int m2, short int * max);
//Compute min of 3 elements
void computeMin3(short int m1, short int m2, short int m3, short int * min);
//Compute max of 3 elements
void computeMax3(short int m1, short int m2, short int m3, short int * max);

//Compute the hue of HSV
void computeH(short int ** red, short int ** green, short int ** blue, short int *** h, int length, int heigth);
//Compute the saturation of HSV
void computeS(short int ** red, short int ** green, short int ** blue, short int *** sat, int length, int heigth);
//Compute the value of HSV
void computeV(short int ** red, short int ** green, short int ** blue, short int *** val, int length, int heigth);

//Convert RGB in HSV
void fromRGBtoHSV(MatImage ** picture);
