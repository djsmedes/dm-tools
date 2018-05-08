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

const model_api_url = '/' + template_context.api_url;

const model_actions = {
    get_model(context, id) {
        axios.get(id + '/', {
            baseURL: model_api_url,
            params: {
                inclusion_distance: context.state.campaign.place_inclusion_distance
            }
        }).then(r => {
            context.commit('set_model', r.data);
        }).catch(e => {
            console.log(e);
        });
    },
    get_model_list(context) {
        axios.get('', {
            baseURL: model_api_url,
        }).then(r => {
            context.commit('set_model_list', r.data);
        }).catch(e => {
            console.log(e);
        });
    },
    add_model(context, model) {
        axios.post('', model, {
            baseURL: model_api_url,
        }).then(_ => {
            context.dispatch('get_model_list');
        }).catch(e => {
            console.log(e)
        });
    },
    change_model(context, model) {
        let id = model.id;
        axios.post(id + '/', model, {
            baseURL: model_api_url,
        }).then(_ => {
            context.dispatch('get_model_list');
            context.dispatch('get_model', id);
        }).catch(e => {
            console.log(e)
        });
    },
    delete_model(context, id) {
        axios.delete(id + '/', {
            baseURL: model_api_url
        }).then(_ => {
            context.dispatch('get_model_list');
            context.commit('set_model', null);
        }).catch(e => {
            console.log(e)
        });
    }
};

const model_mutators = {
    set_model(state, new_data) {
        state.model = new_data;
    },
    set_model_list(state, new_data) {
        state.model_list = new_data;
    }
};


const store = new Vuex.Store({
    state: Object.assign({}, template_context, {
        model: null,
        model_list: null,
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