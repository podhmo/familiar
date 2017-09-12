import logging
import os
from designer.core import create_root_context
from designer.naming import snakecase, goname

logger = logging.getLogger(__name__)


def design_newtypes(ctx):
    if "newtypes" not in ctx:
        logger.info("design #/newtypes is not found")
        return
    f = ctx.package.file("newtypes.go")
    for name, opts in ctx["newtypes"].items():
        typ = getattr(f, opts["type"])
        ob = f.newtype(name, typ, comment=opts.get("description"))
        ctx.register("#/newtypes/{}".format(name), ob)


def design_structs(ctx):
    if "structs" not in ctx:
        logger.info("design #/structs is not found")
        return

    package = ctx.package
    for name, props in ctx["structs"].items():
        filename = "{}.go".format(snakecase(name))
        f = package.file(filename)
        ob = f.struct(goname(name), comment=props.get("description"))
        ctx.register("#/structs/{}".format(name), ob)
        for fieldname, opts in props["properties"].items():
            typ = resolve(ctx, f, opts["type"])
            ob.define_field(goname(fieldname), typ, tag="`json:{}`".format(fieldname))


def resolve(ctx, f, ref):
    if "#/" not in ref:
        return getattr(f, ref)
    # todo: lazy eval
    return ctx.lookup(ref)


def run(src, pkg):
    ctx = create_root_context(src, pkg)
    design_newtypes(ctx)
    design_structs(ctx)
    ctx.repository.emitter.emit(ctx.package, onemit=lambda f, fname: print("goimports -w {}".format(fname).replace(os.environ["GOPATH"], "$GOPATH")))


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
