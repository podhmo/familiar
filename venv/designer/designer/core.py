import logging
from dictknife import loading
from goaway import get_repository
logger = logging.getLogger(__name__)


class Registry:
    def __init__(self, repository, doc, pkg):
        self.repository = repository
        self.doc = doc
        self.pkg = pkg
        self.universe = {}

    def register(self, address, ob):
        self.universe[address] = ob

    def lookup(self, address):
        try:
            return self.universe[address]
        except KeyError:
            import sys
            print(list(self.universe.keys()), "@", file=sys.stderr)
            raise


class Path(list):
    def __str__(self):
        return "#/" + "/".join(self)

    def appended(self, value):
        new = self.__class__(self[:])
        new.append(value)
        return new


class Context:
    def __init__(self, stack, path, registry):
        self.stack = stack
        self.registry = registry
        self.path = path

    def new_child(self, name):
        stack = self.stack[:]
        path = self.path.appended(name)
        stack.append(self.stack[-1].get(name))
        logger.debug("new child: %s", path)
        return self.__class__(stack, path, self.registry)

    @property
    def is_empty(self):
        return self.stack[-1] is None

    def __contains__(self, k):
        return k in self.stack[-1]

    def __getitem__(self, k):
        return self.stack[-1][k]

    def items(self):
        return self.stack[-1].items()

    def register(self, ob, name=None):
        if name is None:
            address = self.path
        else:
            address = self.path.appended(name)
        logger.debug("register: %s", address)
        return self.registry.register(str(address), ob)

    def lookup(self, path):
        return self.registry.lookup(str(path))

    @property
    def repository(self):
        return self.registry.repository

    @property
    def package(self):
        return self.registry.repository.package(self.registry.pkg)

    @property
    def root(self):
        return self.stack[0]


def create_root_context(src, pkg):
    doc = loading.loadfile(src)
    repository = get_repository()
    registry = Registry(repository, doc, pkg)
    return Context([doc], Path(), registry)
