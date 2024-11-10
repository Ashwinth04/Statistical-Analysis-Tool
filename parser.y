%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex(void);
extern void yyerror(const char *s);

void run_linear_regression();
void run_knn();
void run_svm(double gamma, double C);
void preprocess();
void export_to_file();
void set_split_size();
void reduce_dimensions(char* method);
void scale_data(char* path);
void run_auto_model();
void evaluate_model();
void set_target_variable(char* variable);

char* filename;
double svm_gamma = 0.0; 
double svm_C = 1.0;
%}

%union {
    int num;
    char *str;
    double val;
}

%token <num> NUMBER
%token <str> STRING_LITERAL
%token IMPORT PREPROCESS VISUALIZE MODEL EXPORT SPLIT SUMMARIZE
%token KERNEL AUTO_MODEL X Y C GAMMA TRAIN_SIZE METHOD TARGET SAVE_MODEL EVAL
%type <str> program statement preprocessing method_clause visualize model

%%

program:
    /* Empty */
    | program statement
    ;

statement:
      IMPORT STRING_LITERAL          { filename = strdup($2); printf("Importing data file: %s\n", $2); free($2); }
    | PREPROCESS preprocessing       { printf("Preprocess called with: %s\n", $2); free($2); }
    | VISUALIZE visualize            { printf("Visualization type: %s\n", $2); free($2); }
    | MODEL model                    { printf("Model specified: %s\n", $2); free($2); }
    | MODEL AUTO_MODEL               { printf("Auto model selection enabled.\n"); run_auto_model(); }
    | MODEL STRING_LITERAL GAMMA '=' NUMBER C '=' NUMBER {
                                      if (strcmp($2, "\"SVM\"") == 0) {
                                          svm_gamma = $5;
                                          svm_C = $8;
                                          printf("SVM with gamma=%f, C=%f\n", svm_gamma, svm_C);
                                          run_svm(svm_gamma, svm_C);
                                      } else {
                                          yyerror("Only SVM supports gamma and C parameters");
                                          YYERROR;
                                      }
                                      free($2);
                                    }
    | TARGET STRING_LITERAL          { set_target_variable($2); printf("Target variable set: %s\n", $2); free($2); }
    | SUMMARIZE                      { printf("Generating summary report.\n"); }
    | EXPORT STRING_LITERAL          { export_to_file($2); }
    | SPLIT STRING_LITERAL           { set_split_size($2); }
    | EVAL                           { printf("Evaluating model performance.\n"); evaluate_model(); }
    ;

preprocessing:
      STRING_LITERAL                 { 
                                      if (strcmp($1, "\"Scaling\"") == 0) {
                                          $$ = strdup("Scaling");
                                          scale_data(filename);
                                      } else {
                                          yyerror("Invalid preprocessing type. Expected \"Scaling\" or \"Dimensionality Reduction\"");
                                          YYERROR;
                                      }
                                      free($1);
                                    }
    | STRING_LITERAL METHOD STRING_LITERAL  { 
                                      if (strcmp($1, "\"Dimensionality Reduction\"") == 0) {
                                          if (strcmp($3, "\"PCA\"") == 0 ||
                                              strcmp($3, "\"LDA\"") == 0 ||
                                              strcmp($3, "\"TSNE\"") == 0) {
                                              char buffer[100];
                                              snprintf(buffer, sizeof(buffer), "Dimensionality Reduction with %s", $3);
                                              reduce_dimensions($3);
                                              $$ = strdup(buffer);
                                          } else {
                                              yyerror("Invalid method. Expected PCA, LDA, or TSNE");
                                              YYERROR;
                                          }
                                      } else {
                                          yyerror("Only Dimensionality Reduction accepts method parameter");
                                          YYERROR;
                                      }
                                      free($1);
                                      free($3);
                                    }
    ;

visualize:
      STRING_LITERAL                 {
                                      if (strcmp($1, "\"Box Plot\"") == 0 || strcmp($1, "\"Scatter Plot\"") == 0) {
                                          $$ = strdup($1);
                                      } else {
                                          yyerror("Invalid visualization type. Expected \"Box Plot\" or \"Scatter Plot\"");
                                          YYERROR;
                                      }
                                      free($1);
                                    }
    | X '=' STRING_LITERAL Y '=' STRING_LITERAL {
                                      printf("Plotting with x-axis: %s, y-axis: %s\n", $3, $6);
                                      free($3);
                                      free($6);
                                    }
    ;

model:
      STRING_LITERAL                 { 
                                      if (strcmp($1, "\"Linear Regression\"") == 0) {
                                          $$ = strdup("Linear Regression");
                                          run_linear_regression();
                                      } else if (strcmp($1, "\"KNN\"") == 0) {
                                          $$ = strdup("KNN");
                                          run_knn();
                                      } else if (strcmp($1, "\"SVM\"") == 0) {
                                          $$ = strdup("SVM");
                                          run_svm(svm_gamma, svm_C);
                                      } else {
                                          yyerror("Invalid model type. Expected \"Linear Regression\", \"KNN\", or \"SVM\"");
                                          YYERROR;
                                      }
                                      free($1);
                                    }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    yyparse();
    return 0;
}
