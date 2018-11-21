from app.aspects.CryptoAspect import encrypt, decrypt
from app.decorators.LoggingAspect import before, after


@encrypt
def send_data(data:str):
    print('sending: {0}'.format(data))
    return data


@decrypt
def receive_data(data:bytes):
    print('received: {0}'.format(data))


sent_data = send_data(b'Hello')
receive_data(sent_data)