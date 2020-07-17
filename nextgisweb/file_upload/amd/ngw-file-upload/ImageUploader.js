define([
    "dojo/_base/declare",
    "ngw-pyramid/i18n!file_upload",
    "ngw-pyramid/hbs-i18n",
    "dojo/text!./template/ImageUploader.hbs",
    './Uploader'
], function (
    declare,
    i18n,
    hbsI18n,
    template,
    Uploader,
) {
    return declare([Uploader], {
        templateString: hbsI18n(template, i18n),

        startup: function () {
            this.inherited(arguments);

            this.setAccept('image/png');
        },

        setImageUrl: function (url) {
            this.dropTarget.style.background = 'url(' + url + ') no-repeat';
        },

        uploadBegin: function () {
            this.inherited(arguments);

            var files = this.uploaderWidget.inputNode.files;
            if (files.length === 1) {
                var reader = new FileReader();
                reader.onloadend = function () {
                    var image = reader.result;
                    this.setImageUrl(image);
                }.bind(this);
                reader.readAsDataURL(files[0]);
            }
        }
    });
});
