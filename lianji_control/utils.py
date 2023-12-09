def bytecoding(fun):
    def wrapper(*args, **kwargs):
        kk = fun(*args, **kwargs)
        kk = bytes.fromhex(kk)
        return kk
    return wrapper


def distance(fun):
    def wrapper(*args, **kwargs):
        r = fun(*args, **kwargs)
        # d = 4 * r # 假设的线性导程是一圈4mm
        d = r # 假设的线性导程是一圈1mm
        d = "%.3f" %d
        return d
    return wrapper
