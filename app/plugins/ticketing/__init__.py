import importlib
import pkgutil
import plugins.ticketing as ticketing
from functools import cache

def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    #
    # Source: https://packaging.python.org/guides/creating-and-discovering-plugins/
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

@cache
def load_plugins(plugin = ''):
    if plugin:
        importlib.import_module(plugin)
    else:
        for _, name, _ in iter_namespace(ticketing):
            importlib.import_module(name)
@cache
def get_services():
    services = {}
    for _, name, _ in ticketing.iter_namespace(ticketing):
        temp = name.split(".")
        services[temp[2]] = temp[2]
    return services
