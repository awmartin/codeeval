var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    var elements = line.split(",");
    var haystack = elements[0];
    var needle = elements[1];
    
    for (var i = haystack.length - 1; i >= 0; i --) {
      if (haystack[i] == needle) {
        console.log(i);
        return;
      }
    }
    
    console.log(-1);
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
