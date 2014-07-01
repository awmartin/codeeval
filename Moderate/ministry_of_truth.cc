/**
 * Ministry of Truth
 */

#include <string>
#include <iostream>
#include <vector>
#include <fstream>
#include <cmath>
#include <algorithm>



// Helper class for string operations for all CodeEval submissions.
class Helpers {
public:
  // Split a string with the given single-character separator.
  static std::vector<std::string> split_string(
    const std::string& inString, 
    const std::string separator
    );
  
  // Trim spaces from the beginning and end of a string.
  static std::string trim_string(std::string& inString);
  
  // Parses a string that is a separated list of integers.
  static std::vector<int64_t> parse_list_of_integers(
    std::string& to_parse, 
    std::string separator
    );
  
  // Join a list of strings given a separator.
  static std::string join(
    std::vector<std::string>& values_to_join,
    std::string separator
    );
  
  // Join a list of integers given a separator.
  static std::string join_integers(
    std::vector<int64_t>& integers_to_join,
    std::string separator
    );
  
  // Return a list of strings with the given item at the beginning.
  static std::vector<std::string> prepend(
    std::string& item,
    std::vector<std::string>& items
    );
  
  // Return a list of strings excluding the given string 'element'.
  static std::vector<std::string> exclude(
    std::string& element,
    std::vector<std::string>& elements
    );
};



std::vector<std::string> Helpers::prepend(
    std::string& item,
    std::vector<std::string>& items
    ) {
  std::vector<std::string> result;
  result.push_back(item);
  
  std::vector<std::string>::iterator it = items.begin();
  for(; it != items.end(); ++it) {
    result.push_back(*it);
  }
  
  return result;
}



std::vector<std::string> Helpers::exclude(
    std::string& element,
    std::vector<std::string>& elements
    ) {
  std::vector<std::string> result;
  
  std::vector<std::string>::iterator it = elements.begin();
  for (; it != elements.end(); ++it) {
    if ((*it).compare(element) != 0) {
      result.push_back(*it);
    } // end if
  } // end for
  
  return result;
}


std::vector<int64_t> Helpers::parse_list_of_integers(
  std::string& to_parse, 
  std::string separator
  ) {
  std::vector<std::string> values_str = split_string(to_parse, separator);
  std::vector<int64_t> values;
  
  std::vector<std::string>::iterator it = values_str.begin();
  int64_t value;
  for (; it != values_str.end(); ++it) {
    value = atoi((*it).c_str());
    values.push_back(value);
  }
  
  return values;
}

std::string Helpers::join(std::vector<std::string>& values_to_join, std::string separator) {
  std::string result;
  
  for (int64_t i = 0; i < values_to_join.size(); i ++) {
    bool is_last = i == values_to_join.size() - 1;
    result.append(values_to_join.at(i));
    if (!is_last) {
      result.append(separator);
    }
  }
  
  return result;
}

std::string Helpers::join_integers(
    std::vector<int64_t>& integers_to_join, 
    std::string separator
    ) {
  std::string result;
  
  for (int64_t i = 0; i < integers_to_join.size(); i ++) {
    bool is_last = i == integers_to_join.size() - 1;
    result.append(std::to_string(integers_to_join[i]));
    if (!is_last) {
      result.append(separator);
    }
  }
  
  return result;
}

std::string Helpers::trim_string(std::string& inString) {
  int64_t start = 0, end = inString.size() - 1;
  
  // Trim spaces from the beginning.
  for (int64_t i = 0; i < inString.size(); i++) {
    if (inString[i] != ' ') {
      start = i;
      break;
    }
  }
  
  // Trim spaces from the end. TODO Also include end-of-line chars.
  for (int64_t i = inString.size() - 1; i >= 0; i--) {
    if (inString[i] != ' ') {
      end = i;
      break;
    }
  }
  
  return inString.substr(start, end - start + 1);
}

std::vector<std::string> Helpers::split_string(
    const std::string& inString,
    const std::string separator
    ) {
  std::vector<std::string> values;
  
  int64_t word_start = 0;
  int64_t word_stop = 0;
  for (int64_t i=0; i < inString.length(); i ++) {
    bool found_separator = inString.substr(i, 1).compare(separator) == 0;
    bool is_last = i == inString.length() - 1;
    
    if (found_separator) {
      // i = pos of separator char: hello___world
      //                                 ^
      
      if (i < (inString.size() - 1) && inString.substr(i + 1, 1).compare(separator) == 0) {
        // Next character is also a separator. Skip to the next character.

      } else {
        std::string value = inString.substr(word_start, word_stop);
        word_start = i + 1;
        word_stop = i + 1;
        values.push_back(value);
      }
      
    } else if (is_last) {
      // Last one.
      std::string value = inString.substr(word_start, word_stop);
      values.push_back(value);
      
    } else {
      word_stop = i + 1;
      
    }
    
  }
  
  return values;
}


// ---------------------------------------------------------------------------------------------


class Word {
public:
  Word(std::string word);
  Word(const Word& w);
  
  // Given a word, return this word with the missing letters as underscores.
  std::string getRedacted(Word& other);
  
  // Returns whether this word is equivalent to the given word.
  bool isEquivalent(Word& other);

  // Returns the string this Word wraps.
  const std::string* root() const;
private:
  std::string mWord;
};

Word::Word(std::string word) : mWord(word) {
  
}

Word::Word(Word& w) : mWord(*w.root()){

}

Word::Word(const Word& w) {
  mWord = *w.root();
}


const std::string* Word::root() const {
  return &mWord;
}

std::string Word::getRedacted(Word& other) {
  std::string tr;
  std::string::iterator it = mWord.begin();
  std::string::iterator other_it = other.root()->begin();
  
  for(; it != mWord.end(); ++it) {
    if (other_it < other.root()->end() && *it == *other_it) {
      tr.push_back(*it);
      ++other_it;
    } else {
      tr.push_back('_');
    }
  }
  
  return tr;
}

bool Word::isEquivalent(Word& other) {
  std::string::iterator it = mWord.begin();
  std::string::iterator other_it = other.root()->begin();
  
  for(; it != mWord.end(); ++it) {
    if (other_it != other.root()->end() && *it == *other_it) {
      ++ other_it;
    }
  }
  
  // Equivalent if we consumed every character in 'other'.
  return other_it == other.root()->end();
}


class Utterance {
public:
  Utterance(std::string words);
  
  // Whether this Utterance can be translated into the given one.
  bool isEquivalent(Utterance& other);
  
  std::vector<std::string> getRedacted(Utterance& other);
  
  Word* at(int64_t index);
  
  int64_t numWords();
  
private:
  std::vector<Word> mWords;
};

Utterance::Utterance(std::string words) {
  std::vector<std::string> strings = Helpers::split_string(words, std::string(" "));
  
  std::vector<std::string>::iterator it = strings.begin();
  for(; it != strings.end(); ++it) {
    mWords.push_back(Word(*it));
  }
}

Word* Utterance::at(int64_t index) {
  return &mWords.at(index);
}

int64_t Utterance::numWords() {
  return mWords.size();
}

bool Utterance::isEquivalent(Utterance& other) {
  int64_t j = 0;
  for (int64_t i = 0; i < numWords(); i ++) {
    if (j < other.numWords() && at(i)->isEquivalent(*other.at(j))) {
      j ++;
    }
  }
  return j == other.numWords();
}

std::vector<std::string> Utterance::getRedacted(Utterance& other) {
  int64_t j = 0;
  std::vector<std::string> result;
  
  for (int64_t i = 0; i < numWords(); i ++) {
    if (j < other.numWords() && at(i)->isEquivalent(*other.at(j))) {
      result.push_back(
        at(0)->getRedacted(*other.at(j))
        );
      j ++;
    }
  }
  
  return result;
}


// ---------------------------------------------------------------------------------------------
// Main class to run the solution.

class TaskRunner {
public:
  TaskRunner();
  
  // Initialize any state for this problem.
  void initialize();
  
  // Given a line, return the result to print.
  void evaluate(std::string line);
  
};

TaskRunner::TaskRunner() {
  // Placeholder constructor.
}

void TaskRunner::initialize() {
  // Initialize any state for this TaskRunner instance.
}


void TaskRunner::evaluate(std::string line) {

  std::vector<std::string> input = Helpers::split_string(line, std::string(";"));

  Utterance left(input[0]);
  Utterance right(input[1]);
  
  if (left.isEquivalent(right)) {
    std::vector<std::string> result(left.getRedacted(right));
    std::cout << Helpers::join(result, std::string(" ")) << std::endl;
  } else {
    std::cout << "I cannot fix history" << std::endl;
  }
  
}


int main(int argc, char *argv[]) {
  TaskRunner runner;
  runner.initialize();
  
  bool skip_first_line = false;
  bool first = true;
  
  std::ifstream file;
  file.open(argv[1]);
  while (!file.eof()) {
    std::string lineBuffer;
    
    std::getline(file, lineBuffer);
    
    if (lineBuffer.length() == 0) {
      continue;
    } else { 
      
      // Routine to skip the first line.
      if (!skip_first_line || (skip_first_line && !first)) {
        runner.evaluate(lineBuffer);
      } else {
        first = false;
      }
      
    }
    
  }
  
  return 0;
}