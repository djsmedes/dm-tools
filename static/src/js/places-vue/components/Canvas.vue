<template>

  <div class="ml-5 p-0" style="width: 1200px; height: 900px">

    <svg id="place-canvas" width="1200" height="900">
      <defs>
        <filter id="innershadow">
          <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur"></feGaussianBlur>
          <feComposite in2="SourceGraphic" operator="arithmetic" k2="-1" k3="1" result="shadowDiff"></feComposite>
        </filter>

      </defs>

      <g v-for="shape in shapes">
        <polygon :points="shape.points" stroke="green" fill="green" stroke-width="2" filter="url(#innershadow)"></polygon>
        <polygon :points="shape.points" fill="transparent" stroke="green" stroke-width="2"></polygon>
      </g>

      <!--<polygon points="200,50 300,50 250,190 160,210" filter="url(#innershadow)" fill="green" stroke="green"-->
               <!--stroke-width="2"></polygon>-->

      <!--<polygon points="200,50 300,50 250,190 160,210" fill="transparent" stroke="green" stroke-width="2"></polygon>-->

      <rect width="1200" height="900" fill="transparent" stroke="black" stroke-width="2"
            v-on:click="test_method($event)">
      </rect>
    </svg>

  </div>

</template>

<script>
  import axios from 'axios';

  axios.defaults.xsrfCookieName = 'csrftoken';
  axios.defaults.xsrfHeaderName = 'X-CSRFToken';

  export default {
      data() {
          return {
              shapes: []
          }
      },
      methods: {
          load_shapes: function() {
              axios
                  .get('/places/api/get-place-data/')
                  .then(r => { this.shapes = r.data.shape_set })
                  .catch(e => { console.log(e) })
          },
          test_method: function(event) {
              let bound = document.getElementById('place-canvas').getBoundingClientRect();
              let html = document.documentElement;
              let left = bound.left + window.pageXOffset - html.clientLeft;
              let top = bound.top + window.pageYOffset - html.clientTop;
              let x = event.pageX - left;
              let y = event.pageY - top;
              console.log(x, y);
          }
      },
      created() { this.load_shapes() }
  }
</script>