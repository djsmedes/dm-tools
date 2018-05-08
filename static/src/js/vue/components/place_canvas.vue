<template>
  <div class="m-0 p-0">

    <div class="row container-fluid px-5">

      <div class="col">
        <div v-if="selected_place" class="card">
          <div class="card-header bg-dark text-white">
            <div class="row form-inline">
              <h4 class="col" v-if="! editing">{{ selected_place.name }}</h4>
              <label v-else>
                Name: <input v-model="selected_place_edits.name" class="mx-1 col form-control">
              </label>
              <button v-if="! editing" class="btn btn-outline-light col-auto ml-auto mr-1"
                      @click="enter_edit_selected_place_context">
                Edit
              </button>
              <button v-if="editing"
                      class="btn btn-danger col-auto ml-auto mr-1"
                      data-toggle="modal" data-target="#confirm-delete-modal">
                Delete
              </button>
              <button v-if="editing" class="btn btn-secondary col-auto mr-1" @click="exit_edit_context">
                Cancel
              </button>
              <button v-if="editing" class="btn btn-success col-auto mr-1" @click="exit_and_save_selected_place">
                Save
              </button>
            </div>
          </div>
          <div class="card-body">
            <template v-if="! editing">{{ selected_place.description }}</template>
            <template v-else>
              <label for="selected-place-description">Description: </label>
              <textarea v-model="selected_place_edits.description"
                        class="form-control"
                        id="selected-place-description"
              ></textarea>
            </template>
          </div>
          <template v-if="! editing">
            <hr>
            <div class="card-body">
              Nearby places:
              <ul class="list-inline">
                <li class="list-inline-item" v-for="place in selected_place.nearby_places">
                  <button class="btn btn-outline-dark"
                          @click="select_place(parseInt(place.id))">
                    {{ place.name }}
                  </button>
                </li>
              </ul>
            </div>
          </template>
          <div class="card-footer">
            <template v-if="! editing">{{ place_types[selected_place.type] }}</template>
            <template v-else>
              <label for="selected-place-type">Type: </label>
              <select id="selected-place-type" class="form-control" v-model="selected_place_edits.type">
                <template v-for="(name, type) in place_types">
                  <option v-if="have_same_dimensions(type, selected_place.type)" :value="type">
                    {{ name }}
                  </option>
                </template>
              </select>
            </template>
          </div>
        </div>
      </div>

      <div class="col-auto ml-auto p-0">

        <svg id="place-canvas" @click="generate_temp_point($event)">
          <defs>
            <filter id="innershadow">
              <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"></feGaussianBlur>
              <feComposite in2="SourceGraphic" operator="arithmetic" k2="-1" k3="1" result="shadowDiff"></feComposite>
            </filter>

          </defs>

          <template v-for="shape in shapes">
            <template v-if="shape.id !== editing">
              <g v-if="have_same_dimensions(shape.type, 200)">
                <polygon :points="points_to_pointstring(shape.points)"
                         :class="place_type_2_class(shape.type)"
                         filter="url(#innershadow)"></polygon>
                <polygon :points="points_to_pointstring(shape.points)"
                         :id="pk_2_html_id(shape.id)"
                         :class="[{ 'hoverable-place': hovering_enabled},
                                  is_active(shape.id) ? 'active' : '',
                                  'place-poly-outline',
                                  place_type_2_class(shape.type)]"
                         @click="place_clicked($event)"></polygon>
              </g>
              <g v-else-if="have_same_dimensions(shape.type, 100)">
                <polyline :points="points_to_pointstring(shape.points)"
                          :class="['line-expander', place_type_2_class(shape.type)]"
                          @click="place_clicked($event)"></polyline>
                <polyline
                    :points="points_to_pointstring(shape.points)"
                    :class="[{ 'hoverable-place': hovering_enabled},
                             place_type_2_class(shape.type),
                             is_active(shape.id) ? 'active' : '']"
                    :id="pk_2_html_id(shape.id)"
                    @click="place_clicked($event)"></polyline>
              </g>
              <circle v-else-if="have_same_dimensions(shape.type, 0)"
                      v-for="pt in shape.points"
                      :cx="pt.x" :cy="pt.y" r="5"
                      :id="pk_2_html_id(shape.id)"
                      :class="[{ 'hoverable-place': hovering_enabled},
                               place_type_2_class(shape.type),
                               is_active(shape.id) ? 'active' : '']"
                      @click="place_clicked($event)"></circle>
            </template>
          </template>

          <g v-if="200 <= temp_type">
            <polygon :points="points_to_pointstring(temp_points)"
                     :class="place_type_2_class(temp_type)"
                     filter="url(#innershadow)"></polygon>
            <polygon :points="points_to_pointstring(temp_points)"
                     :class="['place-poly-outline',
                              place_type_2_class(temp_type)]"></polygon>
          </g>
          <polyline v-else-if="100 <= temp_type" :points="points_to_pointstring(temp_points)"
                    :class="place_type_2_class(temp_type)"></polyline>
          <circle v-else v-for="pt in temp_points"
                  :cx="pt.x" :cy="pt.y" r="5"
                  :class="place_type_2_class(temp_type)"
          ></circle>
          <circle v-if="100 <= temp_type" v-for="(pt, index) in temp_points"
                  :id="'temp-circle-' + index"
                  :cx="pt.x" :cy="pt.y" r="5"
                  @mousedown="temp_point_mousedown($event)"
                  @click="temp_point_click($event)"
                  :class="{ 'place-temp-point': true,
                          'hoverable-place': true,
                          active: pt.selected }"></circle>
        </svg>

      </div>

      <div class="col-auto ml-2">
        <div v-if="editing" class="mb-1">
          <button :class="['btn', 'btn-danger',
                           {'disabled': no_temp_points_selected}]"
                  @click="delete_temp_points">
            Delete point(s)
          </button>
        </div>
        <div v-if="temp_type && !editing" class="mb-1">
          <button class="btn btn-outline-success"
                  @click="exit_and_save_shape">
            Save
          </button>
          <button class="btn btn-outline-danger"
                  @click="exit_edit_shape_context">
            Cancel
          </button>
        </div>
        <div class="card">
          <div class="card-header bg-dark text-white">
            Key
          </div>
          <ul class="list-group list-group-flush">
            <li v-for="(name, type) in place_types" class="list-group-item d-flex align-items-center px-3">
              <svg width="16" height="16" class="mr-1">
                <circle v-if="type < 100" cx="8" cy="8" r="5" :class="place_type_2_class(type)"></circle>
                <polyline v-else-if="type < 200" points="2,2 4,12 14,14" :class="place_type_2_class(type)"></polyline>
                <g v-else>
                  <polygon points="2,2 50,0 0,50" :class="place_type_2_class(type)"
                           filter="url(#innershadow)"></polygon>
                  <polygon points="2,2 50,0 0,50" :class="['place-poly-outline', place_type_2_class(type)]"></polygon>
                </g>
              </svg>
              <span class="mr-1">{{ name }}</span>
              <button class="btn btn-sm btn-outline-dark ml-auto mr-1"
                      data-toggle="button" aria-pressed="false"
                      style="position: relative;"
                      @click="toggle_type_visibility(type)">
                <svg width="14" height="14" style="position: absolute; top: 7px; left: 8px">
                  <polyline points="14,0 0,14" stroke="white" fill="none" stroke-width="2"></polyline>
                </svg>
                <span class="oi oi-eye" title="visibility" aria-hidden="true"></span>
              </button>
              <button class="btn btn-sm btn-outline-dark" @click="enter_create_shape_context(type)">+</button>
            </li>
          </ul>
        </div>
      </div>

    </div>

    <div v-if="selected_place && editing" class="modal fade" id="confirm-delete-modal" tabindex="-1" role="dialog"
         aria-labelledby="confirm-delete-title"
         aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirm-delete-title">Confirm delete</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            Are you sure you want to delete {{ selected_place.name }}? This cannot be undone.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" data-dismiss="modal"
                    @click="delete_selected_place">
              Yes, delete {{ selected_place.name }}
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
    import axios from 'axios';
    import _ from 'lodash';

    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';

    export default {
        data() {
            return {
                shapes: [],
                temp_points: [],
                temp_type: null,
                hoverable_place_class: 'hoverable-place',
                hovering_enabled: true,
                selected_place: null,
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
                user: null,
                editing: null,
                mousedown_on_temp_point: false,
                mouse_moving_on_temp_point: false,
            }
        },
        computed: {
            no_temp_points_selected() {
                for (let i = 0; i < this.temp_points.length; i++) {
                    if (this.temp_points[i].selected) {
                        return false;
                    }
                }
                return true;
            },
            inclusion_distance() {
                return this.$store.state.place_inclusion_distance
            }
        },
        watch: {
            inclusion_distance(new_dist, old_dist) {
                this.debounced_load_selected_place_details()
            }
        },
        methods: {
            load_shapes: function () {
                axios
                    .get('/api/places/')
                    .then(r => {
                        this.shapes = r.data;
                    })
                    .catch(e => {
                        console.log(e);
                    });
            },
            load_selected_place_details() {
                if (this.selected_place) this.load_place_details(this.selected_place.id);
            },
            load_place_details: function (place_id) {
                axios
                    .get('/api/places/' + place_id + '/', {
                        params: {
                            inclusion_distance: this.inclusion_distance
                        }
                    })
                    .then(r => {
                        this.selected_place = r.data;
                    })
                    .catch(e => {
                        console.log(e);
                    });
            },
            get_click_coords: function (event) {
                let bound = document.getElementById('place-canvas').getBoundingClientRect();
                let html = document.documentElement;
                let left = bound.left + window.pageXOffset - html.clientLeft;
                let top = bound.top + window.pageYOffset - html.clientTop;
                let x = event.pageX - left;
                let y = event.pageY - top;
                return {x: x, y: y};
            },
            enter_create_shape_context: function (context) {
                this.temp_type = context;
                this.hoverable_place_class = '';
                this.hovering_enabled = false;
                this.selected_place = null;
            },
            exit_and_save_shape: function () {
                axios
                    .post('/api/places/', {
                        points: this.temp_points,
                        type: this.temp_type
                    })
                    .then(_ => {
                        this.load_shapes()
                    })
                    .catch(e => {
                        console.log(e)
                    });
                this.exit_edit_shape_context();
            },
            exit_edit_shape_context: function () {
                this.temp_points = [];
                this.temp_type = null;
                this.hoverable_place_class = 'hoverable-place';
                this.hovering_enabled = true;
            },
            generate_temp_point: function (event) {
                if (this.mousedown_on_temp_point) return;
                if (this.temp_type) {
                    let coords = this.get_click_coords(event);
                    if (this.temp_type < 100) {
                        this.temp_points.pop();
                    }
                    this.temp_points.push(coords);
                }
            },
            points_to_pointstring: function (points_obj) {
                let pointstring = '';
                points_obj.forEach(function (point) {
                    pointstring += point.x + ',' + point.y + ' ';
                });
                return pointstring
            },
            place_clicked: function (event) {
                // don't do anything if we are in the process of adding a new place
                if (this.temp_type) {
                    return;
                }
                let place = $(event.target);
                if (place.hasClass('line-expander')) {
                    place = place.next();
                }
                this.select_place(this.html_id_2_pk(place.attr('id')));
            },
            select_place: function (pk) {
                if (this.selected_place && (this.selected_place.id === pk)) {
                    this.selected_place = null;
                } else {
                    // load details about place
                    this.load_place_details(pk);
                }
            },
            enter_edit_selected_place_context: function () {
                this.hoverable_place_class = '';
                this.hovering_enabled = false;
                this.editing = this.selected_place.id;
                this.temp_type = this.selected_place.type;
                this.temp_points = JSON.parse(JSON.stringify(this.selected_place.points));
                this.selected_place_edits = JSON.parse(JSON.stringify(this.selected_place));
            },
            exit_and_save_selected_place: function () {
                this.selected_place_edits.points = this.temp_points;

                axios
                    .post(
                        '/api/places/' + this.selected_place_edits.id + '/',
                        this.selected_place_edits
                    )
                    .then(_ => {
                        this.load_shapes();
                        this.load_place_details(parseInt(this.selected_place_edits.id));
                        this.exit_edit_context();
                    })
                    .catch(e => {
                        console.log(e)
                    });
            },
            delete_selected_place: function () {
                axios
                    .delete(
                        '/api/places/' + this.selected_place.id + '/'
                    )
                    .then(_ => {
                        this.load_shapes();
                        this.exit_edit_context();
                        this.selected_place = null;
                    })
                    .catch(e => {
                        console.log(e)
                    });
            },
            exit_edit_context: function () {
                this.editing = null;
                this.selected_place_edits = null;
                this.exit_edit_shape_context();
            },
            have_same_dimensions: function (type1, type2) {
                return ~~(type1 / 100) === ~~(type2 / 100)
            },
            temp_point_mousedown: function (event) {
                let id = parseInt(event.target.id.split('-')[2]);
                let $body = $('body');
                let parent = this;
                this.mousedown_on_temp_point = true;
                $body.on('mousemove click', function handler(event) {
                    if (event.type === 'mousemove') {
                        let coords = parent.get_click_coords(event);
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
            temp_point_click: function (event) {
                if (this.mouse_moving_on_temp_point) return;

                let $clicked = $(event.target);
                let id = parseInt($clicked.attr('id').split('-')[2]);
                if (this.temp_points[id].selected) {
                    this.temp_points[id].selected = false;
                } else {
                    this.$set(this.temp_points[id], 'selected', true);
                }
            },
            delete_temp_points: function () {
                for (let i = this.temp_points.length - 1; i >= 0; i--) {
                    if (this.temp_points[i].selected) {
                        this.temp_points.splice(i, 1);
                    }
                }
            },
            html_id_2_pk: function (html_id) {
                return parseInt(html_id.split('-')[1]);
            },
            pk_2_html_id: function (pk) {
                return 'place-' + pk
            },
            place_type_2_class: function (type) {
                return 'place-type-' + type;
            },
            class_2_place_type: function (cls) {
                return parseInt(cls.split('-')[2]);
            },
            active_if_active: function (pk) {
                if (this.selected_place && this.selected_place.id === pk) {
                    return 'active'
                } else return ''
            },
            is_active: function (pk) {
                return (this.selected_place && this.selected_place.id === pk)
            },
            toggle_type_visibility: function (type) {
                $('.' + this.place_type_2_class(type)).toggleClass('d-none')
            }
        },
        created() {
            this.load_shapes();
            this.user = user;
            this.debounced_load_selected_place_details = _.debounce(this.load_selected_place_details, 350)
        },

    }
</script>