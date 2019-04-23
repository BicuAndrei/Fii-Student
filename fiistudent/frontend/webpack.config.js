const path = require('path');
const webpack = require('webpack');

const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

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
			},
			{
				test: /\.(html)$/,
				include: path.join(__dirname, 'src/pages'),
				use: {
					loader: 'html-loader',
					options: {
						interpolate: true
					}
				}
			}
		]
	},

	plugins: [
		new CleanWebpackPlugin(),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'pages', 'index.html'),
			filename: 'index.html'
		}),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'pages', 'schedule.html'),
			filename: 'schedule.html'
		}),
		new HtmlWebpackPlugin({

			template: path.join(__dirname, 'src', 'pages', 'subjects.html'),
			filename: 'subjects.html'
		}),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'pages', 'teachers.html'),
			filename: 'teachers.html'
		}),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'pages', 'free-rooms.html'),
			filename: 'free-rooms.html'

		}),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'pages', 'team.html'),
			filename: 'team.html'
		}),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'pages', 'about.html'),
			filename: 'about.html'
		}),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'pages', 'contact.html'),
			filename: 'contact.html'
		}),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'pages', 'settings.html'),
			filename: 'settings.html'
		}),
		new HtmlWebpackPlugin({
			template: path.join(__dirname, 'src', 'pages', 'services.html'),
			filename: 'services.html'
		})
	]
};
