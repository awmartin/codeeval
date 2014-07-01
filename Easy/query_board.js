var fs = require('fs');

(function Solution(fs){
  
  var Board = function(){
    this.board = [];
    for (var r = 0; r < 256; r ++) {
      this.board.push([]);
      for (var c = 0; c < 256; c ++) {
        this.board[r].push(0);
      }
    }
  };
  
  Board.prototype.SetRow = function(i, x) {
    for (var c = 0; c < 256; c ++) {
      this.board[i][c] = x;
    }
    return null;
  };
  
  Board.prototype.SetCol = function(j, x) {
    for (var r = 0; r < 256; r ++) {
      this.board[r][j] = x;
    }
    return null;
  };
  
  Board.prototype.QueryRow = function(i) {
    var s = 0;
    for (var c = 0; c < 256; c ++) {
      s += this.board[i][c];
    }
    return s;
  };
  
  Board.prototype.QueryCol = function(j) {
    var s = 0;
    for (var r = 0; r < 256; r ++) {
      s += this.board[r][j];
    }
    return s;
  };
  
  
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
    var board = new Board();
    
    var evaluateLine = function(line) {
      var values = line.split(" ");
      
      var command = values[0];
      var arg1 = Number(values[1]);
      var arg2 = Number(values[2]);
      
      if (command.length == 0) return;
      
      var result = board[command](arg1, arg2);
      
      if (result !== null) {
        console.log(result);
      }
    };
    
    lines.forEach(evaluateLine);
  }
  
  main();
})(fs);
