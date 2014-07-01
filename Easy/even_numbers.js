var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    var mod = Number(line) % 2;
    if (mod === 0) {
      console.log("1");
    } else {
      console.log("0");
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
