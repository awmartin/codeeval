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


class Pair {
public:
  Pair(int x, int y);
  std::string to_string();
private:
  int64_t mX, mY;
};

Pair::Pair(int x, int y) {
  mX = x;
  mY = y;
}

std::string Pair::to_string(){
  std::string result;
  result.append(std::to_string(mX));
  result.append(std::string(","));
  result.append(std::to_string(mY));
  return result;
}

std::string TaskRunner::evaluate(std::string line) {
  std::vector<std::string> values = split_string(line, std::string(";"));
  
  std::vector<int64_t> integers = parse_list_of_integers(values.at(0), std::string(","));
  int64_t target_sum = atoi(values.at(1).c_str());
  
  std::vector<std::string> pairs;
  
  int64_t x, y;
  for (int64_t i = 0; i < integers.size() - 1; i++) {
    for (int64_t j = i + 1; j < integers.size(); j++) {
      x = integers.at(i);
      y = integers.at(j);
      if (x + y == target_sum) {
        Pair p(x,  y);
        pairs.push_back(p.to_string());
      }
    }
  }

  if (pairs.size() > 0) {
    return join(pairs, std::string(";"));
  } else {
    return std::string("NULL");
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