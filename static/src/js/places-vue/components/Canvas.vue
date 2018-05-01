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
          <g v-if="shape.dimensions === '2'">
            <polygon :points="points_to_pointstring(shape.points)"
                     stroke="green" fill="green" stroke-width="2"
                     filter="url(#innershadow)"></polygon>
            <polygon :points="points_to_pointstring(shape.points)"
                     fill="transparent" stroke="green"
                     :id="'place-' + shape.id"
                     :class="hoverable_place_class"
                     @click="place_clicked($event)"
                     stroke-width="2"></polygon>
          </g>
          <polyline v-else-if="shape.dimensions === '1'"
                    :points="points_to_pointstring(shape.points)"
                    stroke="blue" stroke-width="2"
                    :class="hoverable_place_class"
                    :id="'place-' + shape.id"
                    @click="place_clicked($event)"
                    fill="none"></polyline>
          <circle v-else-if="shape.dimensions === '0'"
                  v-for="pt in shape.points"
                  :cx="pt.x" :cy="pt.y" r="5"
                  :id="'place-' + shape.id"
                  :class="hoverable_place_class"
                  @click="place_clicked($event)"
                  stroke="black" stroke-width="2" fill="transparent"></circle>
        </template>

        <polyline v-if="temp_dimensions === 1" :points="points_to_pointstring(temp_points)" stroke="blue"
                  stroke-width="2" fill="none"></polyline>
        <g v-if="temp_dimensions === 2">
          <polygon :points="points_to_pointstring(temp_points)" stroke="green" fill="green" stroke-width="2"
                   filter="url(#innershadow)"></polygon>
          <polygon :points="points_to_pointstring(temp_points)" fill="transparent" stroke="green"
                   stroke-width="2"></polygon>
        </g>
        <circle v-for="pt in temp_points"
                :cx="pt.x" :cy="pt.y" r="5"
                stroke="black" stroke-width="2" fill="transparent"></circle>


      </svg>

    </div>

    <div class="col">
      <button v-if="temp_dimensions == null"
              class="btn btn-outline-dark"
              @click="enter_create_context(0)">
        Create new Point
      </button>
      <button v-if="temp_dimensions === 0"
              class="btn btn-dark"
              @click="exit_and_save">
        Save this Point
      </button>
      <button v-if="temp_dimensions == null"
              class="btn btn-outline-dark"
              @click="enter_create_context(1)">
        Create new Line
      </button>
      <button v-if="temp_dimensions === 1"
              class="btn btn-dark"
              @click="exit_and_save">
        Save this Line
      </button>
      <button v-if="temp_dimensions == null"
              class="btn btn-outline-dark"
              @click="enter_create_context(2)">
        Create new Polygon
      </button>
      <button v-if="temp_dimensions === 2"
              class="btn btn-dark"
              @click="exit_and_save">
        Save this Polygon
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
                hoverable_place_class: 'hoverable-place'
            }
        },
        methods: {
            load_shapes: function () {
                axios
                    .get('/api/places/')
                    .then(r => {
                        this.shapes = r.data
                    })
                    .catch(e => {
                        console.log(e)
                    })
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
                this.temp_dimensions = context;
                this.hoverable_place_class = '';
            },
            exit_and_save: function () {
                axios
                    .post('/api/places/', {
                        points: this.temp_points,
                        dimensions: this.temp_dimensions
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
            }
        },
        created() {
            this.load_shapes()
        }
    }
</script>