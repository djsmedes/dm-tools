<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
    export default {
        props: {
            user_json: null,
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
                    that[prop_name] = null;
                }
            });
        },

    }
</script>