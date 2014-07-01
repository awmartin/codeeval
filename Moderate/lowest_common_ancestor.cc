#include <iostream>
#include <vector>
#include <fstream>


class Node {
public:
  // Initialize a Node with the given value.
  Node(int value);
  Node(const Node& other);
  
  // Adds another child node, at the right, to this Node.
  void add_child(Node& child);
  
  // Return whether this Node has child nodes.
  bool has_children() const;
  
  // Sets the parent of this node.
  void set_parent(Node& parent);
  
  // Return a list of this node's children, left to right.
  std::vector<Node*> get_children() const;
  
  // Retrieves a child of this Node by index.
  Node* get_child(int64_t index);
  
  // Return the value of this node.
  int value() const;
  
  // Return this node's parent.
  Node* parent() const;
  
  // Whether this node is the root node.
  bool is_root();
  
  // Finds the first node in the tree with the given value, depth-first search, 
  // left-side precedence.
  Node* find(int value);
  
  // Returns all the ancestors of this node.
  std::vector<Node*> ancestors();
  
private:
  // The Node's parent.
  Node* mParent;
  
  // The value the node holds.
  int mValue;
  
  // The list of Node children.
  std::vector<Node*> mChildren;
};


Node::Node(int value) {
  mValue = value;
  mParent = 0;
};

Node::Node(const Node& other){
  mValue = other.value();
  mChildren = other.get_children();
  mParent = other.parent();
}

std::vector<Node*> Node::get_children() const {
  return mChildren;
}

void Node::add_child(Node& child) {
  mChildren.push_back(&child);
  child.set_parent(*this);
}

bool Node::has_children() const {
  return mChildren.size() > 0;
}

Node* Node::get_child(int64_t index) {
  return mChildren.at(index);
}

int Node::value() const {
  return mValue;
}

Node* Node::parent() const {
  return mParent;
}

void Node::set_parent(Node& parent) {
  mParent = &parent;   // variable in body, &=address of
}

bool Node::is_root() {
  return mParent == 0;
}

Node* Node::find(int value) {
  if (value == this->value()) {
    return this;
  }
  
  std::vector<Node*>::iterator it = mChildren.begin();
  
  for (; it != mChildren.end(); ++ it) {
    
    if ((*it)->value() == value) {
      return *it;
    } else {
      if ((*it)->has_children()) {
        Node* found = (*it)->find(value);
        if (found) {
          return found;
        }
      } // end check for children
      
    }
  }
  
  return 0;
}

std::vector<Node*> Node::ancestors() {
  std::vector<Node*> result;
  
  result.push_back(this);
  
  Node* n = (*this).parent();
  while (n) {
    result.push_back(n);
    n = n->parent();
  }
  
  return result;
};



class TaskRunner {
public:
  TaskRunner();
  
  // Initialize the hard-coded tree for this problem.
  void initialize();
  
  // Given a string of integers (e.g. "8 50") return a list of Nodes.
  std::vector<Node*> nodes_from_string(const std::string& inString);
  
  // Given a string of two integers, return the value of the common ancestor of the 
  // corresponding Nodes.
  int64_t evaluate(std::string line);
private:
  Node* root;
};

TaskRunner::TaskRunner() {
}

void TaskRunner::initialize() {
  // Build the tree.
  root = new Node(30);
  
  static Node left1(8);
  static Node right1(52);
  root->add_child(left1);
  root->add_child(right1);
  
  static Node left2(3);
  static Node right2(20);
  left1.add_child(left2);
  left1.add_child(right2);
  
  static Node left3(10);
  static Node right3(29);
  right2.add_child(left3);
  right2.add_child(right3);
}

int64_t TaskRunner::evaluate(std::string line) {
  std::vector<Node*> nodes = nodes_from_string(line);
  
  std::vector<Node*> ancestors_left = nodes.at(0)->ancestors();
  std::vector<Node*> ancestors_right = nodes.at(1)->ancestors();
    
  std::vector<Node*>::iterator left_it = ancestors_left.begin();
  for (; left_it != ancestors_left.end(); ++left_it) {
    
    std::vector<Node*>::iterator right_it = ancestors_right.begin();
    for (; right_it != ancestors_right.end(); ++right_it) {
      
      if ((*left_it)->value() == (*right_it)->value()) {
        return (*left_it)->value();
      }
    }
  }
  
  return -1;
}

std::vector<Node*> TaskRunner::nodes_from_string(const std::string& inString) {
  std::vector<std::string> values;
  std::string space(" ");
  
  int64_t k = 0;
  for (int64_t i=0; i < inString.length(); i ++) {
    if (inString.substr(i, 1).compare(space) == 0) {
      std::string value = inString.substr(k, i - k);
      k = i;
      values.push_back(value);
    } else if (i == inString.length() - 1) {
      // Last one.
      std::string value = inString.substr(k, i - k + 1);
      values.push_back(value);
    }
  }
  
  
  std::vector<Node*> result;
  std::vector<std::string>::iterator it = values.begin();
  for (; it != values.end(); ++it) {
    int64_t value = atoi((*it).c_str());
    Node* n = root->find(value);
    if (n) {
      result.push_back(n);
    }
  }

  return result;
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
      std::cout << runner.evaluate(lineBuffer) << std::endl;
    }
  }
  
  return 0;
}
