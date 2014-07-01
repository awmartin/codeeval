var fs = require('fs');

(function Solution(fs){
  function size(thing) {
    return thing.length;
  }
  
  function evaluateLine(line) {
    var words = line.split(" ");
    
    var longest = "";
    words.forEach(function(word){
      if (word.length > longest.length) {
        longest = word;
      }
    });
    
    console.log(longest);
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
