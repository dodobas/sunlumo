'use strict';

// global events
var EVENTS = require('../events');

var UI_Button = require('./button');

var DistanceTool = function(options) {
    this.options = {
        // initial module options
    };

    // override and extend default options
    for (var opt in options) {
        if (options.hasOwnProperty(opt)) {
            this.options[opt] = options[opt];
        }
    }

    this.init();

    return {
        controller: this.controller,
        view: this.view
    };
};

DistanceTool.prototype = {

    init: function() {
        var self = this;
        // this.controller = new Controller(this.options);
        // this.view = View;

        var button = new UI_Button({
            'name': 'AreaTool',
            'style': 'i.fa.fa-arrows'
        });

        this.controller = button.controller;
        this.view = button.view;

        button.controller.vm.events.on('button.activated', function () {
            EVENTS.emit('control.AreaTool.activate');
        });
        button.controller.vm.events.on('button.deactivated', function () {
            EVENTS.emit('control.AreaTool.deactivate');
        });
    }
};

module.exports = DistanceTool;