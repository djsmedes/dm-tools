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
    $('.clickable-row').click(function () {
        window.location = $(this).data("href");
    });

    require('js/vue/main.js');
});
});

require.register("js/vue/components/combo_detail_place.vue", function(exports, require, module) {
;(function(){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.default = {
    props: {
        model_name: '',
        model_name_plural: '',
        object_json: null
    },
    data: function data() {
        return {};
    },

    computed: {
        object: function object() {
            return this.$store.state.model;
        }
    },
    watch: {},
    methods: {},
    created: function created() {
        if (this.object_json) {
            this.$store.commit('set_model', JSON.parse(this.object_json));
        }
    }
};
})()
if (module.exports.__esModule) module.exports = module.exports.default
var __vue__options__ = (typeof module.exports === "function"? module.exports.options: module.exports)
if (__vue__options__.functional) {console.error("[vueify] functional components are not supported and should be defined in plain js files using render functions.")}
__vue__options__.render = function render () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('div',[(_vm.object)?_c('div',{staticClass:"card"},[_c('h3',{staticClass:"card-header bg-dark text-white"},[_vm._v("\n    "+_vm._s(_vm.object.name)+"\n  ")]),_vm._v(" "),_c('div',{staticClass:"card-body"},[_vm._v("\n    "+_vm._s(_vm.object.description)+"\n  ")]),_vm._v(" "),_c('div',{staticClass:"card-footer"},[_vm._v("\n    Some footer text\n  ")])]):_vm._e()])}
__vue__options__.staticRenderFns = []
if (module.hot) {(function () {  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), true)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-98f0227c", __vue__options__)
  } else {
    hotAPI.rerender("data-v-98f0227c", __vue__options__)
  }
})()}
});

;require.register("js/vue/components/combo_list.vue", function(exports, require, module) {
;(function(){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _lodash = require('lodash');

var _lodash2 = _interopRequireDefault(_lodash);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

exports.default = {
    props: {
        model_name: '',
        model_name_plural: '',
        object_list_json: null
    },
    data: function data() {
        return {
            search_bar: ''
        };
    },

    computed: {
        object_list: function object_list() {
            return this.$store.state.model_list;
        },
        sorted_object_list: function sorted_object_list() {
            if (this.object_list) {
                return _lodash2.default.sortBy(this.object_list, function (model) {
                    return model.name;
                });
            } else return [];
        },
        sorted_and_filtered_object_list: function sorted_and_filtered_object_list() {
            var _this = this;

            if (this.sorted_object_list) {
                return this.sorted_object_list.filter(function (model) {
                    return model.name.toLowerCase().includes(_this.search_bar.toLowerCase());
                });
            } else return [];
        }
    },
    watch: {},
    methods: {
        set_object: function set_object(id) {
            this.$store.dispatch('get_model', id);
        },
        is_active: function is_active(id) {
            if (!this.$store.state.model) return false;
            return id === this.$store.state.model.id;
        }
    },
    created: function created() {
        if (this.object_list_json) {
            this.$store.commit('set_model_list', JSON.parse(this.object_list_json));
        } else {
            this.$store.dispatch('get_model_list');
        }
    }
};
})()
if (module.exports.__esModule) module.exports = module.exports.default
var __vue__options__ = (typeof module.exports === "function"? module.exports.options: module.exports)
if (__vue__options__.functional) {console.error("[vueify] functional components are not supported and should be defined in plain js files using render functions.")}
__vue__options__.render = function render () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('div',[_c('div',{staticClass:"mb-1 form-group bg-secondary text-white rounded py-2 px-3"},[_c('label',{attrs:{"for":"combo-list-filter"}},[_vm._v("Filter")]),_vm._v(" "),_c('input',{directives:[{name:"model",rawName:"v-model",value:(_vm.search_bar),expression:"search_bar"}],staticClass:"form-control",attrs:{"id":"combo-list-filter"},domProps:{"value":(_vm.search_bar)},on:{"input":function($event){if($event.target.composing){ return; }_vm.search_bar=$event.target.value}}})]),_vm._v(" "),_c('div',{staticClass:"card"},[_c('div',{staticClass:"card-header bg-dark text-white",staticStyle:{"text-transform":"capitalize"}},[_c('h3',[_vm._v(_vm._s(_vm.model_name_plural))])]),_vm._v(" "),_c('div',{staticStyle:{"max-height":"500px","overflow-y":"auto"}},[_c('div',{staticClass:"list-group list-group-flush"},_vm._l((_vm.sorted_and_filtered_object_list),function(object){return _c('button',{staticClass:"list-group-item list-group-item-action",class:_vm.is_active(object.id) ? 'active' : '',on:{"click":function($event){_vm.set_object(object.id)}}},[_vm._v("\n          "+_vm._s(object.name)+"\n        ")])}))]),_vm._v(" "),_c('div',{staticClass:"card-footer"},[_c('button',{staticClass:"btn btn-outline-primary"},[_vm._v("Add a new "+_vm._s(_vm.model_name))])])])])}
__vue__options__.staticRenderFns = []
if (module.hot) {(function () {  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), true)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-7799bb72", __vue__options__)
  } else {
    hotAPI.rerender("data-v-7799bb72", __vue__options__)
  }
})()}
});

;require.register("js/vue/components/place_canvas.vue", function(exports, require, module) {
;(function(){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _axios = require('axios');

var _axios2 = _interopRequireDefault(_axios);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

exports.default = {
    props: {
        place_list_json: null
    },
    data: function data() {
        return {
            temp_points: [],
            temp_type: null,
            hovering_enabled: true,
            selected_place_edits: null,
            place_types: {
                200: 'misc region',
                201: 'geological',
                202: 'vegetation',
                203: 'water',
                204: 'political',
                100: 'misc line',
                101: 'road',
                102: 'river',
                0: 'misc point',
                1: 'settlement',
                2: 'natural',
                3: 'dungeon'
            },
            editing: null,
            mousedown_on_temp_point: false,
            mouse_moving_on_temp_point: false
        };
    },

    computed: {
        no_temp_points_selected: function no_temp_points_selected() {
            for (var i = 0; i < this.temp_points.length; i++) {
                if (this.temp_points[i].selected) {
                    return false;
                }
            }
            return true;
        },
        inclusion_distance: function inclusion_distance() {
            return this.$store.state.campaign.place_inclusion_distance;
        },
        selected_place: function selected_place() {
            return this.$store.state.model;
        },
        places: function places() {
            return this.$store.state.model_list;
        }
    },
    watch: {
        inclusion_distance: function inclusion_distance(new_dist, old_dist) {
            this.$store.state.refresh_model();
        }
    },
    methods: {
        get_click_coords: function get_click_coords(event) {
            var bound = document.getElementById('place-canvas').getBoundingClientRect();
            var html = document.documentElement;
            var left = bound.left + window.pageXOffset - html.clientLeft;
            var top = bound.top + window.pageYOffset - html.clientTop;
            var x = event.pageX - left;
            var y = event.pageY - top;
            return { x: x, y: y };
        },
        enter_create_place_context: function enter_create_place_context(context) {
            this.temp_type = context;
            this.hovering_enabled = false;
            this.selected_place = null;
        },
        exit_and_save_place: function exit_and_save_place() {
            var new_place = {
                name: 'new Place',
                points: this.temp_points,
                type: this.temp_type
            };
            this.$store.dispatch('add_model', new_place);
            this.exit_edit_place_context();
        },
        exit_edit_place_context: function exit_edit_place_context() {
            this.temp_points = [];
            this.temp_type = null;
            this.hovering_enabled = true;
        },
        generate_temp_point: function generate_temp_point(event) {
            if (this.mousedown_on_temp_point) return;
            if (this.temp_type) {
                var coords = this.get_click_coords(event);
                if (this.temp_type < 100) {
                    this.temp_points.pop();
                }
                this.temp_points.push(coords);
            }
        },
        points_to_pointstring: function points_to_pointstring(points_obj) {
            var pointstring = '';
            points_obj.forEach(function (point) {
                pointstring += point.x + ',' + point.y + ' ';
            });
            return pointstring;
        },
        place_clicked: function place_clicked(event) {
            if (this.temp_type) {
                return;
            }
            var place = $(event.target);
            if (place.hasClass('line-expander')) {
                place = place.next();
            }
            this.select_place(this.html_id_2_pk(place.attr('id')));
        },
        select_place: function select_place(pk) {
            if (this.selected_place && this.selected_place.id === pk) {
                this.selected_place = null;
            } else {
                this.$store.dispatch('get_model', pk);
            }
        },
        enter_edit_selected_place_context: function enter_edit_selected_place_context() {
            this.hovering_enabled = false;
            this.editing = this.selected_place.id;
            this.temp_type = this.selected_place.type;
            this.temp_points = JSON.parse(JSON.stringify(this.selected_place.points));
            this.selected_place_edits = JSON.parse(JSON.stringify(this.selected_place));
        },
        exit_and_save_selected_place: function exit_and_save_selected_place() {
            this.selected_place_edits.points = this.temp_points;
            this.$store.dispatch('change_model', this.selected_place_edits);
            this.exit_edit_context();
        },
        delete_selected_place: function delete_selected_place() {
            this.$store.dispatch('delete_model', this.selected_place.id);
            this.exit_edit_context();
        },
        exit_edit_context: function exit_edit_context() {
            this.editing = null;
            this.selected_place_edits = null;
            this.exit_edit_place_context();
        },
        have_same_dimensions: function have_same_dimensions(type1, type2) {
            return ~~(type1 / 100) === ~~(type2 / 100);
        },
        temp_point_mousedown: function temp_point_mousedown(event) {
            var id = parseInt(event.target.id.split('-')[2]);
            var $body = $('body');
            var parent = this;
            this.mousedown_on_temp_point = true;
            $body.on('mousemove click', function handler(event) {
                if (event.type === 'mousemove') {
                    var coords = parent.get_click_coords(event);
                    parent.temp_points[id].x = coords.x;
                    parent.temp_points[id].y = coords.y;
                    parent.mouse_moving_on_temp_point = true;
                } else {
                    $body.off('mousemove click', handler);
                    parent.mousedown_on_temp_point = false;
                    parent.mouse_moving_on_temp_point = false;
                }
            });
        },
        temp_point_click: function temp_point_click(event) {
            if (this.mouse_moving_on_temp_point) return;

            var $clicked = $(event.target);
            var id = parseInt($clicked.attr('id').split('-')[2]);
            if (this.temp_points[id].selected) {
                this.temp_points[id].selected = false;
            } else {
                this.$set(this.temp_points[id], 'selected', true);
            }
        },
        delete_temp_points: function delete_temp_points() {
            for (var i = this.temp_points.length - 1; i >= 0; i--) {
                if (this.temp_points[i].selected) {
                    this.temp_points.splice(i, 1);
                }
            }
        },
        html_id_2_pk: function html_id_2_pk(html_id) {
            return parseInt(html_id.split('-')[1]);
        },
        pk_2_html_id: function pk_2_html_id(pk) {
            return 'place-' + pk;
        },
        place_type_2_class: function place_type_2_class(type) {
            return 'place-type-' + type;
        },
        class_2_place_type: function class_2_place_type(cls) {
            return parseInt(cls.split('-')[2]);
        },
        is_active: function is_active(pk) {
            return this.selected_place && this.selected_place.id === pk;
        },
        toggle_type_visibility: function toggle_type_visibility(type) {
            $('.' + this.place_type_2_class(type)).toggleClass('d-none');
        }
    },
    created: function created() {
        if (this.place_list_json) {
            this.$store.commit('set_model_list', JSON.parse(this.place_list_json));
        } else {
            this.$store.dispatch('get_model_list');
        }
    }
};
})()
if (module.exports.__esModule) module.exports = module.exports.default
var __vue__options__ = (typeof module.exports === "function"? module.exports.options: module.exports)
if (__vue__options__.functional) {console.error("[vueify] functional components are not supported and should be defined in plain js files using render functions.")}
__vue__options__.render = function render () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('div',{staticClass:"m-0 p-0"},[_c('div',{staticClass:"row container-fluid px-5"},[_c('div',{staticClass:"col"},[(_vm.selected_place)?_c('div',{staticClass:"card"},[_c('div',{staticClass:"card-header bg-dark text-white"},[_c('div',{staticClass:"row form-inline"},[(! _vm.editing)?_c('h4',{staticClass:"col"},[_vm._v(_vm._s(_vm.selected_place.name))]):_c('label',[_vm._v("\n              Name: "),_c('input',{directives:[{name:"model",rawName:"v-model",value:(_vm.selected_place_edits.name),expression:"selected_place_edits.name"}],staticClass:"mx-1 col form-control",domProps:{"value":(_vm.selected_place_edits.name)},on:{"input":function($event){if($event.target.composing){ return; }_vm.$set(_vm.selected_place_edits, "name", $event.target.value)}}})]),_vm._v(" "),(! _vm.editing)?_c('button',{staticClass:"btn btn-outline-light col-auto ml-auto mr-1",on:{"click":_vm.enter_edit_selected_place_context}},[_vm._v("\n              Edit\n            ")]):_vm._e(),_vm._v(" "),(_vm.editing)?_c('button',{staticClass:"btn btn-danger col-auto ml-auto mr-1",attrs:{"data-toggle":"modal","data-target":"#confirm-delete-modal"}},[_vm._v("\n              Delete\n            ")]):_vm._e(),_vm._v(" "),(_vm.editing)?_c('button',{staticClass:"btn btn-secondary col-auto mr-1",on:{"click":_vm.exit_edit_context}},[_vm._v("\n              Cancel\n            ")]):_vm._e(),_vm._v(" "),(_vm.editing)?_c('button',{staticClass:"btn btn-success col-auto mr-1",on:{"click":_vm.exit_and_save_selected_place}},[_vm._v("\n              Save\n            ")]):_vm._e()])]),_vm._v(" "),_c('div',{staticClass:"card-body"},[(! _vm.editing)?[_vm._v(_vm._s(_vm.selected_place.description))]:[_c('label',{attrs:{"for":"selected-place-description"}},[_vm._v("Description: ")]),_vm._v(" "),_c('textarea',{directives:[{name:"model",rawName:"v-model",value:(_vm.selected_place_edits.description),expression:"selected_place_edits.description"}],staticClass:"form-control",attrs:{"id":"selected-place-description"},domProps:{"value":(_vm.selected_place_edits.description)},on:{"input":function($event){if($event.target.composing){ return; }_vm.$set(_vm.selected_place_edits, "description", $event.target.value)}}})]],2),_vm._v(" "),(! _vm.editing)?[_c('hr'),_vm._v(" "),_c('div',{staticClass:"card-body"},[_vm._v("\n            Nearby places:\n            "),_c('ul',{staticClass:"list-inline"},_vm._l((_vm.selected_place.nearby_places),function(place){return _c('li',{staticClass:"list-inline-item"},[_c('button',{staticClass:"btn btn-outline-dark",on:{"click":function($event){_vm.select_place(parseInt(place.id))}}},[_vm._v("\n                  "+_vm._s(place.name)+"\n                ")])])}))])]:_vm._e(),_vm._v(" "),_c('div',{staticClass:"card-footer"},[(! _vm.editing)?[_vm._v(_vm._s(_vm.place_types[_vm.selected_place.type]))]:[_c('label',{attrs:{"for":"selected-place-type"}},[_vm._v("Type: ")]),_vm._v(" "),_c('select',{directives:[{name:"model",rawName:"v-model",value:(_vm.selected_place_edits.type),expression:"selected_place_edits.type"}],staticClass:"form-control",attrs:{"id":"selected-place-type"},on:{"change":function($event){var $$selectedVal = Array.prototype.filter.call($event.target.options,function(o){return o.selected}).map(function(o){var val = "_value" in o ? o._value : o.value;return val}); _vm.$set(_vm.selected_place_edits, "type", $event.target.multiple ? $$selectedVal : $$selectedVal[0])}}},[_vm._l((_vm.place_types),function(name,type){return [(_vm.have_same_dimensions(type, _vm.selected_place.type))?_c('option',{domProps:{"value":type}},[_vm._v("\n                  "+_vm._s(name)+"\n                ")]):_vm._e()]})],2)]],2)],2):_vm._e()]),_vm._v(" "),_c('div',{staticClass:"col-auto ml-auto p-0"},[_c('svg',{staticClass:"rounded",attrs:{"id":"place-canvas"},on:{"click":function($event){_vm.generate_temp_point($event)}}},[_c('defs',[_c('filter',{attrs:{"id":"innershadow"}},[_c('feGaussianBlur',{attrs:{"in":"SourceGraphic","stdDeviation":"5","result":"blur"}}),_vm._v(" "),_c('feComposite',{attrs:{"in2":"SourceGraphic","operator":"arithmetic","k2":"-1","k3":"1","result":"shadowDiff"}})],1)]),_vm._v(" "),_vm._l((_vm.places),function(place){return [(place.id !== _vm.editing)?[(_vm.have_same_dimensions(place.type, 200))?_c('g',[_c('polygon',{class:_vm.place_type_2_class(place.type),attrs:{"points":_vm.points_to_pointstring(place.points),"filter":"url(#innershadow)"}}),_vm._v(" "),_c('polygon',{class:[{ 'hoverable-place': _vm.hovering_enabled},
                                _vm.is_active(place.id) ? 'active' : '',
                                'place-poly-outline',
                                _vm.place_type_2_class(place.type)],attrs:{"points":_vm.points_to_pointstring(place.points),"id":_vm.pk_2_html_id(place.id)},on:{"click":function($event){_vm.place_clicked($event)}}})]):(_vm.have_same_dimensions(place.type, 100))?_c('g',[_c('polyline',{class:['line-expander', _vm.place_type_2_class(place.type)],attrs:{"points":_vm.points_to_pointstring(place.points)},on:{"click":function($event){_vm.place_clicked($event)}}}),_vm._v(" "),_c('polyline',{class:[{ 'hoverable-place': _vm.hovering_enabled},
                           _vm.place_type_2_class(place.type),
                           _vm.is_active(place.id) ? 'active' : ''],attrs:{"points":_vm.points_to_pointstring(place.points),"id":_vm.pk_2_html_id(place.id)},on:{"click":function($event){_vm.place_clicked($event)}}})]):(_vm.have_same_dimensions(place.type, 0))?_vm._l((place.points),function(pt){return _c('circle',{class:[{ 'hoverable-place': _vm.hovering_enabled},
                             _vm.place_type_2_class(place.type),
                             _vm.is_active(place.id) ? 'active' : ''],attrs:{"cx":pt.x,"cy":pt.y,"r":"5","id":_vm.pk_2_html_id(place.id)},on:{"click":function($event){_vm.place_clicked($event)}}})}):_vm._e()]:_vm._e()]}),_vm._v(" "),(200 <= _vm.temp_type)?_c('g',[_c('polygon',{class:_vm.place_type_2_class(_vm.temp_type),attrs:{"points":_vm.points_to_pointstring(_vm.temp_points),"filter":"url(#innershadow)"}}),_vm._v(" "),_c('polygon',{class:['place-poly-outline',
                            _vm.place_type_2_class(_vm.temp_type)],attrs:{"points":_vm.points_to_pointstring(_vm.temp_points)}})]):(100 <= _vm.temp_type)?_c('polyline',{class:_vm.place_type_2_class(_vm.temp_type),attrs:{"points":_vm.points_to_pointstring(_vm.temp_points)}}):_vm._l((_vm.temp_points),function(pt){return _c('circle',{class:_vm.place_type_2_class(_vm.temp_type),attrs:{"cx":pt.x,"cy":pt.y,"r":"5"}})}),_vm._v(" "),_vm._l((_vm.temp_points),function(pt,index){return (100 <= _vm.temp_type)?_c('circle',{class:{ 'place-temp-point': true,
                        'hoverable-place': true,
                        active: pt.selected },attrs:{"id":'temp-circle-' + index,"cx":pt.x,"cy":pt.y,"r":"5"},on:{"mousedown":function($event){_vm.temp_point_mousedown($event)},"click":function($event){_vm.temp_point_click($event)}}}):_vm._e()})],2)]),_vm._v(" "),_c('div',{staticClass:"col-auto ml-2"},[(_vm.editing)?_c('div',{staticClass:"mb-1"},[_c('button',{class:['btn', 'btn-danger',
                         {'disabled': _vm.no_temp_points_selected}],on:{"click":_vm.delete_temp_points}},[_vm._v("\n          Delete point(s)\n        ")])]):_vm._e(),_vm._v(" "),(_vm.temp_type && !_vm.editing)?_c('div',{staticClass:"mb-1"},[_c('button',{staticClass:"btn btn-outline-success",on:{"click":_vm.exit_and_save_place}},[_vm._v("\n          Save\n        ")]),_vm._v(" "),_c('button',{staticClass:"btn btn-outline-danger",on:{"click":_vm.exit_edit_place_context}},[_vm._v("\n          Cancel\n        ")])]):_vm._e(),_vm._v(" "),_c('div',{staticClass:"card"},[_c('div',{staticClass:"card-header bg-dark text-white"},[_vm._v("\n          Key\n        ")]),_vm._v(" "),_c('ul',{staticClass:"list-group list-group-flush"},_vm._l((_vm.place_types),function(name,type){return _c('li',{staticClass:"list-group-item d-flex align-items-center px-3"},[_c('svg',{staticClass:"mr-1",attrs:{"width":"16","height":"16"}},[(type < 100)?_c('circle',{class:_vm.place_type_2_class(type),attrs:{"cx":"8","cy":"8","r":"5"}}):(type < 200)?_c('polyline',{class:_vm.place_type_2_class(type),attrs:{"points":"2,2 4,12 14,14"}}):_c('g',[_c('polygon',{class:_vm.place_type_2_class(type),attrs:{"points":"2,2 50,0 0,50","filter":"url(#innershadow)"}}),_vm._v(" "),_c('polygon',{class:['place-poly-outline', _vm.place_type_2_class(type)],attrs:{"points":"2,2 50,0 0,50"}})])]),_vm._v(" "),_c('span',{staticClass:"mr-1"},[_vm._v(_vm._s(name))]),_vm._v(" "),_c('button',{staticClass:"btn btn-sm btn-outline-dark ml-auto mr-1",staticStyle:{"position":"relative"},attrs:{"data-toggle":"button","aria-pressed":"false"},on:{"click":function($event){_vm.toggle_type_visibility(type)}}},[_c('svg',{staticStyle:{"position":"absolute","top":"7px","left":"8px"},attrs:{"width":"14","height":"14"}},[_c('polyline',{attrs:{"points":"14,0 0,14","stroke":"white","fill":"none","stroke-width":"2"}})]),_vm._v(" "),_c('span',{staticClass:"oi oi-eye",attrs:{"title":"visibility","aria-hidden":"true"}})]),_vm._v(" "),_c('button',{staticClass:"btn btn-sm btn-outline-dark",on:{"click":function($event){_vm.enter_create_place_context(type)}}},[_vm._v("+")])])}))])])]),_vm._v(" "),(_vm.selected_place && _vm.editing)?_c('div',{staticClass:"modal fade",attrs:{"id":"confirm-delete-modal","tabindex":"-1","role":"dialog","aria-labelledby":"confirm-delete-title","aria-hidden":"true"}},[_c('div',{staticClass:"modal-dialog modal-dialog-centered",attrs:{"role":"document"}},[_c('div',{staticClass:"modal-content"},[_vm._m(0),_vm._v(" "),_c('div',{staticClass:"modal-body"},[_vm._v("\n          Are you sure you want to delete "+_vm._s(_vm.selected_place.name)+"? This cannot be undone.\n        ")]),_vm._v(" "),_c('div',{staticClass:"modal-footer"},[_c('button',{staticClass:"btn btn-secondary",attrs:{"type":"button","data-dismiss":"modal"}},[_vm._v("Cancel")]),_vm._v(" "),_c('button',{staticClass:"btn btn-danger",attrs:{"type":"button","data-dismiss":"modal"},on:{"click":_vm.delete_selected_place}},[_vm._v("\n            Yes, delete "+_vm._s(_vm.selected_place.name)+"\n          ")])])])])]):_vm._e()])}
__vue__options__.staticRenderFns = [function render () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('div',{staticClass:"modal-header"},[_c('h5',{staticClass:"modal-title",attrs:{"id":"confirm-delete-title"}},[_vm._v("Confirm delete")]),_vm._v(" "),_c('button',{staticClass:"close",attrs:{"type":"button","data-dismiss":"modal","aria-label":"Close"}},[_c('span',{attrs:{"aria-hidden":"true"}},[_vm._v("×")])])])}]
if (module.hot) {(function () {  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), true)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-7661dca8", __vue__options__)
  } else {
    hotAPI.rerender("data-v-7661dca8", __vue__options__)
  }
})()}
});

;require.register("js/vue/components/place_inclusion_distance.vue", function(exports, require, module) {
;(function(){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.default = {
    data: function data() {
        return {};
    },

    computed: {
        inclusion_distance: {
            get: function get() {
                return this.$store.state.campaign.place_inclusion_distance;
            },
            set: function set(value) {
                this.$store.commit('set_place_inclusion_distance', value);
            }
        }
    },
    methods: {},
    created: function created() {}
};
})()
if (module.exports.__esModule) module.exports = module.exports.default
var __vue__options__ = (typeof module.exports === "function"? module.exports.options: module.exports)
if (__vue__options__.functional) {console.error("[vueify] functional components are not supported and should be defined in plain js files using render functions.")}
__vue__options__.render = function render () {var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('div',{staticClass:"form-group"},[_c('label',{staticClass:"dropdown-header",attrs:{"for":"navbar-inclusion-distance"}},[_vm._v("Inclusion distance")]),_vm._v(" "),_c('div',{staticClass:"px-4"},[_c('input',{directives:[{name:"model",rawName:"v-model",value:(_vm.inclusion_distance),expression:"inclusion_distance"}],staticClass:"form-control",attrs:{"id":"navbar-inclusion-distance","type":"number","min":"0"},domProps:{"value":(_vm.inclusion_distance)},on:{"input":function($event){if($event.target.composing){ return; }_vm.inclusion_distance=$event.target.value}}})])])}
__vue__options__.staticRenderFns = []
if (module.hot) {(function () {  var hotAPI = require("vue-hot-reload-api")
  hotAPI.install(require("vue"), true)
  if (!hotAPI.compatible) return
  module.hot.accept()
  if (!module.hot.data) {
    hotAPI.createRecord("data-v-82b131f0", __vue__options__)
  } else {
    hotAPI.rerender("data-v-82b131f0", __vue__options__)
  }
})()}
});

;require.register("js/vue/main.js", function(exports, require, module) {
'use strict';

var _axios = require('axios');

var _axios2 = _interopRequireDefault(_axios);

var _lodash = require('lodash');

var _lodash2 = _interopRequireDefault(_lodash);

var _vue = require('vue/dist/vue');

var _vue2 = _interopRequireDefault(_vue);

var _vuex = require('vuex');

var _vuex2 = _interopRequireDefault(_vuex);

var _place_canvas = require('./components/place_canvas');

var _place_canvas2 = _interopRequireDefault(_place_canvas);

var _place_inclusion_distance = require('./components/place_inclusion_distance');

var _place_inclusion_distance2 = _interopRequireDefault(_place_inclusion_distance);

var _combo_list = require('./components/combo_list');

var _combo_list2 = _interopRequireDefault(_combo_list);

var _combo_detail_place = require('./components/combo_detail_place');

var _combo_detail_place2 = _interopRequireDefault(_combo_detail_place);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

_vue2.default.use(_vuex2.default);

_vue2.default.component('place-canvas', require('./components/place_canvas'));
_vue2.default.component('place-inclusion-distance', require('./components/place_inclusion_distance'));
_vue2.default.component('combo-list', require('./components/combo_list'));
_vue2.default.component('combo-detail-place', require('./components/combo_detail_place'));

var components = { place_canvas: _place_canvas2.default, place_inclusion_distance: _place_inclusion_distance2.default, combo_list: _combo_list2.default, combo_detail_place: _combo_detail_place2.default };

_axios2.default.defaults.xsrfCookieName = 'csrftoken';
_axios2.default.defaults.xsrfHeaderName = 'X-CSRFToken';

var model_api_url = template_context.api_url;

var model_actions = {
    get_model: function get_model(context, id) {
        _axios2.default.get(id + '/', {
            baseURL: model_api_url,
            params: {
                inclusion_distance: context.state.campaign.place_inclusion_distance
            }
        }).then(function (r) {
            context.commit('set_model', r.data);
        }).catch(function (e) {
            console.log(e);
        });
    },
    get_model_list: function get_model_list(context) {
        _axios2.default.get('', {
            baseURL: model_api_url
        }).then(function (r) {
            context.commit('set_model_list', r.data);
        }).catch(function (e) {
            console.log(e);
        });
    },
    add_model: function add_model(context, model) {
        _axios2.default.post('', model, {
            baseURL: model_api_url
        }).then(function (_) {
            context.dispatch('get_model_list');
        }).catch(function (e) {
            console.log(e);
        });
    },
    change_model: function change_model(context, model) {
        var id = model.id;
        _axios2.default.post(id + '/', model, {
            baseURL: model_api_url
        }).then(function (_) {
            context.dispatch('get_model_list');
            context.dispatch('get_model', id);
        }).catch(function (e) {
            console.log(e);
        });
    },
    delete_model: function delete_model(context, id) {
        _axios2.default.delete(id + '/', {
            baseURL: model_api_url
        }).then(function (_) {
            context.dispatch('get_model_list');
            context.commit('set_model', null);
        }).catch(function (e) {
            console.log(e);
        });
    }
};

var model_mutators = {
    set_model: function set_model(state, new_data) {
        state.model = new_data;
    },
    set_model_list: function set_model_list(state, new_data) {
        state.model_list = new_data;
    }
};

var store = new _vuex2.default.Store({
    state: Object.assign({}, template_context, {
        model: null,
        model_list: null
    }),
    mutations: Object.assign({}, {
        set_place_inclusion_distance: function set_place_inclusion_distance(state, n) {
            state.campaign.place_inclusion_distance = n;
        }
    }, model_mutators),
    actions: model_actions
});

store.state.refresh_model = _lodash2.default.debounce(function () {
    if (!store.state.model) return;
    store.dispatch('get_model', store.state.model.id);
}, 300);

new _vue2.default({
    el: '#app',
    store: store,
    components: components
});
});

require.alias("buffer/index.js", "buffer");
require.alias("process/browser.js", "process");process = require('process');require.register("___globals___", function(exports, require, module) {
  

// Auto-loaded modules from config.npm.globals.
window["$"] = require("jquery");
window.jQuery = require("jquery");
window.bootstrap = require("bootstrap");


});})();require('___globals___');

require('js/initialize');
//# sourceMappingURL=app.js.map