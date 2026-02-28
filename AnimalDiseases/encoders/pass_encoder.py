from random import choice
from string import ascii_letters, digits, punctuation


def encoder(p: str) -> str:
    """ Password encoder function aka hash-function but with unreverse ability. """
    enc = []
    for c in p:
        c = hex(ord(c))[2:]
        salt = ''.join([choice(ascii_letters + digits + punctuation) for _ in range(6)])
        enc.append(c[0] + salt + c[1])
    enc = enc[::-1]
    return ''.join(enc)


def decoder(p: str) -> str:
    """ This function decode encoded password. """
    elems = []
    for e in range(0, len(p), 8):
        part = p[e:e + 8]
        elems.append(part[0] + part[-1])
    elems = elems[::-1]
    ord_format = map(lambda x: chr(int(x, 16)), elems)
    return ''.join(ord_format)
