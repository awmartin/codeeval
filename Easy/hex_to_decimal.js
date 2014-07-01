var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    var values = {
      '0' : 0,
      '1' : 1,
      '2' : 2,
      '3' : 3,
      '4' : 4,
      '5' : 5,
      '6' : 6,
      '7' : 7,
      '8' : 8,
      '9' : 9,
      'a' : 10,
      'b' : 11,
      'c' : 12,
      'd' : 13,
      'e' : 14,
      'f' : 15
    };
    
    var i;
    var result = 0;
    for (i = 0; i < line.length; i++) {
      var char = line[line.length - 1 - i];
      var value = values[char];
      
      var mag = Math.pow(16, i);
      
      result += value * mag;
    }
    console.log(result);
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
