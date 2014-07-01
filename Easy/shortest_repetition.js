var fs = require('fs');

(function Solution(fs){

  function evaluateLine(line) {
    var first = line[0];
    
    var next = line.slice(1,line.length).indexOf(first);
    if (next === -1) {
      console.log(line.length);
    } else {
      console.log(next + 1);
    }
    
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
