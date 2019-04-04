'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  APP_URL: '"http://localhost:2323/"',
  API_URL: '"http://localhost:5000/"'
})
