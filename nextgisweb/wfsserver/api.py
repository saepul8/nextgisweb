# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyramid.response import Response

from ..resource import resource_factory, ServiceScope

from .wfs_handler import WFSHandler
from .model import Service

from .third_party.FeatureServer.Server import Server, FeatureServerException
from .third_party.web_request.response import Response as FeatureserverResponse

from nextgis_to_fs import NextgiswebDatasource


NS_XLINK = 'http://www.w3.org/1999/xlink'


def wfs(resource, request):
    request.resource_permission(ServiceScope.connect)

    wfsHandler = WFSHandler(resource, request)
    try:
        xml = wfsHandler.response()
        return Response(xml, content_type='text/xml')
    except NotImplementedError:
        return legacy_handler(resource, request)


def legacy_handler(obj, request):
    params = dict((k.upper(), v) for k, v in request.params.items())

    req = params.get('REQUEST')
    post_data = request.body
    request_method = request.method

    # If request_method is POST and request is KeyValue Parameter request
    # change the requset_method to GET. It allows do not rewrite
    # featureserver's parsing methods. (Featureserver expects GET
    # requests and none post_data in case of KVP).
    # (If request method is POST and post_data is XML, we'll pass the
    # data to Service.Request method)
    if request_method == 'POST' and req in \
            ['GetCapabilities', 'DescribeFeatureType', 'GetFeature']:
        request_method = 'GET'
        post_data = None

    # WFS 1.0.0 bbox: 'BBOX=minX,minY,maxX,maxY'
    # WFS 2.0.0 bbox: 'BBOX=minX,minY,maxX,maxY,EPSG:3857'
    bbox = params.get('BBOX')
    bbox = ','.join(bbox.split(',')[:4]) if bbox else None

    params = {
        'service': params.get('SERVICE'),
        'request': req,
        'typename': params.get('TYPENAME'),     # WFS 1.0.0
        'typenames': params.get('TYPENAMES'),   # WFS 2.0.0
        'srsname': params.get('SRSNAME'),
        'version': params.get('VERSION'),
        'acceptversions': params.get('ACCEPTVERSIONS'),  # WFS 2.0.0 GetCapabilities
        'maxfeatures': params.get('MAXFEATURES'),   # WFS 1.0.0
        'count': params.get('COUNT'),               # WFS 2.0.0
        'startfeature': params.get('STARTFEATURE'),
        'filter': params.get('FILTER'),
        'format': params.get('OUTPUTFORMAT'),
        'bbox': bbox
    }
    # None values can cause parsing errors in featureserver. So delete 'Nones':
    params = {key: params[key] for key in params if params[key] is not None}

    datasources = {
        l.keyname: NextgiswebDatasource(
            l.keyname,
            layer=l.resource,
            maxfeatures=l.maxfeatures,
            title=l.display_name) for l in obj.layers
    }
    sourcenames = '/'.join([sourcename for sourcename in datasources])

    server = Server(datasources)
    base_path = request.path_url

    try:
        # import ipdb; ipdb.set_trace()
        result = server.dispatchRequest(
            base_path=base_path,
            path_info='/' + sourcenames, params=params,
            post_data=post_data,
            request_method=request_method)
    except FeatureServerException as e:
        data = e.data
        content_type = e.mime
        return Response(data, content_type=content_type)

    # Send results

    if isinstance(result, tuple):
        # respond
        # for req.lower() in ['getcapabilities', 'describefeaturetype'] requests
        content_type, resxml = result
        resp = Response(resxml, content_type=content_type)
        return resp
    elif isinstance(result, FeatureserverResponse):
        # respond to GetFeature, Update, Insert, Delete requests
        data = result.getData()
        return Response(data, content_type=result.content_type)


def setup_pyramid(comp, config):
    config.add_route(
        'wfsserver.wfs', r'/api/resource/{id:\d+}/wfs',
        factory=resource_factory
    ).add_view(wfs, context=Service)