var fs = require('fs');

(function Solution(fs){
  
  var letters = {
    'a' : 0,
    'b' : 1,
    'c' : 2,
    'd' : 3,
    'e' : 4,
    'f' : 5,
    'g' : 6,
    'h' : 7,
    'i' : 8,
    'j' : 9
  };
  
  // Return whether the given array contains the element.
  function contains(list, element) {
    return list.indexOf(element) !== -1;
  }
  
  function evaluateLine(line) {
    var digits = "0123456789";
    var char;
    var result = "";
    
    for (var i = 0; i < line.length; i++){
      char = line[i];
      
      if (char in letters) {
        result += letters[char];
      } else if (contains(digits, char)) {
        result += char;
      } else {
        // ignore.
      }
    }
    
    if (result.length === 0) {
      console.log("NONE");
    } else {
      console.log(result);
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
