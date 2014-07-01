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

};

TaskRunner::TaskRunner() {
  
}

void TaskRunner::initialize() {
  
}


std::string TaskRunner::evaluate(std::string line) {
  std::vector<std::string> numbers = split_string(line, std::string(","));
  
  std::vector<int64_t> integers;
  std::vector<std::string>::iterator it = numbers.begin();
  for(; it != numbers.end(); ++it) {
    integers.push_back(atoi((*it).c_str()));
  }
  
  int64_t max_sum = -10000000;
  for(int64_t i = 0; i < integers.size(); i++) { // start
    for(int64_t j = i; j < integers.size(); j++) { // end
      
      int64_t s = 0;
      for(int64_t k = i; k <= j; k++) {
        s += integers.at(k);
      }
      max_sum = s > max_sum ? s : max_sum;
      
    }
  }
  
  return std::to_string(max_sum);
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