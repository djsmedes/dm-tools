<template>

  <div class="ml-5 p-0" style="width: 1200px; height: 900px">

    <svg id="place-canvas" width="1200" height="900">

      <!--<script>-->
          <!--function mouse_coords(event) {-->
              <!--let bound = document.getElementById('place-canvas').getBoundingClientRect();-->
              <!--var html = document.documentElement;-->
              <!--var left = bound.left + window.pageXOffset - html.clientLeft;-->
              <!--var top = bound.top + window.pageYOffset - html.clientTop;-->
              <!--var x = event.pageX - left;-->
              <!--var y = event.pageY - top;-->
              <!--console.log(x, y);-->
              <!--return {x: x, y: y};-->
          <!--}-->

          <!--function getNode(n, v) {-->
              <!--n = document.createElementNS("http://www.w3.org/2000/svg", n);-->
              <!--for (var p in v)-->
                  <!--n.setAttributeNS(null, p.replace(/[A-Z]/g, function (m, p, o, s) {-->
                      <!--return "-" + m.toLowerCase();-->
                  <!--}), v[p]);-->
              <!--return n-->
          <!--}-->

          <!--function draw_clicked_point(event) {-->
              <!--var coords = mouse_coords(event);-->
              <!--var svg = document.getElementById('place-canvas');-->
              <!--svg.appendChild(getNode('circle', {cx: coords.x, cy: coords.y, r: '5', fill: 'red'}));-->
          <!--}-->

      <!--</script>-->

      <defs>
        <filter id="innershadow">
          <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur"></feGaussianBlur>
          <feComposite in2="SourceGraphic" operator="arithmetic" k2="-1" k3="1" result="shadowDiff"></feComposite>
        </filter>

      </defs>

      <polygon points="200,50 300,50 250,190 160,210" filter="url(#innershadow)" fill="green" stroke="green"
               stroke-width="2"></polygon>

      <polygon points="200,50 300,50 250,190 160,210" fill="transparent" stroke="green" stroke-width="2"></polygon>

      <rect width="1200" height="900" fill="transparent" stroke="black" stroke-width="2"
            onclick="draw_clicked_point(evt)"
      ></rect>
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
          loadShapes: function() {
              // axios
              //     .get('/get/endpoint')
              //     .then(r => { this.shapes = r.data.shape_set })
              //     .catch(e => { console.log(e) })
          }
      },
      created() { this.loadShapes() }
  }
</script>