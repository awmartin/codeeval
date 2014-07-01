var fs = require('fs');

(function Solution(fs){
  
  function toBinary(number) {
    var i = number;
    var bits = [];
    while (i !== 0 && i !== 1) {
      var bit = i % 2;
      bits.push(bit);
      i = Math.floor(i / 2);
      if (i === 1) {
        bits.push(i);
      }
    }
    
    return bits;
  }
  
  function evaluateLine(line) {
    var elements = line.split(",");
    
    var target = Number(elements[0]);
    var p1 = Number(elements[1]);
    var p2 = Number(elements[2]);
    
    var bits = toBinary(target);
    var same = bits[p1 - 1] === bits[p2 - 1];
    if (same) {
      console.log("true");
    } else {
      console.log("false");
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
