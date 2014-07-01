var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    var values = line.split(",");
    var n = Number(values[0]);
    var m = Number(values[1]);
    
    var multiple;
    for (multiple = 0; multiple < n; multiple += m) {}
    if (multiple > n)
      multiple -= m;
    
    console.log(n - multiple);
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
