bison -d -o parser.c parser.y
flex -o scanner.c scanner.l
gcc -o statpiler backend.c scanner.c parser.c -lfl -I/usr/include/python3.10 -lpython3.10
