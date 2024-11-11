%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex(void);
extern void yyerror(const char *s);

void run_linear_regression();
void run_knn();
void run_svm(double gamma, double C);
void preprocess(char *path,char* target);
void export_to_file();
void set_split_size();
void reduce_dimensions(char* path,char* method,char *dimensions);
void run_auto_model();
void set_target_variable(char* variable);
void initialize_python();
void print_outliers();
void vis_boxplot();

char* filename;
double svm_gamma = 0.0; 
double svm_C = 1.0;
char *target;
%}

%union {
    int num;
    char *str;
    double val;
}

%token <num> NUMBER
%token <str> STRING_LITERAL
%token IMPORT PREPROCESS VISUALIZE MODEL EXPORT SPLIT SUMMARIZE SETFILE
%token KERNEL AUTO_MODEL X Y C GAMMA TRAIN_SIZE METHOD TARGET SAVE_MODEL DET_OUTLIERS
%token DIM
%type <str> program statement preprocessing method_clause visualize model

%%

program:
    /* Empty */
    | program statement
    ;

statement:
      IMPORT STRING_LITERAL          { filename = strdup($2); initialize_python(); printf("Importing data file: %s\n", $2); free($2); }
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
    | TARGET STRING_LITERAL          { target = strdup($2); printf("Target variable set: %s\n", target); free($2); }
    | SUMMARIZE                      { printf("Generating summary report.\n"); }
    | EXPORT STRING_LITERAL          { export_to_file($2); }
    | SPLIT STRING_LITERAL           { set_split_size($2); }
    | DET_OUTLIERS                   { printf("Evaluating model performance.\n"); print_outliers(filename,target); }
    | SETFILE STRING_LITERAL         { filename = strdup($2); }
    ;

preprocessing:
      STRING_LITERAL                 { 
                                      if (strcmp($1, "\"General\"") == 0) {
                                          $$ = strdup("General");
                                          preprocess(filename,target);
                                      } else {
                                          yyerror("Invalid preprocessing type. Expected \"General\" or \"Dimensionality Reduction\"");
                                          YYERROR;
                                      }
                                      free($1);
                                    }
    | STRING_LITERAL METHOD STRING_LITERAL DIM STRING_LITERAL  { 
                                      if (strcmp($1, "\"Dimensionality Reduction\"") == 0) {
                                          if (strcmp($3, "\"PCA\"") == 0 ||
                                              strcmp($3, "\"LDA\"") == 0 ||
                                              strcmp($3, "\"TSNE\"") == 0) {
                                              char buffer[100];
                                              snprintf(buffer, sizeof(buffer), "Dimensionality Reduction with %s", $3);
                                              reduce_dimensions(filename,$3,$5);
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
                                          vis_boxplot(filename,target);
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
                                          printf("%s\n",target);
                                          run_linear_regression(filename,target);
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
