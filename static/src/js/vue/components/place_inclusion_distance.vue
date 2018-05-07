<template>
  <div class="form-group">
    <label for="navbar-inclusion-distance" class="dropdown-header">Inclusion distance</label>
    <div class="px-4">
      <input id="navbar-inclusion-distance"
             type="number"
             class="form-control"
             v-model="inclusion_distance">
    </div>
  </div>
</template>

<script>
    export default {
        data() {
            return {
                inclusion_distance: 0,
            }
        },
        computed: {},
        methods: {},
        created() {
        },

    }
</script>