var fs = require('fs');

(function Solution(fs){
  
  var morseCode = {
    ".-"    : "A",
    "-.-."  : "C",
    "."	    : "E",
    "--."   : "G",
    ".."	  : "I",
    "-.-"	  : "K",
    "--"	  : "M",
    "---"	  : "O",
    "--.-"  : "Q",
    "..."	  : "S",
    "..-"	  : "U",
    ".--"	  : "W",
    "-.--"  : "Y",
    "-----" : "0",
    "..---" : "2",
    "....-" : "4",
    "-...." : "6",
    "---.." : "8",
    "-..."  : "B",	
    "-.."   : "D",	
    "..-."  : "F",	
    "...."  : "H",	
    ".---"  : "J",	
    ".-.."  : "L",	
    "-."    : "N",	
    ".--."  : "P",	
    ".-."   : "R",	
    "-"     : "T",	
    "...-"  : "V",	
    "-..-"  : "X",	
    "--.."  : "Z",	
    ".----" : "1",	
    "...--" : "3",	
    "....." : "5",	
    "--..." : "7",
    "----." : "9"
  };
  
  function evaluateLine(line) {
    var words = line.split("  ");
    var decoded = [];
    
    words.forEach(function(word){
      var result = "";
      var codes = word.split(" ");
      codes.forEach(function(code){
        if (code in morseCode) {
          result += morseCode[code];
        } else {
          result += code;
        }
      });
      decoded.push(result);
    });
    
    console.log(decoded.join(" "));
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
