import webp from "gulp-webp";
import imagemin from "gulp-imagemin"
import debug from "gulp-debug"
import {createPathForDeploy, isDeploy} from "../config/sftp.js";


export const images = () => {
  return app.gulp.src(app.path.src.images)

    .pipe(app.plugins.plumber(
      app.plugins.notify.onError({
        title: "IMAGES",
        message: "Error: <%= error.message %>"
      })
    ))
    .pipe(app.plugins.newer(app.path.build.images))
    .pipe(app.gulp.dest(app.path.build.images))
    .pipe(app.gulp.src(app.path.src.images))
    .pipe(app.plugins.newer(app.path.build.images))
    .pipe(app.gulp.dest(app.path.build.images))
    .pipe(app.plugins.git.add())
    .pipe(app.plugins.if(isDeploy, app.plugins.sftp(createPathForDeploy('assets/images/'))))
    .pipe(app.plugins.browserSync.stream())
}
