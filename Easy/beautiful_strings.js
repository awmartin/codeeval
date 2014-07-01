var fs = require('fs');

(function Solution(fs){
  var allLetters = "abcdefghijklmnopqrstuvwxyz";
  
  function isLetter(char) {
    return contains(allLetters, char);
  }
  
  // Given a sentence, return a mapping from letters found to how many found.
  function getFrequencyTable(sentence) {
    var i = 0;
    var char;
    var table = {};
    
    for (i = 0; i < sentence.length; i++) {
      char = sentence[i];
      if (isLetter(char)) {
        if (char in table) {
          table[char] ++;
        } else {
          table[char] = 1;
        }
      } // end if isLetter
    }
    
    return table;
  }
  
  // Takes the mapping from letter to count and produces a mapping from count to list of letters.
  function invertFrequencyTable(letterToCount) {
    var countToLetters = {};
    for (var letter in letterToCount) {
      var count = letterToCount[letter];
      if (count in countToLetters) {
        countToLetters[count].push(letter);
      } else {
        countToLetters[count] = [letter];
      }
    }
    return countToLetters;
  }
  
  // Given the map from letters to count, return the highest count.
  function getMaxCount(letterToCount) {
    var maxCount = 0;
    for (var letter in letterToCount) {
      var count = letterToCount[letter];
      maxCount = Math.max(maxCount, count);
    }
    return maxCount;
  }
  
  // Return whether the given array contains the element.
  function contains(list, element) {
    return list.indexOf(element) !== -1;
  }
  
  function evaluateLine(line) {
    line = line.toLowerCase();
    
    var letterToCount = getFrequencyTable(line);
    var countToLetters = invertFrequencyTable(letterToCount);
    var maxCount = getMaxCount(letterToCount);
    
    // Combine all the letters in order from most frequent to least.
    var letters = [];
    for (var i = maxCount; i >= 1; i--) {
      if (i in countToLetters) {
        letters = letters.concat(countToLetters[i]);
      }
    }
    
    // console.log(letters.join(","))
    
    // Iterate over the sentence and use the 'letters' array to score each character.
    var score = 0;
    var char, index;
    for (var i = 0; i < line.length; i++) {
      char = line[i];
      if (isLetter(char)) {
        index = letters.indexOf(char);
        score += 26 - index;
      }
    }
    
    console.log(score);
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
