%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex(void);
extern void yyerror(const char *s);

void run_linear_regression();
void run_knn();
void run_svm();
void preprocess();

char* filename;

%}

%union {
    int num;
    char *str;  // Add char* for string-related non-terminals
}

%token <num> NUMBER
%token <str> STRING_LITERAL
%token IMPORT
%token PREPROCESS
%token VISUALIZE
%token MODEL
%type <str> model preprocessing visualize

%%

program:
    /* Empty */
    | program statement
    ;

statement:
      IMPORT STRING_LITERAL          { filename = strdup($2); printf("Importing data file: %s\n", $2); free($2); }
    | PREPROCESS STRING_LITERAL      { preprocess($2); printf("Preprocessing data: %s\n", $2); free($2); }
    | VISUALIZE STRING_LITERAL       { printf("Visualizing outliers: %s\n", $2); free($2); }
    | MODEL STRING_LITERAL           { printf("Model: %s\n", $2); run_linear_regression(filename); free($2); }
    ;

preprocessing:
      "Scaling"                      { $$ = strdup("Scaling"); }
    | "Dimensionality Reduction"     { $$ = strdup("Dimensionality Reduction"); }
    ;

visualize:
      "Box Plot"                     { $$ = strdup("Box Plot"); }
    | "Scatter Plot"                 { $$ = strdup("Scatter Plot"); }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    yyparse();
    return 0;
}
