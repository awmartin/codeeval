var fs = require('fs');

(function Solution(fs){
  
  function contains(set1, element) {
    return set1.indexOf(element) !== -1;
  }
  
  function intersection(set1, set2) {
    var tr = [];
    set1.forEach(function(element){
      if (contains(set2, element)) {
        tr.push(element);
      }
    });
    
    return tr.sort();
  }
  
  function evaluateLine(line) {
    var sets = line.split(";");
    var set1 = [];
    if (sets[0] != null && sets[0].length > 0)
      set1 = sets[0].split(",");
    var set2 = [];
    if (sets[1] != null && sets[1].length > 0)
      set2 = sets[1].split(",");
    
    console.log(intersection(set1, set2).join(","));
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
