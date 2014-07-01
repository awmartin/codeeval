var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    var i;
    var sum = 0;
    for (i = 0; i < line.length; i++) {
      sum += Number(line[i]);
    }
    console.log(sum);
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
