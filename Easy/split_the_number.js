var fs = require('fs');

(function Solution(fs){
  // Return whether the given array contains the element.
  function contains(list, element) {
    return list.indexOf(element) !== -1;
  }
  
  function evaluateLine(line) {
    if (line.length === 0) return;
    
    var input = line.split(" ");
    var number = input[0];
    var instructions = input[1];
    
    var operation = "+";
    if (contains(instructions, '-')) {
      operation = "-";
    }
    
    var splitPoint = instructions.indexOf(operation);
    
    var left = number.slice(0, splitPoint);
    var right = number.slice(splitPoint, number.length);
    
    var result;
    if (operation === "+") {
      result = Number(left) + Number(right);
    } else {
      result = Number(left) - Number(right);
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
