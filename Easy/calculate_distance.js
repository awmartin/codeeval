var fs = require('fs');

(function Solution(fs){
  
  var Point = function(str) {
    var coords = str.split(",");
    this.x = Number(coords[0]);
    this.y = Number(coords[1]);
  };
  
  Point.prototype.distanceTo = function(pt) {
    var dx = pt.x - this.x;
    var dy = pt.y - this.y;
    return Math.sqrt(dx * dx + dy * dy);
  };
  
  function evaluateLine(line) {
    var pt1 = "";
    var pt2 = "";
    var first = true;
    
    var char;
    for (var i = 0; i < line.length; i++) {
      char = line[i];

      if (char == ')' && first) {
        first = false;
      } else if (first) {
        pt1 += char;
      } else {
        pt2 += char;
      }
      
    }
    
    var openParen = new RegExp('\\(', 'g');
    var closeParen = new RegExp('\\)', 'g');
    var clean = function(str) {
      return str.replace(openParen, '').replace(closeParen, '').trim();
    };
    
    pt1 = new Point(clean(pt1));
    pt2 = new Point(clean(pt2));
    
    console.log(pt1.distanceTo(pt2));
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
