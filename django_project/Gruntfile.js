module.exports = function(grunt) {
    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        browserify: {
            js: {
                src: 'lib_js/app.js',
                dest: 'core/base_static/js/app.module.js'
            }
        },
        cssmin: {
            contrib: {
                src: 'lib_css/ol.css',
                dest: 'core/base_static/css/contrib.module.css'
            }
        },
        uglify: {
            js: {
                files: {
                    'core/base_static/js/app.module.js': ['core/base_static/js/app.module.js']
                }
            }
        },
        jshint: {
            options: {
                jshintrc: true
            },
            app: ['lib_js/*.js']
        },
        watch: {
            scripts: {
                files: ['lib_js/*.js'],
                tasks: ['default'],
                options: {
                    spawn: false,
                },
            },
        }
    });

    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-css');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['jshint', 'browserify', 'cssmin']);
    grunt.registerTask('build', ['browserify', 'cssmin', 'uglify']);
};