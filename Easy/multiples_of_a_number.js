var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    var elements = line.split(",");
    
    var target = Number(elements[0]);
    var n = Number(elements[1]);
    
    var x = n;
    while (x < target) {
      x += n;
    }
    console.log(x);
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
