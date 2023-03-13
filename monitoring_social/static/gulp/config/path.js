import * as nodePath from 'path';

const rootFolder = nodePath.basename(nodePath.resolve());

const buildFolder = './assets';
const assetsPath = './assets_src';

export const path = {
  build: {
    js: `${buildFolder}/js/`,
    css: `${buildFolder}/css/`,
  },
  src: {
    js: `${assetsPath}/ts/app.ts`,
    scss: `${assetsPath}/scss/styles.css`,
    svg: `${assetsPath}/img/**/*.svg`,
  },
  watch: {
    js: `${assetsPath}/ts/**/*.ts`,
    scss: `${assetsPath}/scss/**/*.css`,
    svg: `${assetsPath}/images/**/*.svg`,
  },
  clean: [`!${buildFolder}/**/*`, `!${buildFolder}/fonts`],
  srcFolder: assetsPath,
  rootFolder: rootFolder,
  ftp: '',
};

