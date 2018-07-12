<template>
  <div>
    <div class="mb-1 form-group bg-secondary text-white rounded py-2 px-3">
      <label for="combo-list-filter">Filter</label>
      <input id="combo-list-filter"
             class="form-control"
             v-model="search_bar">
    </div>
    <div class="card">
      <div class="card-header bg-dark text-white"
           style="text-transform: capitalize;">
        <h3>{{ model_name_plural }}</h3>

      </div>
      <div style="max-height: 500px; overflow-y: auto">
        <div class="list-group list-group-flush">
          <button v-for="object in sorted_and_filtered_object_list"
                  class="list-group-item list-group-item-action"
                  :class="is_active(object.id) ? 'active' : ''"
                  @click="set_object(object.id)">
            {{ object.name }}
          </button>
        </div>
      </div>
      <div class="card-footer">
        <button class="btn btn-outline-primary">Add a new {{ model_name }}</button>
      </div>
    </div>
  </div>
</template>

<script>
    import _ from 'lodash'

    export default {
        props: {
            model_name: '',
            model_name_plural: '',
            object_list_json: null
        },
        data() {
            return {
                search_bar: ''
            }
        },
        computed: {
            object_list() {
                return this.$store.state.model_list
            },
            sorted_object_list() {
                if (this.object_list) {
                    return _.sortBy(
                        this.object_list,
                        model => model.name
                    )
                } else return []
            },
            sorted_and_filtered_object_list() {
                if (this.sorted_object_list) {
                    return this.sorted_object_list.filter(
                        model => model.name.toLowerCase().includes(this.search_bar.toLowerCase())
                    );
                } else return []
            }
        },
        watch: {},
        methods: {
            set_object(id) {
                this.$store.dispatch('get_model', id)
            },
            is_active(id) {
                if (!this.$store.state.model) return false;
                return id === this.$store.state.model.id;
            }
        },
        created() {
            // let that = this;
            // Object.keys(this._props).forEach(function (prop_name) {
            //     if (prop_name.includes('_json') && that[prop_name]) {
            //         let data_name = prop_name.replace('_json', '');
            //         that[data_name] = JSON.parse(that[prop_name]);
            //     }
            // });
            if (this.object_list_json) {
                this.$store.commit('set_model_list', JSON.parse(this.object_list_json));
            } else {
                this.$store.dispatch('get_model_list');
            }
        },

    }
</script>