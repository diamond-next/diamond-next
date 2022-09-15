#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

import optparse
import os
import shutil
import sys
import tempfile
import traceback

import configobj

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))


def get_include_paths(path):
    for f in os.listdir(path):
        c_path = os.path.abspath(os.path.join(path, f))

        if os.path.isfile(c_path) and len(f) > 3 and f.endswith('.py'):
            sys.path.append(os.path.dirname(c_path))
        elif os.path.isdir(c_path):
            get_include_paths(c_path)


collectors = {}


def get_collectors(path):
    for f in os.listdir(path):
        c_path = os.path.abspath(os.path.join(path, f))

        if os.path.isfile(c_path) and len(f) > 3 and f.endswith('.py'):
            modname = f[:-3]

            if modname.startswith('Test'):
                continue

            if modname.startswith('test'):
                continue

            try:
                # Import the module
                module = __import__(modname, globals(), locals(), ['*'])

                # Find the name
                for attr in dir(module):
                    if not attr.endswith('Collector'):
                        continue

                    cls = getattr(module, attr)

                    if cls.__module__ != modname:
                        continue

                    if cls.__name__ not in collectors:
                        collectors[cls.__name__] = module
            except Exception:
                print("Failed to import module: %s. %s" % (modname, traceback.format_exc()))
                collectors[modname] = False

        elif os.path.isdir(c_path):
            get_collectors(c_path)


handlers = {}


def get_handlers(path, name=None):
    for f in os.listdir(path):
        c_path = os.path.abspath(os.path.join(path, f))

        if os.path.isfile(c_path) and len(f) > 3 and f.endswith('.py'):
            modname = f[:-3]

            if name and f is not "%s.py" % name:
                break

            try:
                # Import the module
                module = __import__(modname, globals(), locals(), ['*'])

                # Find the name
                for attr in dir(module):
                    if not attr.endswith('Handler') or attr.startswith('Handler'):
                        continue

                    cls = getattr(module, attr)

                    if cls.__name__ not in handlers:
                        handlers[cls.__name__] = module
            except Exception:
                print("Failed to import module: %s. %s" % (modname, traceback.format_exc()))
                handlers[modname] = False

        elif os.path.isdir(c_path):
            get_handlers(c_path)


def write_doc_header(doc_file):
    doc_file.write("<!--")
    doc_file.write("This file was generated from the python source\n")
    doc_file.write("Please edit the source to make changes\n")
    doc_file.write("-->\n")


def write_doc_string(doc_file, name, doc):
    doc_file.write("%s\n" % name)
    doc_file.write("=====\n")

    if doc is None:
        print("No __doc__ string for %s!" % name)

    doc_file.write("%s\n" % doc)


def write_doc_options_header(doc_file):
    doc_file.write("#### Options\n")
    doc_file.write("\n")

    doc_file.write("Setting | Default | Description | Type\n")
    doc_file.write("--------|---------|-------------|-----\n")


def write_doc_options(doc_file, options, default_options):
    for option in sorted(options.keys()):
        default_option = ''
        default_option_type = ''

        if option in default_options:
            default_option_type = default_options[option].__class__.__name__

            if isinstance(default_options[option], list):
                default_option = ', '.join(map(str, default_options[option]))
                default_option += ','
            else:
                default_option = str(default_options[option])

        doc_file.write("%s | %s | %s | %s\n" % (option, default_option, options[option].replace("\n", '<br>\n'), default_option_type))


def write_doc(items, type_name, doc_path):
    for item in sorted(iter(items.keys())):
        # Skip configuring the basic item object
        if item == type_name:
            continue

        if item.startswith('Test'):
            continue

        print("Processing %s..." % item)

        if not hasattr(items[item], item):
            continue

        cls = getattr(items[item], item)

        item_options = None
        default_options = None

        try:
            tmpfile = None

            if type_name == "Collector":
                obj = cls(config=config, handlers={})
            elif type_name == "Handler":
                tmpfile = tempfile.mkstemp()
                obj = cls({'log_file': tmpfile[1]})

            item_options = obj.get_default_config_help()
            default_options = obj.get_default_config()

            if type_name == "Handler":
                os.remove(tmpfile[1])
        except Exception as e:
            print("Caught Exception {}".format(e))

        doc_file = open(os.path.join(doc_path, item + ".md"), 'w')

        write_doc_header(doc_file)
        write_doc_string(doc_file, item, items[item].__doc__)
        write_doc_options_header(doc_file)

        if item_options:
            write_doc_options(doc_file, item_options, default_options)

        if type_name == "Collector":
            doc_file.write("\n")
            doc_file.write("#### Example Output\n")
            doc_file.write("\n")
            doc_file.write("```\n")
            doc_file.write("__EXAMPLESHERE__\n")
            doc_file.write("```\n")
            doc_file.write("\n")

        doc_file.close()


if __name__ == "__main__":
    # Initialize Options
    parser = optparse.OptionParser()
    parser.add_option("-c", "--configfile", dest="configfile", default="/etc/diamond/diamond.conf", help="Path to the config file")
    parser.add_option("-C", "--collector", dest="collector", default=None, help="Configure a single collector")
    parser.add_option("-H", "--handler", dest="handler", default=None, help="Configure a single handler")
    parser.add_option("-p", "--print", action="store_true", dest="dump", default=False, help="Just print the defaults")

    # Parse Command Line Args
    (options, args) = parser.parse_args()

    # Initialize Config
    if os.path.exists(options.configfile):
        config = configobj.ConfigObj(os.path.abspath(options.configfile))
    else:
        print("ERROR: Config file: %s does not exist." % options.configfile, file=sys.stderr)
        print("Please run python build_doc.py -c /path/to/diamond.conf", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'docs'))

    if options.collector or (not options.collector and not options.handler):
        collector_path = config['server']['collectors_path']
        collectors_doc_path = os.path.join(docs_path, "collectors")
        get_include_paths(collector_path)

        if options.collector:
            single_collector_path = os.path.join(collector_path, options.collector)
            get_collectors(single_collector_path)
        else:
            # Ugly hack for snmp collector overrides
            get_collectors(os.path.join(collector_path, 'snmp'))
            get_collectors(collector_path)

            shutil.rmtree(collectors_doc_path)
            os.mkdir(collectors_doc_path)

        write_doc(collectors, "Collector", collectors_doc_path)

    if options.handler or (not options.collector and not options.handler):
        handler_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'diamond', 'handler'))
        handlers_doc_path = os.path.join(docs_path, "handlers")
        get_include_paths(handler_path)

        if options.handler:
            get_handlers(handler_path, name=options.handler)
        else:
            get_handlers(handler_path)
            shutil.rmtree(handlers_doc_path)
            os.mkdir(handlers_doc_path)

        write_doc(handlers, "Handler", handlers_doc_path)
