#include <string>
#include <iostream>
#include <vector>
#include <fstream>
#include <cmath>


class Helpers {
public:
  // Split a string with the given single-character separator.
  static std::vector<std::string> split_string(
    const std::string& inString, 
    const std::string& separator
      );
  
  // Trim spaces from the beginning and end of a string.
  static std::string trim_string(std::string inString);
  
  static std::vector<int64_t> parse_list_of_integers(
    std::string to_parse, 
    std::string separator
    );
  
  static std::string join(std::vector<std::string> values_to_join, std::string separator);
  
  static std::vector<std::string> prepend(
    std::string item,
    std::vector<std::string> items
    );
  
  static std::vector<std::string> exclude(
    std::string element,
    std::vector<std::string> elements
    );
};


// Return a list of strings with the given item at the beginning.
std::vector<std::string> Helpers::prepend(
    std::string item,
    std::vector<std::string> items
    ) {
  std::vector<std::string> result;
  result.push_back(item);
  
  std::vector<std::string>::iterator it = items.begin();
  for(; it != items.end(); ++it) {
    result.push_back(*it);
  }
  
  return result;
}


// Return a list of strings excluding the given string 'element'.
std::vector<std::string> Helpers::exclude(
    std::string element,
    std::vector<std::string> elements
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

std::string Helpers::join(std::vector<std::string> values_to_join, std::string separator) {
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

std::string Helpers::trim_string(std::string inString) {
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

// ---------------------------------------------------------------------------------------------
// Main class that contains the custom problem logic.
class TaskRunner {
public:
  TaskRunner();
  
  // Initialize any state for this problem.
  void initialize();
  
  // Given a line, return the result to print.
  std::string evaluate(std::string line);
  
};

TaskRunner::TaskRunner() {
  
}

void TaskRunner::initialize() {
  // Initialize any state for this TaskRunner instance.
}

int64_t sum(std::vector<int64_t>& integers, int64_t start) {
  int64_t s = 0;
  for (int64_t i = start; i < integers.size(); i++) {
    s += integers.at(i);
  }
  return s;
}

// Get num_to_sum integers out of [start, ...)
std::vector<int64_t> sum_subset(std::vector<int64_t>& integers, int64_t num_to_sum, int64_t start) {
  std::vector<int64_t> to_return;
  if (num_to_sum == 0) {
    to_return.push_back(0);
    return to_return;
  }
  
  int64_t num_integers = integers.size() - start;
  int64_t num_leading = num_integers - (num_to_sum - 1);
  
  int64_t s, value;
  
  for (int64_t i = start; i < num_leading + start; i++) {
    value = integers.at(i);
    std::vector<int64_t> subsums = sum_subset(integers, num_to_sum - 1, i + 1);
    
    for (int64_t j = 0; j < subsums.size(); j++) {
      s = value + subsums.at(j);
      to_return.push_back(s);
    }
  }
  
  return to_return;
}

std::string TaskRunner::evaluate(std::string line) {
  std::vector<int64_t> integers = Helpers::parse_list_of_integers(line, std::string(","));
  std::vector<int64_t> sums = sum_subset(integers, 4, 0);
  
  int64_t count = 0;
  
  std::vector<int64_t>::iterator it = sums.begin();
  for(; it != sums.end(); ++it) {
    if (*it == 0) count ++;
  }
  
  return std::to_string(count);
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