var fs = require('fs');

(function Solution(fs){
  // Return whether the given array contains the element.
  function contains(list, element) {
    return list.indexOf(element) !== -1;
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
  
  function getPreferredPosition(line) {
    if (contains(line, "C")) {
      position = line.indexOf("C");
    } else if (contains(line, "_")) {
      position = line.indexOf("_");
    }
    return position;
  }
  
  String.prototype.replaceAt = function(index, char) {
    return this.substr(0, index) + char + this.substr(index+1, this.length - 1);
  }
  
  function drawPath(line, pos, nextPos) {
    if (pos === nextPos) {
      line = line.replaceAt(pos, "|");
    } else if (pos > nextPos) {
      line = line.replaceAt(pos, "\\");
    } else if (pos < nextPos) {
      line = line.replaceAt(pos, "/");
    }
    return line;
  }
  
  function print(x) {
    console.log(x);
  }
  
  function main(){
    var lines = FileReader.read(process.argv[2]);
    lines = lines.filter(function(line) { return line.length > 0; });
    
    var positions = lines.map(getPreferredPosition);

    for (var i = positions.length - 1; i >= 0; i --) {
      lines[i] = drawPath(lines[i], positions[i], positions[i-1]);
    }
    var end = lines.length - 1;
    lines[0] = lines[0].replaceAt(positions[0], "|");
    
    lines.forEach(print);
  }
  
  main();
})(fs);
