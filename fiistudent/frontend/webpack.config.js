const path = require('path');

const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const FileIncludeWebpackPlugin = require('file-include-webpack-plugin')

module.exports = {
	mode: "development",
	entry: { main: './src/index.js' },
	output: {
		path: path.resolve(__dirname, 'dist'),
		filename: '[name].[chunkhash].js'
	},
	module: {
		rules: [
			{
				test: /\.js$/,
				exclude: /node_modules/,
				use: ["babel-loader", "eslint-loader"]
			},
			{
				test: /\.css$/,
				use: [
					'style-loader',
					{
						loader: 'css-loader',
						options: {
							sourceMap: true
						}
					},
				]
			},
			{
				test: /\.scss/,
				use: [
					'style-loader',
					{
						loader: 'css-loader',
						options: {
							sourceMap: true
						}
					},
					{
						loader: 'sass-loader',
						options: {
							sourceMap: true,
							includePaths: [path.join(__dirname, 'src')]
						}
					}
				]
			},
			{
				test: /\.(jpe?g|png|gif)$/,
				loader: 'file-loader',
				options: {
					name: '[path][name].[ext]'
				}
			}
		]
	},
	plugins: [
		new CleanWebpackPlugin(),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'index.html'),
			filename: 'index.html'
		}),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'pages', 'login.html'),
			filename: 'login.html'
		}),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'pages', 'register.html'),
			filename: 'register.html'
		})
	]
};