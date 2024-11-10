bison -d parser.y
flex scanner.l
gcc -o statpiler parser.tab.c lex.yy.c backend.c -lfl
