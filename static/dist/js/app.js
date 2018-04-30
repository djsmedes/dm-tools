(function() {
  'use strict';

  var globals = typeof global === 'undefined' ? self : global;
  if (typeof globals.require === 'function') return;

  var modules = {};
  var cache = {};
  var aliases = {};
  var has = {}.hasOwnProperty;

  var expRe = /^\.\.?(\/|$)/;
  var expand = function(root, name) {
    var results = [], part;
    var parts = (expRe.test(name) ? root + '/' + name : name).split('/');
    for (var i = 0, length = parts.length; i < length; i++) {
      part = parts[i];
      if (part === '..') {
        results.pop();
      } else if (part !== '.' && part !== '') {
        results.push(part);
      }
    }
    return results.join('/');
  };

  var dirname = function(path) {
    return path.split('/').slice(0, -1).join('/');
  };

  var localRequire = function(path) {
    return function expanded(name) {
      var absolute = expand(dirname(path), name);
      return globals.require(absolute, path);
    };
  };

  var initModule = function(name, definition) {
    var hot = hmr && hmr.createHot(name);
    var module = {id: name, exports: {}, hot: hot};
    cache[name] = module;
    definition(module.exports, localRequire(name), module);
    return module.exports;
  };

  var expandAlias = function(name) {
    return aliases[name] ? expandAlias(aliases[name]) : name;
  };

  var _resolve = function(name, dep) {
    return expandAlias(expand(dirname(name), dep));
  };

  var require = function(name, loaderPath) {
    if (loaderPath == null) loaderPath = '/';
    var path = expandAlias(name);

    if (has.call(cache, path)) return cache[path].exports;
    if (has.call(modules, path)) return initModule(path, modules[path]);

    throw new Error("Cannot find module '" + name + "' from '" + loaderPath + "'");
  };

  require.alias = function(from, to) {
    aliases[to] = from;
  };

  var extRe = /\.[^.\/]+$/;
  var indexRe = /\/index(\.[^\/]+)?$/;
  var addExtensions = function(bundle) {
    if (extRe.test(bundle)) {
      var alias = bundle.replace(extRe, '');
      if (!has.call(aliases, alias) || aliases[alias].replace(extRe, '') === alias + '/index') {
        aliases[alias] = bundle;
      }
    }

    if (indexRe.test(bundle)) {
      var iAlias = bundle.replace(indexRe, '');
      if (!has.call(aliases, iAlias)) {
        aliases[iAlias] = bundle;
      }
    }
  };

  require.register = require.define = function(bundle, fn) {
    if (bundle && typeof bundle === 'object') {
      for (var key in bundle) {
        if (has.call(bundle, key)) {
          require.register(key, bundle[key]);
        }
      }
    } else {
      modules[bundle] = fn;
      delete cache[bundle];
      addExtensions(bundle);
    }
  };

  require.list = function() {
    var list = [];
    for (var item in modules) {
      if (has.call(modules, item)) {
        list.push(item);
      }
    }
    return list;
  };

  var hmr = globals._hmr && new globals._hmr(_resolve, require, modules, cache);
  require._cache = cache;
  require.hmr = hmr && hmr.wrap;
  require.brunch = true;
  globals.require = require;
})();

(function() {
var global = typeof window === 'undefined' ? this : window;
var process;
var __makeRelativeRequire = function(require, mappings, pref) {
  var none = {};
  var tryReq = function(name, pref) {
    var val;
    try {
      val = require(pref + '/node_modules/' + name);
      return val;
    } catch (e) {
      if (e.toString().indexOf('Cannot find module') === -1) {
        throw e;
      }

      if (pref.indexOf('node_modules') !== -1) {
        var s = pref.split('/');
        var i = s.lastIndexOf('node_modules');
        var newPref = s.slice(0, i).join('/');
        return tryReq(name, newPref);
      }
    }
    return none;
  };
  return function(name) {
    if (name in mappings) name = mappings[name];
    if (!name) return;
    if (name[0] !== '.' && pref) {
      var val = tryReq(name, pref);
      if (val !== none) return val;
    }
    return require(name);
  }
};
require.register("js/clickable_row.js", function(exports, require, module) {
"use strict";

module.exports = {

    initialize: function initialize() {
        $('.clickable-row').click(function () {
            window.location = $(this).data("href");
        });
    }

};
});

require.register("js/homepagescripts.js", function(exports, require, module) {
"use strict";

module.exports = {

    initialize: function initialize() {
        var body = $('body');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
            );
        }

        var csrftoken = $("[name=csrfmiddlewaretoken]").val();

        $.ajaxSetup({
            beforeSend: function beforeSend(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $('#display-only-toggle-button').click(function () {
            body.toggleClass('context-display-only');
            $(this).toggleClass('text-muted');
        });

        body.on('click', '.combatant-context-enter', function () {
            var combatant = $(this).data('combatant');
            body.addClass('context-combatant').data('combatant', combatant);
            label_matched_combatants();
        });
        body.on('click', '.combatant-context-leave', function () {
            body.removeClass('context-combatant').data('combatant', '');
            $('.context-combatant-match').each(function () {
                $(this).removeClass('context-combatant-match');
            });
        });

        $('.enter-apply-context').click(function () {
            var which_context_type = $(this).data('apply-effect-type');
            body.addClass('context-apply').data('apply-effect-type', which_context_type);
        });

        $('.exit-apply-context').click(exit_apply_context);

        $('#effect-to-apply').on("change paste keyup", function () {
            var myval = $(this).val();
            var active_combatant_buttons = $('.context-activatable.active');
            if (myval === '') {
                $('#apply-button').prop('disabled', true);
            } else if (active_combatant_buttons.length) {
                $('#apply-button').prop('disabled', false);
            }
            active_combatant_buttons.each(function () {
                var combatant = $(this).data('combatant');
                $('#' + combatant + '-' + body.data('apply-effect-type')).val(myval);
            });
        });

        var effect_add_form = $('#effect-add-form');
        effect_add_form.submit(function () {
            $.ajax({
                type: effect_add_form.attr('method'),
                url: effect_add_form.attr('action'),
                data: effect_add_form.serialize(),
                success: function success(data) {
                    $(".combatant-card-body").each(function () {
                        // todo change combatant card body data-id to data-combatant
                        var id = $(this).data('id');
                        $(this).html(data[id]);
                    });
                }
            });
            exit_apply_context();
            $('#effect-to-apply').val('');
            return false;
        });

        body.on('click', '.remove-effect', function () {
            var index = $(this).data('index');
            var effect_type = $(this).data('effect-type');
            var combatant_id = $(this).data('combatant');

            $.ajax({
                type: 'post',
                url: '/ajax/remove-effect/',
                data: {
                    'index': index,
                    'effect_type': effect_type,
                    'combatant': combatant_id
                },
                success: function success(return_html) {
                    if (return_html === '') {
                        return;
                    }
                    $(".combatant-card-body").each(function () {
                        if ($(this).data('id') === combatant_id) {
                            $(this).html(return_html);
                        }
                    });
                }
            });
        });

        body.on('click', '#enter-remove-context', function () {
            body.addClass('context-remove');
        });

        var remove_combatants_form = $('#remove-combatants-form');
        remove_combatants_form.submit(function () {
            $.ajax({
                type: remove_combatants_form.attr('method'),
                url: remove_combatants_form.attr('action'),
                data: remove_combatants_form.serialize(),
                success: function success(return_html) {
                    if (return_html === '') {
                        return;
                    }
                    $('#combatant-card-deck').html(return_html);
                    label_matched_combatants();
                }
            });
            exit_remove_context();
            return false;
        });

        body.on('click', '.context-activatable', function () {
            $(this).toggleClass('active');
            var combatant = $(this).data('combatant');
            if (body.hasClass('context-remove')) {
                var combatant_to_remove_selector = $("#combatant-to-remove-" + combatant);
                if ($(this).hasClass('active')) {
                    combatant_to_remove_selector.val('True');
                } else {
                    combatant_to_remove_selector.val('');
                }
                if ($('.context-activatable.active').length) {
                    $('#confirm-remove-combatants-button').prop('disabled', false);
                } else {
                    $('#confirm-remove-combatants-button').prop('disabled', true);
                }
            }
            if (body.hasClass('context-apply')) {
                var effect = '';
                var effect_to_apply = $('#effect-to-apply').val();
                var apply_effect_type = body.data('apply-effect-type');
                if ($(this).hasClass('active')) {
                    effect = effect_to_apply;
                }
                $('#' + combatant + '-' + apply_effect_type).val(effect);
                if (effect_to_apply !== '') {
                    if ($('.context-activatable.active').length) {
                        $('#apply-button').prop('disabled', false);
                    } else {
                        $('#apply-button').prop('disabled', true);
                    }
                }
            }
        });

        body.on('click', '#cancel-remove', exit_remove_context);

        body.on('submit', '.update-initiative-form', function () {
            $.ajax({
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                data: $(this).serialize(),
                success: function success(return_html) {
                    if (return_html === '') {
                        return;
                    }
                    $("#combatant-card-deck").html(return_html);
                    label_matched_combatants();
                }
            });
            return false;
        });
        var last_updated = new Date().getTime();
        setTimeout(function () {
            poll_server(last_updated);
        }, 2500);
    }
};

function exit_apply_context() {
    $('body').removeClass('context-apply');
    $('.effect-input').val('');
    $('.context-activatable').removeClass('active');
    $('#apply-button').prop('disabled', true);
}

function exit_remove_context() {
    $('body').removeClass('context-remove');
    $('.combatant-to-remove').val('');
    $('.context-activatable').removeClass('active');
    $('#confirm-remove-combatants-button').prop('disabled', true);
}

function poll_server(last_updated) {
    $.ajax({
        type: 'get',
        url: '/ajax/poll/',
        data: {
            last_updated: last_updated
        },
        success: function success(return_data) {
            if (return_data.needs_update) {
                update_all_combatants();
                last_updated = new Date().getTime();
            }
        },
        complete: function complete(data) {
            setTimeout(function () {
                poll_server(last_updated);
            }, 2500);
        }
    });
}

function update_all_combatants() {
    var url = '/ajax/update-all-combatants/';
    $.ajax({
        type: 'post',
        url: url,
        data: {},
        success: function success(return_html) {
            if (return_html === '') {
                return;
            }
            $("#combatant-card-deck").html(return_html);
            label_matched_combatants();
        }
    });
}

function label_matched_combatants() {
    var body = $('body');
    if (body.hasClass('context-combatant')) {
        var combatant = body.data('combatant');
        if (combatant) {
            $('.combatant-context-match-hide, .combatant-context-unmatch-hide').each(function () {
                if ($(this).data('combatant') === combatant) {
                    $(this).addClass('context-combatant-match');
                }
            });
        }
    }
}
});

;require.register("js/initialize.js", function(exports, require, module) {
'use strict';

document.addEventListener('DOMContentLoaded', function () {
    // setup?
    console.log('Initialized app');
});
});

require.register("js/places-vue/components/Canvas.vue", function(exports, require, module) {
;(function(){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _axios = require('axios');

var _axios2 = _interopRequireDefault(_axios);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

_axios2.default.defaults.xsrfCookieName = 'csrftoken';
_axios2.default.defaults.xsrfHeaderName = 'X-CSRFToken';

exports.default = {
    data: function data() {
        return {
            shapes: []
        };
    },

    methods: {
        load_shapes: function load_shapes() {
            var _this = this;

            _axios2.default.get('/places/api/get-place-data/').then(function (r) {
                _this.shapes = r.data.shape_set;
            }).catch(function (e) {
                console.log(e);
            });
        },
        test_method: function test_method(event) {
            var bound = document.getElementById('place-canvas').getBoundingClientRect();
            var html = document.documentElement;
            var left = bound.left + window.pageXOffset - html.clientLeft;
            var top = bound.top + window.pageYOffset - html.clientTop;
            var x = event.pageX - left;
            var y = event.pageY - top;
            console.log(x, y);
        }
    },
    created: function created() {
        this.load_shapes();
    }
};
})()
if (module.exports.__esModule) module.exports = module.exports.default
var __vue__options__ = (typeof module.exports === "function"? module.exports.options: module.exports)
if (__vue__options__.functional) {console.error("[vueify] functional components are not supported and should be defined in plain js files using render functions.")}
__vue__options__.render = function render () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('div',{staticClass:"ml-5 p-0",staticStyle:{"width":"1200px","height":"900px"}},[_c('svg',{attrs:{"id":"place-canvas","width":"1200","height":"900"}},[_c('defs',[_c('filter',{attrs:{"id":"innershadow"}},[_c('feGaussianBlur',{attrs:{"in":"SourceGraphic","stdDeviation":"10","result":"blur"}}),_vm._v(" "),_c('feComposite',{attrs:{"in2":"SourceGraphic","operator":"arithmetic","k2":"-1","k3":"1","result":"shadowDiff"}})],1)]),_vm._v(" "),_vm._l((_vm.shapes),function(shape){return _c('g',[_c('polygon',{attrs:{"points":shape.points,"stroke":"green","fill":"green","stroke-width":"2","filter":"url(#innershadow)"}}),_vm._v(" "),_c('polygon',{attrs:{"points":shape.points,"fill":"transparent","stroke":"green","stroke-width":"2"}})])}),_vm._v(" "),_c('rect',{attrs:{"width":"1200","height":"900","fill":"transparent","stroke":"black","stroke-width":"2"},on:{"click":function($event){_vm.test_method($event)}}})],2)])}
__vue__options__.staticRenderFns = []
if (module.hot) {(function () {  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), true)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-43273a22", __vue__options__)
  } else {
    hotAPI.reload("data-v-43273a22", __vue__options__)
  }
})()}
});

;require.register("js/places-vue/main.js", function(exports, require, module) {
'use strict';

var _axios = require('axios');

var _axios2 = _interopRequireDefault(_axios);

var _vue = require('vue');

var _vue2 = _interopRequireDefault(_vue);

var _Canvas = require('./components/Canvas.vue');

var _Canvas2 = _interopRequireDefault(_Canvas);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

new _vue2.default({
    el: '#canvas',
    render: function render(h) {
        return h(_Canvas2.default);
    }
});
});

require.alias("process/browser.js", "process");process = require('process');require.register("___globals___", function(exports, require, module) {
  

// Auto-loaded modules from config.npm.globals.
window["$"] = require("jquery");
window.jQuery = require("jquery");
window.bootstrap = require("bootstrap");


});})();require('___globals___');


//# sourceMappingURL=app.js.map