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

// 1 2 1
// 1 3 3 1
// 1 4 6 4 1
std::vector<int64_t> next_row(std::vector<int64_t> previous_row) {
  std::vector<int64_t> new_row;
  new_row.push_back(1);
  
  for (int64_t i = 1; i <= previous_row.size(); i ++) {
    int64_t previous_value = previous_row.at(i - 1);
    
    int64_t current_value = 0;
    if (i < previous_row.size()) {
      current_value = previous_row.at(i);
    }
    
    new_row.push_back(previous_value + current_value);
  }
  
  return new_row;
}


std::string TaskRunner::evaluate(std::string line) {
  int64_t depth = atoi(line.c_str());
  
  std::string result;
  result.append(std::string("1 "));
  
  std::vector<int64_t> current_row;
  current_row.push_back(1);
  
  for (int64_t i = 1; i < depth; i ++) {
    std::vector<int64_t> next = next_row(current_row);
    
    std::vector<int64_t>::iterator it = next.begin();
    for(; it != next.end(); ++it) {
      result.append(std::to_string(*it));
      result.push_back(' ');
    }
    
    current_row = next;
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