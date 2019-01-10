
////////////////////////////////
		//Setup//
////////////////////////////////

var replace = require('gulp-replace-path');
var path = require('path');

// Plugins
var gulp = require('gulp'),
      pjson = require('./package.json'),
      gutil = require('gulp-util'),
      sass = require('gulp-sass'),
      autoprefixer = require('gulp-autoprefixer'),
      cssnano = require('gulp-cssnano'),
      
      concat = require('gulp-concat'),
      
      rename = require('gulp-rename'),
      del = require('del'),
      plumber = require('gulp-plumber'),
      pixrem = require('gulp-pixrem'),
      uglify = require('gulp-uglify'),
      inlineCss = require('gulp-inline-css'),
      imagemin = require('gulp-imagemin'),
      spawn = require('child_process').spawn,
      runSequence = require('run-sequence'),
      browserSync = require('browser-sync').create(),
      reload = browserSync.reload;


// Relative paths function
var pathsConfig = function (appName) {
  this.app = "./" + (appName || pjson.name);
  var vendorsRoot = 'node_modules/';

  return {
    
    bootstrapSass: vendorsRoot + '/bootstrap/scss',
    vendorsJs: [
      vendorsRoot + '@vendor/jquery/dist/jquery.slim.js',
      vendorsRoot + 'popper.js/dist/umd/popper.js',
      vendorsRoot + '@vendor/bootstrap/dist/js/bootstrap.js'
    ],
    
    app: this.app,
    templates: this.app + '/templates',
    css: this.app + '/static/css',
    sass: this.app + '/static/sass',
    fonts: this.app + '/static/fonts',
    images: this.app + '/static/images',
    js: this.app + '/static/js',
    email_src: this.app + '/**/email-src/**',
    emails: this.app + '/templates/emails'
  }
};

var paths = pathsConfig();

////////////////////////////////
		//Tasks//
////////////////////////////////

// Styles autoprefixing and minification
gulp.task('styles', function() {
  return gulp.src(paths.sass + '/project.scss') //, {sourcemaps: true})
    .pipe(sass({
      includePaths: [
        
        paths.bootstrapSass,
        
        paths.sass
      ]
    }).on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(autoprefixer({browsers: ['last 2 versions']})) // Adds vendor prefixes
    .pipe(pixrem())  // add fallbacks for rem units
    .pipe(gulp.dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(cssnano()) // Minifies the result
    .pipe(gulp.dest(paths.css));
});

// Javascript minification
gulp.task('scripts', function() {
  return gulp.src(paths.js + '/project.js')
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest(paths.js));
});



// Vendor Javascript minification
gulp.task('vendor-scripts', function() {
  return gulp.src(paths.vendorsJs)
    .pipe(concat('vendors.js'))
    .pipe(gulp.dest(paths.js))
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest(paths.js));
});


// Image compression
gulp.task('imgCompression', function(){
  return gulp.src(paths.images + '/*')
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
    .pipe(gulp.dest(paths.images));
});

gulp.task('inlineCss', function() {
    return gulp.src(paths.email_src + '/*.html')
        .pipe(inlineCss({
          applyStyleTags: false,
          applyLinkTags: true,
          removeStyleTags: false,
          removeLinkTags: true
        }))
        .pipe(rename(function(path) {
          // remove dirname including email-src (allauth)
          var reg = /^(.+)\/([^/]+)\/email-src/i;
          path.dirname = path.dirname.replace(reg, '');
          path.extname='.email';
          return path;
        }))
        // .pipe(replace('**/email-src/', ''))
        .pipe(gulp.dest(paths.emails));
});

// Run django server
gulp.task('runServer', function(cb) {
  var cmd = spawn('python', ['manage.py', 'runserver'], {stdio: 'inherit'});
  cmd.on('close', function(code) {
    console.log('runServer exited with code ' + code);
    cb(code);
  });
});

// Browser sync server for live reload
gulp.task('browserSync', function() {
    browserSync.init(
      [paths.css + "/*.css", paths.js + "*.js", paths.templates + '*.html'], {
        proxy:  "localhost:8012"
    });
});

// Watch
gulp.task('watch', function() {

  gulp.watch(paths.sass + '/**/*.scss', ['styles']);
  gulp.watch(paths.js + '/*.js', ['scripts']).on("change", reload);
  gulp.watch(paths.images + '/*', ['imgCompression']);
  gulp.watch(paths.templates + '/**/*.html').on("change", reload);
  gulp.watch(paths.email_src + '/*.html', ['inlineCss']);
  gulp.watch(paths.email_src + '/styles.css', ['inlineCss']);

});

// Default task
gulp.task('default', function() {
    runSequence(['styles', 'scripts', 'vendor-scripts', 'imgCompression'], ['runServer', 'browserSync', 'watch']);
});
