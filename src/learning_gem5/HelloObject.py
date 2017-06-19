from m5.params import *
from m5.SimObject import SimObject

class HelloObject(SimObject):
    #Type is C++ class that I am wrapping with this python simobject
    type = 'HelloObject'
    #cxx_header has declr of class used as the type parameter.
    cxx_header = "learning_gem5/hello_object.hh"

