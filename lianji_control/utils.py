def bytecoding(fun):
    def wrapper(*args, **kwargs):
        kk = fun(*args, **kwargs)
        kk = bytes.fromhex(kk)
        return kk
    return wrapper