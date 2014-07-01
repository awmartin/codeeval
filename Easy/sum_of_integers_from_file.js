var fs = require('fs');

(function Solution(fs){
  
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
    var sum = 0;
    lines.forEach(function(line){ sum += Number(line); });
    console.log(sum);
  }
  
  main();
})(fs);
