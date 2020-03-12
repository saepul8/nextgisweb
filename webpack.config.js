const path = require('path');
const fs = require('fs');
const glob = require('glob');
const exec = require('child_process');

const WebpackAssetsManifest = require('webpack-assets-manifest');

function collectPackageEntry(package) {
    const result = [];
    for (const compPath of glob.sync(`node_modules/@${package}/*`)) {
        const compIdentity = compPath.split('/').slice(-1)[0];
        const packageJson = JSON.parse(fs.readFileSync(compPath + '/package.json'));
        if ('entry' in packageJson) {
            for (const compEntry of packageJson.entry) {
                result.push(`@${package}/${compIdentity}/${compEntry}`);
            }
        }
    }
    return result;
}

const ngwBuildConfig = JSON.parse(exec.execFileSync(
    'nextgisweb', ['webpack.build_config'], {
        encoding: 'utf-8'
    }
));

const entry = {};
const entryRules = [];

const creqLoaderPath = path.resolve(__dirname, 'creq-loader.js');

for (const package of ngwBuildConfig.packages) {
    const pname = package.name; 
    const ppath = package.path;
    for (const e of collectPackageEntry(pname)) {
        const entryFile = require.resolve(e);   
        entry[e] = entryFile;
        entryRules.push({
            test: entryFile,
            use: [{
                loader: creqLoaderPath,
                options: { entry: e }
            }]
        });
    }
}


module.exports = {
    mode: 'development',
    devtool: 'source-map',
    entry: entry,
    module: {
        rules: entryRules,
    },
    plugins: [
        new WebpackAssetsManifest({ entrypoints: true }),
    ],
    output: {
        filename: '[name].js',
        chunkFilename: 'cdata/[chunkHash].js',
        path: path.resolve('./', 'dist'),
        libraryTarget: 'amd',
    },
    externals: [
        function(context, request, callback) {
            // External nextgisweb AMD module from package
            for (const amd of ngwBuildConfig.amd_packages) {
                if (request.startsWith(amd + '/')) {
                    return callback(null, "amd " + request);    
                }
            }
            
            // ADM-style chunk loader from manifest.json
            if (/^cload[\/\!]/.test(request)) {
                return callback(null, "amd " + request);
            }
            
            callback();
        }
    ],
    optimization: {
        splitChunks: {
            chunks: 'all'
        },
    },    
}