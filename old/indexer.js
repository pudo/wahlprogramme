var lunr = require('lunr'),
    fs = require('fs');



fs.readFile('stopwords.de.txt', function (err, raw) {
    var sw = raw.toString().split('\n').sort();
    lunr.stopWordFilter.stopWords.length = sw.length;
    lunr.stopWordFilter.stopWords.elements = sw;
    var idx = lunr(function () {
      this.ref('id');
      this.field('title', { boost: 10 });
      this.field('topic', { boost: 100 });
      this.field('party', { boost: 100 });
      this.field('text');
    });
    //return;
    fs.readFile('./data/sections.json', function (err, raw) {
      if (err) throw err;
      var data = JSON.parse(raw);

      var sections = [];
      for (var party in data) {
        for (var section_id in data[party]) {
            var section = data[party][section_id];
            idx.add({
                'id': section.key,
                'title': section.title,
                'topic': section.topic,
                'party': party,
                'text': section.texts.join('\n')
            });
            //console.log(section);
        }
      }


        fs.writeFile('./data/lunr.json', JSON.stringify(idx), function (err) {
            if (err) throw err;
            console.log('done');
        });
    });
});