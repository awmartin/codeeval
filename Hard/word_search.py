import sys

class Edge(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_other_node(self, node):
        if self.x is node:
            return self.y
        return self.x


class Node(object):
    def __init__(self, letter, position):
        self.position = position
        self.letter = letter
        self.edges = []
        self.visited = False

    def __str__(self):
        return "Node(%s,%s)" % (self.letter, self.position)

    def add_edge(self, edge):
        self.edges.append(edge)

    def adjacent_nodes_with_letter(self, letter, only_unvisited=False):
        tr = []
        for edge in self.edges:
            other = edge.get_other_node(self)
            if other.letter == letter and (not only_unvisited or (only_unvisited and not other.visited)):
                tr.append(other)
        return tr

    def reset(self):
        self.visited = False


class WordSearch(object):
    board = [
        "ABCE",
        "SFCS",
        "ADEE"
        ]

    def evaluate(self, lines):
        self.build_adjacency_graph()

        for line in lines:
            line = Util.sanitize_line(line)
            print self.compute(line)

    def build_adjacency_graph(self):
        self.board_str = "".join(self.board)
        self.nodes = [None for i in range(12)]

        for r,row in enumerate(self.board):
            for c,char in enumerate(row):
                letter = self.board[r][c]
                node = Node(letter, r * 4 + c)
                self.nodes[r*4+c] = node

        # Vertical edges
        for r in range(2):
            for c in range(4):
                x = self.nodes[r*4+c]
                y = self.nodes[(r+1)*4+c]
                edge = Edge(x, y)
                x.add_edge(edge)
                y.add_edge(edge)

        # Horizontal edges
        for r in range(3):
            for c in range(3):
                x = self.nodes[r*4+c]
                y = self.nodes[r*4+c+1]
                edge = Edge(x, y)
                x.add_edge(edge)
                y.add_edge(edge)

    def compute(self, line):
        def reset():
            for node in self.nodes:
                node.reset()

        def consume_letter(node, pos):
            at_end = pos == len(line)
            if at_end:
                reset()
                return True

            next_letter = line[pos]
            #print "NEXT:", next_letter
            next_nodes = node.adjacent_nodes_with_letter(next_letter, only_unvisited=True)
            #print "  FOUND", next_letter, "=", [str(n) for n in next_nodes]

            if len(next_nodes) == 0:
                return False

            found = False
            for next_node in next_nodes:
                next_node.visited = True
                found = found or consume_letter(next_node, pos+1)
            return found

        seed_letter = line[0]
        seed_nodes = self.find_nodes(seed_letter)

        found = False
        for seed_node in seed_nodes:
            seed_node.visited = True
            found = found or consume_letter(seed_node, 1)
            reset()
        return found

    def find_nodes(self, letter):
        found = []
        for i, char in enumerate(self.board_str):
            if char == letter:
                found.append(self.nodes[i])
        return found



class Util(object):
    """Utility functions for formatting and parsing."""

    @classmethod
    def sanitize_line(cls, line):

        # Remove the trailing newline.
        if line[-1] == "\n":
            line = line[:-1]

        return line

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

    lines = open_input_file(filename)

    if test_flag:
        WordSearch().run_tests(lines)
    else:
        WordSearch().evaluate(lines)

if __name__ == "__main__":
    main()


