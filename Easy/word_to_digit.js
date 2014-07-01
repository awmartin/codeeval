var fs = require('fs');

(function Solution(fs){
  
  var digitToNumeral = {
    'zero': '0',
    'one': '1',
    'two' : '2',
    'three' : '3',
    'four' : '4',
    'five' : '5',
    'six' : '6',
    'seven' : '7',
    'eight' : '8',
    'nine' : '9'
  };
  
  function evaluateLine(line) {
    var digits = line.split(";");
    var result = "";
    var char;
    digits.forEach(function(digit){
      result += digitToNumeral[digit];
    });
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
