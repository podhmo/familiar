import os
from dictknife import loading
from goaway import get_repository


class Registry:
    def __init__(self, repository, doc, pkg):
        self.repository = repository
        self.doc = doc
        self.pkg = pkg


class Context:
    def __init__(self, stack, registry):
        self.stack = stack
        self.registry = registry

    def new_child(self, value):
        stack = self.stack[:]
        stack.append(value)
        return self.__class__(stack, self.registry)

    def __getitem__(self, k):
        return self.stack[-1][k]

    @property
    def repository(self):
        return self.registry.repository

    @property
    def package(self):
        return self.registry.repository.package(self.registry.pkg)


def create_root_context(src, pkg):
    doc = loading.loadfile(src)
    repository = get_repository()
    registry = Registry(repository, doc, pkg)
    return Context([doc], registry)


def run(src, pkg):
    ctx = create_root_context(src, pkg)
    design_newtypes(ctx)
    ctx.repository.emitter.emit(ctx.package, onemit=lambda f, fname: print("goimports -w {}".format(fname).replace(os.environ["GOPATH"], "$GOPATH")))


def design_newtypes(ctx):
    f = ctx.package.file("newtypes.go")
    for name, props in ctx["newtypes"].items():
        typ = getattr(f, props["type"])
        f.newtype(name, typ, comment=props.get("description"))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("--pkg", default="github.com/podhmo/familiar/app")
    args = parser.parse_args()
    import logging
    logging.basicConfig(level=logging.DEBUG)
    return run(args.src, args.pkg)


if __name__ == "__main__":
    main()
