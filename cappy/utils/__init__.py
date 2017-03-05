import sys
import importlib


def import_mod(imp,silent_error=False):
    '''
    Lazily imports a module from a string
    @param imp:
    '''
    if not silent_error:
        return importlib.import_module(imp)
    try:
        return importlib.import_module(imp)
    except ImportError:
        return


def import_util(imp):
    '''
    Lazily imports a utils (class,
    function,or variable) from a module) from
    a string.
    @param imp:
    '''

    mod_name, obj_name = imp.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    return getattr(mod, obj_name)
