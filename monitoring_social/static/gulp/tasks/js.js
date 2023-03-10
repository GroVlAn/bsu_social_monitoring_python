import webpackStream from 'webpack-stream';
import webpack from 'webpack';
import webpackConfig from '../../webpack.config.js';

export const js = () => {
  return app.gulp
    .src(app.path.src.js, {sourcemap: app.isDev})
    .pipe(
      app.plugins.plumber(
        app.plugins.notify.onError({
          title: 'JS',
          message: 'Error: <%= error.message %>',
        }),
      ),
    )
    .pipe(
      webpackStream(webpackConfig),
      webpack,
    )
    .pipe(app.gulp.dest(app.path.build.js))
    .pipe(app.plugins.git.add())
    .pipe(app.plugins.browserSync.stream());
};
