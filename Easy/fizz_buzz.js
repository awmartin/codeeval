var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    var elements = line.split(" ");
    
    var A = Number(elements[0]);
    var B = Number(elements[1]);
    var N = Number(elements[2]);
    
    var result = [];
    var i;
    for (i = 1; i <= N; i++) {
      if (i % A === 0 && i % B === 0) {
        result.push("FB");
      } else if (i % A === 0) {
        result.push("F");
      } else if (i % B === 0) {
        result.push("B");
      } else {
        result.push(i);
      }
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
