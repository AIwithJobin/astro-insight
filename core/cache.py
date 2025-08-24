import time
_CACHE, _TTL = {}, 300  

def cache_get(key):
    val, exp = _CACHE.get(key, (None, 0))
    return val if time.time() < exp else None

def cache_set(key, val):
    _CACHE[key] = (val, time.time() + _TTL)