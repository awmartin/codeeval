import sys


class Cell(object):
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.edges = []
        self.is_visited = False
        
    def add_edge_to(self, other):
        edge = Edge(self, other)
        self.edges.append(edge)
        other.edges.append(edge)
    
    def __str__(self):
        edges_to = str([str(e) for e in self.edges])
        return "Cell(%s, %s, edges=%s)" % (self.r, self.c, edges_to)

class Edge(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return "Edge()"
    
    def get_other_cell(self, cell):
        if cell not in (self.left, self.right):
            assert False
        if self.left is cell:
            return self.right
        return self.left

NUM_COLUMNS = 4
NUM_ROWS = 4

class Grid(object):
    def __init__(self):
        self.path_count = 0
        
        self.cells = []
        for r in range(NUM_ROWS):
            row = []
            for c in range(NUM_COLUMNS):
                row.append(Cell(r, c))
            self.cells.append(row)
        
        self.init_edges()
    
    def init_edges(self):
        indices = [(0, 1), (1, 0)]
        for r in range(NUM_ROWS):
            for c in range(NUM_COLUMNS):
                cell = self.cells[r][c]
                for index in indices:
                    other = self.get_cell(r + index[0], c + index[1])
                    if other is not None:
                        cell.add_edge_to(other)
    
    def start(self):
        self.compute_paths(self.cells[0][0])
        
    def compute_paths(self, origin):
        if origin.c == NUM_COLUMNS - 1 and origin.r == NUM_ROWS - 1:
            if origin.is_visited:
                assert False, "Can't visited the lower-right corner twice."
            self.count()
            return

        origin.is_visited = True
        
        # Loop through all the edges, and traverse the paths available to them.
        for edge in origin.edges:
            other = edge.get_other_cell(origin)
            if not other.is_visited:
                self.compute_paths(other)
        
        origin.is_visited = False
    
    def reset(self):
        for row in self.cells:
            for cell in row:
                cell.is_visited = False
        
    def count(self):
        self.path_count += 1
    
    def get_cell(self, r, c):
        if r < 0 or c < 0 or r >= NUM_ROWS or c >= NUM_COLUMNS:
            return None
        return self.cells[r][c]
                
def main():
    grid = Grid()
    grid.start()
    print grid.path_count

if __name__ == "__main__":
    main()

