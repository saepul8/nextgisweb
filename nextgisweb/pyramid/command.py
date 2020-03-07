# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals

from ..command import Command
from ..package import amd_packages


@Command.registry.register
class AMDPackagesCommand():
    identity = 'amd_packages'

    @classmethod
    def argparser_setup(cls, parser, env):
        pass

    @classmethod
    def execute(cls, args, env):
        for pname, path in amd_packages():
            print(pname)
