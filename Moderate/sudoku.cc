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
  
  bool evaluate_grid(std::vector<int64_t> &board, int64_t size);
  bool evaluate_subgrids(std::vector<int64_t> &board, int64_t size);
  bool evaluate_subgrid(std::vector<int64_t> &subgrid, int64_t size);
};

TaskRunner::TaskRunner() {
  
}

void TaskRunner::initialize() {
  
}



std::string TaskRunner::evaluate(std::string line) {
  std::vector<std::string> values = split_string(line, std::string(";"));
  int64_t size = atoi(values.at(0).c_str());
  
  std::vector<std::string> board_str = split_string(values.at(1), std::string(","));
  std::vector<int64_t> board;
  std::vector<std::string>::iterator it = board_str.begin();
  
  int64_t value;
  for(; it != board_str.end(); ++it) {
    value = atoi((*it).c_str());
    board.push_back(value);
  }
  
  
  if (evaluate_grid(board, size) && evaluate_subgrids(board, size)) {
    return std::string("True");
  } else {
    return std::string("False");
  }
}

bool TaskRunner::evaluate_grid(std::vector<int64_t> &board, int64_t size) {
  // Assure that each row contains all expected digits, 1...size.
  
  std::vector<bool> digits;
  for (int64_t i = 0; i < size * size; i++) {
    digits.push_back(false);
  }
  int64_t pos, value;
  
  // Check rows.
  for (int64_t inner_row = 0; inner_row < size; inner_row++) {

    // Reset
    for (int64_t i = 0; i < size * size; i++) {
      digits[i] = false;
    }

    for (int64_t inner_col = 0; inner_col < size; inner_col++) {
      pos = inner_row * size + inner_col;
      value = board.at(pos);
      
      if (!digits[value - 1]) {
        digits[value - 1] = true;
      } else {
        return false;
      }
      
    }

  }
  
  
  // Check columns.
  for (int64_t inner_col = 0; inner_col < size; inner_col++) {
    
    // Reset
    for (int64_t i = 0; i < size * size; i++) {
      digits[i] = false;
    }

    for (int64_t inner_row = 0; inner_row < size; inner_row++) {
      pos = inner_row * size + inner_col;
      value = board.at(pos);
      
      if (!digits[value - 1]) {
        digits[value - 1] = true;
      } else {
        return false;
      }
      
    }
  }
  
  return true;
}

bool TaskRunner::evaluate_subgrids(std::vector<int64_t> &board, int64_t size) {
  int64_t subsize = sqrt(size);
  std::vector<std::vector<int64_t> > subgrids;  
  
  int64_t row, col, pos;
  
  // Across subgrids.
  for (int64_t outer_row = 0; outer_row < subsize; outer_row++) {
    for (int64_t outer_col = 0; outer_col < subsize; outer_col++) {
      
      std::vector<int64_t> subgrid;
      
      // Within a subgrid.
      for (int64_t inner_row = 0; inner_row < subsize; inner_row++) {
        for (int64_t inner_col = 0; inner_col < subsize; inner_col++) {
          
          row = outer_row * subsize + inner_row;
          col = outer_col * subsize + inner_col;
          pos = row * size + col;
          
          subgrid.push_back(board.at(pos));
        }
      }
      
      subgrids.push_back(subgrid);
      
    } // outer_col
  } // outer_row
  
  
  bool ok = true;
  // Evaluate the subgrids.
  std::vector<std::vector<int64_t> >::iterator it = subgrids.begin();
  for(; it != subgrids.end(); ++it) {
    ok = ok && evaluate_subgrid(*it, subsize);
  }
  return ok;
}

bool TaskRunner::evaluate_subgrid(std::vector<int64_t> &subgrid, int64_t size) {
  
  std::vector<bool> digits;
  for (int64_t i = 0; i < size * size; i++) {
    digits.push_back(false);
  }
  
  std::vector<int64_t>::iterator it = subgrid.begin();
  for (; it != subgrid.end(); ++it) {
    if (!digits[*it - 1]) {
      digits[*it - 1] = true;
    } else {
      return false;
    }
  }
  
  return true;
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