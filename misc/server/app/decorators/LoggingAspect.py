import logging
import aspectlib
from aspectlib import Aspect, Return, Proceed


@Aspect(bind=True)
def before(cut_point, *args, **kws):  
    """
    Display a message before calling a function
    """
    logging.warn('Before function %s.' % cut_point.__name__)
    yield
    
@Aspect(bind=True)
def after(cut_point, *args, **kws):
    """
    Display a message before calling a function
    """
    yield
    logging.warn('After function %s.' % cut_point.__name__)
