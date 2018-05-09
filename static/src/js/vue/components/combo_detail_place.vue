<template>
  <div>
  <div v-if="object" class="card">
    <h3 class="card-header bg-dark text-white"
        style="text-transform: capitalize;">
      {{ object.name }}
    </h3>
    <div class="card-body">
      {{ object.description }}
    </div>
    <div class="card-footer">
      Some footer text
    </div>
  </div>
  </div>
</template>

<script>
    export default {
        props: {
            model_name: '',
            model_name_plural: '',
            object_json: null
        },
        data() {
            return {
            }
        },
        computed: {
            object() {
                return this.$store.state.model;
            }
        },
        watch: {},
        methods: {
        },
        created() {
            if (this.object_json) {
                this.$store.commit('set_model', JSON.parse(this.object_json));
            }
        },

    }
</script>