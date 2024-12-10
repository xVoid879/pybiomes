#include <stdio.h>
#include <stdbool.h>

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include "../external/cubiomes/biomenoise.h"

typedef struct {
    PyObject_HEAD
    Range range;
} RangeObject;

static int Range_traverse(RangeObject *self, visitproc visit, void *arg) {
    return 0;
}

static int Range_clear(RangeObject *self) {
    return 0;
}

static void Range_dealloc(RangeObject *self) {
    PyObject_GC_UnTrack(self);
    Range_clear(self);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *Range_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    RangeObject *self;
    self = (RangeObject *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->range = (Range){0};
    }
    return (PyObject *) self;
}

static int Range_init(RangeObject *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = {"scale", "x", "y", "z", "sx", "sy", "sz", NULL};

    int scale, x, y, z, sx, sy, sz;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "iiiiiii", kwlist, &scale, &x, &y, &z, &sx, &sy, &sz)) {
        return -1;
    }

    self->range.scale = scale;
    self->range.x = x;
    self->range.y = y;
    self->range.z = z;
    self->range.sx = sx;
    self->range.sy = sy;
    self->range.sz = sz;

    return 0;
}

static PyObject *get_scale(RangeObject *self)  {
    return PyLong_FromLong(self->range.scale);
}

static PyObject *get_x(RangeObject *self)  {
    return PyLong_FromLong(self->range.x);
}

static PyObject *get_y(RangeObject *self)  {
    return PyLong_FromLong(self->range.y);
}

static PyObject *get_z(RangeObject *self)  {
    return PyLong_FromLong(self->range.z);
}

static PyObject *get_sx(RangeObject *self)  {
    return PyLong_FromLong(self->range.sx);
}

static PyObject *get_sy(RangeObject *self)  {
    return PyLong_FromLong(self->range.sy);
}

static PyObject *get_sz(RangeObject *self)  {
    return PyLong_FromLong(self->range.sz);
}

static int set_scale(RangeObject *self, PyObject *args)  {
    if (PyLong_Check(args)) {
        self->range.scale = PyLong_AsLong(args);
        return 0;
    }
    return -1;
}

static int set_x(RangeObject *self, PyObject *args)  {
    if (PyLong_Check(args)) {
        self->range.x = PyLong_AsLong(args);
        return 0;
    }
    return -1;
}

static int set_y(RangeObject *self, PyObject *args)  {
    if (PyLong_Check(args)) {
        self->range.y = PyLong_AsLong(args);
        return 0;
    }
    return -1;
}

static int set_z(RangeObject *self, PyObject *args)  {
    if (PyLong_Check(args)) {
        self->range.z = PyLong_AsLong(args);
        return 0;
    }
    return -1;
}

static int set_sx(RangeObject *self, PyObject *args)  {
    if (PyLong_Check(args)) {
        self->range.sx = PyLong_AsLong(args);
        return 0;
    }
    return -1;
}

static int set_sy(RangeObject *self, PyObject *args)  {
    if (PyLong_Check(args)) {
        self->range.sy = PyLong_AsLong(args);
        return 0;
    }
    return -1;
}

static int set_sz(RangeObject *self, PyObject *args)  {
    if (PyLong_Check(args)) {
        self->range.sz = PyLong_AsLong(args);
        return 0;
    }
    return -1;
}

static PyMemberDef Range_members[] = {
    {NULL}  /* Sentinel */
};

static PyMethodDef Range_methods[] = {
    {NULL}  /* Sentinel */
};

static PyGetSetDef Range_getsets[] = {
    {"x", (getter)get_x, (setter)set_x, NULL, NULL},
    {"y", (getter)get_y, (setter)set_y, NULL, NULL},
    {"z", (getter)get_z, (setter)set_z, NULL, NULL},
    {"sx", (getter)get_sx, (setter)set_sx, NULL, NULL},
    {"sy", (getter)get_sy, (setter)set_sy, NULL, NULL},
    {"sz", (getter)get_sz, (setter)set_sz, NULL, NULL},
    {"scale", (getter)get_scale, (setter)set_scale, NULL, NULL},
    {NULL, 0, NULL, NULL, NULL} /* Sentinel */
};

static PyTypeObject RangeType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "pybiomes.Range",
    .tp_doc = "Range objects",
    .tp_basicsize = sizeof(RangeObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_new = Range_new,
    .tp_init = (initproc) Range_init,
    .tp_dealloc = (destructor) Range_dealloc,
    .tp_traverse = (traverseproc) Range_traverse,
    .tp_clear = (inquiry) Range_clear,
    .tp_members = Range_members,
    .tp_methods = Range_methods,
    .tp_getset = Range_getsets,
};
