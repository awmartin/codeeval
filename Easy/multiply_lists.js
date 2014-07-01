var fs = require('fs');

(function Solution(fs){
  
  
  function evaluateLine(line) {
    line = line.replace("| ", "")
    var values = line.split(" ");
    var result = [];
    var half = values.length / 2;
    for (var i = 0; i < half; i++) {
      result.push(values[i] * values[i + half]);
    }
    console.log(result.join(" "));
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
