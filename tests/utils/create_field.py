import string
from random import choice


def random_symbols(length: int, start_symbols="", lower=True, upper=True, digits=False, punctuation=False):
    symbols = ""
    if lower:       symbols += string.ascii_lowercase
    if upper:       symbols += string.ascii_uppercase
    if digits:      symbols += string.digits
    if punctuation: symbols += string.punctuation
    random_line = start_symbols + ''.join(choice(symbols) for _ in range(length))
    return random_line


def create_email(length: int = 10, start_symbols="max", post_email="@gmail.com"):
    return random_symbols(length, start_symbols=start_symbols, digits=True) + post_email


def create_password(length: int = 10):
    return random_symbols(length, digits=True, punctuation=True)


def create_phone():
    return "+7912" + random_symbols(7, digits=True, lower=False, upper=False)
