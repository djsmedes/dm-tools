<template>
  <div class="row">
    <div class="ml-5 p-0 col" style="width: 1200px; height: 900px">

      <svg id="place-canvas" width="1200" height="900" @click="generate_temp_point($event)">
        <defs>
          <filter id="innershadow">
            <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur"></feGaussianBlur>
            <feComposite in2="SourceGraphic" operator="arithmetic" k2="-1" k3="1" result="shadowDiff"></feComposite>
          </filter>

        </defs>

        <rect width="1200" height="900" fill="transparent" stroke="black" stroke-width="2"></rect>

        <template v-for="shape in shapes">
          <g v-if="shape.dimensions === 2">
            <polygon :points="points_to_pointstring(shape.points)"
                     :fill="get_shape_color(shape)"
                     filter="url(#innershadow)"></polygon>
            <polygon :points="points_to_pointstring(shape.points)"
                     fill="transparent"
                     :stroke="get_shape_color(shape)"
                     :id="'place-' + shape.id"
                     :class="hoverable_place_class"
                     @click="place_clicked($event)"
                     stroke-width="2"></polygon>
          </g>
          <polyline v-else-if="shape.dimensions === 1"
                    :points="points_to_pointstring(shape.points)"
                    :stroke="get_shape_color(shape)"
                    stroke-width="2"
                    :class="hoverable_place_class"
                    :id="'place-' + shape.id"
                    @click="place_clicked($event)"
                    fill="none"></polyline>
          <circle v-else-if="shape.dimensions === 0"
                  v-for="pt in shape.points"
                  :cx="pt.x" :cy="pt.y" r="5"
                  :id="'place-' + shape.id"
                  :class="hoverable_place_class"
                  @click="place_clicked($event)"
                  :stroke="get_shape_color(shape)"
                  stroke-width="2" fill="transparent"></circle>
        </template>

        <polyline v-if="temp_dimensions === 1" :points="points_to_pointstring(temp_points)"
                  :stroke="shape_types.d1[100+temp_type].rgbcolor"
                  stroke-width="2" fill="none"></polyline>
        <g v-if="temp_dimensions === 2">
          <polygon :points="points_to_pointstring(temp_points)"
                   :fill="shape_types.d2[200+temp_type].rgbcolor"
                   filter="url(#innershadow)"></polygon>
          <polygon :points="points_to_pointstring(temp_points)" fill="transparent"
                   :stroke="shape_types.d2[200+temp_type].rgbcolor"
                   stroke-width="2"></polygon>
        </g>
        <circle v-for="pt in temp_points"
                :cx="pt.x" :cy="pt.y" r="5"
                :stroke="get_circle_color()"
                stroke-width="2" fill="transparent"></circle>


      </svg>

    </div>

    <div class="col">
      <div v-if="temp_dimensions == null"
              class="btn-group" role="group" aria-label="Point creation buttons">
        <button v-for="(type, key) in shape_types.d0" type="button"
                :class="'btn btn-outline-' + type.bscolor"
                @click="enter_create_context(key)" >
          New {{ type.name }}
        </button>
      </div>
      <br>
      <div v-if="temp_dimensions == null"
              class="btn-group" role="group" aria-label="Line creation buttons">
        <button v-for="(type, key) in shape_types.d1" type="button"
                :class="'btn btn-outline-' + type.bscolor"
                @click="enter_create_context(key)" >
          New {{ type.name }}
        </button>
      </div>
      <br>
      <div v-if="temp_dimensions == null"
              class="btn-group" role="group" aria-label="Shape creation buttons">
        <button v-for="(type, key) in shape_types.d2" type="button"
                :class="'btn btn-outline-' + type.bscolor"
                @click="enter_create_context(key)" >
          New {{ type.name }}
        </button>
      </div>

      <button v-if="temp_dimensions != null"
              class="btn btn-outline-success"
              @click="exit_and_save">
        Save
      </button>
      <button v-if="temp_dimensions != null"
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
                temp_dimensions: null,
                temp_type: null,
                hoverable_place_class: 'hoverable-place',
                shape_types: {
                    d2: {
                        200: {name: 'misc region', bscolor: 'dark', rgbcolor: 'rgb(52, 58, 64)'},
                        201: {name: 'geological', bscolor: 'brown', rgbcolor: 'rgb(87, 53, 17)'},
                        202: {name: 'vegetation', bscolor: 'success', rgbcolor: 'rgb(40, 167, 69)'},
                        203: {name: 'water', bscolor: 'primary', rgbcolor: 'rgb(0, 123, 255)'},
                        204: {name: 'political', bscolor: 'danger', rgbcolor: 'rgb(220, 53, 69)'}
                    },
                    d1: {
                        100: {name: 'misc line', bscolor: 'dark', rgbcolor: 'rgb(52, 58, 64)'},
                        101: {name: 'road', bscolor: 'danger', rgbcolor: 'rgb(220, 53, 69)'},
                        102: {name: 'river', bscolor: 'primary', rgbcolor: 'rgb(0, 123, 255)'}
                    },
                    d0: {
                        0: {name: 'misc point', bscolor: 'dark', rgbcolor: 'rgb(52, 58, 64)'},
                        1: {name: 'settlement', bscolor: 'danger', rgbcolor: 'rgb(220, 53, 69)'},
                        2: {name: 'natural', bscolor: 'brown', rgbcolor: 'rgb(87, 53, 17)'},
                        3: {name: 'dungeon', bscolor: 'warning', rgbcolor: 'rgb(255, 193, 7)'}
                    }
                }
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
                        console.log(e)
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
            enter_create_context: function (context) {
                this.temp_dimensions = ~~(context / 100);
                this.temp_type = context % 100;
                this.hoverable_place_class = '';
            },
            exit_and_save: function () {
                axios
                    .post('/api/places/', {
                        points: this.temp_points,
                        dimensions: this.temp_dimensions,
                        type: (this.temp_type + (this.temp_dimensions * 100))
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
                this.temp_dimensions = null;
                this.temp_type = null;
                this.hoverable_place_class = 'hoverable-place';
            },
            generate_temp_point: function (event) {
                if (this.temp_dimensions != null) {
                    let coords = this.get_click_coords(event);
                    if (this.temp_dimensions === 0) {
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
                // toggle display active state
                let $clicked = $(event.target);
                let was_active = $clicked.hasClass('active');
                $('.active').removeClass('active');
                if (!was_active) {
                    $clicked.addClass('active');
                }

                // load details about place
                let pk = event.target.id.split('-')[1];
                console.log(pk);
            },
            get_circle_color: function() {
                if ( this.temp_dimensions === 0) {
                    return this.shape_types.d0[this.temp_type].rgbcolor
                } else {
                    return 'rgb(108, 117, 125)'
                }
            },
            get_shape_color: function(shape) {
                if ( shape.type > 199 ) {
                    return this.shape_types.d2[shape.type].rgbcolor
                } else if ( shape.type > 99 ) {
                    return this.shape_types.d1[shape.type].rgbcolor
                } else {
                    return this.shape_types.d0[shape.type].rgbcolor
                }
            }
        },
        created() {
            this.load_shapes()
        }
    }
</script>