const path = require('path');

const fs = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

function generateHtmlPlugins(templateDir) {
	const templateFiles = fs.readdirSync(path.resolve(__dirname, templateDir)).filter(function (file) {
		if (file.indexOf(".html") > -1) {
			return file;
		}
	});

	return templateFiles.map(item => {
		const parts = item.split('.');
		const name = parts[0];
		const extension = parts[1];

		return new HtmlWebpackPlugin({
			filename: `${name}.html`,
			template: path.resolve(__dirname, `${templateDir}/${name}.${extension}`)
		});
	})
}

const htmlPlugins = generateHtmlPlugins('./src/pages');

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
		new CleanWebpackPlugin()
	].concat(htmlPlugins)
};
