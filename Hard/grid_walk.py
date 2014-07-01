

class GridWalk(object):
    def __init__(self):
        self.visited = []
        self.matrix = {}
        self.count = 1   # origin
    
    def walk(self):
        self.build_matrix()
        self.traverse((1, 0))
        return self.count
    
    def build_matrix(self):
        dim = 1 + 299 + 1 # one extra
        
        # one quadrant
        for x in range(dim):
            for y in range(dim):
                cell = (x, y)
                self.matrix[cell] = self.is_accessible(*cell)
        
    def traverse(self, cell):
        dirs = [(1, 0), (0, 1)] #, (-1, 0), (0, -1)]
        for direction in dirs:
            next = (cell[0] + direction[0], cell[1] + direction[1])
            if next not in self.visited and self.matrix[next]:
                self.visited.append(next)
                self.count += 1
                self.traverse(next)
    
    def is_accessible(self, x, y):
        value = 0
        for digit in str(abs(x)):
            value += int(digit)
        for digit in str(abs(y)):
            value += int(digit)
        return value <= 19
            

def main():
    print GridWalk().walk()

if __name__ == "__main__":
    main()
