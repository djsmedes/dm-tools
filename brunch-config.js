// See http://brunch.io for documentation.
exports.paths = {
    public: 'static/'
};

exports.files = {
    javascripts: {
        joinTo: {
            'js/app.js': /^app/,
            'js/vendor.js': /^(?!app)/
        }
    },
    stylesheets: {
        joinTo: {
            'css/app.css': /^app/
        }
    }
};

exports.plugins = {
    postcss: {
        processors: [
            require('autoprefixer')(['last 8 versions']),
            require('csswring')()
        ]
    }
};

exports.npm = {
    globals: {
        $: 'jquery',
        jQuery: 'jquery',
        bootstrap: 'bootstrap'
    }
};