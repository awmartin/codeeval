var fs = require('fs');

(function Solution(fs){
  
  var romanNumerals = [
    [1000, 'M'],
    [900, 'CM'],
    [500, 'D'],
    [400, 'CD'],
    [100, 'C'],
    [90, 'XC'],
    [50, 'L'],
    [40, 'XL'],
    [10, 'X'],
    [9, 'IX'],
    [5, 'V'],
    [4, 'IV'],
    [1, 'I']
  ];
  
  function evaluateLine(line) {
    var cardinal = Number(line);
    
    var roman = "";
    while (cardinal > 0) {
      
      for (var i = 0; i < romanNumerals.length; i++) {
        var map = romanNumerals[i];
        var num = map[0];
        if (cardinal >= num) {
          roman += map[1];
          cardinal -= num;
          break;
        }
      } // end for
      
    } // end while
    
    console.log(roman);
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
