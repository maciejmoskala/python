#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Skrypt do tworenia plików exe do dla allegro gui.

Sposób wywołania sryptu: `python setup.py build`
"""

from cx_Freeze import setup, Executable


executables = [
    Executable(
        'allegro_gui.py',
        base='Win32GUI',
    )
]

setup(
    name='allegro_gui',
    version='0.1',
    description='Allego GUI',
    executables=executables,
)
