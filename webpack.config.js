const LodashModuleReplacementPlugin = require("lodash-webpack-plugin");
const path = require("path");
const plugins = [new LodashModuleReplacementPlugin()];

module.exports = (env, argv) => {
  const config = {
    entry: "./sudokuop/frontend/src/index.js",
    output: {
      path: path.resolve(__dirname, "./sudokuop/frontend/static/frontend/")
    },
    resolve: {
      extensions: [".tsx", ".ts", ".js", ".json"]
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          include: path.resolve(__dirname, "./sudokuop/frontend/src/"),
          use: {
            loader: "babel-loader"
          }
        },
        {
          test: /\.tsx?$/,
          exclude: /node_modules/,
          include: path.resolve(__dirname, "./sudokuop/frontend/src/"),
          use: {
            loader: "babel-loader"
          }
        }
      ]
    },
    watchOptions: {
      ignored: /node_modules/
    },
    plugins: plugins,
    externals: { react: "React", "react-dom": "ReactDOM" }
  };
  if (argv.mode === "development") {
    config.devtool = "eval-source-map";
  }
  return config;
};
