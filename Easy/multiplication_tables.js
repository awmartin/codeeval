
(function Solution(){
  
  function formatElement(number) {
    number = String(number);
    var numLeadingSpaces = 4 - number.length;
    var tr = "";
    for (var i = 0; i < numLeadingSpaces; i++) {
      tr += " ";
    }
    tr += number;
    return tr;
  }
  
  function main() {
    var row;
    
    for (var i = 1; i <= 12; i ++) {
      row = "";
      for (var j = 1; j <= 12; j ++) {
        row += formatElement(i * j);
      }
      console.log(row.trim());
    }
    
  }
  
  main();
})();