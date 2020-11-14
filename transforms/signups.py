import hashlib
import random


ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def accept(data):
    # event
    email = data.get('email')
    if not email:
        raise Exception('No event in data')
    email = email.lower()

    password = data.get('password')
    if not password:
        raise Exception('no password')
    if len(password) < 8:
        raise Exception('password too short')

    chars = []
    for _ in range(8):
        chars.append(random.choice(ALPHABET))

    salt = "".join(chars)
    m = hashlib.sha256()
    m.update(bytes(salt, 'utf8'))
    m.update(bytes(password, 'utf8'))
    passwd = m.hexdigest()

    return {
        'email': email,
        'passwd': passwd,
        'salt': salt,
    }


def output(data):
    return {}