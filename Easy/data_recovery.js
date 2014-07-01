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
  
  
  function evaluateLine(line) {
    // Parse the input.
    var input = line.split(";");
    var words = input[0].split(" ");
    var indices = input[1].split(" ").map(Number);
    
    // Find the missing index.
    for (var i = 1; i <= words.length; i++) {
      if (!indices.contains(i)) {
        indices.push(i);
        break;
      }
    }
    
    // Create a mapping from index to word.
    var mapping = [];
    var pair;
    for (var i = 0; i < words.length; i++) {
      var index = indices[i];
      
      pair = [indices[i], words[i]];
      mapping.push(pair);
    }
    
    // Sort the mapping by index.
    mapping.sort(function(a, b){ return a[0] - b[0]; });
    
    var result = mapping.map(function(pair){ return pair[1]; });
    
    console.log(result.join(" "));
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
