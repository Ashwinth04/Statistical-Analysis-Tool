bison -d parser.y
flex scanner.l
gcc -o dsl_compiler parser.tab.c lex.yy.c backend.c -lfl
