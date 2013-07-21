var lunr = require('lunr'),
    fs = require('fs');

fs.readFile('stopwords.de.txt', function (err, raw) {
  var sw = raw.toString().split('\n').sort();
  lunr.stopWordFilter.stopWords.length = sw.length;
  lunr.stopWordFilter.stopWords.elements = sw;
  fs.readFile('./data/lunr.json', function (err, raw) {
    if (err) throw err;
    var data = JSON.parse(raw);
    var idx = lunr.Index.load(data);
    var results = idx.search('wohlstand');
    console.log(results);
  });
});