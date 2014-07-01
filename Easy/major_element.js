var fs = require('fs');

(function Solution(fs){
  // Return whether the given array contains the element.
  function contains(list, element) {
    return list.indexOf(element) !== -1;
  }
  
  function evaluateLine(line) {
    if (line.length === 0) return;
    
    var values = line.split(",");
    
    var counts = {};
    var major = null;
    values.forEach(function(value){
      if (value in counts) {
        counts[value] ++;
        
        if (counts[value] > values.length / 2) {
          major = value;
        }
        
      } else {
        counts[value] = 1;
      }
    });
    
    if (major === null) {
      console.log("None");
    } else {
      console.log(major);
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
