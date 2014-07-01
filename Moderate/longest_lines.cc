#include <string>
#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>


class TaskRunner {
public:
  TaskRunner();
  
  // Initialize the hard-coded tree for this problem.
  void initialize();
  
  // Split a string with the given single-character separator.
  std::vector<std::string> split_string(const std::string& inString, const std::string& separator);
  
  // Trim spaces from the beginning and end of a string.
  std::string trim_string(std::string inString);
  
  // Given the entire file, return a list of strings to print.
  std::vector<std::string> evaluate(std::vector<std::string> lines);

};

TaskRunner::TaskRunner() {
  
}

void TaskRunner::initialize() {
  
}

bool sort_by_size(std::string a, std::string b) { 
  return a.size() > b.size();
}

std::vector<std::string> TaskRunner::evaluate(std::vector<std::string> lines) {
  
  int64_t num_lines_to_show = atoi(lines.at(0).c_str());
  
  lines.erase(lines.begin());   // Remove the first element.
  
  std::sort(lines.begin(), lines.end(), sort_by_size);
  
  std::vector<std::string> result;
  for (int64_t i = 0; i < num_lines_to_show; i++) {
    result.push_back(trim_string(lines.at(i)));
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
  
  std::vector<std::string> lines;
  
  std::ifstream file;
  file.open(argv[1]);
  while (!file.eof()) {
    std::string lineBuffer;
    
    std::getline(file, lineBuffer);
    
    if (lineBuffer.length() == 0) {
      continue;
    } else {
      lines.push_back(lineBuffer);
    }
  }
  
  
  std::vector<std::string> result = runner.evaluate(lines);
  std::vector<std::string>::iterator it = result.begin();
  
  for (; it != result.end(); ++it) {
    std::cout << *it << std::endl;
  }
  
  return 0;
}