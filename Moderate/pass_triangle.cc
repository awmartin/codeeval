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
  std::string evaluate(std::vector<std::string>& lines);
  
};

TaskRunner::TaskRunner() {
  // Placeholder constructor.
}

void TaskRunner::initialize() {
  // Initialize any state for this TaskRunner instance.
}

class Node {
public:
  Node(int64_t value);
  void add_left(Node* left);
  void add_right(Node* right);
  int64_t get_value();
  int64_t calculate();
  Node* get_left();
  Node* get_right();
private:
  int64_t mValue;
  Node* mLeft;
  Node* mRight;
  
  bool mHasAnswer;
  int64_t mSum;
};

Node::Node(int64_t value) : mValue(value), mLeft(0), mRight(0), mHasAnswer(false), mSum(0) {

}

void Node::add_left(Node* left) {
  mLeft = left;
}

void Node::add_right(Node* right) {
  mRight = right;
}

int64_t Node::get_value() {
  return mValue;
}

Node* Node::get_left() {
  return mLeft;
}

Node* Node::get_right() {
  return mRight;
}

int64_t Node::calculate() {
  if (mHasAnswer) {
    return mSum;
  }
  
  int64_t left_value = 0, right_value = 0;
  
  if (mLeft != 0) {
    left_value = mLeft->calculate();
  }
  if (mRight != 0) {
    right_value = mRight->calculate();
  }
  
  mSum = mValue + fmax(left_value, right_value);
  mHasAnswer = true;
  return mSum;
}

std::string TaskRunner::evaluate(std::vector<std::string>& lines) {
  std::vector<std::vector<int64_t> > values;
  
  std::vector<std::string>::iterator it = lines.begin();
  for(; it != lines.end(); ++it) {
    values.push_back(Helpers::parse_list_of_integers(*it, std::string(" ")));
  }
  
  std::vector<Node> nodes;
  
  int64_t value;
  for (int64_t i = 0; i < values.size(); i ++) {
    std::vector<int64_t>* row = &values.at(i);
    
    for (int64_t j = 0; j < row->size(); j++) {
      value = row->at(j);
      Node n(value);
      nodes.push_back(n);
    }
  }
    
  // 0  1 2  3 4 5  6 7 8 9
  // 0 - 1 2
  // 1 - 3 4, 2 - 4 5
  // 3 - 6 7, 4 - 7 8, 5 - 8 9
  
  int64_t start = 0;
  for (int64_t upper = 1; upper < values.back().size(); upper ++) {
    
    for (int64_t i = 0; i < upper; i ++) {
      Node* n = &nodes.at(start + i);
      
      Node* left  = &nodes.at(start + i + upper);
      Node* right = &nodes.at(start + i + upper + 1);
      
      n->add_left(left);
      n->add_right(right);
    }
    
    start += upper;
  }
  
  Node root(nodes.at(0));
  return std::to_string(root.calculate());
}


int main(int argc, char *argv[]) {
  TaskRunner runner;
  runner.initialize();
  
  bool skip_first_line = false;
  bool first = true;
  
  std::vector<std::string> to_evaluate;
  
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
        to_evaluate.push_back(lineBuffer);
      } else {
        first = false;
      }
      
    }

  }
  
  std::string result = runner.evaluate(to_evaluate);
  std::cout << result << std::endl;
  
  return 0;
}