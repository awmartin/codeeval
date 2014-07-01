#include <string>
#include <iostream>
#include <vector>
#include <fstream>


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

};

TaskRunner::TaskRunner() {
  
}

void TaskRunner::initialize() {
  
}

std::string TaskRunner::evaluate(std::string line) {
  std::vector<std::string> values = split_string(line, std::string(","));
  
  std::string result;
  std::string haystack = trim_string(values.at(0));
  std::string chars_to_remove = trim_string(values.at(1));
  
  bool include;
  std::string::iterator haystack_it = haystack.begin();
  std::string::iterator remove_it;
  
  for(; haystack_it != haystack.end(); ++haystack_it) {
    include = true;
    
    // Have to reset the iterator.
    remove_it = chars_to_remove.begin();
    
    // Search through all the characters and flag as not to include if found.
    for(; remove_it != chars_to_remove.end(); ++remove_it) {
      if (*haystack_it == *remove_it) {
        include = false;
        break;
      }
    }
    
    if (include) {
      result.push_back(*haystack_it);
    }
  }
  
  return trim_string(result);
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
  
  std::ifstream file;
  file.open(argv[1]);
  while (!file.eof()) {
    std::string lineBuffer;
    
    std::getline(file, lineBuffer);
    
    if (lineBuffer.length() == 0) {
      continue;
    } else { 
      std::string result = runner.evaluate(lineBuffer);
      std::cout << result << std::endl;
    }
  }
  
  return 0;
}