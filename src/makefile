# export LD_LIBRARY_PATH=`pwd`

CC=clang
CFLAGS= -std=c99 -Wall -pedantic -fPIC
SWIG=swig

all: _phylib.so

_phylib.so: libphylib.so phylib_wrap.o
	$(CC) -shared phylib_wrap.o -L. -I/usr/include/python3.11 -lphylib -lpython3.11 -o _phylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o

phylib_wrap.c phylib.py: phylib.i
	$(SWIG) -python phylib.i

libphylib.so: phylib.o  
	$(CC) -shared -o libphylib.so phylib.o -lm

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11 -fPIC -o phylib_wrap.o

clean:
	rm -f *.o *.so