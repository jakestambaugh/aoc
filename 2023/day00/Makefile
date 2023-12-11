CC=gcc
CFLAGS=-I.

solution: solution.o
	$(CC) -o solution solution.o $(CFLAGS)

solution.o: solution.c
	$(CC) -c solution.c $(CFLAGS)

clean:
	rm -f solution solution.o