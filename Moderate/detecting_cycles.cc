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
    const std::string separator
    );
  
  // Trim spaces from the beginning and end of a string.
  static std::string trim_string(std::string& inString);
  
  static std::vector<int64_t> parse_list_of_integers(
    std::string& to_parse, 
    std::string separator
    );
  
  static std::string join(
    std::vector<std::string>& values_to_join,
    std::string separator
    );
  
  static std::vector<std::string> prepend(
    std::string& item,
    std::vector<std::string>& items
    );
  
  static std::vector<std::string> exclude(
    std::string& element,
    std::vector<std::string>& elements
    );
};


// Return a list of strings with the given item at the beginning.
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


// Return a list of strings excluding the given string 'element'.
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
  std::string evaluate(std::string& line);
  
};

TaskRunner::TaskRunner() {
  // Placeholder constructor.
}

void TaskRunner::initialize() {
  // Initialize any state for this TaskRunner instance.
}

class Tuple {
public:
  Tuple(int64_t x, int64_t y, int64_t z);
  int64_t mX, mY, mZ;
};

Tuple::Tuple(int64_t x, int64_t y, int64_t z) : mX(x), mY(y), mZ(z) {
  
}

Tuple find_first(std::vector<int64_t>& elements, int64_t start) {
  int64_t tortoise = start, hare = start + 1;
  
  if (tortoise >= elements.size() || hare >= elements.size()) { 
    return Tuple(-1, -1, -1);
  }

  bool found = true;
  // Tortoise and Hare pointers advance, with the hare twice as fast as the tortoise.
  while (elements.at(tortoise) != elements.at(hare)) {
    tortoise++;
    hare+=2;
    if (tortoise >= elements.size() || hare >= elements.size()) { 
      found = false;
      break;
    }
  }
  
  if (!found) {
    return find_first(elements, start + 1);
  } else {
    return Tuple(tortoise, hare, start);
  }
}

std::string find_loop(std::vector<int64_t>& elements) {
  // Implementation of the tortoise/hare algorithm found at
  // http://en.wikipedia.org/wiki/Cycle_detection
  
  Tuple tup = find_first(elements, 0);
  if (tup.mX == -1 || tup.mY == -1) return std::string("");
  
  int64_t hare = tup.mY;
  // int64_t offset = tup.mZ;
  
  // Attempt to find mu, the first element of the first cycle.
  int64_t mu = tup.mX;
  int64_t tortoise = tup.mX;  // x0

  // while (elements.at(tortoise) != elements.at(hare)) {
  //   hare ++;
  //   tortoise ++;
  //   
  //   if (tortoise >= elements.size() || hare >= elements.size()) { break; }
  //   
  //   mu ++;
  // }
  
  
  // Find the length of the cycle, lambda.
  int64_t lam = 1;
  hare = tortoise + 1;
  while (elements.at(tortoise) != elements.at(hare)) {
    hare++;
    if (tortoise >= elements.size() || hare >= elements.size()) { break; }
    lam ++;
  }
  
  // Use mu and lambda to get the elements in the cycle.
  std::vector<std::string> result;
  for (int64_t i = mu; i < mu + lam; i++) {
    result.push_back(std::to_string(elements.at(i)));
  }
  
  return Helpers::join(result, std::string(" "));
}


std::string TaskRunner::evaluate(std::string& line) {
  std::vector<int64_t> elements = Helpers::parse_list_of_integers(line, std::string(" "));
  return find_loop(elements);
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
        if (result.size() > 0)
          std::cout << result << std::endl;
      } else {
        first = false;
      }
      
    }
  }
  
  return 0;
}