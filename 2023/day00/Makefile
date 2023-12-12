CC=gcc
CFLAGS=-I.

solution: solution.o
	$(CC) -g -o solution solution.o $(CFLAGS)

solution.o: solution.c
	$(CC) -g -c solution.c $(CFLAGS)

clean:
	rm -f solution solution.o
