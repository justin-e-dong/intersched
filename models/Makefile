CC=gcc
CFLAGS=-O3 -march=native -msse2 -mavx2 -ffast-math -ftree-vectorize -fno-math-errno \
	   -fassociative-math -freciprocal-math -Wall
regression: regression.o
	$(CC) $(CFLAGS) -o regression regression.o

regression.o: regression.c
	$(CC) $(CFLAGS) -c regression.c

clean:
	rm -f regression *.o