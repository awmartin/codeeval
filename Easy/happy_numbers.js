var fs = require('fs');

(function Solution(fs){
  
  // Return whether the given array contains the element.
  function contains(list, element) {
    return list.indexOf(element) !== -1;
  }
  
  // Return the next number in the happy number sequence.
  function nextInSequence(number) {
    number = String(number);
    
    var sum = 0;
    for (var i = 0;i < number.length; i ++) {
      sum += number[i] * number[i];
    }
    
    return sum;
  }
  
  function evaluateLine(line) {
    var number = Number(line);
    
    var sequence = [number];
    while (number !== 1) {
      number = nextInSequence(number);
      
      // If we see the same number again, we have a cycle, and the number is not happy.
      if (contains(sequence, number)) {
        console.log("0");
        return;
      }
      
      sequence.push(number);
    }
    
    // Happy!
    console.log("1");
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
