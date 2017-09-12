import logging
import os.path
from designer.core import create_root_context
from designer.naming import snakecase, goname

logger = logging.getLogger(__name__)


def design_newtypes(ctx):
    if ctx.is_empty:
        logger.info("%s is not found", ctx.path)
        return
    f = ctx.package.file("newtypes.go")
    for name, opts in ctx.items():
        typ = getattr(f, opts["type"])
        ob = f.newtype(name, typ, comment=opts.get("description"))
        ctx.register(ob, name=name)


def design_structs(ctx, *, package=None):
    if ctx.is_empty:
        logger.info("%s is not found", ctx.path)
        return

    package = package or ctx.package
    for name, props in ctx.items():
        _design_struct(ctx.new_child(name), package=package)


def _design_struct(ctx, *, package=None):
    if ctx.is_empty:
        logger.info("%s is not found", ctx.path)
        return
    name = ctx.path[-1]
    props = ctx.stack[-1]
    filename = "{}.go".format(snakecase(name))
    f = package.file(filename)
    ob = f.struct(goname(name), comment=props.get("description"))
    ctx.register(ob)
    for fieldname, opts in props["properties"].items():
        if "items" in opts:
            typ = resolve(ctx, f, opts["items"])
            ob.define_field(goname(fieldname), typ.slice, tag='`json:"{}"`'.format(fieldname))
        else:
            typ = resolve(ctx, f, opts["type"])
            ob.define_field(goname(fieldname), typ, tag='`json:"{}"`'.format(fieldname))


def design_events(ctx, *, package=None):
    if ctx.is_empty:
        logger.info("%s is not found", ctx.path)
        return

    package = package or ctx.repository.package(os.path.join(ctx.package.fullname, "events"))
    f = package.file("event_type.go")
    ev = f.enum(goname("event_type"), f.string)
    ctx.register(ev, name=":event_type:")
    for name, opts in ctx.items():
        ev.define_member(name, name)

    for evname, opts in ctx.items():
        _design_struct(ctx.new_child(evname), package=package)


def p(*args):
    import sys
    print(*args, file=sys.stderr)


def resolve(ctx, f, ref):
    if "#/" not in ref:
        return getattr(f, ref)
    # todo: lazy eval
    return ctx.lookup(ref)


def run(src, pkgpath):
    ctx = create_root_context(src, pkgpath)
    design_newtypes(ctx.new_child("newtypes"))
    design_structs(ctx.new_child("structs"))
    design_events(ctx.new_child("events"))
    for fullname, package in ctx.repository.packages.items():
        if fullname.startswith(pkgpath):
            ctx.repository.emitter.emit(package, onemit=lambda f, fname: print("goimports -w {}".format(fname).replace(os.environ["GOPATH"], "$GOPATH")))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("--pkg", default="github.com/podhmo/familiar/app/gen")
    args = parser.parse_args()
    import logging
    logging.basicConfig(level=logging.DEBUG)
    return run(args.src, args.pkg)


if __name__ == "__main__":
    main()
