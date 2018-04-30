import axios from 'axios'
import Vue from 'vue'

import Canvas from './components/Canvas.vue'

new Vue({
    el: '#canvas',
    render: h => h(Canvas)
});