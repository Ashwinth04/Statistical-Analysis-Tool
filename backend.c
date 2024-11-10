#include <stdio.h>

void run_linear_regression(const char *filename) {
    if (filename == NULL) {
        fprintf(stderr, "Error: No data file imported.\n");
        return;
    }
    // Process the file, e.g., read data, perform calculations, etc.
    printf("Running Linear Regression on %s\n", filename);
}
void run_knn() {
    printf("Running K-Nearest Neighbors...\n");
}

void run_svm() {
    printf("Running Support Vector Machines...\n");
}

void preprocess(char *type)
{
    printf("Preprocessing type: %s\n",type);
}