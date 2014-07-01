var fs = require('fs');

(function Solution(fs){

  function getLocation(station) {
    return Number(station.split(",")[1]);
  }
  
  function evaluateLine(line) {
    var stations = line.split(";");
    stations = stations.filter(function(x){ return x.length > 0; });
    
    var locations = [0].concat( stations.map(getLocation) );
    locations.sort(function(a, b){ return a - b; });

    var distances = [];
    for (var i = 0; i < locations.length - 1; i++) {
      distances.push(locations[i+1] - locations[i]);
    }
    var result = distances.join(",");
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
