"""Method to recursively update a dictionary."""
import collections.abc


def recursive_update(d, u, merge_lists=False):
    """Method to recursively update a dictionary."""
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = recursive_update(d.get(k, {}), v, merge_lists)
        elif merge_lists and isinstance(v, list) and isinstance(d.get(k), list):
            d[k] += v
        else:
            d[k] = v
    return d
