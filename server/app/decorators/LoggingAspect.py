import logging

def before(fn):
    def wrapped(*args, **kws):
        logging.warn('Before function %s.' % fn.func_name)
        return fn(*args, **kws)
    return wrapped

def after(fn):
    def wrapped(*args, **kws):
        retVal = fn(*args, **kws)
        logging.warn('After function %s.' % fn.func_name)
        return retVal
    return wrapped