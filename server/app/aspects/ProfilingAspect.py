import os, sys, aspectlib, profilestats
 
def profile(fn):
    """
    Decrypts the result of the given function.
    """
    def wrapped(*args, **kws):
        # Weave (Patch) the function with a profiling code, and then call it.
        with aspectlib.weave(fn, profilestats.profile(print_stats=10, dump_stats=True)):
            yield aspectlib.Proceed
    return wrapped

# 'fn' will be run with a profiler:
#     function calls in ... seconds
# 
#    Ordered by: cumulative time
# 
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#       ...    0.000    0.000    0.000    0.000 ...
#       ...    0.000    0.000    0.000    0.000 ...
#       ...    0.000    0.000    0.000    0.000 ...
#       ...    0.000    0.000    0.000    0.000 ...
# 


"""
Validari.
Fortari de metode.

Punem intr-o coada toate metodele apelate. Un 'History'. De ex: Check login().call_count == 1, inainte de a executa send_money()
"""