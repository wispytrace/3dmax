# undo with exception

import pymxs
from pymxs import runtime as rt

def make_box_and_raise():
    with pymxs.undo(True, 'Making box'):
        rt.Box()
        # this will undo the box, and the error will not show up
        # in the listener, because it is handled:
        raise RuntimeError('This is an error')

def make_sphere_and_raise():
    rt.Sphere()
    # this will show up in the lister as an unhandled exception
    raise RuntimeError('This is an error')

make_box_and_raise()
make_spher  e_and_raise()

# pymxs.print_(msg[, isErr[, [forceOnMainThread]])

# msg - the string to print.
# isErr - an optional boolean that indicates whether the message should be formatted as an error (in red, by default). The default is False.
# forceOnMainThread - an optional boolean that indicates whether the print should happen on the main thread. In a threaded script, setting this to True ensures that output is sent to the Listener window even if called from a worker thread. If False, when called from a worker thread, output is sent to stdout/stderr (the 3dsmax_ouput.log file or console). The default is True.

# This function exists because both MAXScript print() and assert() functions are disabled and not callable from pymxs.runtime. There are a couple of ways to work around this limitation to send messages to the Listener window. The simplest is to use the standard Python print() function and assert statement. However, you cannot control formatting or threading behavior with these functions, so there may be situations where pymxs.print_() is the better solution.