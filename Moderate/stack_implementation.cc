#include <string>
#include <iostream>
#include <vector>
#include <fstream>


template <class T>
class Stack {
public:
  Stack();
  
  // Push a new value onto the stack.
  void push(T* value);
  
  // Pop the top value off the stack and return it.
  T* pop();
  
  // Return the number of items on the stack.
  int64_t size();
  
private:
  std::vector<T*> stack;
};

template <class T>
Stack<T>::Stack() {
  
}

template <class T>
void Stack<T>::push(T* value) {
  stack.push_back(value);
}

template <class T>
T* Stack<T>::pop() {
  if (size() == 0) return 0;
  
  T* last = stack.back();
  stack.pop_back();
  return last;
}

template <class T>
int64_t Stack<T>::size() {
  return stack.size();
}



class TaskRunner {
public:
  TaskRunner();
  
  // Initialize the hard-coded tree for this problem.
  void initialize();
  
  std::vector<std::string> split_string(const std::string& inString, const std::string& separator);
  
  // Given a line, return the result to print.
  std::string evaluate(std::string line);

};

TaskRunner::TaskRunner() {
  
}

void TaskRunner::initialize() {
  
}

std::string TaskRunner::evaluate(std::string line) {
  std::vector<std::string> values = split_string(line, std::string(" "));
  
  Stack<std::string> stack;
  
  std::vector<std::string>::iterator it = values.begin();
  for(; it != values.end(); ++it) {
    stack.push(&(*it));
  }
  
  std::string result;
  
  int64_t num_values = stack.size();
  for (int64_t i = 0; i < num_values; i+=2 ){
    std::string value = *stack.pop();
    result.append(value);
    
    if (stack.size() > 1) {
      result.push_back(' ');
    }
    
    stack.pop();
  }
  
  return result;
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