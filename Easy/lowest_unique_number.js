var fs = require('fs');

(function Solution(fs){
  
  
  function count(list, value) {
    var result = 0;
    for (var i = 0; i < list.length; i++) {
      if (list[i] === value) result ++;
    }
    return result;
  }
  
  function evaluateLine(line) {
    var values = line.split(" ");
    values = values.map(Number);
    
    var unique = [];
    var value;
    for (var i = 0; i < values.length; i++) {
      if (count(values, values[i]) == 1) {
        unique.push(values[i]);
      }
    }
    
    unique.sort(function(a, b){ return Number(a) - Number(b); });
    
    var player = values.indexOf(unique[0]) + 1;
    console.log(player);
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
