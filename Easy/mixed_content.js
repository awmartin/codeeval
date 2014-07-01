var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    var values = line.split(",");
    var words = [];
    var numbers = [];
    values.forEach(function(value){
      if (isNaN(Number(value))) {
        words.push(value);
      } else {
        numbers.push(value);
      }
    });
    
    var result = words.join(",");
    if (words.length > 0 && numbers.length > 0)
       result += "|";
    result += numbers.join(",");
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
