/* globals define */
define([
    "dojo/_base/declare",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "ngw-pyramid/i18n!vector_layer",
    "ngw-pyramid/hbs-i18n",
    "ngw-resource/serialize",
    // resource
    "dojo/text!./template/VersionedWidget.hbs",
    // template
    "dijit/form/CheckBox",
    "dojox/layout/TableContainer"
], function (
    declare,
    _WidgetBase,
    _TemplatedMixin,
    _WidgetsInTemplateMixin,
    i18n,
    hbsI18n,
    serialize,
    template
) {
    return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin, serialize.Mixin], {
        title: i18n.gettext("Versioning"),
        templateString: hbsI18n(template, i18n),
        prefix: "vector_layer",

        serializeInMixin: function (data) {
            var value = data.vector_layer;
            if (value.versioned === "on") {
                value.versioned = true;
            }
        }
    });
});