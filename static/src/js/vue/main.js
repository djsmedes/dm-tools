import axios from 'axios'
import _ from 'lodash'
import Vue from 'vue/dist/vue'
import Vuex from 'vuex'

Vue.use(Vuex);

import place_canvas from './components/place_canvas'
import place_inclusion_distance from './components/place_inclusion_distance'

Vue.component('place-canvas', require('./components/place_canvas'));
Vue.component('place-inclusion-distance', require('./components/place_inclusion_distance'));

const store = new Vuex.Store({
    state: {
        place_inclusion_distance: 0
    },
    mutations: {
        set_place_inclusion_distance (state, n) {
            state.place_inclusion_distance = n;
        }
    }
});

new Vue({
    el: '#app',
    store,
    components: { place_canvas, place_inclusion_distance }
});