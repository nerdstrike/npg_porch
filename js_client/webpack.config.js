const path = require('path')
const HtmlWebPackPlugin = require('html-webpack-plugin')

module.exports = {
    entry: {
        index: './src/main.js'
    },
    plugins: [
        new HtmlWebPackPlugin({title: 'Porch Viewer'})
    ],
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].bundle.js',
        clean: true
    },
    devServer: {
        static: './dist'
    },
    mode: 'development',
    module: {
        rules: [
            {
                test: /\.(html|svelte)$/,
                use: 'svelte-loader'
            },
            {
                test: /node_modules\/svelte\/.*\.mjs$/,
                resolve: {
                  fullySpecified: false
                }
            }
        ]
    }
}
