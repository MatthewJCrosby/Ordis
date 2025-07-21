import importlib
import pkgutil
from pathlib import Path

RESOLVER_PACKAGE = "gql.resolvers"

# dynamically grabs all resolver files at runtime
def discover_resolvers():
    package_dir = Path(__file__).parent / "resolvers"
    modules = []

    for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
        full_module = f"{RESOLVER_PACKAGE}.{module_name}"
        module = importlib.import_module(full_module)
        if hasattr(module, "resolvers"):
            modules.extend(module.resolvers)

    return modules

bindables = discover_resolvers()
