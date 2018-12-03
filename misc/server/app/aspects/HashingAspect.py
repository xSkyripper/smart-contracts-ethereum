import hashlib
import aspectlib

hash_object = hashlib.sha256(b'Hello World')
hex_dig = hash_object.hexdigest()

def hash256(fn):
    """
    Hashes the result of the given function, using sha256.
    """
    def wrapped(*args, **kws):
        result = yield aspectlib.Proceed        # Get function result.
        hash_object = hashlib.sha256(result)    # Hash result.
        hex_dig = hash_object.hexdigest()       # Get hex digest.
        return aspectlib.Return(hex_dig)        # Return hex digest.
    return wrapped