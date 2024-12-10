#include <stdio.h>
#include <stdlib.h>

#include <Python.h>

#include "pybiomes.c"
#include "objects/range.c"
#include "objects/generator.c"
#include "modules/versions.c"
#include "modules/dimensions.c"
#include "modules/biomes.c"

static PyMethodDef base_methods[] = {
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pybiomes = {
    PyModuleDef_HEAD_INIT,
    "core", /* library name */
    "core module", /* module docs */
    -1,
    base_methods,
};

PyMODINIT_FUNC PyInit_pybiomes(void){
    if (PyType_Ready(&GeneratorType) < 0) {
        return NULL;
    }

    if (PyType_Ready(&RangeType) < 0) {
        return NULL;
    }
    
    PyObject *base = PyModule_Create(&pybiomes);

    PyObject *versions = PyInit_versions(&pybiomes);
    PyObject *dimensions = PyInit_dimensions(&pybiomes);
    PyObject *biomes = PyInit_biomes(&pybiomes);

    PyObject *moduleDict = PyImport_GetModuleDict();

    Py_INCREF(versions);
    PyDict_SetItemString(moduleDict, "pybiomes.versions", versions);

    Py_INCREF(dimensions);
    PyDict_SetItemString(moduleDict, "pybiomes.dimensions", dimensions);

    Py_INCREF(biomes);
    PyDict_SetItemString(moduleDict, "pybiomes.biomes", biomes);
    PyModule_AddObject(base, "biomes", biomes);

    Py_INCREF(&GeneratorType);
    PyModule_AddObject(base, "Generator", (PyObject *)&GeneratorType);

    Py_INCREF(&RangeType);
    PyModule_AddObject(base, "Range", (PyObject *)&RangeType);

    return base; 
}