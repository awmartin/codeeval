var fs = require('fs');

(function Solution(fs){
  
  
  // ----------------------------------------------------------
  // Conveniences and Utilities
  
  Array.prototype.sum = function(){ return sum(this); };
  
  Number.prototype.apply = function(fun) { return fun(this); };

  Array.prototype.contains = function(element) {
    return this.indexOf(element) !== -1;
  };
  
  String.prototype.forEach = function(fun) {
    for (var i = 0; i < this.length; i ++) {
      fun(this[i]);
    }
  };

  // ----------------------------------------------------------
  // Main evaluation function.
  
  function binary_string_to_int(num) {
    var i = num.length - 1;
    var value = 0;
    while (i >= 0) {
      value += Number(num[i]) * Math.pow(2, (num.length - 1 - i));
      i -= 1;
    }
    return value;
  }
  
  function convertZerosToOnes(zeros) {
    var result = "";
    zeros.forEach(function(){
      result += "1";
    });
    return result;
  }
  
  function evaluateLine(line) {
    var sequence = line.split(" ");
    var result = "";
    
    for (var i = 0; i < sequence.length; i+=2) {
      var flag = sequence[i];
      var zeros = sequence[i+1];
      if (flag === '0') {
        result += zeros;
      } else if (flag === '00') {
        result += convertZerosToOnes(zeros);
      }
    }
    
    console.log(binary_string_to_int(result));
  }
  
  // ----------------------------------------------------------
  // File loading and execution.
  
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
    lines = lines.filter(function(line){ return line.length > 0; });
    lines.forEach(evaluateLine);
  }
  
  main();
})(fs);
