# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals
import os.path

from pyramid.response import FileResponse


def dist(request):
    dist_path = request.env.webpack.options['dist_path']
    return FileResponse(os.path.join(dist_path, *request.matchdict['subpath']))


def test(request):
    return dict()


def setup_pyramid(comp, config):
    config.add_route('webpack.dist', '/static/dist/*subpath') \
        .add_view(dist)

    config.add_route('webpack.test', '/webpack/test') \
        .add_view(test, renderer="nextgisweb:webpack/template/test.mako")
