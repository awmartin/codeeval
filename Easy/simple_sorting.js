var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    var values = line.split(" ");
    
    var sortAsInteger = function(a, b){
      return Number(a) - Number(b);
    };
    values.sort(sortAsInteger);
    
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
