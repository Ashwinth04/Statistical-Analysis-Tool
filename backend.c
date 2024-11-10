#include <stdio.h>
#include <stdlib.h>
#include <Python.h>

void run_linear_regression(const char *filename,char *target) {
    Py_Initialize();
    printf("%s",filename);
    // Add current directory to the sys.path to enable importing from the current directory
    PyRun_SimpleString("import sys; sys.path.append('.')");

    // Import the Python script (ensure that preprocess.py is in the same directory)
    PyObject *pName = PyUnicode_DecodeFSDefault("preprocess");  // Name of the Python file (without .py)
    PyObject *pModule = PyImport_Import(pName);
    
    if (pModule != NULL) {
        // Get the preprocess_data function from the module
        PyObject *pFunc = PyObject_GetAttrString(pModule, "linear_regression");
        
        if (PyCallable_Check(pFunc)) {
            // Create Python arguments
            PyObject *pArgs = PyTuple_Pack(2, 
                PyUnicode_FromString(filename), 
                PyUnicode_FromString(target)
            );
            
            // Call the function
            PyObject *pValue = PyObject_CallObject(pFunc, pArgs);
            
            if (pValue != NULL) {
                printf("Data processed successfully.\n");
                Py_DECREF(pValue);
            } else {
                PyErr_Print();
            }
            
            // Clean up
            Py_XDECREF(pArgs);
            Py_XDECREF(pFunc);
        } else {
            PyErr_Print();
        }
        
        // Clean up
        Py_XDECREF(pModule);
    } else {
        PyErr_Print();
    }
    
    // Finalize the Python interpreter
    Py_Finalize();
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
