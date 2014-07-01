var fs = require('fs');

(function Solution(fs){
  
  
  // ----------------------------------------------------------
  // Conveniences and Utilities
  
  Array.prototype.sum = function(){ return sum(this); };
  
  Number.prototype.apply = function(fun) { return fun(this); };

  // ----------------------------------------------------------
  // Main evaluation function.
  
  var uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var lowercase = "abcdefghijklmnopqrstuvwxyz";
  
  // Return whether the given array contains the element.
  function contains(list, element) {
    return list.indexOf(element) !== -1;
  }
  
  function evaluateLine(line) {
    var upperCount = 0;
    var lowerCount = 0;
    var char;
    for (var i = 0; i < line.length; i++) {
      char = line[i];
      if (contains(uppercase, char)) {
        upperCount ++;
      } else if (contains(lowercase, char)) {
        lowerCount ++;
      }
    }
    
    var upperPercentage = 100.0 * upperCount / (upperCount + lowerCount);
    var lowerPercentage = 100.0 * lowerCount / (upperCount + lowerCount);
    
    var result = "lowercase: " + lowerPercentage.toFixed(2) + " uppercase: " + upperPercentage.toFixed(2);
    console.log(result);
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
