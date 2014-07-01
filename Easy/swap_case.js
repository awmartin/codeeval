var fs = require('fs');

(function Solution(fs){
  
  var uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var lowercase = "abcdefghijklmnopqrstuvwxyz";
  
  // Return whether the given array contains the element.
  function contains(list, element) {
    return list.indexOf(element) !== -1;
  }
  
  function evaluateLine(line) {
    var tr = "";
    
    var char;
    for (var i = 0; i < line.length; i++) {
      char = line[i];
      if (contains(uppercase, char)) {
        tr += char.toLowerCase();
      } else if (contains(lowercase, char)) {
        tr += char.toUpperCase();
      } else {
        tr += char;
      }
    }
    
    console.log(tr);
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
