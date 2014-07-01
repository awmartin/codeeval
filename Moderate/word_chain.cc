#include <string>
#include <iostream>
#include <vector>
#include <fstream>
#include <cmath>


class TaskRunner {
public:
  TaskRunner();
  
  // Initialize the hard-coded tree for this problem.
  void initialize();
  
  // Split a string with the given single-character separator.
  std::vector<std::string> split_string(const std::string& inString, const std::string& separator);
  
  // Trim spaces from the beginning and end of a string.
  std::string trim_string(std::string inString);
  
  // Given a line, return the result to print.
  std::string evaluate(std::string line);
  
  std::vector<int64_t> parse_list_of_integers(
    std::string to_parse, 
    std::string separator
    );
  
  std::string join(std::vector<std::string> values_to_join, std::string separator);
};

TaskRunner::TaskRunner() {
  
}

void TaskRunner::initialize() {
  
}


// Return a list of strings with the given item at the beginning.
std::vector<std::string> prepend(std::string item, std::vector<std::string> items) {
  std::vector<std::string> result;
  result.push_back(item);
  
  std::vector<std::string>::iterator it = items.begin();
  for(; it != items.end(); ++it) {
    result.push_back(*it);
  }
  
  return result;
}


// Return a list of strings excluding the given string 'element'.
std::vector<std::string> exclude(std::string element, std::vector<std::string> elements) {
  std::vector<std::string> result;
  
  std::vector<std::string>::iterator it = elements.begin();
  for (; it != elements.end(); ++it) {
    if ((*it).compare(element) != 0) {
      result.push_back(*it);
    } // end if
  } // end for
  
  return result;
}


// Recursively get a chain of words.
std::vector<std::string> chain(std::string word, std::vector<std::string> words) {
  // Get all words that begin with the last letter of 'word'.

  char last_letter = word.back();
  
  std::vector<std::string> to_return;
  
  std::vector<std::string>::iterator it = words.begin();
  for(; it != words.end(); ++it) {
    char first_letter = (*it).front();
    
    if (first_letter == last_letter) {
      std::vector<std::string> remaining_words(exclude(*it, words));
      
      std::vector<std::string> words_in_chain = chain(*it, remaining_words);
      
      if (words_in_chain.size() > to_return.size()) {
        to_return = words_in_chain;
      }
    } // end if
    
  } // end for
  
  return prepend(word, to_return);
}


std::string TaskRunner::evaluate(std::string line) {
  std::vector<std::string> words = split_string(line, std::string(","));
  
  std::vector<std::string> longest;
  
  std::vector<std::string>::iterator it = words.begin();
  for(; it != words.end(); ++it) {
    std::vector<std::string> remaining_words(exclude(*it, words));
    
    std::vector<std::string> word_chain = chain(*it, remaining_words);
    if (word_chain.size() > longest.size()) {
      longest = word_chain;
    }
  }
  if (longest.size() == 1) {
    return std::string("None");
  } else {
    return std::to_string(longest.size());    
  }
}


std::vector<int64_t> TaskRunner::parse_list_of_integers(
  std::string to_parse, 
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

std::string TaskRunner::join(std::vector<std::string> values_to_join, std::string separator) {
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

std::string TaskRunner::trim_string(std::string inString) {
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

std::vector<std::string> TaskRunner::split_string(
    const std::string& inString,
    const std::string& separator
    ) {
  std::vector<std::string> values;
  
  int64_t k = 0;
  for (int64_t i=0; i < inString.length(); i ++) {
    
    bool found_separator = inString.substr(i, 1).compare(separator) == 0;
    bool is_last = i == inString.length() - 1;
    
    if (found_separator) {
      std::string value = inString.substr(k, i - k);
      k = i + 1;
      values.push_back(value);
      
    } else if (is_last) {
      // Last one.
      std::string value = inString.substr(k, i - k + 1);
      values.push_back(value);
      
    }
    
  }
  
  return values;
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
        std::string result = runner.evaluate(lineBuffer);
        std::cout << result << std::endl;
      } else {
        first = false;
      }
      
    }
  }
  
  return 0;
}