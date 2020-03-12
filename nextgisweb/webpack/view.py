# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals
import io
import json
import os.path

from pyramid.response import Response, FileResponse


def dist(request):
    dist_path = request.env.webpack.options['dist_path']
    return FileResponse(os.path.join(dist_path, *request.matchdict['subpath']))


def cload(request):
    manifest_path = os.path.join(
        request.env.webpack.options['dist_path'],
        'manifest.json')

    # TODO: Cache manifest.json reading
    with io.open(manifest_path, 'r') as fd:
        manifest = json.load(fd)
        entrypoints = manifest['entrypoints']

    entry = '/'.join(request.matchdict['subpath'])
    if entry.endswith('.js'):
        entry = entry[:-3]

    if entry in entrypoints:
        chunks = entrypoints[entry].get('js')
    else:
        chunks = []

    chunks = filter(lambda (chunk): chunk.startswith('cdata/'), chunks)
    chunks = map(lambda (c): (c[:-3] if c.endswith('.js') else c), chunks)

    return Response(
        "define(" + json.dumps(chunks) + ", function () {});",
        content_type="text/javascript")


def cdata(request):
    dist_path = request.env.webpack.options['dist_path']
    return FileResponse(os.path.join(dist_path, 'cdata', *request.matchdict['subpath']))


def test(request):
    return dict()


def setup_pyramid(comp, config):
    config.add_route('webpack.dist', '/static/dist/*subpath') \
        .add_view(dist)

    config.add_route('webpack.cload', '/webpack/cload/*subpath') \
        .add_view(cload)

    config.add_route('webpack.cdata', '/webpack/cdata/*subpath') \
        .add_view(cdata)

    config.add_route('webpack.test', '/webpack/test') \
        .add_view(test, renderer="nextgisweb:webpack/template/test.mako")
