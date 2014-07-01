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
  
  static std::string join_integers(
    std::vector<int64_t>& integers_to_join,
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


class Point {
public:
  Point();
  Point(double x, double y);
  
  double slope_to(Point* other);
  double dist_to(Point* other);
  bool equals(Point& other);
  bool isNull();
  
  double x();
  double y();
  
  std::string to_string();
  
private:
  double mX;
  double mY;
  bool mIsNull;
};

Point::Point() {
  mIsNull = true;
}

bool Point::isNull() {
  return mIsNull;
}

Point::Point(double x, double y) : mX(x), mY(y) {
  mIsNull = false;
}

std::string Point::to_string() {
  std::string tr = std::string("Point(");
  tr.append(std::to_string(mX));
  tr.append(std::string(","));
  tr.append(std::to_string(mY));
  tr.append(std::string(")"));
  return tr;
}

double Point::x() {
  return mX;
}

double Point::y() {
  return mY;
}

double Point::slope_to(Point* other) {
  double dx = other->x() - mX;
  double dy = other->y() - mY;
  return dy / dx;
}

double Point::dist_to(Point* other) {
  double dx = other->x() - mX;
  double dy = other->y() - mY;
  return sqrt(dx * dx + dy * dy);
}

bool Point::equals(Point& other) {
  return other.x() == mX && other.y() == mY;
}


class Segment {
public:
  Segment(Point start, Point stop);
  
  Point line_through(Point* start, Point* stop);
  Point intersection(Point* pt1, Point* pt2, Point* pt3, Point* pt4);
  Point intersection_segment(Point* pt1, Point* pt2, Point* pt3, Point* pt4);
  
  std::string to_string();
  
private:
  Point mStart;
  Point mStop;
};

Segment::Segment(Point start, Point stop): mStart(start), mStop(stop) {
  
}

std::string Segment::to_string() {
  std::string tr = std::string("Segment(");
  tr.append(mStart.to_string());
  tr.append(std::string(","));
  tr.append(mStop.to_string());
  tr.append(std::string(")"));
  return tr;
}

Point Segment::line_through(Point* start, Point* stop) {
  return intersection_segment(start, stop, &mStart, &mStop);
}

Point Segment::intersection_segment(Point* pt1, Point* pt2, Point* pt3, Point* pt4) {
  Point pt(intersection(pt1, pt2, pt3, pt4));
  
  double segment_length = pt3->dist_to(pt4);
  
  double dist3 = pt.dist_to(pt3);
  double dist4 = pt.dist_to(pt4);
  
  if (dist3 + dist4 == segment_length) {
    return pt;
  } else {
    return Point();
  }
}

Point Segment::intersection(Point* pt1, Point* pt2, Point* pt3, Point* pt4) {
  double denominator = 
      ((pt1->x() - pt2->x()) * (pt3->y() - pt4->y()) - 
       (pt1->y() - pt2->y()) * (pt3->x() - pt4->x()));
  
  if (denominator == 0) {
    // Parallel lines
    return Point();
  }
  
  double x = 
      ((pt1->x() * pt2->y() - pt1->y() * pt2->x()) * (pt3->x() - pt4->x()) - 
       (pt1->x() - pt2->x()) * (pt3->x() * pt4->y() - pt3->y() * pt4->x())) /
      denominator;
  
  double y = 
      ((pt1->x() * pt2->y() - pt1->y() * pt2->x()) * (pt3->y() - pt4->y()) -
       (pt1->y() - pt2->y()) * (pt3->x() * pt4->y() - pt3->y() * pt4->x())) /
      denominator;
  
  return Point(x, y);
}



class Block {
public:
  Block(int64_t street1, int64_t street2, int64_t avenue1, int64_t avenue2);
  bool line_through(Point* pt1, Point* pt2);
private:
  Point mBottomLeft;
  Point mBottomRight;
  Point mTopLeft;
  Point mTopRight;
  std::vector<Segment> mSegments;
};


Block::Block(int64_t street_left, int64_t street_right, int64_t avenue_bottom, int64_t avenue_top) :
    mBottomLeft(Point(street_left, avenue_bottom)),
    mBottomRight(Point(street_right, avenue_bottom)),
    mTopLeft(Point(street_left, avenue_top)),
    mTopRight(Point(street_right, avenue_top))
  {
    mSegments.push_back( Segment(mBottomLeft,  mTopLeft)     );
    mSegments.push_back( Segment(mTopLeft,     mTopRight)    );
    mSegments.push_back( Segment(mTopRight,    mBottomRight) );
    mSegments.push_back( Segment(mBottomRight, mBottomLeft)  );
  }

bool Block::line_through(Point* pt1, Point* pt2) {
  std::vector<Point> pts;
  
  std::vector<Segment>::iterator it = mSegments.begin();
  for(; it != mSegments.end(); ++it) {
    Point pt((*it).line_through(pt1, pt2));
    if (!pt.isNull()) {
      pts.push_back(pt);
    }
  }
  
  bool tr;
  if (pts.size() == 2) {
    
    if (pts[0].equals(pts[1])) {
      // Corner case.
      tr = false;
    } else {
      tr = true;
    }
    
  } else if (pts.size() > 0) {
    tr = true;
  } else {
    tr = false;
  }

  return tr;
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

std::string TaskRunner::evaluate(std::string& line) {
  std::vector<std::string> input = Helpers::split_string(line, std::string(" "));
  
  // first = streets, second = avenues
  std::string streets_string(input[0].substr(1, input[0].size() - 2));
  std::string avenues_string(input[1].substr(1, input[1].size() - 2));

  std::vector<int64_t> streets = 
    Helpers::parse_list_of_integers(streets_string, std::string(","));
  std::vector<int64_t> avenues = 
    Helpers::parse_list_of_integers(avenues_string, std::string(","));
  
  std::vector<Block> blocks;
  
  int64_t i = 0;
  int64_t j;
  while (i < streets.size() - 1) {
    j = 0;
    while (j < avenues.size() - 1) {
      blocks.push_back(
        Block(streets[i], streets[i+1], avenues[j], avenues[j+1])
        );
      j++;
    }
    i++;
  }
  
  Point start(streets.front(), avenues.front());
  Point stop(streets.back(), avenues.back());

  int64_t count(0);
  std::vector<Block>::iterator it = blocks.begin();
  for(; it != blocks.end(); ++it) {
    if ((*it).line_through(&start, &stop)) {
      count ++;
    }
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
        if (result.size() > 0)
          std::cout << result << std::endl;
      } else {
        first = false;
      }
      
    }
  }
  
  return 0;
}