var fs = require('fs');

(function Solution(fs){
  
  function capitalize(word) {
    if (word.length == 0) { return word; }
    if (word.length == 1) { return word.toUpperCase(); }
    
    return word[0].toUpperCase() + word.slice(1, word.length);
  }
  
  function evaluateLine(line) {
    var words = line.split(" ");
    
    var result = [];
    words.forEach(function(word){
      result.push(capitalize(word));
    });
    
    console.log(result.join(" "));
  }
  
  var FileReader = {
    getLinesFromData: function(data) {
      return data.toString().split('\n');
    },
    
    read: function(filename) {
      var data = fs.readFileSync(process.argv[2]);
      var lines = FileReader.getLinesFromData(data);
      return lines;
    }
  };
  
  
  function main(){
    var lines = FileReader.read(process.argv[2]);
    lines.forEach(evaluateLine);
  }
  
  main();
})(fs);
