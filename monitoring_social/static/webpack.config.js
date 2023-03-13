import path from 'path';
import argv from 'yargs';
// import { fileURLToPath } from 'url';

// const __filename = fileURLToPath(import.meta.url);
const __dirname = '/';


const isDev = argv['dev'] === true;
const setModuleRules = () => {
  const arr = {
    test: /\.(jsx|tsx|ts|js)$/,
    exclude: /node_modules/,
    use:  ['babel-loader'],
  };
  if (isDev) {
    arr.use.push('eslint-loader');
  }
  return arr;
};
export default {
  watch: isDev,
  output: {
    filename: '[name].js',
    publicPath: '/assets/js/',
    chunkFilename: '[id].js',
    path: path.resolve('/assets/js/'),
  },
  plugins: [

  ],
  resolve: {
    extensions: ['.ts', '.js', '.jsx', '.tsx'],
  },
  // optimization: {
  //   splitChunks: {
  //     chunks: 'initial',
  //   },
  // },
  target: ['web', 'es5'],
  mode: isDev ? 'development' : 'production',
  devtool: isDev ? 'source-map' : false,
  optimization: {
    minimize: false,
  },
  module: {
    rules: [setModuleRules()],
  },
};
