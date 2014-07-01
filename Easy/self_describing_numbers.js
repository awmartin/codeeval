var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    var counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    
    var digit;
    for (var i = 0; i < line.length; i++) {
      digit = Number(line[i]);
      counts[digit] ++;
    }
    
    for (var i = 0; i < line.length; i++) {
      digit = Number(line[i]);
      
      if (counts[i] != digit) {
        console.log("0");
        return
      }
    }
    
    console.log("1");
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
