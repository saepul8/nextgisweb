# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals
import json
from collections import OrderedDict
from pkg_resources import get_distribution

from ..command import Command
from ..package import amd_packages, pkginfo


@Command.registry.register
class BuildConfigCommand():
    identity = 'webpack.build_config'
    no_initialize = True

    @classmethod
    def argparser_setup(cls, parser, env):
        pass

    @classmethod
    def execute(cls, args, env):
        result = OrderedDict()
        result['amd_packages'] = [pname for pname, ppath in amd_packages()]
        
        packages = result['packages'] = list()
        pkg_names = []
        for compid in env._components.keys():
            pkg = pkginfo.comp_pkg(compid)
            if pkg not in pkg_names:
                pkg_names.append(pkg)
                dist = get_distribution(pkg)
                packages.append(OrderedDict((
                    ('name', pkg),
                    # TODO: Use pkg_resources api for package path
                    ('path', dist.location + '/' + pkg.replace('_', '-')),
                )))

        print(json.dumps(result))