import axios from 'axios'
import _ from 'lodash'
import Vue from 'vue/dist/vue'
import Vuex from 'vuex'

Vue.use(Vuex);

import place_canvas from './components/place_canvas'
import place_inclusion_distance from './components/place_inclusion_distance'

Vue.component('place-canvas', require('./components/place_canvas'));
Vue.component('place-inclusion-distance', require('./components/place_inclusion_distance'));

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
// axios.defaults.baseURL = template_context.api_url;

const model_actions = {
    get_model(context, id) {
        let url = context.state.api_url + id + '/';
        axios.get(url, {
            baseURL: '/',
            params: {
                inclusion_distance: context.state.campaign.place_inclusion_distance
            }
        }).then(
            r => {
                context.commit('set_model', r.data);
            }
        ).catch(
            e => {
                console.log(e);
            }
        );
    },
    add_model(context) {

    }
    ,
    change_model(context) {

    }
    ,
    delete_model(context) {

    }
};

const model_mutators = {
    set_model(state, new_data) {
        state.model = new_data
    }
};


const store = new Vuex.Store({
    state: Object.assign({}, template_context, {
        model: null
    }),
    mutations: Object.assign({},
        {
            set_place_inclusion_distance(state, n) {
                state.campaign.place_inclusion_distance = n;
            },
        },
        model_mutators
    ),
    actions: model_actions
});

store.state.refresh_model = _.debounce(function() {
    if (! store.state.model) return;
    store.dispatch('get_model', store.state.model.id);
}, 300);

new Vue({
    el: '#app',
    store,
    components: {place_canvas, place_inclusion_distance}
});