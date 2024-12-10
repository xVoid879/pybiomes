#include <Python.h>

PyMODINIT_FUNC PyInit_dimensions(PyModuleDef *pybiomes) {
    PyObject *mod = PyModule_Create(pybiomes);
    
    PyModule_AddIntMacro(mod, DIM_OVERWORLD);
    PyModule_AddIntMacro(mod, DIM_NETHER);
    PyModule_AddIntMacro(mod, DIM_END);
    
    return mod;
}
