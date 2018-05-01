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

    <div class="col">
      <div v-if="temp_type == null"
              class="btn-group" role="group" aria-label="Point creation buttons">
        <button v-for="(type, key) in shape_types.d0" type="button"
                :class="'btn btn-outline-' + type.bscolor"
                @click="enter_create_context(key)" >
          New {{ type.name }}
        </button>
      </div>
      <br>
      <div v-if="temp_type == null"
              class="btn-group" role="group" aria-label="Line creation buttons">
        <button v-for="(type, key) in shape_types.d1" type="button"
                :class="'btn btn-outline-' + type.bscolor"
                @click="enter_create_context(key)" >
          New {{ type.name }}
        </button>
      </div>
      <br>
      <div v-if="temp_type == null"
              class="btn-group" role="group" aria-label="Shape creation buttons">
        <button v-for="(type, key) in shape_types.d2" type="button"
                :class="'btn btn-outline-' + type.bscolor"
                @click="enter_create_context(key)" >
          New {{ type.name }}
        </button>
      </div>

      <button v-if="temp_type != null"
              class="btn btn-outline-success"
              @click="exit_and_save">
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
                shape_types: {
                    d2: {
                        200: {name: 'misc region', bscolor: 'dark'},
                        201: {name: 'geological', bscolor: 'brown'},
                        202: {name: 'vegetation', bscolor: 'success'},
                        203: {name: 'water', bscolor: 'primary'},
                        204: {name: 'political', bscolor: 'danger'}
                    },
                    d1: {
                        100: {name: 'misc line', bscolor: 'dark'},
                        101: {name: 'road', bscolor: 'danger'},
                        102: {name: 'river', bscolor: 'primary'}
                    },
                    d0: {
                        0: {name: 'misc point', bscolor: 'dark'},
                        1: {name: 'settlement', bscolor: 'danger'},
                        2: {name: 'natural', bscolor: 'brown'},
                        3: {name: 'dungeon', bscolor: 'warning'}
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
                this.temp_type = context;
                this.hoverable_place_class = '';
            },
            exit_and_save: function () {
                axios
                    .post('/api/places/', {
                        points: this.temp_points,
                        dimensions: ~~(this.temp_type / 100),
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
            get_temp_circle_class: function() {
                if ( this.temp_type < 100) {
                    return 'place-type-' + this.temp_type
                } else {
                    return 'place-temp-point'
                }
            }
        },
        created() {
            this.load_shapes()
        }
    }
</script>