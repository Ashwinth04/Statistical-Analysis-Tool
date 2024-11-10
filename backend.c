#include <stdio.h>
#include <stdlib.h>

void run_linear_regression(const char *filename) {
    if (filename == NULL) {
        fprintf(stderr, "Error: No data file imported.\n");
        return;
    }

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

void export_to_file(char *filename)
{
    printf("Exported to %s\n",filename);
}

void set_split_size(char *split)
{
    printf("%s",split);
    float num = atof(split); //There is a small issue here
    printf("Split size is %f\n",num);
}

void reduce_dimensions(char *method_name)
{
    printf("Dimensionalty reduction. Method: %s\n",method_name);
}

void scale_data(char *path)
{
    printf("Scaling the data on %s\n",path);
}

void run_auto_model() {
    printf("Automatically selecting and training a model...\n");
    // Add model selection and training logic here
}

void set_target_variable(char* variable) {
    printf("Setting target variable: %s\n", variable);
    // Add logic to set the target variable here
}

void evaluate_model() {
    printf("Evaluating model performance...\n");
    // Add evaluation logic here
}
