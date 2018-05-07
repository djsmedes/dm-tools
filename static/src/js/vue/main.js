import axios from 'axios'
import Vue from 'vue/dist/vue'

import place_canvas from './components/place_canvas'
import place_inclusion_distance from './components/place_inclusion_distance'

Vue.component('place-canvas', require('./components/place_canvas'));
Vue.component('place-inclusion-distance', require('./components/place_inclusion_distance'));

new Vue({
    el: '#app',
    components: { place_canvas, place_inclusion_distance }
});