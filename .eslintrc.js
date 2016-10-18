module.exports = {
    "extends": "eslint:recommended",
    "parser": "espree",
    "parserOptions": {
        "ecmaVersion" : 6,
        "sourceType" : "module",
        "ecmaFeatures" : {
            "jsx" : true
        }
    },
    "rules": {
        "semi" : ["error", "always"],
        "no-undef" : "warn",
        "no-unused-vars" : "warn",
        "indent" : "error",
        "key-spacing" : ["warn", { "beforeColon" : true }],
        "no-console" : "warn"
    },
    "globals" : {
    },
    "env": {
        "browser" : true,
        "node" : true,
        "commonjs" : true
    }
};
