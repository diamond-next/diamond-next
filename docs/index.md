# Status

Currently `master` branch is under audit, the latest stable version is 4.0.916 same as the last known release of Diamond. Python 3 support.

  
# Diamond-next

Diamond is a python daemon that collects system metrics and publishes them to [Graphite](handlers/GraphiteHandler.md) (and others).
It is capable of collecting cpu, memory, network, i/o, load and disk metrics.
Additionally, it features an API for implementing custom collectors for gathering metrics from almost any source.

## Huh, -next ?

This is fork of [python-diamond/Diamond](https://github.com/python-diamond/Diamond).
Unfortunately development of Diamond is stuck, let's face it - project is abandoned.
Diamond-next is an effort to continue the work. Besides the name of the package, under the hood, from user perspective, everything will be the same.

## Getting Started

Steps to getting started:

  * Read the [documentation](http://diamond.readthedocs.org)
  * Install via `pip install diamond-next`.
    The releases on GitHub are not recommended for use.
    Use `pypi-install diamond` on Debian/Ubuntu systems with python-stdeb installed to build packages.
  * Copy the `diamond.conf.example` file to `diamond.conf`.
  * Optional: Run `diamond-setup` to help set collectors in `diamond.conf`.
  * Modify `diamond.conf` for your needs.
  * Run diamond with one of: `diamond` or `initctl start diamond` or `/etc/init.d/diamond restart`.

## Success Stories

 * Diamond has successfully been deployed to a cluster of 1000 machines pushing [3 million points per minute](https://answers.launchpad.net/graphite/+question/178969).
 * Diamond is deployed on [Fabric's](https://get.fabric.io/) infrastructure, polling hundreds of metric sources and pushing millions of points per minute.
 * **Have a story? Please share!**

## History

Diamond was a brightcove project and hosted at [BrightcoveOS](https://github.com/brightcoveos/Diamond).
However none of the active developers are brightcove employees and so the development
has moved to [python-diamond](https://github.com/python-diamond/Diamond). We request
that any new pull requests and issues be cut against python-diamond. We will keep
BrightcoveOS updated and still honor issues/tickets cut on that repo. Unfortunately development of Diamond is stuck,
let's face it - project is abandoned. Diamond-next is an effort to continue development.

## Diamond Related Projects

 * [Related Projects](Related-Projects.md)


## License

Code: MIT
Logo: Vector Designed By Darwisgraphic from   [pngtree.com](https://pngtree.com/freepng/diamond-logo-template-vector-icon-illustration-design_3626181.html)
