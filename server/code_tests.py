from app.aspects.CryptoAspect import encrypt, decrypt
from app.decorators.LoggingAspect import before, after

@before
@after
@encrypt
def send_data(data:str):
    print('sending: %s' % data)
    return data

@before
@after
def receive_data(data:str):
    print('received: %s' % data)
    return data

receive_data(send_data(b'Hello'))