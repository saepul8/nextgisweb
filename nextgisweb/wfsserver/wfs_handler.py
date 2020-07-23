# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals

from lxml import etree

from ..feature_layer import FIELD_TYPE, GEOM_TYPE
from ..resource import DataScope

from .model import Layer

# Spec: http://docs.opengeospatial.org/is/09-025r2/09-025r2.html
VERSION = '2.0.2'


def El(tag, attrs=None, parent=None, text=None):
    e = etree.Element(tag, attrs)
    if text is not None:
        e.text = text
    if parent is not None:
        parent.append(e)
    return e


WFS_OPERATIONS = (
    ('GetCapabilities', ()),
    ('DescribeFeatureType', ()),
    ('GetFeature', ('GML2', )),
    ('Transaction', ('GML2', )),
)


GEOM_TYPE_TO_GML_TYPE = {
    GEOM_TYPE.POINT: 'gml:PointPropertyType',
    GEOM_TYPE.LINESTRING: 'gml:LineStringPropertyType',
    GEOM_TYPE.POLYGON: 'gml:PolygonPropertyType',
    GEOM_TYPE.MULTIPOINT: 'gml:MultiPointPropertyType',
    GEOM_TYPE.MULTILINESTRING: 'gml:MultiLineStringPropertyType',
    GEOM_TYPE.MULTIPOLYGON: 'gml:MultiPolygonPropertyType',
}


class WFSHandler():
    def __init__(self, resource, request):
        self.resource = resource
        self.request = request

        # 6.2.5.2 Parameter names shall not be case sensitive
        params = dict((k.upper(), v) for k, v in request.params.items())
        self.p_requset = params.get('REQUEST')
        self.p_typename = params.get('TYPENAME')

    def response(self):
        if self.p_requset == 'GetCapabilities':
            return self._get_capabilities()
        elif self.p_requset == 'DescribeFeatureType':
            return self._describe_feature_type()
        else:
            raise NotImplementedError()

    def _get_capabilities(self):
        root = El('WFS_Capabilities', dict(version=VERSION))

        __s = El('Service', parent=root)
        El('Name', parent=__s, text='WFS Server')
        El('Title', parent=__s, text='Web Feature Service Server')
        El('Abstract', parent=__s, text='Supports WFS')

        __c = El('Capability', parent=root)
        __r = El('Request', parent=__c)

        wfs_url = self.request.route_url('wfsserver.wfs', id=self.resource.id)
        for wfs_operation, result_formats in WFS_OPERATIONS:
            __wfs_op = El(wfs_operation, parent=__r)
            for request_method in ('Get', 'Post'):
                __dcp = El('DCPType', parent=__wfs_op)
                __http = El('HTTP', parent=__dcp)
                El(request_method, dict(onlineResource=wfs_url), parent=__http)
            for result_format in result_formats:
                __format = El('ResultFormat', parent=__wfs_op)
                El(result_format, parent=__format)

        __list = El('FeatureTypeList', parent=root)
        __ops = El('Operations', parent=__list)
        El('Query', parent=__ops)

        for layer in self.resource.layers:
            feature_layer = layer.resource
            if not feature_layer.has_permission(DataScope.read, self.request.user):
                continue
            __type = El('FeatureType', parent=__list)
            El('Name', parent=__type, text=layer.keyname)
            El('Title', parent=__type, text=layer.display_name)
            El('Abstract', parent=__type)
            El('SRS', parent=__type, text="EPSG:%s" % layer.resource.srs_id)

            __ops = El('Operations', parent=__type)
            if feature_layer.has_permission(DataScope.write, self.request.user):
                El('Insert', parent=__ops)
                El('Update', parent=__ops)
                El('Delete', parent=__ops)

            extent = feature_layer.extent
            El('bbox', dict(maxx=str(extent['maxLon']), maxy=str(extent['maxLat']),
                            minx=str(extent['minLon']), miny=str(extent['minLat'])), parent=__type)

        return etree.tostring(root)

    def _describe_feature_type(self):
        root = El('schema')
        typename = self.p_typename.split(',')
        if len(typename) == 1:
            layer = Layer.filter_by(service_id=self.resource.id, keyname=typename[0]).one()
            El('element', dict(name=layer.keyname, type="fs:%s_Type" % layer.keyname), parent=root)
            __ctype = El('complexType', dict(name="%s_Type" % layer.keyname), parent=root)
            __ccontent = El('complexContent', parent=__ctype)
            __ext = El('extension', parent=__ccontent)
            __seq = El('sequence', parent=__ext)
            for field in layer.resource.fields:
                if field.datatype == FIELD_TYPE.REAL:
                    datatype = 'double'
                else:
                    datatype = field.datatype.lower()
                El('element', dict(name=field.keyname, type=datatype), parent=__seq)
            El('element', dict(name='geom', type=GEOM_TYPE_TO_GML_TYPE[
                layer.resource.geometry_type]), parent=__seq)
        else:
            for keyname in typename:
                import_url = self.request.route_url(
                    'wfsserver.wfs', id=self.resource.id,
                    _query=dict(REQUEST='DescribeFeatureType', TYPENAME=keyname))
                El('import', dict(schemaLocation=import_url), parent=root)

        return etree.tostring(root)
