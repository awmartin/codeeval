var fs = require('fs');

(function Solution(fs){
  
  function evaluateLine(line) {
    if (line.length == 0) return;
    
    var data = line.split("|");
    var encodedName = data[0];
    var keys = data[1].trim().split(" ");
    
    var name = "";
    keys.forEach(function(key){
      name += encodedName[Number(key) - 1];
    });
    
    console.log(name);
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
