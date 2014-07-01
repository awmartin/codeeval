#include <string>
#include <iostream>
#include <vector>
#include <fstream>
#include <cmath>
#include <algorithm>

// Helper class for string operations for all CodeEval submissions.
class Helpers {
public:
  // Split a string with the given single-character separator.
  static std::vector<std::string> split_string(
    const std::string& inString, 
    const std::string separator
    );
  
  // Trim spaces from the beginning and end of a string.
  static std::string trim_string(std::string& inString);
  
  // Parses a string that is a separated list of integers.
  static std::vector<int64_t> parse_list_of_integers(
    std::string& to_parse, 
    std::string separator
    );
  
  // Join a list of strings given a separator.
  static std::string join(
    std::vector<std::string>& values_to_join,
    std::string separator
    );
  
  // Join a list of integers given a separator.
  static std::string join_integers(
    std::vector<int64_t>& integers_to_join,
    std::string separator
    );
  
  // Return a list of strings with the given item at the beginning.
  static std::vector<std::string> prepend(
    std::string& item,
    std::vector<std::string>& items
    );
  
  // Return a list of strings excluding the given string 'element'.
  static std::vector<std::string> exclude(
    std::string& element,
    std::vector<std::string>& elements
    );
};



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

std::string Helpers::join_integers(
    std::vector<int64_t>& integers_to_join, 
    std::string separator
    ) {
  std::string result;
  
  for (int64_t i = 0; i < integers_to_join.size(); i ++) {
    bool is_last = i == integers_to_join.size() - 1;
    result.append(std::to_string(integers_to_join[i]));
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

int64_t levenshtein_distance(std::string& word_a, std::string& word_b, int64_t i, int64_t j) {
  // key = (word_a, word_b, i, j)
  // if key in self.cache:
  //     return self.cache[key]
  
  if (fmin(i, j) == 0) {
    return fmax(i, j);
  } else {
    int64_t deletion = levenshtein_distance(word_a, word_b, i - 1, j) + 1;
    // key = (word_a, word_b, i - 1, j)
    // if key not in self.cache:
    //     self.cache[key] = deletion - 1

    int64_t insertion = levenshtein_distance(word_a, word_b, i, j - 1) + 1;
    // key = (word_a, word_b, i, j - 1)
    // if key not in self.cache:
    //     self.cache[key] = insertion - 1
    
    int64_t indicator;
    if (word_a[i - 1] == word_b[j - 1]) {
      indicator = 0;
    } else {
      indicator = 1;
    }
    
    int64_t match = levenshtein_distance(word_a, word_b, i - 1, j - 1) + indicator;
    // key = (word_a, word_b, i - 1, j - 1)
    // if key not in self.cache:
    //     self.cache[key] = match - indicator
    
    return fmin(fmin(deletion, insertion), match);
  }
}

int64_t levenshtein_distance(std::string& word_a, std::string& word_b) {
  return levenshtein_distance(word_a, word_b, word_a.size(), word_b.size());
}

class Word {
public:
  Word(std::string* rootWord);
  
  // Return the root word given at construction time.
  std::string* root();
  
  // Add a friend to this word. Lev dist = 1.
  void add_friend(Word* w);
  
  // Construct the social network by adding this Word's friends and their friends, etc.
  void social_network(std::vector<Word*>& net);

private:
  std::string* mRootWord;
  std::vector<Word*> mFriends;
};

Word::Word(std::string* rootWord) : mRootWord(rootWord) {
  
}

std::string* Word::root() {
  return mRootWord;
}

void Word::add_friend(Word* w) {
  mFriends.push_back(w);
}

void Word::social_network(std::vector<Word*>& net) {
  std::vector<Word*>::iterator it = mFriends.begin();
  
  for (; it != mFriends.end(); ++it) {
    bool alreadyInNetwork = std::find(net.begin(), net.end(), *it) != net.end();
    if (!alreadyInNetwork) {
      net.push_back(*it);
      (*it)->social_network(net);
    }
  } // end for
  
}


class Network {
public:
  Network(std::vector<std::string>& words);
  void initialize_network();
  void add_friends_of_word(Word& word);
  
private:
  
  std::vector<Word> mWords;
};

Network::Network(std::vector<std::string>& words) {
  std::vector<std::string>::iterator it = words.begin();
  for(; it != words.end(); ++it) {
    mWords.push_back(Word(&(*it)));
  }
  
  // Initialize the network by computing all the friends of all the words.
  initialize_network();
}

void Network::initialize_network() {
  std::vector<Word>::iterator it = mWords.begin();
  for(; it != mWords.end(); ++it) {
    add_friends_of_word(*it);
  }
}

void Network::add_friends_of_word(Word& word) {
  std::vector<Word>::iterator it = mWords.begin();
  
  for(; it != mWords.end(); ++it) {
    int64_t dist = levenshtein_distance(*word.root(), *(*it).root());
    if (dist == 1) {
      word.add_friend(&*it);
    }
  } // end for
}


// ---------------------------------------------------------------------------------------------
// Main class to run the solution.

class TaskRunner {
public:
  TaskRunner();
  
  // Initialize any state for this problem.
  void initialize();
  
  // Given a line, return the result to print.
  void evaluate(std::vector<std::string>& lines);
  
};

TaskRunner::TaskRunner() {
  // Placeholder constructor.
}

void TaskRunner::initialize() {
  // Initialize any state for this TaskRunner instance.
}


void TaskRunner::evaluate(std::vector<std::string>& lines) {
  // -------------------------------------------------------
  // Parse
  std::vector<std::string> test_cases;
  std::vector<std::string> words;
  
  bool gatheringWords = false;
  std::string splitter("END OF INPUT");
  
  std::vector<std::string>::iterator it = lines.begin();

  for(; it != lines.end(); ++it) {
    
    if (gatheringWords) {
      words.push_back(*it);
    } else if ((*it).compare(splitter) == 0) {
      gatheringWords = true;
    } else {
      test_cases.push_back(*it);
    }

  }
  
  // -------------------------------------------------------
  // Build the network.
  
  Network network(words);
  
  // -------------------------------------------------------
  // Loop through all the test cases and calculate the network size for each.
  
  std::vector<Word*> word_social_network;
  
  std::vector<std::string>::iterator test = test_cases.begin();
  for(; test != test_cases.end(); ++test) {
    word_social_network.clear();
    
    Word test_case_word(&*test);
    
    // Determine the immediate friends of this word.
    network.add_friends_of_word(test_case_word);
    
    // Calculate the entire social network for the word.
    test_case_word.social_network(word_social_network);
    
    std::cout << word_social_network.size() << std::endl;
  }
  
}


int main(int argc, char *argv[]) {
  TaskRunner runner;
  runner.initialize();
  
  bool skip_first_line = false;
  bool first = true;
  
  std::vector<std::string> lines;
  
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
        lines.push_back(lineBuffer);
      } else {
        first = false;
      }
      
    }
    
  }
  
  runner.evaluate(lines);
  
  return 0;
}