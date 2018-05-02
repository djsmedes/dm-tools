<template>
  <div class="row container-fluid px-5">

    <div class="col">
      <div v-if="selected_place" class="card">
        <div class="card-header bg-dark text-white">
          <div class="row form-inline">
            <h4 class="col" v-if="! editing">{{ selected_place.name }}</h4>
            <label v-else>
              Name: <input v-model="selected_place_edits.name" class="mx-1 col form-control">
            </label>
            <button v-if="! editing" class="btn btn-outline-light col-auto ml-auto mr-1" @click="enter_edit_selected_place_context">
              Edit
            </button>
            <button v-if="editing" class="btn btn-success col-auto ml-auto mr-1" @click="exit_and_save_selected_place">Save
            </button>
            <button v-if="editing" class="btn btn-danger col-auto mr-1" @click="exit_edit_context">Cancel</button>
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
        <div class="card-footer">
          {{ selected_place.type }}
        </div>
      </div>
    </div>

    <div class="col-auto ml-auto p-0" style="width: 1200px; height: 900px">

      <svg id="place-canvas" width="1200" height="900" @click="generate_temp_point($event)">
        <defs>
          <filter id="innershadow">
            <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"></feGaussianBlur>
            <feComposite in2="SourceGraphic" operator="arithmetic" k2="-1" k3="1" result="shadowDiff"></feComposite>
          </filter>

        </defs>

        <rect width="1200" height="900" fill="transparent" stroke="black" stroke-width="2"></rect>

        <template v-for="shape in shapes">
          <g v-if="shape.dimensions === 2">
            <polygon :points="points_to_pointstring(shape.points)"
                     :class="'place-type-' + shape.type"
                     filter="url(#innershadow)"></polygon>
            <polygon :points="points_to_pointstring(shape.points)"
                     :id="'place-' + shape.id"
                     :class="hoverable_place_class + ' place-poly-outline place-type-' + shape.type"
                     @click="place_clicked($event)"></polygon>
          </g>
          <polyline v-else-if="shape.dimensions === 1"
                    :points="points_to_pointstring(shape.points)"
                    :class="hoverable_place_class + ' place-type-' + shape.type"
                    :id="'place-' + shape.id"
                    @click="place_clicked($event)"></polyline>
          <circle v-else-if="shape.dimensions === 0"
                  v-for="pt in shape.points"
                  :cx="pt.x" :cy="pt.y" r="5"
                  :id="'place-' + shape.id"
                  :class="hoverable_place_class + ' place-type-' + shape.type"
                  @click="place_clicked($event)"></circle>
        </template>

        <g v-if="200 <= temp_type">
          <polygon :points="points_to_pointstring(temp_points)"
                   :class="'place-type-' + temp_type"
                   filter="url(#innershadow)"></polygon>
          <polygon :points="points_to_pointstring(temp_points)"
                   :class="'place-poly-outline place-type-' + temp_type"></polygon>
        </g>
        <polyline v-else-if="100 <= temp_type" :points="points_to_pointstring(temp_points)"
                  :class="'place-type-' + temp_type"></polyline>
        <circle v-for="pt in temp_points"
                :cx="pt.x" :cy="pt.y" r="5"
                :class="get_temp_circle_class()"></circle>
      </svg>

    </div>

    <div class="col-auto ml-2">
      <div class="card">
        <div class="card-header bg-dark text-white">
          Key
        </div>
        <ul class="list-group list-group-flush">
          <li v-for="(name, type) in place_types" class="list-group-item">
            <svg width="16" height="16">
              <circle v-if="type < 100" cx="8" cy="8" r="5" :class="'place-type-' + type"></circle>
              <polyline v-else-if="type < 200" points="2,2 4,12 14,14" :class="'place-type-' + type"></polyline>
              <g v-else>
                <polygon points="2,2 50,0 0,50" :class="'place-type-' + type" filter="url(#innershadow)"></polygon>
                <polygon points="2,2 50,0 0,50" :class="'place-poly-outline place-type-' + type"></polygon>
              </g>
            </svg>
            {{ name }}
            <button class="btn btn-sm btn-outline-dark" @click="enter_create_shape_context(type)">+</button>
          </li>
        </ul>
      </div>
      <button v-if="temp_type != null"
              class="btn btn-outline-success"
              @click="exit_and_save_shape">
        Save
      </button>
      <button v-if="temp_type != null"
              class="btn btn-outline-danger"
              @click="exit_create_context">
        Cancel
      </button>
    </div>

  </div>
</template>

<script>
    import axios from 'axios';

    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';

    export default {
        data() {
            return {
                shapes: [],
                temp_points: [],
                temp_type: null,
                hoverable_place_class: 'hoverable-place',
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
                editing: false
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
            load_place_details: function (place_id) {
                axios
                    .get('/api/places/' + place_id + '/')
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
                this.exit_create_context();
            },
            exit_create_context: function () {
                this.temp_points = [];
                this.temp_type = null;
                this.hoverable_place_class = 'hoverable-place';
            },
            generate_temp_point: function (event) {
                if (this.temp_type != null) {
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

                // toggle display active state
                let $clicked = $(event.target);
                let was_active = $clicked.hasClass('active');
                $('.active').removeClass('active');
                if (!was_active) {
                    $clicked.addClass('active');
                    // load details about place
                    let pk = parseInt(event.target.id.split('-')[1]);
                    this.load_place_details(pk);
                } else {
                    this.selected_place = null;
                }
            },
            get_temp_circle_class: function () {
                if (this.temp_type < 100) {
                    return 'place-type-' + this.temp_type
                } else {
                    return 'place-temp-point'
                }
            },
            enter_edit_selected_place_context: function () {
                this.editing = true;
                this.selected_place_edits = JSON.parse(JSON.stringify(this.selected_place));
            },
            exit_and_save_selected_place: function() {
                axios
                    .post(
                        '/api/places/' + this.selected_place_edits.id + '/',
                        this.selected_place_edits
                    )
                    .then(_ => {
                        this.load_place_details(parseInt(this.selected_place_edits.id));
                        this.exit_edit_context();
                    })
                    .catch(e => {
                        console.log(e)
                    });
            },
            exit_edit_context: function () {
                this.editing = false;
                this.selected_place_edits = null;
            }
        },
        created() {
            this.load_shapes();
            this.user = user;
        }
    }
</script>