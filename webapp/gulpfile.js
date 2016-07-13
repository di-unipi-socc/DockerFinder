
var path = require('path');
var gulp = require('gulp');
var ts = require('gulp-typescript');

gulp.task('buildServer', function () {
	var tsProject = ts.createProject(path.resolve('./public/app/tsconfig.json'));
	return gulp.src(path.resolve('./public/app/**/*.ts'))
		.pipe(ts(tsProject))
		.js
		.pipe(gulp.dest(path.resolve('./public/app')))
});