import sys

class Expression(object):
    def __init__(self, left, right):
        pass
        
    def compute(self):
        pass

class Number(Expression):
    def __init__(self, value):
        self.value = float(value)
    
    def __str__(self):
        return "Number(%s)" % int(self.value)
        
    def compute(self):
        return self.value

class Operator(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    

    def compute(self):
        pass

class Multiply(Operator):
    def __str__(self):
        return "Multiply(%s, %s)" % (self.left, self.right)
    
    def compute(self):
        return self.left.compute() * self.right.compute()

class Add(Operator):
    def __str__(self):
        return "Add(%s, %s)" % (self.left, self.right)
    
    def compute(self):
        return self.left.compute() + self.right.compute()

class Divide(Operator):
    def __str__(self):
        return "Divide(%s, %s)" % (self.left, self.right)
    
    def compute(self):
        return self.left.compute() / self.right.compute()


def parse_token(token):
    if token == '*':
        return Multiply
    elif token == '+':
        return Add
    elif token == '/':
        return Divide
    else:
        return Number


def parse_expression(tokens):
    expr = parse_token(tokens[0])
    
    if issubclass(expr, Operator):
        left, left_consumed = parse_expression(tokens[1:])
        right, right_consumed = parse_expression(tokens[left_consumed+1:])
        return (expr(left, right), left_consumed + right_consumed + 1)
    
    elif issubclass(expr, Number):
        return (expr(tokens[0]), 1)

def compute(line):
    tokens = line.split(" ")
    expr, _ = parse_expression(tokens)
    return expr.compute()

def main():
    args = sys.argv
    assert len(args) == 2, "Please specify one file as an argument."
    filename = args[1]
    
    lines = None
    with open(filename) as f:
        lines = f.readlines()
    assert lines is not None and isinstance(lines, list), "File wasn't read properly."
    
    for line in lines:
        if len(line.strip()) == 0:
            continue
        print int(compute(line))
    
if __name__ == "__main__":
    main()