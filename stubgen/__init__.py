"""Generate python stub files for pybind11 modules."""

from stubgen.stubgenc import generate_stub_for_c_module


Options = NamedTuple('Options', [('modules', List[str]),
                                 ('ignore_errors', bool),
                                 ('recursive', bool),
                                 ('output_dir', str),
                                 ])


def parse_options(args: List[str]) -> Options:
    # TODO: why not use click and reduce the amount of code to maintain
    # within this module.
    recursive = False
    ignore_errors = False
    output_dir = 'out'
    while args and args[0].startswith('-'):
        if args[0] in '-o':
            output_dir = args[1]
            args = args[1:]
        elif args[0] == '--recursive':
            recursive = True
        elif args[0] == '--ignore-errors':
            ignore_errors = True
        elif args[0] in ('-h', '--help'):
            usage(exit_nonzero=False)
        else:
            raise SystemExit('Unrecognized option %s' % args[0])
        args = args[1:]
    if not args:
        usage()

    # Create the output folder if it doesn't already exist.
    os.makedirs(output_dir, exist_ok=True)
    return Options(modules=args,
                   ignore_errors=ignore_errors,
                   recursive=recursive,
                   output_dir=output_dir)


def usage(exit_nonzero: bool = True) -> None:
    usage = textwrap.dedent("""\
        usage: stubgen [--recursive] [--ignore-errors] [-o PATH] MODULE ...

        Generate draft stubs for modules.

        Stubs are generated in directory ./out, to avoid overriding files with
        manual changes.  This directory is assumed to exist.

        Options:
          --recursive     traverse listed modules to generate inner package modules as well
          --ignore-errors ignore errors when trying to generate stubs for modules
          -o PATH         Change the output folder [default: out]
          -h, --help      print this help message and exit
    """.rstrip())

    if exit_nonzero:
        # The user made a mistake, so we should return with an error code
        raise SystemExit(usage)
    else:
        # The user asked for help specifically, so we should exit with success
        print(usage, file=sys.stderr)
        sys.exit()


def walk_packages(packages: List[str]) -> Iterator[str]:
    """Iterates through all packages and sub-packages in the given list.

    Python packages have a __path__ attribute defined, which pkgutil uses to determine
    the package hierarchy.  However, packages in C extensions do not have this attribute,
    so we have to roll out our own.
    """
    for package_name in packages:
        package = importlib.import_module(package_name)
        yield package.__name__
        # get the path of the object (needed by pkgutil)
        path = getattr(package, '__path__', None)
        if path is None:
            # object has no path; this means it's either a module inside a package
            # (and thus no sub-packages), or it could be a C extension package.
            if is_c_module(package):
                # This is a C extension module, now get the list of all sub-packages
                # using the inspect module
                subpackages = [package.__name__ + "." + name
                               for name, val in inspect.getmembers(package)
                               if inspect.ismodule(val)]
                # recursively iterate through the subpackages
                for submodule in walk_packages(subpackages):
                    yield submodule
            # It's a module inside a package.  There's nothing else to walk/yield.
        else:
            all_packages = pkgutil.walk_packages(path, prefix=package.__name__ + ".",
                                                 onerror=lambda r: None)
            for importer, qualified_name, ispkg in all_packages:
                yield qualified_name


def main() -> None:
    # Make sure that the current directory is in sys.path so that
    # stubgen can be run on packages in the current directory.
    if '' not in sys.path:
        sys.path.insert(0, '')

    options = parse_options(sys.argv[1:])
    if not os.path.isdir(options.output_dir):
        raise SystemExit('Directory "{}" does not exist'.format(options.output_dir))
    sigs = {}  # type: Any
    class_sigs = {}  # type: Any
    for module in (options.modules if not options.recursive else walk_packages(options.modules)):
        try:
            target = os.path.join(options.output_dir, module.replace(',', '/') + '.pyi')
            generate_stub_for_c_module(module_name=module,
                                       target=target,
                                       add_header=True,
                                       sigs=sigs,
                                       class_sigs=class_sigs)
            print('Created ' + target)
        except Exception as e:
            if not options.ignore_errors:
                raise e
            else:
                print("Stub generation failed for: ", module, file=sys.stderr)


if __name__ == '__main__':
    main()
