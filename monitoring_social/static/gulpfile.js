import gulp from 'gulp';
import { path } from './gulp/config/path.js';
import { plugins } from './gulp/config/plugins.js';

global.app = {
  isBuild: process.argv.includes('--build'),
  isDev: !process.argv.includes('--build'),
  path: path,
  gulp: gulp,
  plugins: plugins,
};

import { reset } from './gulp/tasks/reset.js';
import { server } from './gulp/tasks/server.js';
import { scss } from './gulp/tasks/scss.js';
import { js } from './gulp/tasks/js.js';

function watcher() {
  gulp.watch(path.watch.scss, scss);
  gulp.watch(path.watch.js, js);

}

const mainTasks = gulp.series(scss, js);
const watchInBrowser = gulp.parallel(watcher, server);
const css = gulp.series(scss);

const dev = gulp.series(reset, mainTasks, watcher);
const build = gulp.series(reset, mainTasks);

export { dev };
export { build };
export { css };

gulp.task('css', css);
gulp.task('default', dev);
gulp.task('--dev', dev);
gulp.task('build', build);
