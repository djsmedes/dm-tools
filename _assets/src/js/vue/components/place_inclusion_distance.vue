<template>
  <div class="form-group">
    <label for="navbar-inclusion-distance" class="dropdown-header">Inclusion distance</label>
    <div class="px-4">
      <input id="navbar-inclusion-distance"
             type="number" min="0"
             class="form-control"
             v-model="inclusion_distance">
    </div>
  </div>
</template>

<script>
    export default {
        data() {
            return {}
        },
        computed: {
            inclusion_distance: {
                get() {
                    return this.$store.state.campaign.place_inclusion_distance
                },
                set(value) {
                    this.$store.commit('set_place_inclusion_distance', value);
                }
            }
        },
        methods: {},
        created() {
        },

    }
</script>