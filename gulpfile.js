// importamos gulp
var gulp = require('gulp');
var sass = require('gulp-sass');
var notify = require('gulp-notify');
var browserSync = require('browser-sync').create();


var sourcemaps = require('gulp-sourcemaps');
var autoprefixer = require('gulp-autoprefixer');
var cssnano = require('gulp-cssnano');
var fontAwesome = require('node-font-awesome');

var resolveDependencies = require('gulp-resolve-dependencies');
var concat = require('gulp-concat');

// source and distribution folder
var source = 'src/',
    dest = 'dist/';
// javascript config
var js = { in: source + "js/**/*.js",
    out: dest + "js/",
    watch: [source + "js/*.js", source + "js/**/*.js"],
    sourcemaps: './'
};

// bootstrap scss source and fonts
var bootstrapSass = { in: './node_modules/bootstrap-sass/'},
    fonts = { in: [
            fontAwesome.fonts,
            bootstrapSass.in + 'assets/fonts/**/*'
        ],
        out: dest + 'fonts/'
    };
// sass config
var scss = { in: source + 'scss/style.scss',
    out: dest + 'css/',
    watch: source + 'scss/**/*',
    sourcemaps: './',
    sassOpts: {
        outputStyle: 'nested',
        precison: 3,
        errLogToConsole: true,
        includePaths: [bootstrapSass.in + 'assets/stylesheets', fontAwesome.scssPath],
    }
};
// copy bootstrap required fonts to dest
gulp.task('fonts', function() {
    gulp
        .src(fonts.in)
        .pipe(gulp.dest(fonts.out))
        // notifications message (uncomment to display them)
        /*.pipe(notify({
            title: "Fonts",
            message: "Fonts moved"
        }))*/
    ;
});
// compile scss
gulp.task('sass', function() {
    return gulp.src(scss.in)
        // .pipe(sourcemaps.init())
        .pipe(sass(scss.sassOpts).on('error', sass.logError))
        .pipe(autoprefixer())
        .pipe(cssnano())
        // .pipe(sourcemaps.write(scss.sourcemaps))
        .pipe(gulp.dest(scss.out))
        .pipe(notify({
            title: "SASS",
            message: "Compiled"
        }))
        .pipe(browserSync.stream());
});


gulp.task('js', function() {
  gulp.src(js.in)
    .pipe(resolveDependencies({
      pattern: /\* @requires [\s-]*(.*\.js)/g
    }))
        .on('error', function(err) {
            console.log(err.message);
        })
    .pipe(concat('app.js'))
    .pipe(gulp.dest(js.out))
    .pipe(notify({
            title: "JS",
            message: "Concatenated"
    }));
});

// default task
gulp.task("default", ["js", "sass", "fonts"], function() {
    // iniciar BrowserSync
    browserSync.init({
        // server: "./", // levanta servidor web en carpeta actual
        proxy: "127.0.0.1:8000" // actúa como proxy enviando las peticiones a sparrest
    });
    gulp.watch(scss.watch, ["sass"]);
    gulp.watch("*.html").on("change", browserSync.reload);
    gulp.watch(js.watch, ["js"]);
});