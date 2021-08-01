import functools

def memoize(func):
    try:
        return functools.cache(func)
    except AttributeError:
        return functools.lru_cache(maxsize=2)(func)
