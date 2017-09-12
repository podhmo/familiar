from dictknife import loading
from goaway import get_repository


class Registry:
    def __init__(self, repository, doc, pkg):
        self.repository = repository
        self.doc = doc
        self.pkg = pkg
        self.universe = {}

    def register(self, address, ob):
        self.universe[address] = ob

    def lookup(self, address):
        return self.universe[address]


class Context:
    def __init__(self, stack, registry):
        self.stack = stack
        self.registry = registry

    def new_child(self, value):
        stack = self.stack[:]
        stack.append(value)
        return self.__class__(stack, self.registry)

    def __contains__(self, k):
        return k in self.stack[-1]

    def __getitem__(self, k):
        return self.stack[-1][k]

    def register(self, address, ob):
        return self.registry.register(address, ob)

    def lookup(self, address):
        return self.registry.lookup(address)

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
    return Context([doc], registry)
