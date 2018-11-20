import logging

def before(fn):
    """
    Display a message before calling a function
    """
    def wrapped(*args, **kws):
        logging.warn('Before function %s.' % fn.func_name)
        return fn(*args, **kws)
    return wrapped

def after(fn):
    """
    Display a message after calling a function
    """
    def wrapped(*args, **kws):
        retVal = fn(*args, **kws)
        logging.warn('After function %s.' % fn.func_name)
        return retVal
    return wrapped