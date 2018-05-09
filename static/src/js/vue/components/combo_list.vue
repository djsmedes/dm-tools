<template>
  <div>
    <div class="row">
      <div class="col-auto">
        <div class="card">
          <h3 class="card-header bg-dark text-white"
              style="text-transform: capitalize;">
            {{ model_name_plural }}
          </h3>
          <div style="max-height: calc(100% - 300px); overflow-y: auto">
            <div class="list-group list-group-flush">
                <button v-for="object in object_list"
                        class="list-group-item list-group-item-action">
                  {{ object.name }}
                </button>
            </div>
          </div>
          <div class="card-footer">
            <button class="btn btn-outline-primary">Add a new {{ model_name }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
        props: {
            model_name: '',
            model_name_plural: '',
            object_list_json: null
        },
        data() {
            return {
                user: null,
                object_list: null
            }
        },
        computed: {},
        watch: {},
        methods: {
            console_log(msg) {
                console.log(msg);
            }
        },
        created() {
            let that = this;
            Object.keys(this._props).forEach(function (prop_name) {
                if (prop_name.includes('_json') && that[prop_name]) {
                    let data_name = prop_name.replace('_json', '');
                    that[data_name] = JSON.parse(that[prop_name]);
                }
            });
        },

    }
</script>