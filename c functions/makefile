all : image clean

image : measure.o hsv.o segmentation.o histo.o filter.o basic.o main.o BMPLib.o OutilsLib.o ESLib.o ErreurLib.o
	gcc -o image measure.o hsv.o segmentation.o histo.o filter.o basic.o main.o BMPLib.o OutilsLib.o ESLib.o ErreurLib.o -lm -O2

OutilsLib.o : OutilsLib.c OutilsLib.h
	gcc -c -Wall OutilsLib.c

BMPLib.o : BMPLib.c BMPLib.h OutilsLib.h
	gcc -c -Wall BMPLib.c

ErreurLib.o : ErreurLib.c ErreurLib.h
	gcc -c -Wall ErreurLib.c

ESLib.o : ESLib.c ErreurLib.h ESLib.h
	gcc -c -Wall ESLib.c

main.o : main.c segmentation.h basic.h histo.h filter.h ErreurLib.h ESLib.h structure.h hsv.h measure.h
	gcc -c -g -v -Wall main.c

histo.o : histo.c segmentation.h basic.h histo.h filter.h ErreurLib.h ESLib.h structure.h hsv.h measure.h
	gcc -c -g -v -Wall histo.c

filter.o : filter.c segmentation.h basic.h filter.h histo.h ErreurLib.h ESLib.h structure.h hsv.h measure.h
	gcc -c -g -v -Wall filter.c

basic.o : basic.c segmentation.h basic.h filter.h histo.h ErreurLib.h ESLib.h structure.h hsv.h measure.h
	gcc -c -g -v -Wall basic.c

segmentation.o : segmentation.c segmentation.h basic.h filter.h histo.h ErreurLib.h ESLib.h structure.h hsv.h measure.h
	gcc -c -g -v -Wall segmentation.c

hsv.o : hsv.c segmentation.h basic.h filter.h histo.h ErreurLib.h ESLib.h structure.h hsv.h measure.h
	gcc -c -g -v -Wall hsv.c

measure.o : measure.c segmentation.h basic.h filter.h histo.h ErreurLib.h ESLib.h structure.h hsv.h measure.h
	gcc -c -g -v -Wall measure.c
	
clean :
	rm *.o
