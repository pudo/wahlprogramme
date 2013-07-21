express = require 'express'
_ = require 'underscore'
solr = require 'solr'
url = require 'url'
fs = require 'fs'

config =
  port: process.env.PORT or 3000
  solr: url.parse process.env.WEBSOLR_URL or 'http://localhost:8983/solr/wahlprogramme'

app = express()
app.use express.logger()
app.use express.compress()
app.use express.errorHandler()
app.use express.static __dirname + '/_site'
app.disable "x-powered-by"

getClient = () ->
  return solr.createClient
    host: config.solr.hostname
    port: config.solr.port or 80
    path: config.solr.path
    auth: config.solr.auth

indexAdd = (data, callback) ->
  add_options =
    overwrite: true
    commit: true
  client = getClient()
  client.add data, add_options, (err) ->
    if err?
      callback err
    client.commit (err) ->
      console.log 'Indexed: ' + data.key + ', ' + data.title
      callback err

indexQuery = (q, options, callback) ->
  options.fl = 'score,key,party'
  options.df = 'text'
  client = getClient()
  client.query q, options, (err, res) ->
    if err?
      try
        data = err.toString().substring 7
        err = JSON.parse(data).error
      catch fail
        err = 
          msg: err.toString()
      return callback null, err
    data = JSON.parse res
    return callback data, err


app.get '/reload', (req, res) ->
  fs.readFile 'data/sections.json', (err, raw) ->
    if err?
      res.jsonp 500, err

    data = JSON.parse raw
    #console.log data
    for [party, sections] in _.pairs data
      for section in sections
        data =
          title: section.title
          key: section.key
          id: section.key
          party: section.party
          topic: section.topic
          level: section.level
          body: section.texts.join '\n'

        #console.log data
        indexAdd data, (err) ->
          if err?
            console.warn err
    res.jsonp 200,
      status: 'ok',
    #  raw: raw


app.get '/status', (req, res) ->
  res.jsonp 200,
    status: 'ok'


app.get '/search', (req, res) ->
  options =
    rows: 4000
  indexQuery req.query.q, options, (data, err) ->
    if err?
      res.jsonp 500,
        status: 'error',
        error: err
    r = data.response
    r.status = 'ok'
    r.sections = {}
    for doc in r.docs
      r.sections[doc.key] = doc.score
    res.set 
      'Cache-Control': 'public; max-age=846000',
      'ETag': req.query.q + '/' + req.query.callback
    delete r.docs
    res.jsonp 200, r

app.listen config.port

