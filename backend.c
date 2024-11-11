#include <stdio.h>
#include <stdlib.h>
#include <Python.h>

void initialize_python() {
    Py_Initialize();
    PyRun_SimpleString("import sys; sys.path.append('.')");  // Add current directory to sys.path
}

void finalize_python() {
    Py_Finalize();
}

void run_linear_regression(const char *filename, char *target) {
    printf("Running Linear Regression with %s\n", filename);
    PyObject *pName = PyUnicode_DecodeFSDefault("preprocess");
    PyObject *pModule = PyImport_Import(pName);
    
    if (pModule != NULL) {
        PyObject *pFunc = PyObject_GetAttrString(pModule, "linear_regression");
        
        if (PyCallable_Check(pFunc)) {
            PyObject *pArgs = PyTuple_Pack(2, PyUnicode_FromString(filename), PyUnicode_FromString(target));
            PyObject *pValue = PyObject_CallObject(pFunc, pArgs);
            
            if (pValue != NULL) {
                printf("Linear Regression completed successfully.\n");
                Py_DECREF(pValue);
            } else {
                PyErr_Print();
            }
            Py_XDECREF(pArgs);
            Py_XDECREF(pFunc);
        } else {
            PyErr_Print();
        }
        Py_XDECREF(pModule);
    } else {
        PyErr_Print();
    }
}

void reduce_dimensions(char *filename, char *method_name, char *dimensions) {
    printf("Reducing dimensions for %s using %s\n", filename, method_name);
    PyObject *pName = PyUnicode_DecodeFSDefault("preprocess");
    PyObject *pModule = PyImport_Import(pName);
    
    if (pModule != NULL) {
        PyObject *pFunc = PyObject_GetAttrString(pModule, "reduce_dimensions");
        
        if (PyCallable_Check(pFunc)) {
            PyObject *pArgs = PyTuple_Pack(3, PyUnicode_FromString(filename),
                                           PyUnicode_FromString(method_name),
                                           PyUnicode_FromString(dimensions));
            PyObject *pValue = PyObject_CallObject(pFunc, pArgs);
            
            if (pValue != NULL) {
                printf("Dimensionality reduction completed successfully.\n");
                Py_DECREF(pValue);
            } else {
                PyErr_Print();
            }
            Py_XDECREF(pArgs);
            Py_XDECREF(pFunc);
        } else {
            PyErr_Print();
        }
        Py_XDECREF(pModule);
    } else {
        PyErr_Print();
    }
}

void preprocess(char *filename,char* target)
{
    printf("Processing data...\n");
    PyObject *pName = PyUnicode_DecodeFSDefault("preprocess");
    PyObject *pModule = PyImport_Import(pName);
    
    if (pModule != NULL) {
        PyObject *pFunc = PyObject_GetAttrString(pModule, "preprocess_data");
        
        if (PyCallable_Check(pFunc)) {
            PyObject *pArgs = PyTuple_Pack(2, PyUnicode_FromString(filename),
                                           PyUnicode_FromString(target));
            PyObject *pValue = PyObject_CallObject(pFunc, pArgs);
            
            if (pValue != NULL) {
                printf("Processing done successfully !!\n");
                Py_DECREF(pValue);
            } else {
                PyErr_Print();
            }
            Py_XDECREF(pArgs);
            Py_XDECREF(pFunc);
        } else {
            PyErr_Print();
        }
        Py_XDECREF(pModule);
    } else {
        PyErr_Print();
    }
}

void print_outliers(char* filename,char *target)
{
    printf("Detecting outliers...\n");
    PyObject *pName = PyUnicode_DecodeFSDefault("preprocess");
    PyObject *pModule = PyImport_Import(pName);
    
    if (pModule != NULL) {
        PyObject *pFunc = PyObject_GetAttrString(pModule, "detect_outliers");
        
        if (PyCallable_Check(pFunc)) {
            PyObject *pArgs = PyTuple_Pack(2, PyUnicode_FromString(filename),
                                           PyUnicode_FromString(target));
            PyObject *pValue = PyObject_CallObject(pFunc, pArgs);
            
            if (pValue != NULL) {
                Py_DECREF(pValue);
            } else {
                PyErr_Print();
            }
            Py_XDECREF(pArgs);
            Py_XDECREF(pFunc);
        } else {
            PyErr_Print();
        }
        Py_XDECREF(pModule);
    } else {
        PyErr_Print();
    }
}

void vis_boxplot(char *filename, char* target)
{
    PyObject *pName = PyUnicode_DecodeFSDefault("preprocess");
    PyObject *pModule = PyImport_Import(pName);
    
    if (pModule != NULL) {
        PyObject *pFunc = PyObject_GetAttrString(pModule, "boxplot");
        
        if (PyCallable_Check(pFunc)) {
            PyObject *pArgs = PyTuple_Pack(2, PyUnicode_FromString(filename),
                                           PyUnicode_FromString(target));
            PyObject *pValue = PyObject_CallObject(pFunc, pArgs);
            
            if (pValue != NULL) {
                Py_DECREF(pValue);
            } else {
                PyErr_Print();
            }
            Py_XDECREF(pArgs);
            Py_XDECREF(pFunc);
        } else {
            PyErr_Print();
        }
        Py_XDECREF(pModule);
    } else {
        PyErr_Print();
    }
}

void run_knn() {
    printf("Running K-Nearest Neighbors...\n");
}

void run_svm() {
    printf("Running Support Vector Machines...\n");
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


void run_auto_model() {
    printf("Automatically selecting and training a model...\n");
    // Add model selection and training logic here
}

void set_target_variable(char* variable) {
    printf("Setting target variable: %s\n", variable);
    // Add logic to set the target variable here
}
