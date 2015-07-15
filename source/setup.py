from distutils.core import setup
import numpy
import py2exe

setup(
    console=['gui.py'],
)
# setup(
#     console=['gui.py'],
#     zipfile=None,
#     options = {'py2exe':{'bundle_files': 1, 'compressed': True}},
# )
