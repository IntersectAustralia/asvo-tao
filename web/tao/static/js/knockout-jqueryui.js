/*! knockout-jqueryui - v0.5.2 - 9/20/2013
* https://github.com/gvas/knockout-jqueryui
* Copyright (c) 2013 Vas Gabor <gvas.munka@gmail.com>; Licensed MIT */
/*global require, define, exports*/
/*jslint browser:true, maxlen:256*/

/****************************************************/
/*** Adapted by Intersect from above github project */
/****************************************************/

// TODO !!!
// spinner was renamed here spinnerx to avoid conflict with our own
// binding. We can use this library

(function (root, factory) {
    'use strict';

    if (typeof exports === 'object') {
        // CommonJS
        factory(exports, require('jquery'), require('knockout'), require('jquery-ui'));
    } else if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['exports', 'jquery', 'knockout', 'jquery-ui'], factory);
    } else {
        // Browser globals
        factory((root.kojqui = {}), root.jQuery, root.ko);
    }
} (this, function (exports, $, ko) {
    'use strict';

    var versions, bindingFactory;
    versions = (function () {
        
    
        var getMajorMinorVersion, jQuery, jQueryUI, knockout;
    
        getMajorMinorVersion = function (version) {
            /// <summary>Returns the major.minor version from the version string.</summary>
            /// <param name='version' type='String'></param>
            /// <returns type='String'></returns>
    
            var match = (version || '').match(/^(\d\.\d+)\.\d+$/);
    
            return match ? match[1] : null;
        };
    
        jQuery = $ && $.fn ? getMajorMinorVersion($.fn.jquery) : null;
        jQueryUI = $ && $.ui ? getMajorMinorVersion($.ui.version) : null;
        knockout = ko ? getMajorMinorVersion(ko.version) : null;
    
        return {
            jQuery: jQuery,
            jQueryUI: jQueryUI,
            knockout: knockout
        };
    }());

    (function () {
        
    
        // dependency checks
        if (!versions.jQuery) {
            throw new Error('jQuery must be loaded before knockout-jquery.');
        }
        if (!versions.jQueryUI) {
            throw new Error('jQuery UI must be loaded before knockout-jquery.');
        }
        if (!versions.knockout) {
            throw new Error('knockout must be loaded before knockout-jquery.');
        }
    
        if (versions.jQueryUI !== '1.8' && versions.jQueryUI !== '1.9' && versions.jQueryUI !== '1.10') {
            throw new Error('This version of the jQuery UI library is not supported.');
        }
    
        if (versions.knockout !== '2.2' && versions.knockout !== '2.3' && versions.knockout !== '3.0') {
            throw new Error('This version of the knockout library is not supported.');
        }
    }());

    bindingFactory = (function () {
        
    
        var filterProperties, unwrapProperties, setOption, subscribeToObservableOptions, subscribeToRefreshOn,
            create;
    
        filterProperties = function (source, properties) {
            /// <summary>Filters the properties of an object.</summary>
            /// <param name='source' type='Object'></param>
            /// <param name='properties' type='Array' elementType='String'></param>
            /// <returns type='Object'>A new object with the specified properties copied from source.</returns>
    
            var result = {};
    
            ko.utils.arrayForEach(properties, function (property) {
                if (source[property] !== undefined) {
                    result[property] = source[property];
                }
            });
    
            return result;
        };
    
        unwrapProperties = function (obj) {
            /// <summary>Returns a new object with obj's unwrapped properties.</summary>
            /// <param name='obj' type='Object'></param>
            /// <returns type='Object'></returns>
    
            var result, prop;
    
            result = {};
    
            for (prop in obj) {
                if (obj.hasOwnProperty(prop)) {
                    if (ko.isObservable(obj[prop])) {
                        result[prop] = obj[prop].peek();
                    } else {
                        result[prop] = obj[prop];
                    }
                }
            }
    
            return result;
        };
    
        setOption = function (widgetName, element, optionName, observableOrValue) {
            /// <summary>Sets an option on the widget.</summary>
            /// <param name='widgetName' type='String'>The widget's name.</param>
            /// <param name='element' type='DOMNode'></param>
            /// <param name='optionName' type='String'>The option to set.</param>
            /// <param name='observableOrValue'>The option's value or an observable containing the value.</param>
    
            $(element)[widgetName]('option', optionName, ko.utils.unwrapObservable(observableOrValue));
        };
    
        subscribeToObservableOptions = function (widgetName, element, options) {
            /// <summary>Creates a subscription to each observable option.</summary>
            /// <param name='widgetName' type='String'>The widget's name.</param>
            /// <param name='element' type='DOMNode'></param>
            /// <param name='options' type='Array'></param>
    
            var prop;
    
            for (prop in options) {
                if (options.hasOwnProperty(prop) && ko.isObservable(options[prop])) {
                    ko.computed({
                        // moved to a separate function to make jslint happy
                        read: setOption.bind(this, widgetName, element, prop, options[prop]),
                        disposeWhenNodeIsRemoved: element
                    });
                }
            }
        };
    
        subscribeToRefreshOn = function (widgetName, element, bindingValue) {
            /// <summary>Creates a subscription to the refreshOn observable.</summary>
            /// <param name='widgetName' type='String'>The widget's name.</param>
            /// <param name='element' type='DOMNode'></param>
            /// <param name='bindingValue' type='Object'></param>
    
            if (ko.isObservable(bindingValue.refreshOn)) {
                ko.computed({
                    read: function () {
                        bindingValue.refreshOn();
                        $(element)[widgetName]('refresh');
                    },
                    disposeWhenNodeIsRemoved: element
                });
            }
        };
    
        create = function (options) {
            /// <summary>Creates a new binding.</summary>
            /// <param name='options' type='Object'></param>
    
            var widgetName, init;
    
            widgetName = options.name;
    
            // skip missing widgets
            if ($.fn[widgetName]) {
                /*jslint unparam:true*/
                init = function (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
    
                    var flag, value, widgetOptions, widgetEvents, unwrappedOptions, unwrappedEvents;
    
                    // prevent multiple inits
                    flag = 'ko_' + widgetName + '_initialized';
                    if (!element[flag]) {
    
                        value = valueAccessor();
                        widgetOptions = filterProperties(value, options.options);
                        widgetEvents = filterProperties(value, options.events);
    
                        // execute the provided callback before the widget initialization
                        if (options.preInit) {
                            options.preInit.apply(this, arguments);
                        }
    
                        // allow inner elements' bindings to finish before initializing the widget
                        ko.applyBindingsToDescendants(bindingContext, element);
    
                        // bind the widget events to the viewmodel
                        unwrappedEvents = unwrapProperties(widgetEvents);
                        $.each(unwrappedEvents, function (key, value) {
                            unwrappedEvents[key] = value.bind(viewModel);
                        });
    
                        // initialize the widget
                        unwrappedOptions = unwrapProperties(widgetOptions);
                        $(element)[widgetName](ko.utils.extend(unwrappedOptions, unwrappedEvents));
    
                        subscribeToObservableOptions(widgetName, element, widgetOptions);
    
                        if (options.hasRefresh) {
                            subscribeToRefreshOn(widgetName, element, value);
                        }
    
                        // store the widget instance in the widget observable
                        if (ko.isWriteableObservable(value.widget)) {
                            value.widget($(element));
                        }
    
                        // handle disposal
                        ko.utils.domNodeDisposal.addDisposeCallback(element, function () {
                            $(element)[widgetName]('destroy');
                            element[flag] = null;
                        });
    
                        // execute the provided callback after the widget initialization
                        if (options.postInit) {
                            options.postInit.apply(this, arguments);
                        }
    
                        element[flag] = true;
                    }
    
                    // the inner elements have already been taken care of
                    return { controlsDescendantBindings: true };
                };
                /*jslint unparam:false*/
    
                ko.bindingHandlers[widgetName] = {
                    init: init
                };
            }
        };
    
        return {
            create: create
        };
    }());

    (function () {
        
    
        var postInit;
    
        postInit = function (element, valueAccessor) {
            /// <summary>Keeps the value binding property in sync with the spinner's value.
            /// </summary>
            /// <param name='element' type='DOMNode'></param>
            /// <param name='valueAccessor' type='Function'></param>
    
            var value = valueAccessor();
    
            if (value.value) {
                ko.computed({
                    read: function () {
                        $(element).spinner('value', ko.utils.unwrapObservable(value.value));
                    },
                    disposeWhenNodeIsRemoved: element
                });
            }
    
            if (ko.isWriteableObservable(value.value)) {
                $(element).on('spinchange.ko', function () {
                    value.value($(element).spinner('value'));
                });
            }
    
            //handle disposal
            ko.utils.domNodeDisposal.addDisposeCallback(element, function () {
                $(element).off('.ko');
            });
        };
    
        bindingFactory.create({
            name: 'spinnerx',
            options: ['culture', 'disabled', 'icons', 'incremental', 'max', 'min',
                'numberFormat', 'page', 'step'],
            events: ['create', 'start', 'spin', 'stop', 'change'],
            postInit: postInit
        });
    } ());

    (function () {
        var postInit;

        postInit = function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
            /// <summary>Ensures the width and height are sync-ed
            /// </summary>

            var options, flag, $e;

            options = valueAccessor();
            flag = 'ko_resizable_size';
            if (options.name) {
                flag += '_' + options.name;
            }
            $e = $(element);

            if (!bindingContext.$data[flag]) {
                bindingContext.$data[flag] = {width:$e.css('width'), height:$e.css('height')};
            }

            if (!element[flag]) {
                var dims = bindingContext.$data[flag];
                $e.css('width', dims.width);
                $e.css('height', dims.height);
                $e.on('resize', function(event, ui){
                    bindingContext.$data[flag] = ui.size;
                });
                element[flag] = true;
            }

        };

        bindingFactory.create({
            name: 'resizable',
            options: ['alsoResize', 'animate', 'aspectRatio', 'autoHide', 'cancel', 'containment',
                      'delay', 'disabled', 'distance', 'ghost', 'grid', 'handles', 'helper', 'maxHeight',
                      'maxWidth', 'minWidth', 'minHeight'],
            events: ['create', 'resize', 'start', 'stop'],
            postInit: postInit,
            hasRefresh: false
        });
    }());
        // make the binding factory accessible for the tests
    ko.jqui = {
        bindingFactory: bindingFactory
    };
    exports.version = '0.5.2';
}));