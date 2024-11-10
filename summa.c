#include <Python.h>
#include <stdio.h>
#include <stdlib.h>

void preprocess_data(const char *filename, const char *target) {
    // Initialize the Python interpreter
    Py_Initialize();
    
    // Add current directory to the sys.path to enable importing from the current directory
    PyRun_SimpleString("import sys; sys.path.append('.')");

    // Import the Python script (ensure that preprocess.py is in the same directory)
    PyObject *pName = PyUnicode_DecodeFSDefault("preprocess");  // Name of the Python file (without .py)
    PyObject *pModule = PyImport_Import(pName);
    
    if (pModule != NULL) {
        // Get the preprocess_data function from the module
        PyObject *pFunc = PyObject_GetAttrString(pModule, "preprocess_data");
        
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

void run_linear_regression(const char *filename, const char *target) {
   Py_Initialize();
    
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

int main(void) {
    const char *filename = "data.csv";  // Example data file
    const char *target = "variety";  // Example target column
    
    // preprocess_data(filename,target);
    run_linear_regression("processed_data.csv", target);
    
    return 0;
}
