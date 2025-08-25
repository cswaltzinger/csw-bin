#!/usr/bin/make


CC = gcc #-I $(INC)

LIBS = -lm -lpthread
# -lpthread -lz -lpng -ljpeg -lSDL2 -lGL -lglfw

CFLAGS = -std=gnu99 -Wall -g  #-DDEBUG



CLEANERS =  *~ *.o *.dSYM


%.o: %.c 
	$(CC) -c $(CFLAGS) $< -o $@


clean: 
	/bin/rm -rf *.dSYM $(OBJ) $(EXECS)  $(CLEANERS)