var fs = require('fs');

(function Solution(fs){
  
  function hasLabelKey(json) {
    for (var key in json) {
      var value = json[key];
      if (key === "label" && value !== null) {
        return true;
      }
    }
    return false;
  }
  
  function evaluateLine(line) {
    if (line.length === 0) return;
    
    var json = JSON.parse(line);
    
    var menu = json.menu;
    if (menu === null) { console.log(0); return; }
    
    var items = menu.items;
    if (items === null) { console.log(0); return; }
    
    var sum = 0;
    items.forEach(function(itemJson){
      if (itemJson === null) return;
      
      var hasLabel = hasLabelKey(itemJson);
      if ('id' in itemJson && hasLabel) {
        sum += itemJson.id;
      }
    });
    console.log(sum);
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
