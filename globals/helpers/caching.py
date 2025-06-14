from functools import wraps
import numpy as np


def make_hashable(arg):
    """
    Convert unhashable arguments like lists and numpy arrays to a hashable type.
    """
    if isinstance(arg, (list, np.ndarray)):
        return tuple(make_hashable(item) for item in arg)
    elif isinstance(arg, dict):
        return tuple((make_hashable(k), make_hashable(v)) for k, v in sorted(arg.items()))
    else:
        return arg


def cache_method(func):
    cache_attr_name = f"_cache_{func.__name__}"

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Initialize the cache attribute if it doesn't exist
        if not hasattr(self, cache_attr_name):
            setattr(self, cache_attr_name, {})

        cache = getattr(self, cache_attr_name)

        # Create a hashable key for the arguments
        key = (tuple(make_hashable(arg) for arg in args),
               tuple((k, make_hashable(v)) for k, v in sorted(kwargs.items())))

        # If the key is not in the cache, call the function and store the result
        if key not in cache:
            cache[key] = func(self, *args, **kwargs)

        return cache[key]

    # Add a method to clear the cache
    def clear_cache(self):
        if hasattr(self, cache_attr_name):
            setattr(self, cache_attr_name, {})

    # Attach the clear_cache function to the wrapper
    wrapper.clear_cache = clear_cache

    return wrapper
