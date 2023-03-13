import replace from 'gulp-replace';
import plumber from 'gulp-plumber';
import notify from 'gulp-notify';
import browserSync from 'browser-sync';
import ifPlugin from 'gulp-if';
import postCss from 'gulp-postcss';
import newer from 'gulp-newer';
import nested from 'postcss-nested';
import short from 'postcss-short';
import assets from 'postcss-assets';
import presetEnv from 'postcss-preset-env';
import atImport from 'postcss-import';
import hexrgba from 'postcss-hexrgba';
import git from 'gulp-git';
import debug from 'gulp-debug';
import sftp from 'gulp-sftp-up4';
import alias from 'gulp-path-alias';


const srcFolder = `./src`;

export const plugins = {
	replace: replace,
	plumber: plumber,
	notify: notify,
	browserSync: browserSync,
	if: ifPlugin,
	postCss: postCss,
	nested: nested,
	assets: assets,
	presetEnv: presetEnv,
	atImport: atImport,
	hexrgba: hexrgba,
	newer: newer,
  git: git,
  debug: debug,
  sftp: sftp,
  alias: alias,
	processors: [
		atImport({}),
		nested,
		short,
		presetEnv(
			{
				stage: 1,
				autoprefixer: { grid: true },
				browsers: ['safari >= 8', 'last 10 version'],
			}
		),
		hexrgba,
		assets({
			loadPaths: [ // путь/пути к картинкам
				srcFolder + 'img/',
				srcFolder + 'img/icons/',
				srcFolder + 'img/bg/'],
			relativeTo: srcFolder + 'dist/css/' // путь к CSS файлу (конечному, если он после обработки меняется)
		})
	]
};
