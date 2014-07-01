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


class Point {
public:
  Point(int64_t x, int64_t y);
  Point(const Point& other);

  double dist(Point other);
  
  static Point parse(std::string &pair);
  
  double x() const;
  double y() const;
  
private:
  int64_t mX, mY;
};

Point::Point(int64_t x, int64_t y) {
  mX = x;
  mY = y;
}

Point::Point(const Point& other) {
  mX = other.x();
  mY = other.y();
}

double Point::x() const {
  return mX;
}

double Point::y() const {
  return mY;
}

double Point::dist(Point other) {
  double dx = other.x() - x();
  double dy = other.y() - y();
  return sqrt(dx * dx + dy * dy);
}

// Parses (x, y) to a Point.
Point Point::parse(std::string &pair) {
  std::string without_parens = pair.substr(1, pair.size() - 2);
  
  std::vector<std::string> values = Helpers::split_string(without_parens, std::string(","));
  
  int64_t x = atof(values.at(0).c_str());
  int64_t y = atof(values.at(1).c_str());
  
  Point p(x, y);
  return p;
}


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
  
}

bool overlap(int64_t x1, int64_t x2, 
              int64_t x3, int64_t x4) {
  return !(x4 < x1 || x2 < x3);
}

std::string TaskRunner::evaluate(std::string line) {
  std::vector<int64_t> coords = Helpers::parse_list_of_integers(line, std::string(","));
  
  bool xs_overlap = overlap(coords.at(0), coords.at(2), coords.at(4), coords.at(6));    // xs
  bool ys_overlap = overlap(coords.at(3), coords.at(1), coords.at(7), coords.at(5));    // ys
  bool rectangles_overlap = xs_overlap && ys_overlap;
  
  if (rectangles_overlap) {
    return std::string("True");
  } else {
    return std::string("False");
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
        std::string result = runner.evaluate(lineBuffer);
        std::cout << result << std::endl;
      } else {
        first = false;
      }
      
    }
  }
  
  return 0;
}