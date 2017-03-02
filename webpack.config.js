var path = require("path");

module.exports = {
  devtool: "source-map",
  resolve: {
    root: path.join(__dirname, "xwing_rulebook", "static"),
    alias: {}
  },
  entry: {
    "main": ['babel-polyfill', "scripts/main"],
  },
  output: {
    path: path.join(__dirname, "xwing_rulebook", "static", "build"),
    filename: "[name].js",
    sourceMapFilename: '[file].map',
    publicPath: "/static/build/"
  },
  plugins: [

  ],
  module: {
    loaders: [
      {
        test: /\.(js|jsx)$/,
        loader: 'babel-loader?presets[]=react,presets[]=es2015,presets[]=stage-0',
      },
    ]
  }
}
