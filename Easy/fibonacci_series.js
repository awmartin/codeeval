var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    var num = Number(line);
    
    var sequence = [0, 1];
    
    for (var i = 2; i <= num; i++) {
      sequence.push(sequence[i - 1] + sequence[i - 2]);
    }
    
    console.log(sequence[num]);
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
