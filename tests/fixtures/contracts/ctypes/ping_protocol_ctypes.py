"""Generated ctypes sample for canonical fixture tests."""

import ctypes


class PingRequest(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint32),
        ("body", ctypes.c_char * 32),
    ]


class PingResponse(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_uint32),
        ("ok", ctypes.c_uint8),
    ]

