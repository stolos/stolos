const webpack = require('webpack');
const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const validate = require('webpack-validator');

const PATHS = {
    src : path.resolve(__dirname, 'src'),
    js : path.resolve(__dirname, 'src', 'js'),
    css : path.resolve(__dirname, 'src', 'css'),
    node_modules : path.resolve(__dirname, 'node_modules'),
    build : path.resolve(__dirname, 'public')
};

function isExternal(module) {
    var userRequest = module.userRequest;

    if (typeof userRequest !== 'string') {
        return false;
    }

    return userRequest.indexOf('node_modules') >= 0;
}

var config = {
    devServer : {},
    entry : {
        app : [
            'index.jsx',
            'index.css'
        ],
        vendor : [
            'jquery',
            'bootstrap',
            'react',
            'react-dom',
            'react-router',
            'bootstrap/scss/bootstrap.scss',
            'font-awesome/scss/font-awesome.scss'
        ]
    },
    output : {
        path : PATHS.build,
        publicPath : '/static/dashboard/public/'
    },
    resolve : {
        root : [
            PATHS.js,
            PATHS.css
        ],
        extensions : ['', '.js', '.jsx', '.json', '.coffee', '.css']
    },
    module : {
        loaders : [
            {
                test : /\.css$/,
                loader : ExtractTextPlugin.extract('style-loader', 'css-loader')
            },
            {
                test : /\.scss$/,
                loader : ExtractTextPlugin.extract('style', 'css!sass')
            },
            {
                test : /\.png$/,
                loader : 'url-loader?limit=100000'
            },
            {
                test : /\.jpg$/,
                loader : 'file-loader'
            },
            {
                test : /\.gif$/,
                loader : 'file-loader'
            },
            {
                test : /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/,
                loader : 'url?limit=10000&mimetype=application/font-woff'
            },
            {
                test : /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
                loader : 'url?limit=10000&mimetype=application/octet-stream'
            },
            {
                test : /\.eot(\?v=\d+\.\d+\.\d+)?$/,
                loader : 'file'
            },
            {
                test : /\.svg(\?v=\d+\.\d+\.\d+)?$/,
                loader : 'url?limit=10000&mimetype=image/svg+xml'
            },
            {
                test : /\.jsx?$/,
                exclude : /node_modules/,
                loader : 'babel-loader',
                query : {
                    presets : ['react', 'es2015']
                }
            }
        ]
    },
    plugins : [
        new webpack.ProvidePlugin({
            $ : 'jquery',
            jQuery : 'jquery',
            'window.jQuery' : 'jquery',
            tether : 'tether',
            Tether : 'tether',
            'window.Tether' : 'tether',
        }),
        // Always expose NODE_ENV to webpack so you can use `process.env.NODE_ENV`
        // inside your code for any environment checks; UglifyJS will automatically
        // drop any unreachable code.
        // Way 1 to do this:
        // https://github.com/webpack/webpack/issues/2537#issuecomment-222363754
        // new webpack.DefinePlugin({
        // 	'process.env': {
        // 		'NODE_ENV': JSON.stringify(process.env.NODE_ENV)
        // 	}
        // })
        // Way 2 to do this
        // https://github.com/webpack/docs/wiki/list-of-plugins#environmentplugin
        new webpack.EnvironmentPlugin([
            'NODE_ENV'
        ]),
        /* Separate common modules from vendor modules */
        new webpack.optimize.CommonsChunkPlugin({
            name : 'common',
            minChunks : function(module, count) {
                return !isExternal(module) && count >= 2; // adjustable cond
            }
        }),
        new webpack.optimize.CommonsChunkPlugin({
            name : 'vendor',
            chunks : ['common'],
            // or if you have an key value object for your entries
            // chunks: Object.keys(entry).concat('common')
            minChunks : function(module) {
                return isExternal(module);
            }
        }),
        /************/
        new webpack.optimize.CommonsChunkPlugin({
            name : 'manifest',
            filename : 'manifest.js'
        })
    ]
};

if (process.env.NODE_ENV === 'production') {
    config.devtool = 'source-map';
    config.output.filename = '[name].bundle.js';
    // This is used for require.ensure. The setup
    // will work without but this is useful to set.
    config.output.chunkFilename = '[chunkhash].js';
    config.plugins.push(new webpack.optimize.UglifyJsPlugin({
        compress : {
            warnings : true,
        },
        output : {
            comments : false,
        },
    }));
    config.plugins.push(new ExtractTextPlugin('[name].css'));
} else {
    config.devtool = 'source-map';
    config.output.filename = '[name].bundle.js';
    config.debug = true;
    config.profile = true;
    config.plugins.push(new ExtractTextPlugin('[name].css'));
}

module.exports = validate(config);
