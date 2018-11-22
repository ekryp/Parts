import urllib

from flask import request
from flask_cache import Cache

cache = Cache()


def has_cache_restriction(*args, **kwargs):
    key = cache_key()
    # For cached value, pass cache=true
    # No cache for download_file=true, file cache not supported
    # For newly calculated data cache=false (dont consider cached data)
    # If has has restriction don't cache it, cache=true cachbale otherwise not
    return not ('cache=true' in key) or ('download_file=true' in key)

def cache_key():
    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])

    # Clear the cached data if 'reset_cache=true' (recalculate and set as new cache data)
    # But don't consider them as cache key_prefix
    if 'reset_cache=true' in key:
        filtered_key = key.replace('&reset_cache=true', '')
        if filtered_key == key:
            filtered_key = key.replace('reset_cache=true', '')
        key = filtered_key
        cache.delete(key)
    return key