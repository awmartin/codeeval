var fs = require('fs');

(function Solution(fs){

  
  function evaluateLine(line) {
    var valuesToCompress = line.split(" ").map(Number);
    
    var result = [];
    var count = 1;
    var currentValue = valuesToCompress[0];
    var value;
    
    for (var i = 1; i < valuesToCompress.length; i++) {
      value = valuesToCompress[i];
      
      if (value === currentValue) {
        count ++;
      } else if (value !== currentValue) {
        result.push(count);
        result.push(currentValue);
        
        currentValue = valuesToCompress[i];
        count = 1;
      }
      
    } // end for
    
    result.push(count);
    result.push(currentValue);
    
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
