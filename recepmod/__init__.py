__version__ = '0.0.1'

try:
    import numpy
except ImportError as ie:
    print(ie, '\nNumPy does not seem to be installed.')
