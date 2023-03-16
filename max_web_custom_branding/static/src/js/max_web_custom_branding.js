odoo.define('max_web_custom_branding.system_name', function (require) {
    "use strict";

    var Model = require('web.Model');
    var WebClient = require('web.WebClient');
    var core = require('web.core');
    var _t = core._t;

    WebClient.include({
        init: function(parent, action, options) {
            this._super.apply(this, arguments);
            var self = this;
            var params = new Model("ir.config_parameter");
            params.call('get_param', ['max_web_custom_branding.system_name']).then(function(system_name) {
                self.set('title_part', {"zopenerp": system_name || ''});
            });
        }
    });
})
