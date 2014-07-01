var fs = require('fs');

(function Solution(fs){
  
  var millisPerYear = 365 * 24 * 60 * 60 * 1000;
  var millisPerAvgMonth = 30 * 24 * 60 * 60 * 1000;
  
  // Return whether the given array contains the element.
  function contains(list, element) {
    return list.indexOf(element) !== -1;
  }
  
  // String.trim for map().
  function trim(x) {
    return x.trim();
  }
  
  // Parse a date range string into two dates.
  function parseRange(range) {
    var dates = range.split("-");
    var parsedDates = dates.map(Date.parse);
    parsedDates[1] += millisPerAvgMonth;
    return parsedDates;
  }
  
  // Given an array of date pairs, return the min of the left-hand date.
  function getMin(ranges){
    var result = Date.parse("Jan 2015");
    ranges.forEach(function(val){
      result = Math.min(val[0], result);
    });
    return result;
  }

  // Given an array of date pairs, return the max of the right-hand date.
  function getMax(ranges){
    var result = 0;
    ranges.forEach(function(val){
      result = Math.max(val[1], result);
    });
    return result;
  }
  
  function overlap(range1, range2) {
    return !(range1[1] < range2[0] || range2[1] < range1[0]);
  }
  
  function collapse(range1, range2) {
    var left = Math.min(range1[0], range2[0]);
    var right = Math.max(range1[1], range2[1]);
    return [left, right];
  }
  
  function collapseOverlappingRanges(ranges) {
    var newRanges = [];
    
    var consumed = false;
    ranges.forEach(function(range){
      consumed = false;
      
      newRanges.map(function(collapsedRange){
        if (overlap(range, collapsedRange)) {
          consumed = true;
          return collapse(range, collapsedRange);
        } else {
          return collapsedRange;
        }
      });
      
      if (!consumed) {
        newRanges.push(range);
      }
      
    });
    return newRanges;
  }
  
  function calculateDuration(range) {
    var diff = range[1] - range[0];
    var numMonths = diff / millisPerAvgMonth;
    // console.log("numMonths = " + numMonths);
    return Math.round(numMonths);
  }
  
  function sum(array) {
    var s = 0;
    array.forEach(function(val) { s += val; });
    return s;
  }
  
  function prettyPrintDate(date){
    return (new Date(date)).toDateString();
  }
  
  function printRange(range){
    return range.map(prettyPrintDate);
  }
  
  // ----------------------------------------------------------
  
  Array.prototype.sum = function(){ return sum(this); };
  
  Number.prototype.apply = function(fun) { return fun(this); };

  // ----------------------------------------------------------
  
  // Main evaluation function.
  function evaluateLine(line) {
    var range_strings = line.split(";").map(trim);
    
    ranges = range_strings.map(parseRange);
    
    ranges = collapseOverlappingRanges(ranges);

    var durations = ranges.map(calculateDuration);
    
    var monthsToYears = function(n){
      return n / 12;
    };
    durations = durations.map(monthsToYears);
    
    console.log(durations.sum().apply(Math.floor));
  }
  
  // ----------------------------------------------------------
  
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
    lines = lines.filter(function(line){ return line.length > 0; });
    lines.forEach(evaluateLine);
  }
  
  main();
})(fs);
