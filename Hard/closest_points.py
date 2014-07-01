import sys
import math

class PointSet(object):
    def __init__(self):
        self.points = []
    
    def add_point(self, pt):
        self.points.append(pt)

class Point(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    @classmethod
    def dist(self, pt1, pt2):
        dx = pt1.x - pt2.x
        dy = pt1.y - pt2.y
        return math.sqrt(dx*dx + dy*dy)

class Parser(object):
    @classmethod
    def is_count(cls, line):
        return len(line.split(" ")) == 1
    
    @classmethod
    def is_point(cls, line):
        return len(line.split(" ")) == 2
    
    @classmethod
    def is_end(cls, line):
        return line == '0'

class ClosestPoints(object):
    def __init__(self):
        self.point_sets = []
        
    def evaluate(self, lines):
        point_set = None
        for line in lines:
            line = Util.sanitize_line(line)
            
            if Parser.is_count(line):
                if point_set is not None:
                    self.point_sets.append(point_set)
                if Parser.is_end(line):
                    break
                
                count = 0
                point_set = PointSet()
                continue
            
            x, y = line.split(" ")
            pt = Point(x, y)
            point_set.add_point(pt)
        
        for point_set in self.point_sets:
            dist = self.compute(point_set)
            print round(dist, 4)
            #print "%.4f" % dist

    def compute(self, point_set):
        sorted_x = sorted(point_set.points, key=lambda pt: pt.x)
        left_dist, right_dist = self.find_distance_divide(sorted_x)
        #sorted_y = sorted(point_set.points, key=lambda pt: pt.y)
        
        # Attempt to solve for each pt on the left, the distances of points
        # on the right contained in the bounding rectangle.
        dist = min(left_dist, right_dist)
        m = dist
        
        midpt_x = len(sorted_x) / 2
        left_pts = sorted_x[:midpt_x]
        right_pts = sorted_x[midpt_x:]
        midpt = sorted_x[midpt_x]
        
        for pt in left_pts:
            pts_rect = self.get_points_in_rect(dist, midpt.x, pt.y, right_pts)
            for pt_rect in pts_rect:
                m = min(m, Point.dist(pt, pt_rect))
        return m
            
    def get_points_in_rect(self, dist, mid_x, pt_y, right_pts):
        assert isinstance(dist, float), "expected dist to be a float, but got %s" % dist
        assert isinstance(mid_x, float), "expected mid_x to be a float, but got %s" % mid_x
        assert isinstance(pt_y, float), "expected pt_y to be a float, but got %s" % pt_y
        
        pts = []
        for pt in right_pts:
            if pt.x <= mid_x + dist and \
                    pt_y - dist <= pt.y and \
                    pt.y <= pt_y + dist:
                pts.append(pt)
        return pts
        
    def find_distance_divide(self, sorted_x):
        if len(sorted_x) <= 3:
            return self.find_distance_brute_force(sorted_x)
        
        num_pts = len(sorted_x)
        midpt_x = num_pts / 2
        left_pts = sorted_x[:midpt_x]
        right_pts = sorted_x[midpt_x:]
        
        left_dist = self.find_distance_divide(left_pts)
        if isinstance(left_dist, tuple):
            left_dist = min(*left_dist)
        right_dist = self.find_distance_divide(right_pts)
        if isinstance(right_dist, tuple):
            right_dist = min(*right_dist)
        
        return left_dist, right_dist
        
    def find_distance_brute_force(self, pts):
        m = 10000000
        for pt1 in pts:
            for pt2 in pts:
                if pt1 is not pt2:
                    m = min(m, Point.dist(pt1, pt2))
        return m
            


class Util(object):
    """Utility functions for formatting and parsing."""

    @classmethod
    def sanitize_line(cls, line):
        # Remove the trailing newline.
        return line.strip()

def open_input_file(filename):
    lines = None
    with open(filename) as f:
        lines = f.readlines()
    assert lines is not None and isinstance(lines, list), "File wasn't read properly."
    return lines

def parse_args():
    args = sys.argv
    assert len(args) in (2, 3), "Provide a filename or filename plus the --test flag."

    filename = args[1]

    test_flag = False
    if len(args) == 3:
        if args[2] in ('--test', '-t'):
            test_flag = True
        else:
            assert False, "First argument should be a filename and the second either --test or -t."

    return filename, test_flag

def main():
    filename, test_flag = parse_args()
    #test_flag = False 
    lines = open_input_file(filename)
    
    if test_flag:
        ClosestPoints().run_tests(lines)
    else:
        ClosestPoints().evaluate(lines)

if __name__ == "__main__":
    main()
