var fs = require('fs');

(function Solution(fs){
  
  function parsePair(pairString){
    var values = pairString.split("-");
    return [Number(values[0]), Number(values[1])];
  }
  
  function swap(list, a, b) {
    var c = list[a];
    list[a] = list[b];
    list[b] = c;
  }
  
  function evaluateLine(line) {
    if (line.length == 0) return;
    
    var input = line.split(":");
    var values = input[0].trim().split(" ");
    var pairs = input[1].trim().split(",");
    pairs = pairs.map(parsePair);
    
    pairs.forEach(function(pair){
      swap(values, pair[0], pair[1]);
    });
    
    console.log(values.join(" "));
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
