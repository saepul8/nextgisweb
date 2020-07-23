# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals, print_function, absolute_import
import os
import logging
import six

from pyramid.paster import setup_logging

from .lib.config import load_config
from .env import Env, setenv

logger = logging.getLogger(__name__)


def pkginfo():
    components = (
        'core',
        'sentry',
        'pyramid',
        'auth',
        'resource',
        'resource_social',
        'resmeta',
        'spatial_ref_sys',
        'layer',
        'feature_layer',
        'feature_description',
        'feature_attachment',
        'render',
        'marker_library',
        'webmap',
        'file_storage',
        'vector_layer',
        'postgis',
        'raster_layer',
        'raster_style',
        'wmsclient',
        'wmsserver',
        'tmsclient',
        'file_upload',
        'audit',
    )

    if six.PY3:
        logger.warning("Component [wfsserver] disabled in Python 3 environment!")
    else:
        components = components + ('wfsserver', )

    return dict(
        components=dict(map(
            lambda i: (i, "nextgisweb.%s" % i),
            components)
        )
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """

    if 'NEXTGISWEB_LOGGING' in os.environ:
        setup_logging(os.environ['NEXTGISWEB_LOGGING'])

    if 'logging' in settings:
        logger.error("Parameter 'logging' was ignored! Use NEXTGISWEB_LOGGING variable instead.")

    if 'config' in settings:
        logger.error("Parameter 'config' was ignored! Use NEXTGISWEB_CONFIG variable instead.")

    kset = set(settings.keys())
    kset = kset.difference(set(('logging', 'config')))
    if len(kset) > 0:
        logger.warn("Ignored paster's parameters: %s", ', '.join(kset))

    env = Env(cfg=load_config(None))
    env.initialize()

    setenv(env)

    config = env.pyramid.make_app({})
    return config.make_wsgi_app()


def amd_packages():
    return (
        # contrib packages
        ('dojo', 'nextgisweb:amd_packages/contrib/dojo'),
        ('dijit', 'nextgisweb:amd_packages/contrib/dijit'),
        ('dojox', 'nextgisweb:amd_packages/contrib/dojox'),
        ('cbtree', 'nextgisweb:amd_packages/contrib/cbtree'),
        ('xstyle', 'nextgisweb:amd_packages/contrib/xstyle'),
        ('put-selector', 'nextgisweb:amd_packages/contrib/put-selector'),
        ('dgrid', 'nextgisweb:amd_packages/contrib/dgrid'),
        ('handlebars', 'nextgisweb:amd_packages/contrib/handlebars'),
        ('openlayers', 'nextgisweb:amd_packages/contrib/openlayers'),
        ('dom-to-image', 'nextgisweb:amd_packages/contrib/dom-to-image'),
        ('svg4everybody', 'nextgisweb:amd_packages/contrib/svg4everybody'),
        ('codemirror', 'nextgisweb:amd_packages/contrib/codemirror'),
        ('jquery', 'nextgisweb:amd_packages/contrib/jquery'),
        ('tus', 'nextgisweb:amd_packages/contrib/tus'),

        # nextgisweb packages
        ('ngw', 'nextgisweb:amd_packages/ngw'),

        # components packages
        ('ngw-pyramid', 'nextgisweb:pyramid/amd/ngw-pyramid'),
        ('ngw-resource', 'nextgisweb:resource/amd/ngw-resource'),
        ('ngw-resource-social', 'nextgisweb:resource_social/amd/ngw-resource-social'),
        ('ngw-resmeta', 'nextgisweb:resmeta/amd/ngw-resmeta'),
        ('ngw-feature-layer', 'nextgisweb:feature_layer/amd/ngw-feature-layer'),
        ('ngw-feature-description', 'nextgisweb:feature_description/amd/ngw-feature-description'),
        ('ngw-feature-attachment', 'nextgisweb:feature_attachment/amd/ngw-feature-attachment'),
        ('ngw-postgis', 'nextgisweb:postgis/amd/ngw-postgis'),
        ('ngw-wmsclient', 'nextgisweb:wmsclient/amd/ngw-wmsclient'),
        ('ngw-wmsserver', 'nextgisweb:wmsserver/amd/ngw-wmsserver'),
        ('ngw-wfsserver', 'nextgisweb:wfsserver/amd/ngw-wfsserver'),
        ('ngw-tmsclient', 'nextgisweb:tmsclient/amd/ngw-tmsclient'),
        ('ngw-vector-layer', 'nextgisweb:vector_layer/amd/ngw-vector-layer'),
        ('ngw-raster-layer', 'nextgisweb:raster_layer/amd/ngw-raster-layer'),
        ('ngw-webmap', 'nextgisweb:webmap/amd/ngw-webmap'),
        ('ngw-auth', 'nextgisweb:auth/amd/ngw-auth'),
        ('ngw-file-upload', 'nextgisweb:file_upload/amd/ngw-file-upload'),
        ('ngw-spatial-ref-sys', 'nextgisweb:spatial_ref_sys/amd/ngw-spatial-ref-sys'),
        ('ngw-render', 'nextgisweb:render/amd/ngw-render'),
        ('ngw-audit', 'nextgisweb:audit/amd/ngw-audit'),
    )
